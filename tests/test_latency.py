import json
import pytest


@pytest.mark.django_db
def test_latency_endpoint(client, create_user, user_data):
    """
    Тест эндпоинта /api/app/latency/.
    Проверяем, что при корректном access токене возвращается latency.
    """
    # Получаем access токен через логин
    response = client.post(
        "/api/accounts/signin/",
        data=json.dumps(user_data),
        content_type="application/json",
    )
    token = response.json()["token"]
    auth_header = "Bearer " + token

    response = client.get("/api/latency/", HTTP_AUTHORIZATION=auth_header)
    assert response.status_code == 200, f"Ошибка эндпоинта latency: {response.json()}"
    data = response.json()
    assert "latency" in data, "Ключ latency отсутствует в ответе"
