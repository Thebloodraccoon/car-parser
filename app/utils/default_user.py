from app.conf import DEFAULT_USER_NAME, DEFAULT_USER_EMAIL, DEFAULT_USER_PASSWORD
from app.db.users_db import UserCRUD
from app.schemas.users import UserCreate


async def create_default_user():
    user_crud = UserCRUD()

    exising = await user_crud.get_user_by_email(DEFAULT_USER_EMAIL)

    if exising:
        return

    user = UserCreate(
        username=DEFAULT_USER_NAME,
        email=DEFAULT_USER_EMAIL,
        password=DEFAULT_USER_PASSWORD,
    )

    await user_crud.create_user(user)
