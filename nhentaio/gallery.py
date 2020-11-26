import dataclasses
import datetime

from typing import List

from .asset import Asset
from .taglike import Taglike


@dataclasses.dataclass
class PartialGallery:
    """PartialGallery()

    Represents a partial gallery.

    .. note::

        This class lacks information compared to :class:`~.Gallery`. If you want more information about a gallery, such as pages and tags,
        fetch it with :meth:`~.Client.fetch_gallery` or :meth:`~.Client.fetch_galleries`.

    This class is usually returned from a search and should not be instantiated manually.

    Attributes
    -----------
    id: :class:`int`
        The ID of this gallery. Can be used in :meth:`~.Client.fetch_gallery` to fetch more information.
    title: :class:`str`
        The title of this gallery.
    thumbnail: :class:`~.Asset`
        An asset representing this gallery's thumbnail.
    url: :class:`str`
        The full URL for this gallery.
    """

    id: int
    title: str
    thumbnail: Asset
    url: str


@dataclasses.dataclass
class GalleryPage:
    """GalleryPage()
    
    Represents a page from a gallery.
    This class is returned from `attr`:~.Gallery.pages: and should not be instantiated manually.

    Attributes
    -----------
    number: :class:`int`
        A number specifying which page this is.
    content: :class:`~.Asset`
        The contents of this page.
    """

    number: int
    content: Asset

    @classmethod
    def from_id_and_count(cls, id, count, _state):
        asset = Asset(f"https://i.nhentai.net/galleries/{id}/{count}.jpg", _state)
        return cls(count, asset)


@dataclasses.dataclass
class Gallery:
    """Gallery()

    Represents an nhentai gallery.
    This class is returned from :meth:`~.Client.fetch_gallery` / :meth:`~.Client.fetch_galleries` and should not be instantiated manually.

    Attributes
    -----------
    id: :class:`int`
        The ID of this gallery.
    title: :class:`str`
        The title of this gallery.
    title_untranslated: :class:`str`
        The title of this gallery without localisation.
    cover: :class:`~.Asset`
        An asset representing this gallery's cover. This is usually the same as the gallery's first page.
    url: :class:`str`
        The full URL for this gallery.
    page_count: :class:`int`
        This gallery's page count.
    uploaded: :class:`datetime.datetime`
        A UTC+0 datetime representing when this gallery was uploaded.
    favourites: :class:`int`
        The amount of favourites this gallery has received.
    url: :class:`str`
        The full URL for this gallery.
    pages: List[:class:`~.GalleryPage`]
        The pages in this gallery.
    similar: List[:class:`~.PartialGallery`]
        A list of up to 5 galleries that are similar to this one.
    parodies: List[:class:`~.Taglike`]
        A list of the parody tags attached to this gallery.
    characters: List[:class:`~.Taglike`]
        A list of the character tags attached to this gallery.
    tags: List[:class:`~.Taglike`]
        A list of content tags attached to this gallery.
    artists: List[:class:`~.Taglike`]
        A list of the artist tags attached to this gallery.
    groups: List[:class:`~.Taglike`]
        A list of the group tags attached to this gallery.
    languages: List[:class:`~.Taglike`]
        A list of the language tags attached to this gallery.
    categories: List[:class:`~.Taglike`]
        A list of the category tags attached to this gallery.
    """

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