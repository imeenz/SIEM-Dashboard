from app.utils.password import hash_password, verify_password


def test_hash_password_does_not_store_plaintext():
    password = "SecurePassword123!"

    hashed = hash_password(password)

    assert hashed != password
    assert password not in hashed


def test_verify_password_accepts_correct_password():
    password = "SecurePassword123!"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True


def test_verify_password_rejects_wrong_password():
    hashed = hash_password("SecurePassword123!")

    assert verify_password("WrongPassword123!", hashed) is False