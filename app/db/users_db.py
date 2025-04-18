from datetime import datetime
from typing import Optional, Dict, Any, Union, List

from bson import ObjectId
from pydantic import EmailStr

from app.conf import database, USER_COLLECTION
from app.db.utils import convert_object_id_to_str, hash_password
from app.exceptions.user_exceptions import (
    UserNotFoundException,
    UserAlreadyExistsException,
)
from app.models import User
from app.schemas.users import UserCreate, UserUpdate


class UserCRUD:
    def __init__(self):
        self.collection = database[USER_COLLECTION]

    async def create_user(self, user: UserCreate):
        if await self._check_if_user_exists(user.email, user.username):
            raise UserAlreadyExistsException()

        new_user = User(
            username=user.username,
            email=user.email,
            password_hash=hash_password(user.password),
            created_at=datetime.now(),
        )

        result = await self.collection.insert_one(new_user.model_dump(by_alias=True))
        created_user = await self.collection.find_one({"_id": result.inserted_id})
        return convert_object_id_to_str(created_user)

    async def get_all_users(self):
        users = await self.collection.find().to_list(length=100)
        return convert_object_id_to_str(users)

    async def get_user_by_id(self, user_id: str):
        user = await self.collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise UserNotFoundException()
        return convert_object_id_to_str(user)

    async def update_user(self, user_id: str, user_update: UserUpdate):
        user = await self.collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise UserNotFoundException()

        update_data = user_update.model_dump(exclude_unset=True)

        if "password" in update_data:
            update_data["password_hash"] = hash_password(update_data.pop("password"))

        if "username" in update_data and update_data["username"] != user["username"]:
            existing = await self.get_user_by_username(update_data["username"])
            if existing:
                raise UserAlreadyExistsException()

        if "email" in update_data and update_data["email"] != user["email"]:
            existing = await self.get_user_by_email(update_data["email"])
            if existing:
                raise UserAlreadyExistsException()

        if update_data:
            await self.collection.update_one(
                {"_id": ObjectId(user_id)}, {"$set": update_data}
            )

        updated_user = await self.collection.find_one({"_id": ObjectId(user_id)})
        return convert_object_id_to_str(updated_user)

    async def delete_user(self, user_id: str):
        user = await self.collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            raise UserNotFoundException()
        await self.collection.delete_one({"_id": ObjectId(user_id)})

    async def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        return await self.collection.find_one({"email": email})

    async def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        return await self.collection.find_one({"username": username})


    async def _check_if_user_exists(self, email: EmailStr, username: str) -> bool:
        count = await self.collection.count_documents(
            {"$or": [{"email": str(email)}, {"username": username}]}
        )
        return count > 0
