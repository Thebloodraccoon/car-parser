from datetime import datetime, timezone
from typing import Any, Coroutine

from fastapi import Depends
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from jose import JWTError
from passlib.context import CryptContext

from app.db.users_db import UserCRUD
from app.exceptions.token_exceptions import (
    InvalidTokenException,
    TokenBlacklistedException,
)
from app.exceptions.user_exceptions import UserNotFoundException
from app.models import User
from app.utils.token import get_payload, blacklist_token, is_token_blacklisted

ACCESS_TOKEN_TYPE = "access"  # nosec
REFRESH_TOKEN_TYPE = "refresh"  # nosec

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


async def logout_user(
    token_str: str,
):
    try:
        token = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token_str)
        payload = get_payload(token)

        email: str = payload.get("sub")
        exp = payload.get("exp")
        token_type: str = payload.get("token_type")

        if token_type != ACCESS_TOKEN_TYPE:
            raise InvalidTokenException()

        await get_user(email)
        success = await blacklist_token(
            token.credentials, datetime.fromtimestamp(exp, tz=timezone.utc)
        )

        if success:
            return {"detail": "Logout successful"}
        return None

    except JWTError:
        return {"detail": "Token already invalid"}


async def get_current_user(
    token: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
) -> dict[str, Any]:
    try:
        email, token_type = await check_token_credential(token)

        if token_type != ACCESS_TOKEN_TYPE:
            raise InvalidTokenException()

    except JWTError:
        raise InvalidTokenException()

    user = await get_user(email)
    if user is None:
        raise UserNotFoundException()

    return user


async def verify_refresh_token(
    token_str: str,
) -> str:
    try:
        token = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token_str)
        email, token_type = await check_token_credential(token)

        if token_type != REFRESH_TOKEN_TYPE:
            raise InvalidTokenException()

        user = await get_user(email)
        if not user:
            raise UserNotFoundException()

        return email

    except JWTError:
        raise InvalidTokenException()


async def check_token_credential(token: HTTPAuthorizationCredentials):
    if await is_token_blacklisted(token.credentials):
        raise TokenBlacklistedException()

    payload = get_payload(token)
    email: str = payload.get("sub")
    token_type: str = payload.get("token_type")

    if email is None:
        raise InvalidTokenException()

    return email, token_type


async def get_user(email: str) -> User:
    user = await UserCRUD().get_user_by_email(email=email)
    if user:
        return user

    raise UserNotFoundException()


async def update_last_login(user: User):
    await UserCRUD().update_user_last_login(user)
