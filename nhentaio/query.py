import dataclasses


@dataclasses.dataclass
class _TimeUnit:
    n: int
    unit: str

    def __str__(self) -> str:
        return f"{self.n}{self.unit}"


Hours = lambda n: _TimeUnit(n, "h")
Days = lambda n: _TimeUnit(n, "d")
Weeks = lambda n: _TimeUnit(n, "w")
Months = lambda n: _TimeUnit(n, "m")
Years = lambda n: _TimeUnit(n, "y")

# RTD autodoc bandaid
Hours.__doc__ = """Represents ``n`` hours. Used in :meth:`~.Query.uploaded`."""
Days.__doc__ = """Represents ``n`` days. Used in :meth:`~.Query.uploaded`."""
Weeks.__doc__ = """Represents ``n`` weeks. Used in :meth:`~.Query.uploaded`."""
Months.__doc__ = """Represents ``n`` months. Used in :meth:`~.Query.uploaded`."""
Years.__doc__ = """Represents ``n`` years. Used in :meth:`~.Query.uploaded`."""

class Query:
    """A helper class for building more complex nhentai search queries."""

    def __init__(self):
        self._query = []

    def add(self, *args):
        """Adds terms to the search query.
        This will only return galleries that have each one of ``args`` in their tags or title.

        This function returns the class instance to allow for fluent-style chaining.

        Parameters
        -----------
        args: :class:`str`
            The terms to add to the query.
        """

        self._query.extend(arg.replace("\"", "").strip(" ") for arg in args)
        return self

    def exclude(self, *args):
        """Excludes terms from the search query.
        This will not return galleries that have any of ``args`` in their tags or title.

        This function returns the class instance to allow for fluent-style chaining.

        Parameters
        -----------
        args: :class:`str`
            The terms to exclude from the query.
        """

        self._query.extend("-{}".format(arg.replace("\"", "").strip(" ")) for arg in args)
        return self

    def parodies(self, *args):
        """Limits search results to specific parodies.

        This function returns the class instance to allow for fluent-style chaining.

        Parameters
        -----------
        args: :class:`str`
            The parodies to limit this search to.
        """

        self._query.extend("parodies:{}".format(arg.replace("\"", "").strip(" ")) for arg in args)
        return self

    def _single_or_range(self, key, exact = None, less_than = None, more_than = None):
        # explicit not-none checks here since 0 may be provided
        if exact and (less_than is not None or more_than is not None):
            raise ValueError(
                "You cannot use the exact parameter in conjunction with the less_than and more_than parameters"
            )

        if exact:
            self._query.append(f"{key}:{exact}")
        else:
            if less_than:
                self._query.append(f"{key}:<{less_than}")
            if more_than:
                self._query.append(f"{key}:>{more_than}")

        return self

    def pages(self, exact = None, *, less_than = None, more_than = None):
        """Limits search results based on page count.

        This function returns the class instance to allow for fluent-style chaining.

        .. note::

            You cannot use the ``exact`` and ``less_than``/``more_than`` parameters together.
            You must use either the ``exact`` parameter exclusively, or the ``less_than``/``more_than`` parameters.

        Parameters
        -----------
        exact: Union[:class:`int`]
            Limits the search results to galleries with exactly ``exact`` pages.
        less_than: Optional[:class:`int`]
            Limits the search results to galleries with less than ``less_than`` pages.
        more_than: Optional[:class:`int`]
            Limits the search results to galleries with more than ``more_than`` pages.
        """

        return self._single_or_range("pages", exact, less_than, more_than)

    def uploaded(self, exact = None, *, less_than = None, more_than = None):
        """Limits search results based on upload date.

        This function returns the class instance to allow for fluent-style chaining.

        .. note::

            You cannot use the ``exact`` and ``less_than``/``more_than`` parameters together.
            You must use either the ``exact`` parameter exclusively, or the ``less_than``/``more_than`` parameters.

        Parameters
        -----------
        exact: :func:`~.Hours`, :func:`~.Days`, :func:`~.Weeks`, :func:`~.Months`, :func:`~.Years` or ``None``
            Limits the search results to galleries uploaded in the last _.
        less_than: :func:`~.Hours`, :func:`~.Days`, :func:`~.Weeks`, :func:`~.Months`, :func:`~.Years` or ``None``
            Limits the search results to galleries uploaded less than _ ago.
        more_than: :func:`~.Hours`, :func:`~.Days`, :func:`~.Weeks`, :func:`~.Months`, :func:`~.Years` or ``None``
            Limits the search results to galleries uploaded more than _ ago.
        """

        return self._single_or_range("uploaded", exact, less_than, more_than)

    def copy(self):
        """Creates a copy of this query.
        
        Returns
        --------
            :class:`~.Query`
                A copy of this query.
        """

        new = Query()
        new._query.extend(self._query)

        return new

    def __str__(self) -> str:
        return " ".join(self._query)