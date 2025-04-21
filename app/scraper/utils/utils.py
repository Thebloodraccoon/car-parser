from typing import Dict
from typing import List

from pydantic import ValidationError, HttpUrl

from app.db.car_db import CarCRUD
from app.schemas.cars import CarCreate
from app.scraper.utils.logger import setup_logger

logger = setup_logger("app.scraper.utils.http_client")


def chunk_list(lst: List, chunk_size: int) -> List[List]:
    """Split a list into chunks of specified size."""
    return [lst[i : i + chunk_size] for i in range(0, len(lst), chunk_size)]


def convert_to_pydantic_model(car_data: Dict) -> CarCreate:
    """Convert parsed car data to Pydantic model."""
    try:
        source_url = car_data.get("source_url")
        image_url = car_data.get("image_url")

        car_create = CarCreate(
            make=car_data.get("make", "Unknown"),
            model=car_data.get("model", "Unknown"),
            year=car_data.get("year", 2000),
            price=float(car_data.get("price", 0)),
            mileage=int(car_data.get("mileage", 0)),
            engine_type=car_data.get("engine_type", "Unknown"),
            engine_capacity=car_data.get("engine_capacity", "Unknown"),
            transmission=car_data.get("transmission", "Unknown"),
            location=car_data.get("location", "Unknown"),
            image_url=image_url,
            source_url=source_url,
            source_site=car_data.get("source_site", "Unknown"),
        )

        return car_create
    except ValidationError as e:
        logger.error(f"Data validation error: {e}")
        logger.error(f"Problematic data: {car_data}")
        raise e


async def process_car_data(car_data: Dict) -> bool:
    """Process a single car listing data."""
    try:
        for required_field in ["make", "model", "year"]:
            if not car_data.get(required_field):
                logger.warning(f"Skipping car with missing {required_field}")
                return False

        exists = await CarCRUD().check_if_car_exists(car_data)

        if not exists:
            try:
                car_model = convert_to_pydantic_model(car_data)
                await CarCRUD().create_car(car_model)
                logger.info(
                    f"Saved {car_data['make']} {car_data['model']} from {car_data.get('source_site', 'Unknown')}"
                )
                return True
            except ValidationError as e:
                logger.error(f"Validation error during car processing: {e}")
                return False
        return False
    except Exception as e:
        logger.error(f"Error processing car data: {str(e)}")
        return False
