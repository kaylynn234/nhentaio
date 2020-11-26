import asyncio
import typing

from typing import Any, Union, TypeVar

from .gallery import Gallery, PartialGallery


class NoMoreItems(Exception):
    pass


_T = typing.TypeVar("_T")


class _AsyncIterator(typing.AsyncIterator[_T]):
    __slots__ = ()

    def map(self, func) -> _MappedAsyncIterator: ...
    def filter(self, func) -> _FilteredAsyncIterator: ...
    async def flatten(self) -> list: ...

    def __aiter__(self) -> _AsyncIterator[_T]: ...
    async def __anext__(self) -> -_T: ...


class _LazyCoroIterator(_AsyncIterator):
    items: asyncio.Queue

    def __init__(self, fill_from) -> None: ...

    async def fill(self) -> None: ...
    async def next(self) -> _AsyncIterator[_T]: ...


class ChunkedCoroIterator(_LazyCoroIterator):
    ...


class CoroIterator(_LazyCoroIterator):
    ...