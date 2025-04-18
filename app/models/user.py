from datetime import datetime
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr
from app.models.base import PyObjectId


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str = Field(..., description="Username")
    email: EmailStr = Field(..., description="Email address")
    password_hash: str = Field(..., description="Hashed password")
    created_at: datetime = Field(default_factory=datetime.now)
    last_login: Optional[datetime] = Field(None)

    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {ObjectId: str},
        "json_schema_extra": {
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "password_hash": "hashed_password",
                "created_at": "2023-05-26T10:00:00",
                "last_login": "2023-05-26T12:30:00",
            }
        },
    }
