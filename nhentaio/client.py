import asyncio
import re
import math

from .enums import SortType
from .errors import NhentaiError
from .http import HTTPClient
from .iterators import ChunkedCoroIterator, CoroIterator


GALLERY_ID_PATTERN = re.compile(r'<h3 id="gallery_id"><span class="hash">#</span>(\d*)</h3>')


class Client:
    """Represents a client that can be used to interact with nhentai."""

    def __init__(self) -> None:
        self.open = True
        self._state = HTTPClient()

    def search(self, query, *, limit=25, sort_by = SortType.recent):
        """Performs an nhentai search with the given query.

        .. note::

            Results from searches are of type :class:`~.PartialGallery`, as opposed to :class:`~.Gallery`, and have less information available.
            To get full information about a gallery, including pages and tags, use :meth:`~Client.fetch_gallery`: or :meth:`~.Client.fetch_galleries`.

        Parameters
        -----------
        query: Union[:class:`str`, :class:`~.Taglike`, :class:`~.Query`]
            The query to use when searching. For ease of use this parameter is implicitly cast to :class:`str` for you.

            .. note::

                For building complex search queries, consider using :class:`~.Query`.

        limit: :class:`int`
            The maximum amount of galleries to return. Defaults to 25.

        sort_by: :class:`~.SortType`
            The method by which results should be sorted. Defaults to `SortType.recent`.

        Returns
        --------
        :class:`~.AsyncIterator`
            An asynchronous iterator yielding the results that were found.
        """

        max_pages = math.ceil(limit / 25)
        lazy_results = []
        for i in range(1, max_pages + 1):
            exact_limit = (limit % 25 if i == max_pages else 25) or 25
            lazy_results.append(self._state.search(query, page=i, sort_by=sort_by, limit=exact_limit))

        return ChunkedCoroIterator(lazy_results)

    async def fetch_gallery(self, id):
        """Fetches a gallery from nhentai with the specified ID.

        Parameters
        -----------
        id: :class:`int`
            The ID of the gallery to fetch.

        Returns
        --------
        Optional[:class:`~.Gallery`]
            The gallery with the passed ID, or ``None`` if not found.
        """

        response = await self._state.route(f"https://nhentai.net/g/{id}", {})
        try:
            return await self._state.gallery_from(response, id)
        except NhentaiError:
            return None

    async def random_gallery(self):
        """Fetches a random gallery from nhentai.

        .. note::

            This is equivalent to using the "random" button on the nhentai website.

        Returns
        --------
        :class:`~.Gallery`
            The gallery that was found.
        """

        response = await self._state.route("https://nhentai.net/random", {})
        gallery_id = re.match(GALLERY_ID_PATTERN, response)
        return await self._state.gallery_from(response, gallery_id)

    def fetch_galleries(self, *args):
        """Fetches multiple galleries using the passed IDs.

        Parameters
        -----------
        args: Iterable[:class:`str`]
            The IDs to use when fetching.

        Returns
        --------
        :class:`~.AsyncIterator`
            An asynchronous iterator yielding the galleries that were found.
        """

        return CoroIterator([self.fetch_gallery(id) for id in args])

    def close(self):
        """Closes the internal connection handler and effectively "switches off" the client."""

        asyncio.create_task(self._state.close())
        self.open = False

    def __del__(self):
        if self.open:
            try:
                self.close()
            except RuntimeError:
                pass