import re

from collections import defaultdict, namedtuple

import aiohttp

from dateutil import parser
from lxml import html

from .asset import Asset
from .errors import NhentaiError, NotFound
from .gallery import Gallery, GalleryPage, PartialGallery
from .taglike import Taglike


NHENTAI_ACTUAL_ID_PATTERN = re.compile(r'data-src="https://t\.nhentai\.net/galleries/(\d+)/\w+\.jpg"')
NHENTAI_ID_PATTERN = re.compile(r"/g/(\d*)/")
NHENTAI_RESULT_COUNT_PATTERN = re.compile(r'\s*(\d+)\s*results')

TITLE_PREFIX = "/html/body/div[2]/div[1]/div[2]/div"

GalleryTags = namedtuple("GalleryTags", "tags pages date")
RawSearchResults = namedtuple("RawSearchResults", "total results")


class HTTPClient:
    def __init__(self) -> None:
        self._session = aiohttp.ClientSession()

    def parse_partial_gallery(self, tree, prefix, *, position):
        # I would grab the img element here, but because of lazyload strangeness a result is not guaranteed
        element = tree.xpath(f"{prefix}/div[{position}]/a")
        if not element:
            return None  # no more results on this page
        else:
            element = element[0]

        gallery_caption = tree.xpath(f"{prefix}/div[{position}]/a/div")[0]
        gallery_id = re.match(NHENTAI_ID_PATTERN, element.get("href"))[1]

        return PartialGallery(
            id=gallery_id,
            title=gallery_caption.text,
            thumbnail=Asset(f"https://t.nhentai.net/galleries/{gallery_id}/thumb.jpg", self),
            url=f"https://nhentai.net/g/{gallery_id}/"
        )

    def parse_tags(self, tree, prefix):
        taglikes = defaultdict(list)
        tag_section = tree.xpath(f"{prefix}")[0]

        # This is each "type" of tag; tags themselves, parody tags, artist tags, and so on.
        # We skip the last two items since those are the page count and upload dates, which aren't "real" tags.
        for tag_container in tag_section[:-2]:
            tag_type = tag_container.text.lower().strip(" \t\n")[:-1]
            for name, count in [(item[0], item[1]) for item in tag_container[0]]:
                taglikes[tag_type].append(Taglike.from_label(name.text, count.text))

        pages = int(tag_section[-2][0][0][0].text)
        date = parser.parse(tag_section[-1][0][0].get("datetime"))

        return GalleryTags(dict(taglikes), pages, date)


    async def route(self, url, parameters):
        async with self._session.get(url, params=parameters) as response:
            if 300 > response.status >= 200:
                return await response.text()
            else:
                raise NhentaiError(f"Error {response.status}: Invalid response")

    async def image_from_url(self, url):
        async with self._session.get(url) as response:
            if 300 > response.status >= 200:
                return await response.read()
            else:
                raise NhentaiError(f"Error {response.status} when attempting to read image")

    async def galleries_from(self, response, *, limit):
        tree = html.fromstring(response)
        results = []

        for i in range(1, limit + 1):
            gallery = self.parse_partial_gallery(tree, "/html/body/div[2]/div[2]", position=i)
            if not gallery:
                break

            results.append(gallery)

        return results

    async def gallery_from(self, response, id):
        tree = html.fromstring(response)
        tags = self.parse_tags(tree, prefix='//*[@id="tags"]')

        # For some bizarre reason, the ID in image URLs and the gallery ID can differ.
        image_id = re.search(NHENTAI_ACTUAL_ID_PATTERN, response)[1]

        # The "[1:-1]" is here to get rid of the enclosing brackets
        favourites = tree.xpath("/html/body/div[2]/div[1]/div[2]/div/div/a[1]/span/span")[0].text[1:-1]
        pages = [GalleryPage.from_id_and_count(image_id, i, self) for i in range(1, tags.pages + 1)]
        similar = [self.parse_partial_gallery(tree, '//*[@id="related-container"]', position=i) for i in range(6)]

        # Element.text may be None, so filtering it (in some way) is required.
        raw_title = filter(None, (element.text for element in tree.xpath(f"{TITLE_PREFIX}/h1")[0]))
        raw_title_untranslated = filter(None, (element.text for element in tree.xpath(f"{TITLE_PREFIX}/h2")[0]))

        # There may be extraneous spaces at either end of the string.
        title = "".join(raw_title).strip(" ")
        title_untranslated = "".join(raw_title_untranslated).strip(" ")

        return Gallery(
            id=id,
            title=title,
            title_untranslated=title_untranslated,
            cover=Asset(f"https://t.nhentai.net/galleries/{image_id}/cover.jpg", self),
            page_count=tags.pages,
            uploaded=tags.date,
            favourites=favourites,
            url=f"https://nhentai.net/g/{id}/",
            pages=pages,
            similar=similar,
            **tags.tags
        )

    async def search(self, query, *, page, sort_by, limit):
        request_parameters = {
            "q": query,
            "sort": str(sort_by),
            "page": page
        }

        search_result = await self.route("https://nhentai.net/search", request_parameters)
        result_count = re.search(NHENTAI_RESULT_COUNT_PATTERN, search_result)[1]

        # don't bother parsing; there are no results
        if not int(result_count):
            raise NotFound("No results found!")

        return await self.galleries_from(search_result, limit=limit)

    async def close(self):
        await self._session.close()