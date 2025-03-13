import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user_data():
    return {"identifier": "test@example.com", "password": "strongpassword123"}


@pytest.fixture
def create_user(db, user_data):
    """
    Фикстура для создания пользователя, используемого в тестах.
    """
    user = User.objects.create_user(**user_data)
    return user
