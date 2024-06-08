from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.db.models import Q

from database.models import User
from helpers.dates import dt_now


class AuthenticationBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs) -> User | None:
        user_data = User.objects.filter(
            Q(username=username) | Q(email=username),
            date_deleted__gt=dt_now()
        ).first()

        if not user_data:
            return None

        if not check_password(password, user_data.password):
            return None

        return user_data

    def get_user(self, user_id: int) -> User | None:
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
