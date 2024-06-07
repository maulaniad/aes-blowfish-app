from django.urls import path

from app.views import DashboardView, EncryptionView


urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("encryption/", EncryptionView.as_view(), name="encryption")
]
