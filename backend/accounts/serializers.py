from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .validators import validate_password_rules, validate_ufu_email

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "name", "email")
        read_only_fields = fields


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ("id", "name", "email", "password")

    def validate_email(self, value):
        value = value.strip().lower()
        validate_ufu_email(value)
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Já existe uma conta com este e-mail.")
        return value

    def validate_password(self, value):
        validate_password_rules(value)
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Login por e-mail (case-insensitive) devolvendo também os dados do usuário."""

    default_error_messages = {
        "no_active_account": "E-mail ou senha incorretos.",
    }

    def validate(self, attrs):
        attrs["email"] = attrs["email"].strip().lower()
        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user).data
        return data