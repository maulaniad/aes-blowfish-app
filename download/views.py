from os.path import join, exists

from django.conf import settings
from django.contrib import messages
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect, FileResponse
from django.views import View

from database.models import File

# Create your views here.

class ObjectDownloadView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse | FileResponse:
        object_id = kwargs['oid']
        try:
            file_data = File.objects.get(oid=object_id)
        except File.DoesNotExist:
            messages.error(request, message="Data rusak ...")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        filepath = join(settings.MEDIA_ROOT, file_data.file.name)

        if not exists(filepath):
            messages.error(request, message="File tidak ditemukan ...")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        return FileResponse(open(filepath, 'rb'), as_attachment=True, filename=file_data.filename)
