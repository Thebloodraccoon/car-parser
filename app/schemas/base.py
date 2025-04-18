from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class BaseDBModel(BaseModel):
    """Base model for database objects with common fields"""

    id: str = Field(..., description="Database ID")
    created_at: datetime = Field(..., description="Creation timestamp")

    model_config = ConfigDict(from_attributes=True)
