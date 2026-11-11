
from django.contrib import admin
from django.urls import include, path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('profile/', views.ProfileAPIView.as_view(), name='profile'),
    path('change-password/', views.ChangePasswordAPIView.as_view(), name='change_password'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('forgot-password/', views.ForgotPasswordAPIView.as_view(), name='forgot_password'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('profile-picture/', views.ProfilePictureAPIView.as_view(), name='profile_picture_update'),
]
