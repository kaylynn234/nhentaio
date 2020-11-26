


from typing import Callable, overload


class _TimeUnit:
    n: int
    unit: str


Hours: Callable[[int], _TimeUnit]
Days: Callable[[int], _TimeUnit]
Weeks: Callable[[int], _TimeUnit]
Months: Callable[[int], _TimeUnit]
Years: Callable[[int], _TimeUnit]



class Query:
    def __init__(self) -> None: ...
    def add(self, *args: str) -> Query: ...
    def exclude(self, *args: str) -> Query: ...
    def parodies(self, *args: str) -> Query: ...

    @overload
    def pages(self, exact: int) -> Query: ...
    @overload
    def pages(self, *, less_than: int) -> Query: ...
    @overload
    def pages(self, *, more_than: int) -> Query: ...
    @overload
    def pages(self, *, less_than: int, more_than: int) -> Query: ...
    @overload

    def uploaded(self, exact: _TimeUnit) -> Query: ...
    @overload
    def uploaded(self, *, less_than: _TimeUnit) -> Query: ...
    @overload
    def uploaded(self, *, more_than: _TimeUnit) -> Query: ...
    @overload
    def uploaded(self, *, less_than: _TimeUnit, more_than: _TimeUnit) -> Query: ...

    def copy(self) -> Query: ...
