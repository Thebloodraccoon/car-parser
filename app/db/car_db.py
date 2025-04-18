from datetime import datetime
from typing import Dict, Any, List, Union

from bson import ObjectId
from bson.errors import InvalidId

from app.conf import database, CAR_COLLECTION
from app.db.utils import convert_object_id_to_str
from app.exceptions.car_exceptions import (
    InvalidCarIDException,
    CarNotFoundException,
    CarAlreadyExistsException,
)
from app.schemas.cars import CarCreate, CarUpdate


class CarCRUD:
    def __init__(self):
        self.collection = database[CAR_COLLECTION]

    async def create_car(
        self, car_data: Union[CarCreate, Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Create a new car entry in the database."""
        if hasattr(car_data, "model_dump"):
            car_data_dict = car_data.model_dump()
        else:
            car_data_dict = car_data

        if await self.check_if_car_exists(car_data_dict):
            raise CarAlreadyExistsException()

        for key in ["image_url", "source_url"]:
            if key in car_data_dict and hasattr(car_data_dict[key], "__str__"):
                car_data_dict[key] = str(car_data_dict[key])

        now = datetime.now()
        car_data_dict["created_at"] = now
        car_data_dict["updated_at"] = now

        result = await self.collection.insert_one(car_data_dict)
        created_car = await self.collection.find_one({"_id": result.inserted_id})
        return convert_object_id_to_str(created_car)

    async def get_car_by_id(self, car_id: str) -> Dict[str, Any]:
        """Get a car by its ID."""
        try:
            car = await self.collection.find_one({"_id": ObjectId(car_id)})
            if not car:
                raise CarNotFoundException(f"Car with ID {car_id} not found")
            return convert_object_id_to_str(car)
        except InvalidId:
            raise InvalidCarIDException()

    async def get_cars(self, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all cars with pagination."""
        cursor = self.collection.find().skip(skip).limit(limit)
        cars = await cursor.to_list(length=limit)
        return [convert_object_id_to_str(car) for car in cars]

    async def update_car(self, car_id: str, car_data: CarUpdate) -> Dict[str, Any]:
        """Update a car by its ID."""
        try:
            update_data = {
                k: v for k, v in car_data.model_dump().items() if v is not None
            }

            for key in ["image_url", "source_url"]:
                if key in update_data and hasattr(update_data[key], "__str__"):
                    update_data[key] = str(update_data[key])

            update_data["updated_at"] = datetime.now()

            result = await self.collection.update_one(
                {"_id": ObjectId(car_id)}, {"$set": update_data}
            )

            if result.modified_count == 0:
                car = await self.collection.find_one({"_id": ObjectId(car_id)})
                if not car:
                    raise CarNotFoundException(f"Car with ID {car_id} not found")

            updated_car = await self.collection.find_one({"_id": ObjectId(car_id)})
            return convert_object_id_to_str(updated_car)
        except InvalidId:
            raise InvalidCarIDException()

    async def delete_car(self, car_id: str) -> bool:
        """Delete a car by its ID."""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(car_id)})
            if result.deleted_count == 0:
                raise CarNotFoundException(f"Car with ID {car_id} not found")
            return True
        except InvalidId:
            raise InvalidCarIDException()

    async def check_if_car_exists(self, car_data: dict) -> bool:
        """Check if a car with the given attributes already exists."""
        query = {
            "source_site": car_data.get("source_site"),
            "make": car_data.get("make"),
            "model": car_data.get("model"),
            "year": car_data.get("year"),
            "price": car_data.get("price"),
            "mileage": car_data.get("mileage"),
            "location": car_data.get("location"),
        }

        query = {k: v for k, v in query.items() if v is not None}

        count = await self.collection.count_documents(query)
        return count > 0

    async def get_cars_by_make(self, make: str, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get cars filtered by make."""
        cursor = self.collection.find({"make": {"$regex": f"^{make}$", "$options": "i"}}).skip(skip).limit(limit)
        cars = await cursor.to_list(length=limit)
        return [convert_object_id_to_str(car) for car in cars]

    async def get_cars_by_year(self, year: int, skip: int = 0, limit: int = 100) -> List[Dict[str, Any]]:
        """Get cars filtered by production year."""
        cursor = self.collection.find({"year": year}).skip(skip).limit(limit)
        cars = await cursor.to_list(length=limit)
        return [convert_object_id_to_str(car) for car in cars]
