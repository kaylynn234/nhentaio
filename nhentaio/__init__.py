"""
Nhentai API Wrapper
~~~~~~~~~~~~~~~~~~~

An asynchronous, read-only nhentai API wrapper for the damned, depraved, and disillusioned.

:copyright: (c) 2020 Kaylynn
:license: MIT, see LICENSE for more details.

"""

__title__ = "nhentaio"
__author__ = "Kaylynn"
__license__ = "MIT"
__copyright__ = "Copyright 2020 Kaylynn"
__version__ = "0.3.0"

from .client import Client
from .enums import SortType
from .errors import *
from .gallery import Gallery, GalleryPage, PartialGallery
from .iterators import NoMoreItems
from .query import Hours, Days, Weeks, Months, Years, Query

