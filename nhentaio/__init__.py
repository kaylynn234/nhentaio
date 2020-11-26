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
__version__ = "0.1.0"

from nhentaio.client import Client
from nhentaio.enums import SortType
from nhentaio.errors import *
from nhentaio.gallery import Gallery, PartialGallery
from nhentaio.query import Hours, Days, Weeks, Months, Years, Query

