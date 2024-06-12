"""
URL configuration for AES-Blowfish-App project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import: from my_app import views
    2. Add a URL to urlpatterns: path('', views.home, name='home')
Class-based views
    1. Add an import: from other_app.views import Home
    2. Add a URL to urlpatterns: path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns: path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from config.errors import ErrorPageView


handler400 = "config.errors.bad_request"
handler403 = "config.errors.forbidden"
handler404 = "config.errors.not_found"
handler500 = "config.errors.internal_server_error"

urlpatterns = [
    path("errors/", ErrorPageView.as_view(), name="errors"),
    path("errors/<int:code>/", ErrorPageView.as_view(), name="errors"),

    path("", include(("app.urls", "app"), namespace="app")),

    path(
        "authentication/",
        include(
            ("authentication.urls", "authentication"),
            namespace="authentication"
        )
    ),

    path("download/", include(("download.urls", "download"), namespace="download")),
    path("rbac/", include(("rbac.urls", "rbac"), namespace="rbac"))
]
