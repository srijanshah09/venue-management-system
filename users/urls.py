from django.urls import path, include
from django.contrib.auth import views as auth_views

from users.views import (
    UserAuthView,
    user_details,
    user_signup,
    user_login,
    user_logout,
)

urlpatterns = [
    path("", user_login, name="login_page"),
    path("user/<int:id>", user_details, name="user_details"),
    path("signup-page/", user_signup, name="signup_page"),
    path("logout/", user_logout, name="logout"),
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="users/password_reset.html"), name="password_reset"),
    path("password_reset_done/", auth_views.PasswordResetDoneView.as_view(template_name="users/password_reset_done.html"), name="password_reset_done"),
    path("password_reset_confirm/<uidb64>/<token>", auth_views.PasswordResetConfirmView.as_view(template_name="users/password_reset_confirm.html"), name="password_reset_confirm"),
    path("password_reset_complete/", auth_views.PasswordResetCompleteView.as_view(template_name="users/password_reset_complete.html"), name="password_reset_complete"),
    path("signup/", UserAuthView.as_view({"post": "register"})),
    path(
        "send-otp/",
        UserAuthView.as_view({"post": "send_otp"}),
    ),
    path("verify-otp/", UserAuthView.as_view({"post": "verify_otp"})),
    path(
        "request-reset-email/",
        UserAuthView.as_view({"post": "send_password_reset_email"}),
        name="request-password-reset",
    ),
    path(
        "password-rest/<uidb64>/<token>/",
        UserAuthView.as_view({"post": "reset_password"}),
        name="password-reset-confirm",
    ),
]
