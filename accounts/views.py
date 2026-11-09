from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render
from django.conf import settings

# Create your views here.
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import LogoutSerializer
from .models import OTP
from django.contrib.auth import get_user_model
user=get_user_model()

from .serializers import (
    ChangePasswordSerializer,
    RegistrationSerializer,
    UserSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer
)
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
    permission_classes = [AllowAny]
class ProfileAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
from rest_framework.views import APIView
from rest_framework.response import Response

class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={"request": request}
        )

        serializer.is_valid(raise_exception=True)

        user = request.user

        user.set_password(
            serializer.validated_data["new_password"]
        )
        user.save(update_fields=["password"])

        return Response(
            {"detail": "Password updated successfully."},
            status=status.HTTP_200_OK
        )



class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        refresh_token = serializer.validated_data["refresh"]

        try:
            token = RefreshToken(refresh_token)
         

            if str(token["user_id"]) != str(request.user.pk):
                return Response(
                    {"detail": "Token does not belong to this user."},
                    status=status.HTTP_403_FORBIDDEN
                )

            token.blacklist()

        except TokenError:
            return Response(
                {"detail": "Invalid or expired refresh token."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"detail": "Logged out successfully."},
            status=status.HTTP_200_OK
        )
from .services import generate_otp

class ForgotPasswordAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        user = get_user_model().objects.filter(
            email__iexact=email,
            is_active=True,
        ).first()

        message = {
            "detail": (
                "If an account with that email exists, "
                "a password reset OTP has been sent."
            )
        }

        if user and user.has_usable_password():

            existing_otp = OTP.objects.filter(user=user).first()

            if existing_otp:
                if existing_otp.is_expired():
                    existing_otp.delete()
                else:
                    return Response(
                        {"detail": "You can send a new OTP after 5 minutes."},
                        status=status.HTTP_429_TOO_MANY_REQUESTS,
                    )

            otp = generate_otp()

            OTP.objects.create(
                user=user,
                code=otp,
            )

            result = send_mail(
                subject="Password Reset OTP",
                message=f"Your OTP for password reset is: {otp}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )

            if result == 0:
                return Response(
                    {"detail": "Unable to send OTP."},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )

        return Response(
            message,
            status=status.HTTP_200_OK,
        )                           

class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        otp_code = serializer.validated_data["otp"]
        new_password = serializer.validated_data["new_password"]

        user = get_user_model().objects.filter(
            email__iexact=email,
            is_active=True,
        ).first()

        if not user:
            return Response(
                {"detail": "Invalid email or OTP."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp_instance = OTP.objects.filter(user=user, code=otp_code).first()

        if not otp_instance or otp_instance.is_expired():
            return Response(
                {"detail": "Invalid or expired OTP."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save(update_fields=["password"])

        otp_instance.delete()

        return Response(
            {"detail": "Password reset successfully."},
            status=status.HTTP_200_OK,
        )
    
 