import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.models.user import User
from app.repositories.user import UserRepository
from app.utils.jwt import decode_access_token


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired authentication token",
    )

    try:
        payload = decode_access_token(credentials.credentials)
        email = payload.get("sub")

        if not email:
            raise credentials_exception

    except jwt.PyJWTError as exc:
        raise credentials_exception from exc

    user = UserRepository().get_by_email(
        db=db,
        email=email,
    )

    if user is None or not user.is_active:
        raise credentials_exception

    return user