from app.core.security import hash_password, verify_password, create_access_token


def test_hash_password():
    password = 'password'
    hashed_password = hash_password(password)
    assert password != hashed_password


def test_verify_password():
    password = 'password'
    hashed_password = hash_password(password)
    assert verify_password(password, hashed_password)
    assert not verify_password('another_password', hashed_password)


def test_create_access_token():
    user_id = 'user_id'
    access_token = create_access_token(user_id=user_id)
    assert access_token is not None
    assert access_token.startswith('eyJ')