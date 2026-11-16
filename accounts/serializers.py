from requests import Response
from rest_framework import serializers, status
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
import re
from django.conf import settings
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import GoogleLoginSerializer

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        validators=[validate_password],
    )
    email=serializers.EmailField(
        required=True,
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
        ]

        read_only_fields = ["id"]
    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use.")
        return value
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must contain at least 8 characters."
            )

        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter."
            )

        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter."
            )

        if not re.search(r"[0-9]", value):
            raise serializers.ValidationError(
                "Password must contain at least one number."
            )

        if not re.search(r"[^A-Za-z0-9]", value):
            raise serializers.ValidationError(
                "Password must contain at least one special character."
            )

        return value
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "is_staff",

        ]

        read_only_fields = ["id", "is_staff"]
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(
        write_only=True,
        required=True,
       
    )

    new_password = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"}
    )

    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
    )

    def validate_old_password(self, value):
        user = self.context["request"].user

        if not user.check_password(value):
            raise serializers.ValidationError(
                "Old password is incorrect."
            )

        return value

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must contain at least 8 characters."
            )

        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError(
                "Password must contain an uppercase letter."
            )

        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError(
                "Password must contain a lowercase letter."
            )

        if not re.search(r"[0-9]", value):
            raise serializers.ValidationError(
                "Password must contain a number."
            )

        if not re.search(r"[^A-Za-z0-9]", value):
            raise serializers.ValidationError(
                "Password must contain a special character."
            )

        return value

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match."
            })

        if attrs["old_password"] == attrs["new_password"]:
            raise serializers.ValidationError({
                "new_password": "New password must be different from old password."
            })

        return attrs
   
class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "No user is associated with this email address."
            )
        return value

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "No user is associated with this email address."
            )
        return value

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(max_length=6, required=True)
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
    )
    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must contain at least 8 characters."
            )

        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError(
                "Password must contain at least one uppercase letter."
            )

        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError(
                "Password must contain at least one lowercase letter."
            )

        if not re.search(r"[0-9]", value):
            raise serializers.ValidationError(
                "Password must contain at least one number."
            )

        if not re.search(r"[^A-Za-z0-9]", value):
            raise serializers.ValidationError(
                "Password must contain at least one special character."
            )

        return value

    def validate(self, attrs):
        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({
                "confirm_password": "Passwords do not match."
            })
        return attrs
from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="user.username",
        read_only=True
    )
    user_id=serializers.IntegerField(
        source="user.id",

        read_only=True
    )
 
    class Meta:
        model = Profile
        fields = [
            "id",
            "username",
            "role",
            "profile_picture",
            "user_id",
        ]
        read_only_fields = [
            "id",
            "username",
            "role",
        ]

    def validate_profile_picture(self, value):
        if value.size > 2 * 1024 * 1024:
            raise serializers.ValidationError(
                "Image size must be 2 MB or less."
            )

        if value.content_type not in ["image/jpeg", "image/png"]:
            raise serializers.ValidationError(
                "Only JPG and PNG images are allowed."
            )

        return value
class GoogleLoginSerializer(serializers.Serializer):
    id_token = serializers.CharField()


class GoogleLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = GoogleLoginSerializer

    def post(self, request):
        serializer = GoogleLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data["id_token"]

        try:
            info = google_id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID,
            )
        except ValueError:
            return Response(
                {"detail": "Invalid Google token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not info.get("email_verified"):
            return Response(
                {"detail": "Google email is not verified."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = info["email"].lower()
        User = get_user_model()

        user = User.objects.filter(email__iexact=email).first()
        if user is None:
            base = email.split("@")[0]
            username = base
            i = 1
            while User.objects.filter(username=username).exists():
                username = f"{base}{i}"
                i += 1
            user = User(
                username=username,
                email=email,
                first_name=info.get("given_name", ""),
                last_name=info.get("family_name", ""),
            )
            user.set_unusable_password()
            user.save()   # your signal creates the Profile (role=Employee)

        if not user.is_active:
            return Response(
                {"detail": "Account is disabled."},
                status=status.HTTP_403_FORBIDDEN,
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )