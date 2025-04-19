from typing import List

from fastapi import APIRouter, status, Query, Depends

from app.db.car_db import CarCRUD
from app.schemas.cars import CarCreate, CarResponse, CarUpdate
from app.schemas.users import UserResponse
from app.utils.auth import get_current_user

router = APIRouter()


async def get_car_crud() -> CarCRUD:
    """Dependency to get CarCRUD instance"""
    return CarCRUD()


@router.get("/", response_model=List[CarResponse])
async def get_cars(
    skip: int = Query(0, ge=0, description="Number of cars to skip"),
    limit: int = Query(
        100, ge=1, le=100, description="Maximum number of cars to return"
    ),
    car_crud: CarCRUD = Depends(get_car_crud),
    _: UserResponse = Depends(get_current_user),
):
    cars = await car_crud.get_cars(skip=skip, limit=limit)
    return cars


@router.get("/{car_id}", response_model=CarResponse)
async def get_car_by_id(
    car_id: str,
    car_crud: CarCRUD = Depends(get_car_crud),
    _: UserResponse = Depends(get_current_user),
):
    return await car_crud.get_car_by_id(car_id)


@router.get("/make/{make}", response_model=List[CarResponse])
async def get_cars_by_make(
    make: str,
    skip: int = Query(0, ge=0, description="Number of cars to skip"),
    limit: int = Query(
        100, ge=1, le=100, description="Maximum number of cars to return"
    ),
    car_crud: CarCRUD = Depends(get_car_crud),
    _: UserResponse = Depends(get_current_user),
):
    """Get cars filtered by make (e.g., Toyota, BMW)"""
    return await car_crud.get_cars_by_make(make, skip=skip, limit=limit)


@router.get("/year/{year}", response_model=List[CarResponse])
async def get_cars_by_year(
    year: int,
    skip: int = Query(0, ge=0, description="Number of cars to skip"),
    limit: int = Query(
        100, ge=1, le=100, description="Maximum number of cars to return"
    ),
    car_crud: CarCRUD = Depends(get_car_crud),
    _: UserResponse = Depends(get_current_user),
):
    """Get cars filtered by production year"""
    return await car_crud.get_cars_by_year(year, skip=skip, limit=limit)


@router.post("/", response_model=CarResponse, status_code=status.HTTP_201_CREATED)
async def create_car(
    car: CarCreate,
    car_crud: CarCRUD = Depends(get_car_crud),
    _: UserResponse = Depends(get_current_user),
):
    return await car_crud.create_car(car)


@router.put("/{car_id}", response_model=CarResponse)
async def update_car(
    car_id: str,
    car_update: CarUpdate,
    car_crud: CarCRUD = Depends(get_car_crud),
    _: UserResponse = Depends(get_current_user),
):
    return await car_crud.update_car(car_id, car_update)


@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car(
    car_id: str,
    car_crud: CarCRUD = Depends(get_car_crud),
    _: UserResponse = Depends(get_current_user),
):
    await car_crud.delete_car(car_id)
    return None
