from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl, model_validator, ConfigDict

from app.schemas.base import BaseDBModel


class CarBase(BaseModel):
    """Base schema for Car data"""

    make: str = Field(..., min_length=1, max_length=100, description="Car make name")
    model: str = Field(..., min_length=1, max_length=100, description="Car model name")
    year: int = Field(..., ge=1900, le=2030, description="Year of manufacture")
    price: float = Field(..., ge=0, description="Price in USD")
    mileage: int = Field(..., ge=0, description="Mileage in kilometers")
    engine_type: str = Field(
        ..., min_length=1, max_length=100, description="Engine details"
    )
    engine_capacity: str = Field(
        ..., min_length=1, max_length=50, description="Engine capacity"
    )
    transmission: str = Field(
        ..., min_length=1, max_length=50, description="Transmission type"
    )
    location: str = Field(..., min_length=1, max_length=100, description="Car location")
    image_url: Optional[HttpUrl] = Field(None, description="URL of the car image")

    @model_validator(mode="after")
    def validate_car_data(self):
        """Validate car data and provide defaults for missing values"""
        if not self.make:
            self.make = "Unknown"
        if not self.model:
            self.model = "Unknown"
        if not self.year or self.year < 1900 or self.year > 2030:
            self.year = 2000
        if self.price is None or self.price < 0:
            self.price = 0.0
        if self.mileage is None or self.mileage < 0:
            self.mileage = 0
        if not self.engine_type:
            self.engine_type = "Unknown"
        if not self.engine_capacity:
            self.engine_capacity = "Unknown"
        if not self.transmission:
            self.transmission = "Unknown"
        if not self.location:
            self.location = "Unknown"
        return self


class CarCreate(CarBase):
    """Schema for creating a new car"""

    source_url: HttpUrl = Field(..., description="Source URL of the listing")
    source_site: str = Field(
        ..., min_length=1, max_length=100, description="Source site name"
    )

    @model_validator(mode="after")
    def validate_source_data(self):
        """Validate source data"""
        if not self.source_site:
            self.source_site = "Unknown"
        return self


class CarUpdate(BaseModel):
    """Schema for updating a car"""

    make: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Car make name"
    )
    model: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Car model name"
    )
    year: Optional[int] = Field(
        None, ge=1900, le=2030, description="Year of manufacture"
    )
    price: Optional[float] = Field(None, ge=0, description="Price in USD")
    mileage: Optional[int] = Field(None, ge=0, description="Mileage in kilometers")
    engine_type: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Engine details"
    )
    engine_capacity: Optional[str] = Field(
        None, min_length=1, max_length=50, description="Engine capacity"
    )
    transmission: Optional[str] = Field(
        None, min_length=1, max_length=50, description="Transmission type"
    )
    location: Optional[str] = Field(
        None, min_length=1, max_length=100, description="Car location"
    )
    image_url: Optional[HttpUrl] = Field(None, description="URL of the car image")

    model_config = ConfigDict(from_attributes=True)


class CarResponse(CarBase, BaseDBModel):
    """Schema for car stored in database"""

    source_url: HttpUrl = Field(..., description="Source URL of the listing")
    source_site: str = Field(
        ..., min_length=1, max_length=100, description="Source site name"
    )
    updated_at: datetime = Field(..., description="Last update timestamp")
    image_url: Optional[HttpUrl] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "make": "Toyota",
                "model": "Camry",
                "year": 2020,
                "price": 25000.0,
                "mileage": 15000,
                "engine_type": "Gasoline",
                "engine_capacity": "2.5 L",
                "transmission": "Automatic",
                "location": "New York",
                "image_url": "https://example.com/car.jpg",
                "source_url": "https://example.com/listing",
                "source_site": "CarSales",
                "created_at": "2023-05-26T10:00:00",
                "updated_at": "2023-05-26T10:00:00",
            }
        },
    )
