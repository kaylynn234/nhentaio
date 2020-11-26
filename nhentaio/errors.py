class NhentaiError(Exception):
    """The base exception that all nhentai-related exceptions inherit from."""


class NotFound(NhentaiError):
    """Raised when content is not found, search results are empty, or similar."""
