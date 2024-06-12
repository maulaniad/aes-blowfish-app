from django.urls import path, include

from rbac.views import RBACView


urlpatterns = [
    path("", RBACView.as_view(), name="rbac")
]
