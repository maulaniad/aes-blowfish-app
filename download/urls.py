from django.urls import path

from download.views import ObjectDownloadView


urlpatterns = [
    path("<str:oid>/", ObjectDownloadView.as_view(), name="object"),
]
