import re
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.db import models

ID_TYPE_CHOICES = (
    ("phone", "Phone"),
    ("email", "Email"),
)

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
PHONE_REGEX = re.compile(r"^\+?1?\d{9,15}$")


class CustomUserManager(BaseUserManager):
    def _normalize_phone(self, phone):
        # Удаляем пробелы и прочие символы, оставляем только цифры
        phone = re.sub(r"\D", "", phone.strip())
        # Если номер начинается с 8, заменяем на 7
        if phone.startswith("8"):
            phone = "7" + phone[1:]
        return f"+{phone}"

    def validate_identifier(self, identifier):
        """
        Валидация идентификатора пользователя
        """
        if not identifier:
            raise ValueError("Identifier (email or phone) is required")

        _type = None
        if "@" in identifier:
            if not EMAIL_REGEX.fullmatch(identifier):
                raise ValueError("Invalid email address")
            _type = "email"
        else:
            normalized_phone = self._normalize_phone(identifier)
            if not PHONE_REGEX.fullmatch(normalized_phone):
                raise ValueError("Invalid phone number")
            _type = "phone"
            identifier = normalized_phone

        if CustomUser.objects.filter(identifier=identifier).exists():
            raise ValueError("User with this identifier already exists")

        return _type

    def create_user(self, identifier, password=None, **extra_fields):
        """
        Идентификатор может быть либо email либо phone. Определяем тип через отдельную валидацию.
        """
        id_type = self.validate_identifier(identifier)
        extra_fields["id_type"] = id_type

        if id_type == "email":
            extra_fields.setdefault("email", identifier)
        else:
            normalized = self._normalize_phone(identifier)
            extra_fields.setdefault("phone", normalized)
            identifier = normalized  # Обновляем идентификатор до нормализованного телефонного номера

        user = self.model(identifier=identifier, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, identifier, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(identifier, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    identifier = models.CharField(max_length=255, unique=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    id_type = models.CharField(max_length=10, choices=ID_TYPE_CHOICES, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "identifier"
    REQUIRED_FIELDS = []

    def __str__(self):  # pylint: disable=invalid-str-returned
        return self.identifier
