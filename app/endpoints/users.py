from typing import List

from fastapi import APIRouter, status, Depends

from app.db.users_db import UserCRUD
from app.schemas.users import UserCreate, UserUpdate, UserResponse


router = APIRouter()


async def get_user_crud() -> UserCRUD:
    """Dependency to get UserCRUD instance"""
    return UserCRUD()


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    user_crud: UserCRUD = Depends(get_user_crud),
):
    return await user_crud.create_user(user)


@router.get("/", response_model=List[UserResponse])
async def get_users(
    user_crud: UserCRUD = Depends(get_user_crud),
):
    return await user_crud.get_all_users()


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: str,
    user_crud: UserCRUD = Depends(get_user_crud),
):
    return await user_crud.get_user_by_id(user_id)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    user_crud: UserCRUD = Depends(get_user_crud),
):
    return await user_crud.update_user(user_id, user_update)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    user_crud: UserCRUD = Depends(get_user_crud),
):
    return await user_crud.delete_user(user_id)
