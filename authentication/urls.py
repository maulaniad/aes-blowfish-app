from django.urls import path

from authentication.views import LoginView, RegisterView, ResetPasswordView, LogoutView


urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),
    path("reset-password/", ResetPasswordView.as_view(), name="reset_password"),
    path("logout/", LogoutView.as_view(), name="logout")
]
