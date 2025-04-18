from fastapi import FastAPI

from app.endpoints.cars import router as cars_router
from app.endpoints.users import router as users_router

app = FastAPI(
    title="Car announcement parser",
    description="Crud for scraper car and users",
    version="1.0.0",
)

app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(cars_router, prefix="/cars", tags=["Cars"])
