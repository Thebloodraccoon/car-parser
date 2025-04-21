from typing import Optional

from app.scraper.parsers.autobazar_parser import AutoBazarParser
from app.scraper.parsers.autoria_parser import AutoRiaParser
from app.scraper.parsers.base import BaseParser


def create_parser(site_type: str) -> Optional[BaseParser]:
    """Factory function to create appropriate parser for the given site type.

    Each parser is instantiated with its predefined URL and site name.

    Args:
        site_type: The type of parser to create ("autoria", "autobazar", etc.)

    Returns:
        An instance of the appropriate parser class, or None if site_type is unknown
    """
    parser_configs = {
        "autoria": {
            "class": AutoRiaParser,
            "base_url": "https://auto.ria.com",
            "site_name": "AutoRia",
        },
        "autobazar": {
            "class": AutoBazarParser,
            "base_url": "https://avtobazar.ua",
            "site_name": "AutoBazar",
        },
    }

    parser_config = parser_configs.get(site_type.lower())
    if not parser_config:
        return None

    return parser_config["class"](
        base_url=parser_config["base_url"], site_name=parser_config["site_name"]
    )
