from django.urls import path

from app.views import DashboardView, EncryptionView, DecryptionView


urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("encryption/", EncryptionView.as_view(), name="encryption"),
    path("decryption/", DecryptionView.as_view(), name="decryption"),
    path("decryption/<str:operation>/", DecryptionView.as_view(), name="decryption"),
]
