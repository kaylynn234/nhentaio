import dataclasses


@dataclasses.dataclass
class Asset:
    """Asset()

    Represents an image from nhentai, such as a user's avatar or a gallery page.

    Attributes
    -----------
    url: :class:`str`
        The URL of the image that this asset represents.
    """

    url: str
    _state: "HTTPClient"

    async def read(self):
        """Returns the content of this asset as :class:`bytes`.

        Returns
        --------
        :class:`bytes`
            the bytes that were read.
        """

        if not hasattr(self, "_cached_bytes"):
            self._cached_bytes = await self._state.image_from_url(self.url)

        return self._cached_bytes

    async def save(self, fp):
        """Saves the content of this asset to a file or file-like object.

        Parameters
        -----------
        fp: :class:`str` or a file-like object
            A filepath or file-like object representing where this asset should be saved.
        """

        result = await self.read()

        if isinstance(fp, str):
            with open(fp, "wb") as output_file:
                output_file.write(result)
        else:
            fp.write(result)

