from typing import Dict, List, Optional, Any

from app.scraper.parsers.base import BaseParser, transform_make_for_source
from app.scraper.utils.http_client import send_request, HEADERS
from app.scraper.utils.logger import setup_logger
from app.scraper.utils.site_helper.autobazar_site_helper import parse_announce

logger = setup_logger("app.scraper.parser.autobazar_parser")


class AutoBazarParser(BaseParser):
    """Parser implementation for Autobazar website."""

    async def get_content(self, make, page: int = 1) -> Optional[Dict]:
        """Get content from Auto.ria for a specific make and page."""
        try:
            url = f"{self.base_url}/api/_posts/"
            params = {
                "make": make["id"],
                "page": page,
                "currency": "uah",
                "transport": 1,
            }
            response = await send_request(
                url=url,
                method="GET",
                headers=HEADERS,
                params=params,
            )

            if response and response.status_code == 200:
                data = response.json()
                if data["results"]:
                    return data["results"]

            logger.error(
                f"Failed to get data for make {make["title"]}: {response.json()["results"] if response else 'No response'}"
            )
            return None

        except Exception as e:
            logger.error(f"Error fetching data for make {make["title"]}: {e}")
            return None

    def parse_data(self, content: Any, make: str = "") -> List[Dict]:
        """Parse content from HTML response into car listings."""
        parsed_cars = []
        for ticket_item in content:
            try:
                announce = parse_announce(ticket_item, self.site_name, self.base_url)
                if announce:
                    if not announce.get("make") and make:
                        announce["make"] = make

                    announce["site_name"] = self.site_name
                    parsed_cars.append(announce)

            except Exception as e:
                logger.error(f"Error parsing car announce: {e}")
                continue

        return parsed_cars

    async def get_car_brands(self, preferred_makes: list) -> List[dict]:
        url = f"{self.base_url}/api/transports/makes/"

        response = await send_request(
            url=url,
            method="GET",
            headers=HEADERS,
        )

        makes = response.json()

        if preferred_makes:
            transformed_preferred = {
                transform_make_for_source(m) for m in preferred_makes
            }
            filtered = [
                make
                for make in makes
                if transform_make_for_source(make["title"]) in transformed_preferred
            ]
            return filtered

        return makes
