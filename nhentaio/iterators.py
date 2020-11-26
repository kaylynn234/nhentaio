import asyncio

from inspect import isawaitable


class NoMoreItems(Exception):
    pass


def _identity(value):
    return value


async def _maybe_coroutine(func, *args, **kwargs):
    if isawaitable(func):
        return await func(*args, **kwargs)

    return func(*args, **kwargs)


class _AsyncIterator:
    __slots__ = ()

    def map(self, func):
        return _MappedAsyncIterator(self, func)

    def filter(self, func):
        return _FilteredAsyncIterator(self, func)

    async def flatten(self):
        results = []

        while True:
            try:
                item = await self.next()
            except NoMoreItems:
                return results
            else:
                results.append(item)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            next = await self.next()
        except NoMoreItems: 
            raise StopAsyncIteration()
        else:
            return next


class _MappedAsyncIterator(_AsyncIterator):
    def __init__(self, iterator, func) -> None:
        self.iterator = iterator
        self.func = func

    async def next(self):
        item = await self.iterator.next()
        return await _maybe_coroutine(self.func, item)


class _FilteredAsyncIterator(_AsyncIterator):
    def __init__(self, iterator, func) -> None:
        self.iterator = iterator
        if func is None:
            func = _identity

        self.func = func

    async def next(self):
        getter = self.iterator.next
        func = self.func

        while True:
            item = await getter()
            result = await _maybe_coroutine(func, item)
            if result:
                return result


class _LazyCoroIterator(_AsyncIterator):
    def __init__(self, fill_from) -> None:
        self.items = asyncio.Queue()
        self.fill_from = fill_from

    async def fill(self):
        raise NotImplementedError

    async def next(self):
        if self.items.empty():
            await self.fill()

        try:
            return self.items.get_nowait()
        except asyncio.QueueEmpty:
            raise NoMoreItems()


class ChunkedCoroIterator(_LazyCoroIterator):
    async def fill(self):
        try:
            results = self.fill_from.pop(0)
        except IndexError:
            raise NoMoreItems

        for result in await results:
            self.items.put_nowait(result)


class CoroIterator(_LazyCoroIterator):
    async def fill(self):
        try:
            result = self.fill_from.pop(0)
        except IndexError:
            raise NoMoreItems

        self.items.put_nowait(result)
