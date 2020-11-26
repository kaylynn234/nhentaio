import dataclasses

from typing import IO, Union

from nhentaio.http import HTTPClient


@dataclasses.dataclass
class Asset:
    url: str
    _state: HTTPClient

    async def read(self) -> bytes: ...
    async def save(self, fp: Union[str, IO[bytes]]) -> None: ...

