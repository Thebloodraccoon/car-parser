from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.endpoints.cars import router as cars_router
from app.endpoints.users import router as users_router
from app.endpoints.auth import router as auth_router
from app.utils.default_user import create_default_user


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_default_user()
    yield
    print("Application is shutting down.")


app = FastAPI(
    title="Car announcement parser",
    description="Crud for scraper car and users",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(users_router, prefix="/users", tags=["Users"])
app.include_router(cars_router, prefix="/cars", tags=["Cars"])
