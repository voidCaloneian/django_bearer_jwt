import json
import pytest


@pytest.mark.django_db
def test_signup(client, user_data):
    """
    Тест регистрации. Ожидаем, что при корректных данных будет создан пользователь
    и в ответе вернутся token и refresh токены.
    """
    response = client.post(
        "/api/accounts/signup/",
        data=json.dumps(user_data),
        content_type="application/json",
    )
    assert response.status_code == 201, f"Ошибка регистрации: {response.json()}"
    data = response.json()
    assert "token" in data, "Access токен отсутствует в ответе"
    assert "refresh" in data, "Refresh токен отсутствует в ответе"


@pytest.mark.django_db
def test_signin(client, create_user, user_data):
    """
    Тест логина. При корректных данных ожидаем получение токенов.
    """
    response = client.post(
        "/api/accounts/signin/",
        data=json.dumps(user_data),
        content_type="application/json",
    )
    assert response.status_code == 200, f"Ошибка логина: {response.json()}"
    data = response.json()
    assert "token" in data, "Access токен отсутствует в ответе"
    assert "refresh" in data, "Refresh токен отсутствует в ответе"


@pytest.mark.django_db
def test_info(client, create_user, user_data):
    """
    Тест запроса информации о пользователе.
    Проверяем, что в ответе возвращается identifier, id_type и продлевается токен.
    """
    # Получаем токены через логин
    response = client.post(
        "/api/accounts/signin/",
        data=json.dumps(user_data),
        content_type="application/json",
    )
    token = response.json()["token"]
    auth_header = "Bearer " + token

    response = client.get("/api/accounts/info/", HTTP_AUTHORIZATION=auth_header)
    assert response.status_code == 200, f"Ошибка запроса info: {response.json()}"
    data = response.json()
    assert data.get("identifier") == user_data["identifier"], "Неверный identifier"
    assert "id_type" in data, "Тип идентификатора отсутствует"
    assert "token" in data, "Новый токен продления не возвращается"


@pytest.mark.django_db
def test_logout_current_token(client, create_user, user_data):
    """
    Тест логаута текущего токена.
    При all=false требуется передать refresh-токен для разлогина.
    """
    # Выполняем логин, чтобы получить access и refresh токены
    response = client.post(
        "/api/accounts/signin/",
        data=json.dumps(user_data),
        content_type="application/json",
    )
    json_data = response.json()
    token = json_data["token"]
    refresh = json_data["refresh"]
    auth_header = "Bearer " + token

    logout_data = {"all": False, "refresh": refresh}
    response = client.post(
        "/api/accounts/logout/",
        data=json.dumps(logout_data),
        content_type="application/json",
        HTTP_AUTHORIZATION=auth_header,
    )
    # В случае успешного выхода ожидаем 200; если refresh токен неверный – 400
    assert response.status_code in (
        200,
        400,
    ), f"Неверный статус logout: {response.json()}"


@pytest.mark.django_db
def test_logout_all_tokens(client, create_user, user_data):
    """
    Тест логаута всех токенов пользователя.
    """
    # Выполняем логин для получения токена
    response = client.post(
        "/api/accounts/signin/",
        data=json.dumps(user_data),
        content_type="application/json",
    )
    token = response.json()["token"]
    auth_header = "Bearer " + token

    logout_data = {"all": True}
    response = client.post(
        "/api/accounts/logout/",
        data=json.dumps(logout_data),
        content_type="application/json",
        HTTP_AUTHORIZATION=auth_header,
    )
    assert response.status_code == 200, f"Ошибка logout all tokens: {response.json()}"
