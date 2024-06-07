from os.path import join, exists

from django.conf import settings
from django.http import HttpRequest, HttpResponse, FileResponse
from django.views import View

# Create your views here.

class DownloadManagerView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse | FileResponse:
        filename = kwargs['filename']
        filepath = join(settings.MEDIA_ROOT, filename)

        if not exists(filepath):
            return HttpResponse(status=404)

        return FileResponse(open(filepath, 'rb'), as_attachment=True, filename=filename)
