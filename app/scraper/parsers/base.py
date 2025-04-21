from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any


def transform_make_for_source(make: str) -> str:
    """Transform make name to format expected by source site."""
    return make.lower().replace(" ", "-")


class BaseParser(ABC):
    """Abstract base class for car site parsers."""

    def __init__(self, base_url: str, site_name: str):
        self.base_url = base_url
        self.site_name = site_name

    @abstractmethod
    async def get_content(self, make: str, page: int = 1) -> Optional[Any]:
        """Get content from the site for a specific make and page."""
        pass

    @abstractmethod
    def parse_data(self, content: Any, make: str = "") -> List[Dict]:
        """Parse content into car listings."""
        pass

    @abstractmethod
    async def get_car_brands(self, preferred_makes: list) -> List[str]:
        """Get list of car brands supported by this parser."""
        pass
