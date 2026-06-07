from datetime import datetime, timezone
import logging
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.common.utils.errorClasses import UnauthorizedAccessError, UserNotFoundError
from app.common.utils.jwtUtil import JwtService
from app.db.database import getDatabase
from app.db.schema.userSchema import UserSchema
from app.db.settings import getSettings

appSettings = getSettings()
jwtService = JwtService(secretKey=appSettings.SECRET_KEY, algorithm=appSettings.ALGORITHM)

_http_bearer = HTTPBearer(auto_error=False)


def validateToken(
    credentials: Annotated[HTTPAuthorizationCredentials,Depends(_http_bearer)],
    databaseCursor: Session = Depends(getDatabase),
) -> UserSchema:
    """
    FastAPI dependency: JWT must come from the ``Authorization`` header
    (``Bearer <token>``). A bare ``str`` parameter would be bound as a **query** param instead.
    """
    try:
        raw_token = credentials.credentials.strip()
        decoded_token = jwtService.decodeToken(token=raw_token)
        expiration_time = decoded_token["exp"]
        current_time = int(datetime.now(timezone.utc).timestamp())
        if expiration_time < current_time:
            raise UnauthorizedAccessError()
        user_id: int = decoded_token["id"]
        user: UserSchema | None = (
            databaseCursor.query(UserSchema).filter(UserSchema.id == user_id).first()
        )
        if not user:
            raise UserNotFoundError()
        return user
    except HTTPException:
        raise
    except (UnauthorizedAccessError, UserNotFoundError) as e:
        raise HTTPException(status_code=401, detail=str(e)) from e
    except Exception as e:
        logging.error(msg=f"error=Error validating token: {e}")
        raise HTTPException(status_code=401, detail="Unauthorized") from e
