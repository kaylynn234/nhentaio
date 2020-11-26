import dataclasses


@dataclasses.dataclass
class Taglike:
    """Taglike()

    Represents an nhentai tag.
    This class should not be instantiated manually.

    Attributes
    -----------
    name: :class:`str`
        The name of this tag.
    count: :class:`int`
        The number of galleries with this tag.

        .. note::

            Nhentai does not provide exact numbers above 1000, instead opting for rounded numbers such as 1000, 3000 and so on.
    """

    name: str
    count: int

    @classmethod
    def from_label(cls, name: str, count_label: str):
        return cls(name, int(count_label[:-1]) * 1000 if "K" in count_label else int(count_label))

    def __str__(self):
        return self.name