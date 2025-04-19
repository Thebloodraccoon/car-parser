from fastapi import APIRouter, Depends, Request, Response  # type: ignore

from app.exceptions.auth_exceptions import InvalidCredentialsException
from app.schemas.auth import Login, Token, LogoutResponse
from app.schemas.users import UserResponse
from app.utils.auth import (
    update_last_login,
    get_user,
    verify_password,
    verify_refresh_token,
    get_current_user,
    logout_user,
)
from app.utils.token import create_access_token, create_refresh_token

router = APIRouter()


@router.post("/login", response_model=Token)
async def login(request: Login, response: Response):
    user = await get_user(request.email)
    if not user or not verify_password(request.password, user["password_hash"]):
        raise InvalidCredentialsException

    await update_last_login(user)

    access_token = create_access_token(data={"sub": user["email"]})
    refresh_token = create_refresh_token(data={"sub": user["email"]})

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="none",
        secure=True,
        max_age=30 * 24 * 60 * 60,
    )

    return {"access_token": str(access_token)}


@router.post("/refresh")
async def refresh_tokens(
    request: Request,
):
    refresh_token = request.cookies.get("refresh_token", "")
    user_email = await verify_refresh_token(refresh_token)
    new_access_token = create_access_token(data={"sub": user_email})

    return {"access_token": new_access_token}


@router.post("/logout", response_model=LogoutResponse)
async def logout(
    http_request: Request,
    _: UserResponse = Depends(get_current_user),
):

    jwt_token = http_request.headers.get("Authorization").replace("Bearer ", "")
    response = await logout_user(jwt_token)

    return response
