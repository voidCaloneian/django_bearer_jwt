from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import CustomUser


class SignupSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate_identifier(self, value):
        try:
            CustomUser.objects.validate_identifier(value)
        except ValueError as e:
            raise serializers.ValidationError(str(e))

        return value

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class SigninSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            identifier=attrs.get("identifier"), password=attrs.get("password")
        )
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        attrs["user"] = user
        return attrs


class InfoSerializer(serializers.Serializer):
    identifier = serializers.CharField(read_only=True)
    id_type = serializers.CharField(read_only=True)


class LogoutSerializer(serializers.Serializer):
    all = serializers.BooleanField()
    refresh = serializers.CharField(required=False)
