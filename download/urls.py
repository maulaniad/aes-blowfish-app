from django.urls import path

from download.views import DownloadManagerView


urlpatterns = [
    path("<str:filename>/", DownloadManagerView.as_view(), name="file"),
]
