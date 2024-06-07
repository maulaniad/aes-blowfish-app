from typing import Any

from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.forms import ModelForm, ValidationError

from database.models import User
from helpers.dates import dt_now

# Create your form validations here.

class LoginForm(ModelForm):
    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        validation_filter = Q(username=username) | Q(email=email)
        user_data = User.objects.filter(validation_filter, date_deleted__gt=dt_now()).first()

        if not user_data:
            raise ValidationError("User does not exist ...")

        if not check_password(password, user_data.password):
            raise ValidationError("Wrong password ...")

        cleaned_data['user'] = user_data.fullname
        cleaned_data['role'] = user_data.role.rolename

        return cleaned_data

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class RegisterForm(ModelForm):
    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        validation_filter = Q(username=username) | Q(email=email)

        if User.objects.filter(validation_filter, date_deleted__gt=dt_now()).exists():
            raise ValidationError("Username or Email is already registered ...")

        return cleaned_data

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'fullname')


class ResetPasswordForm(ModelForm):
    def clean(self) -> dict[str, Any]:
        cleaned_data = super().clean()

        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        validation_filter = Q(username=username) | Q(email=email)
        user_data = User.objects.filter(validation_filter, date_deleted__gt=dt_now()).first()

        if not user_data:
            raise ValidationError("User does not exist ...")

        return cleaned_data

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
