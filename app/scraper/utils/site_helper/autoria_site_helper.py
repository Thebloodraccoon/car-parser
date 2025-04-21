import re

import bs4

from app.scraper.utils.logger import setup_logger

logger = setup_logger("app.scraper.utils.site_helper.autoria_site_helper")


def extract_ticket_items(
    html_content: str,
) -> bs4.ResultSet[bs4.PageElement | bs4.Tag | bs4.NavigableString]:
    """Extract all ticket-item sections from the HTML content."""
    soup = bs4.BeautifulSoup(html_content, "html.parser")
    ticket_items = soup.find_all("section", class_="ticket-item")
    return ticket_items


def parse_announce(ticket_item, site_name, source_url) -> dict:
    """Parse a car announcement from HTML ticket item."""
    try:
        data_div = ticket_item.find("div", attrs={"data-advertisement-data": True})

        make = data_div.get("data-mark-name") if data_div else None
        model = data_div.get("data-model-name") if data_div else None
        year = data_div.get("data-year") if data_div else None

        link_to_view = data_div.get("data-link-to-view") if data_div else None

        full_source_url = (
            f"{source_url}{link_to_view}" if link_to_view and source_url else None
        )
        if full_source_url and not full_source_url.startswith(("http://", "https://")):
            full_source_url = f"https://auto.ria.com{link_to_view}"

        price_div = ticket_item.find("div", class_="price-ticket")
        price_uah = None
        if price_div:
            price_span = price_div.find("span", attrs={"data-currency": "UAH"})
            if price_span:
                price_text = price_span.text.strip().replace(" ", "")
                price_uah = float(price_text) if price_text.isdigit() else None

        mileage = 0
        location = "Unknown"
        engine_type = "Unknown"
        engine_capacity = "Unknown"
        transmission = "Unknown"

        characteristics = ticket_item.find("ul", class_="unstyle characteristic")
        if characteristics:
            mileage_li = characteristics.find("li", class_="item-char js-race")
            if mileage_li and "без пробігу" not in mileage_li.text:
                mileage_text = re.search(r"(\d+)", mileage_li.text)
                if mileage_text:
                    mileage = int(mileage_text.group(1).replace(" ", ""))

            location_li = characteristics.find(
                "li", class_="item-char view-location js-location"
            )
            if location_li:
                icon = location_li.find("i", class_="icon-location")
                if icon and icon.next_sibling:
                    location = icon.next_sibling.strip()
                    # Ensure we don't include the span text
                    if "(" in location:
                        location = location.split("(")[0].strip()

            engine_li = characteristics.find_all("li", class_="item-char")
            for li in engine_li:
                if li.find("i", class_="icon-fuel"):
                    engine_info = li.text.strip().split(",")
                    if len(engine_info) > 0:
                        engine_type = engine_info[0].strip() or engine_type
                    if len(engine_info) > 1:
                        engine_capacity = engine_info[1].strip() or engine_capacity

                if li.find("i", class_="icon-transmission"):
                    icon = li.find("i", class_="icon-transmission")
                    if icon and icon.next_sibling:
                        transmission = icon.next_sibling.strip() or transmission

        image_url = None
        photo_div = ticket_item.find("div", class_="ticket-photo")
        if photo_div:
            img_tag = photo_div.find("img")
            if img_tag:
                image_url = img_tag.get("src")
                if image_url and not image_url.startswith(("http://", "https://")):
                    image_url = f"https:{image_url}"

        car_data = {
            "make": make or "Unknown",
            "model": model or "Unknown",
            "year": int(year) if year and year.isdigit() else 2000,
            "price": price_uah or 0.0,
            "mileage": mileage,
            "engine_type": engine_type,
            "engine_capacity": engine_capacity,
            "transmission": transmission,
            "location": location,
            "image_url": image_url,
            "source_url": full_source_url or "https://auto.ria.com",
            "source_site": site_name or "Auto.ria",
        }

        return car_data
    except Exception as e:
        logger.error(f"Error parsing car announcement: {e}")
        return {}
