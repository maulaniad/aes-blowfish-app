from django.urls import path

from app.views import DashboardView


urlpatterns = [
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
]
