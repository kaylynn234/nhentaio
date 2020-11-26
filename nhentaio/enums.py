from .better_enums import EnumMeta


class SortType(metaclass=EnumMeta):
    """Represents a sorting method when searching."""

    recent              = "recent"
    popular_today       = "popular-today"
    popular_this_week   = "popular-week"
    popular_this_month  = "popular-month"
