from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate
from app.utils.password import hash_password, verify_password


class UserService:
    def __init__(self) -> None:
        self.repository = UserRepository()

    def create_user(
        self,
        db: Session,
        user_data: UserCreate,
    ) -> User:
        existing_user = self.repository.get_by_email(
            db,
            user_data.email,
        )

        if existing_user:
            raise ValueError("A user with this email already exists")

        hashed_password = hash_password(user_data.password)

        return self.repository.create(
            db,
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
        )
    def authenticate_user(
        self,
        db: Session,
        email: str,
        password: str,
    ) -> User | None:
        user = self.repository.get_by_email(
            db,
            email,
        )
        if user is None:
            return None

        if not verify_password(
            password,
            user.hashed_password,
        ):
            return None
        if not user.is_active:
            return None
        return user 