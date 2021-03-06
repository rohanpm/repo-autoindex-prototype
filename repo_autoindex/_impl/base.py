from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator, Awaitable, Callable
from dataclasses import dataclass
from typing import Optional, Type, TypeVar

T = TypeVar("T")
Fetcher = Callable[[str], Awaitable[Optional[str]]]

ICON_FOLDER = "📂"
ICON_PACKAGE = "📦"
ICON_OTHER = "  "


@dataclass
class GeneratedIndex:
    content: str
    relative_dir: str = "."


@dataclass
class IndexEntry:
    href: str
    text: str
    time: str = ""
    size: str = ""
    padding: str = ""
    icon: str = ICON_OTHER


class Repo(ABC):
    def __init__(
        self,
        base_url: str,
        entry_point_content: str,
        fetcher: Fetcher,
    ):
        self.base_url = base_url
        self.entry_point_content = entry_point_content
        self.fetcher = fetcher

    @abstractmethod
    def render_index(
        self, index_href_suffix: str
    ) -> AsyncGenerator[GeneratedIndex, None]:
        pass  # pragma: no cover

    @classmethod
    @abstractmethod
    async def probe(cls: Type[T], fetcher: Fetcher, url: str) -> Optional[T]:
        """Determine if a specified URL seems to point at a repository of this type.

        If so, returns an initialized Repo of a concrete subtype. If not, returns None.
        """
        pass  # pragma: no cover
