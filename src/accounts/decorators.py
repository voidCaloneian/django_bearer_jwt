import json
from functools import wraps
from rest_framework_simplejwt.tokens import RefreshToken


def extend_token(func):
    """
    Декоратор, который после успешного запроса генерирует новый access токен и добавляет его в JSON-ответ.
    Применяется ко всем методам, кроме login/signup.
    """

    @wraps(func)
    def wrapper(self, request, *args, **kwargs):
        response = func(self, request, *args, **kwargs)
        # Если пользователь аутентифицирован и ответ является JSONResponse
        if request.user and request.user.is_authenticated:
            new_token = RefreshToken.for_user(request.user).access_token
            try:
                # Если ответ уже в формате dict
                data = (
                    response.data
                    if hasattr(response, "data")
                    else json.loads(response.content)
                )
                data["token"] = str(new_token)
                response.data = data
            except Exception:
                pass
        return response

    return wrapper
