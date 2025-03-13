from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

from .serializers import (
    SignupSerializer,
    SigninSerializer,
    InfoSerializer,
    LogoutSerializer,
)
from .decorators import extend_token


class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Генерируем токены для нового пользователя
            refresh = RefreshToken.for_user(user)
            data = {
                "token": str(refresh.access_token),
                "refresh": str(refresh),
            }
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SigninView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = SigninSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            refresh = RefreshToken.for_user(user)
            data = {
                "token": str(refresh.access_token),
                "refresh": str(refresh),
            }
            return Response(data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_token
    def get(self, request):
        serializer = InfoSerializer(
            {"identifier": request.user.identifier, "id_type": request.user.id_type}
        )
        return Response(serializer.data)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_token
    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            log_all = serializer.validated_data.get("all", False)
            if log_all:
                # Блокируем все токены пользователя
                tokens = OutstandingToken.objects.filter(  # pylint: disable=no-member
                    user=request.user
                )
                for token in tokens:
                    _, _ = (
                        BlacklistedToken.objects.get_or_create(  # pylint: disable=no-member
                            token=token
                        )
                    )
                return Response({"detail": "Все токены пользователя разлогинены"})
            else:
                # Для удаления только текущего токена ожидаем refresh в теле запроса
                refresh_token = serializer.validated_data.get("refresh", None)
                if not refresh_token:
                    return Response(
                        {
                            "detail": "refresh токен обязателен для логаута текущего токена"
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                try:
                    token_obj = RefreshToken(refresh_token)
                    token_obj.blacklist()
                    return Response({"detail": "Текущий токен разлогинен"})
                except Exception as e:
                    return Response(
                        {"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST
                    )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
