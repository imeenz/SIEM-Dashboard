import pytest

from app.schemas.user import UserCreate
from app.services.user import UserService
from app.utils.password import verify_password


def test_create_user(db_session):
    service = UserService()

    user_data = UserCreate(
        email="analyst@example.com",
        password="SecurePassword123!",
        full_name="SOC Analyst",
    )

    user = service.create_user(
        db=db_session,
        user_data=user_data,
    )

    assert user.id is not None
    assert user.email == "analyst@example.com"
    assert user.full_name == "SOC Analyst"
    assert user.is_active is True

    assert user.hashed_password != "SecurePassword123!"

    assert verify_password(
        "SecurePassword123!",
        user.hashed_password,
    )


def test_create_user_rejects_duplicate_email(db_session):
    service = UserService()

    user_data = UserCreate(
        email="analyst@example.com",
        password="SecurePassword123!",
        full_name="SOC Analyst",
    )

    service.create_user(
        db=db_session,
        user_data=user_data,
    )

    with pytest.raises(
        ValueError,
        match="A user with this email already exists",
    ):
        service.create_user(
            db=db_session,
            user_data=user_data,
        )
def test_authenticate_user_with_correct_password(db_session):
    service = UserService()

    user_data = UserCreate(
        email="login@example.com",
        password="SecurePassword123!",
        full_name="SOC Analyst",
    )

    service.create_user(
        db=db_session,
        user_data=user_data,
    )

    user = service.authenticate_user(
        db=db_session,
        email="login@example.com",
        password="SecurePassword123!",
    )

    assert user is not None
    assert user.email == "login@example.com"


def test_authenticate_user_rejects_wrong_password(db_session):
    service = UserService()

    user_data = UserCreate(
        email="wrong@example.com",
        password="SecurePassword123!",
        full_name="SOC Analyst",
    )

    service.create_user(
        db=db_session,
        user_data=user_data,
    )

    user = service.authenticate_user(
        db=db_session,
        email="wrong@example.com",
        password="WrongPassword!",
    )

    assert user is None


def test_authenticate_user_rejects_unknown_user(db_session):
    service = UserService()

    user = service.authenticate_user(
        db=db_session,
        email="missing@example.com",
        password="SecurePassword123!",
    )

    assert user is None