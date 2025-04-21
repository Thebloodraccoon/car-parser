from typing import Dict, List, Optional, Any

from app.scraper.parsers.base import BaseParser, transform_make_for_source
from app.scraper.utils.http_client import send_request, HEADERS
from app.scraper.utils.logger import setup_logger
from app.scraper.utils.site_helper.autoria_site_helper import (
    extract_ticket_items,
    parse_announce,
)

logger = setup_logger("app.scraper.parser.autoria_parser")


class AutoRiaParser(BaseParser):
    """Parser implementation for Auto.ria website."""

    async def get_content(self, make: str, page: int = 1) -> Optional[Dict]:
        """Get content from Auto.ria for a specific make and page."""
        try:
            make = transform_make_for_source(make=make)

            url = f"{self.base_url}/uk/car/{make}/"
            response = await send_request(
                url=url,
                method="GET",
                headers=HEADERS,
                params={"page": page},
            )

            if response and response.status_code == 200:
                html_content = response.text
                ticket_items = extract_ticket_items(html_content)
                return {"results": ticket_items}

            logger.error(
                f"Failed to get data for make {make}: {response.status_code if response else 'No response'}"
            )
            return None

        except Exception as e:
            logger.error(f"Error fetching data for make {make}: {e}")
            return None

    def parse_data(self, content: Any, make: str = "") -> List[Dict]:
        """Parse content from HTML response into car listings."""
        if not content or "results" not in content:
            return []

        parsed_cars = []
        for ticket_item in content.get("results", []):
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

    async def get_car_brands(self, preferred_makes: list) -> List[str]:
        """Get list of car brands from NHTSA API."""
        if preferred_makes:
            return preferred_makes

        url = "https://vpic.nhtsa.dot.gov/api/vehicles/GetAllMakes?format=json"

        response = await send_request(
            url=url,
            method="GET",
            headers=HEADERS,
        )

        data = response.json()
        makes = [make["Make_Name"] for make in data["Results"]]
        return makes
