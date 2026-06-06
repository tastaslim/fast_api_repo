"""
Auth endpoint — issues JWT tokens.

For a real service replace the hardcoded user lookup with a DB query
and bcrypt password verification.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import create_access_token
from app.schemas.auth import TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])

# ── Stub user store (replace with DB) ────────────────────────────────────────
_FAKE_USERS: dict[str, str] = {
    "admin": "changeme",
}


@router.post("/token", response_model=TokenResponse, summary="Obtain JWT access token")
async def login(form: OAuth2PasswordRequestForm = Depends()) -> TokenResponse:
    password = _FAKE_USERS.get(form.username)
    if password is None or password != form.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(subject=form.username)
    return TokenResponse(access_token=token)
