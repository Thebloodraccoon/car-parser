from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt

from app.conf import JWT_SECRET_KEY, JWT_ALGORITHM, get_redis

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 30


def create_token(
    data: dict, token_type: str, expires_delta: Optional[timedelta]
) -> str:
    to_encode = data.copy()
    to_encode.update({"token_type": token_type})
    expire = datetime.now(timezone.utc) + expires_delta  # type: ignore
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


def create_access_token(data: dict):
    return create_token(data, "access", timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))


def create_refresh_token(data: dict):
    return create_token(data, "refresh", timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))


async def blacklist_token(token: str, expire_time: datetime):
    async with get_redis() as redis:
        ttl = int((expire_time - datetime.now(timezone.utc)).total_seconds())
        if ttl > 0:
            await redis.setex(f"blacklist:{token}", ttl, "blacklisted")
            return True

        return False


async def is_token_blacklisted(token: str):
    async with get_redis() as redis:
        return await redis.exists(f"blacklist:{token}")


def get_payload(token: HTTPAuthorizationCredentials):
    return jwt.decode(token.credentials, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
