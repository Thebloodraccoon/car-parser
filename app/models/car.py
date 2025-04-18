from datetime import datetime
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, HttpUrl
from app.models.base import PyObjectId


class Car(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    make: str = Field(..., description="Car make name")
    model: str = Field(..., description="Car model name")
    year: int = Field(..., description="Year of manufacture")
    price: float = Field(..., description="Price in USD")
    mileage: int = Field(..., description="Mileage in kilometers")
    engine_type: str = Field(..., description="Engine type")
    engine_capacity: str = Field(..., description="Engine capacity")
    transmission: str = Field(..., description="Transmission type")
    location: str = Field(..., description="Car location")
    image_url: Optional[HttpUrl] = Field(None, description="URL of the car image")
    source_url: HttpUrl = Field(..., description="Source URL of the listing")
    source_site: str = Field(..., description="Source site name")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
    }
