from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, ConfigDict, model_validator

from app.schemas.base import BaseDBModel


class UserBase(BaseModel):
    """Base schema for User data"""

    email: EmailStr = Field(..., description="User email address")
    username: str = Field(..., min_length=3, max_length=50, description="Username")

    @model_validator(mode="after")
    def validate_user_data(self):
        """Validate user data"""
        if not self.username:
            raise ValueError("Username cannot be empty")
        if not self.email:
            raise ValueError("Email cannot be empty")
        return self


class UserCreate(BaseModel):
    """Schema for creating a new user"""

    username: str = Field(..., min_length=3, max_length=50, description="Username")
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, description="User password")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "johndoe",
                "email": "john@example.com",
                "password": "strong_password_123",
            }
        }
    )

    @model_validator(mode="after")
    def validate_user_create(self):
        """Validate user creation data"""
        if not self.username:
            raise ValueError("Username cannot be empty")
        if not self.email:
            raise ValueError("Email cannot be empty")
        if not self.password:
            raise ValueError("Password cannot be empty")
        return self


class UserUpdate(BaseModel):
    """Schema for updating a user"""

    username: Optional[str] = Field(
        None, min_length=3, max_length=50, description="Username"
    )
    email: Optional[EmailStr] = Field(None, description="User email address")

    model_config = ConfigDict(from_attributes=True)


class UserResponse(UserBase, BaseDBModel):
    """Schema for user stored in database"""

    last_login: Optional[datetime] = Field(None, description="Last login timestamp")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": "507f1f77bcf86cd799439011",
                "username": "johndoe",
                "email": "john@example.com",
                "created_at": "2023-05-26T10:00:00",
                "last_login": "2023-05-26T12:30:00",
            }
        },
    )
