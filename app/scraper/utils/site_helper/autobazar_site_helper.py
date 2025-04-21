from app.scraper.utils.logger import setup_logger

logger = setup_logger("app.scraper.utils.site_helper.autobazar_site_helper")


def parse_announce(ticket_item, site_name=None, source_url=None) -> dict:
    if ticket_item is None:
        logger.error("Received None ticket_item")
        return {}

    try:
        make = None
        model = None

        if ticket_item.get("make_title"):
            make = ticket_item.get("make_title")
        elif ticket_item.get("make") and isinstance(ticket_item.get("make"), dict):
            make = ticket_item.get("make", {}).get("title")

        if ticket_item.get("model_title"):
            model = ticket_item.get("model_title")
        elif ticket_item.get("model") and isinstance(ticket_item.get("model"), dict):
            model = ticket_item.get("model", {}).get("title")

        year = ticket_item.get("year")

        price_uah = 0.0
        if ticket_item.get("price") and isinstance(ticket_item.get("price"), list):
            for price_item in ticket_item.get("price", []):
                if not isinstance(price_item, dict):
                    continue

                if (
                    price_item.get("currency") == "uah"
                    and price_item.get("value") is not None
                ):
                    price_uah = float(price_item.get("value"))
                    break
                elif (
                    price_item.get("currency") == "usd"
                    and price_item.get("value") is not None
                    and price_uah == 0.0
                ):
                    price_uah = float(price_item.get("value")) * 41.5

        mileage = 0
        if ticket_item.get("mileage") is not None:
            try:
                mileage = int(ticket_item.get("mileage"))
            except (ValueError, TypeError):
                mileage = 0

        engine_capacity = "Unknown"
        if ticket_item.get("capacity") is not None:
            try:
                engine_capacity = str(ticket_item.get("capacity"))
            except (ValueError, TypeError):
                engine_capacity = "Unknown"

        location = "Unknown"
        if ticket_item.get("location") and isinstance(
            ticket_item.get("location"), dict
        ):
            location_obj = ticket_item.get("location")
            if location_obj.get("title"):
                location = location_obj.get("title")

        image_url = None
        if ticket_item.get("photos") and isinstance(ticket_item.get("photos"), list):
            photos = ticket_item.get("photos")
            if photos and len(photos) > 0 and isinstance(photos[0], dict):
                image_url = photos[0].get("image")

        transmission = "Unknown"
        if ticket_item.get("gearbox") and isinstance(ticket_item.get("gearbox"), dict):
            gearbox = ticket_item.get("gearbox")
            if gearbox.get("title"):
                transmission = gearbox.get("title")

        engine_type = "Unknown"
        if ticket_item.get("engine") and isinstance(ticket_item.get("engine"), dict):
            engine = ticket_item.get("engine")
            if engine.get("title"):
                engine_type = engine.get("title")

        base_url = source_url or "https://auto.site.ua"
        permalink = ticket_item.get("permalink")
        full_source_url = f"{base_url}{permalink}" if permalink else base_url

        car_data = {
            "make": make or "Unknown",
            "model": model or "Unknown",
            "year": (
                int(year)
                if year
                and isinstance(year, (int, str))
                and (isinstance(year, int) or str(year).isdigit())
                else 2000
            ),
            "price": float(price_uah) if price_uah is not None else 0.0,
            "mileage": int(mileage) if mileage is not None else 0,
            "engine_type": engine_type,
            "engine_capacity": engine_capacity,
            "transmission": transmission,
            "location": location,
            "image_url": image_url or full_source_url,
            "source_url": full_source_url,
            "source_site": site_name or "AutoBazar",
        }

        return car_data
    except Exception as e:
        import traceback

        logger.error(f"Error parsing car announcement: {e}")
        logger.error(traceback.format_exc())
        return {}
