import dataclasses
import datetime

from typing import List

from nhentaio.asset import Asset
from nhentaio.http import HTTPClient
from nhentaio.iterators import GallerySearchIterator
from nhentaio.taglike import Taglike


@dataclasses.dataclass
class PartialGallery:
    id: int
    title: str
    thumbnail: Asset
    url: str


@dataclasses.dataclass
class GalleryPage:
    number: int
    content: Asset

    @classmethod
    def from_id_and_count(cls, id: int, count: int, _state: HTTPClient) -> GalleryPage: ...


@dataclasses.dataclass
class Gallery:
    id: int
    title: str
    title_untranslated: str
    cover: Asset
    page_count: int
    uploaded: datetime.datetime
    favourites: int
    url: str

    pages: List[GalleryPage] = dataclasses.field(default_factory=list)

    similar: List[PartialGallery] = dataclasses.field(default_factory=list)

    parodies: List[Taglike] = dataclasses.field(default_factory=list)
    characters: List[Taglike] = dataclasses.field(default_factory=list)
    tags: List[Taglike] = dataclasses.field(default_factory=list)
    artists: List[Taglike] = dataclasses.field(default_factory=list)
    groups: List[Taglike] = dataclasses.field(default_factory=list)
    languages: List[Taglike] = dataclasses.field(default_factory=list)
    categories: List[Taglike] = dataclasses.field(default_factory=list)
