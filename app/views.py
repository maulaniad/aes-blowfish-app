from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from database.models import File, Transaction
from core.aes128 import encrypt
from core.checksum import compute_checksum
from helpers.functions import write_bytes_to_file

# Create your views here.

class DashboardView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, template_name="dashboard.html")


class EncryptionView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, template_name="encryption.html")

    def post(self, request: HttpRequest) -> HttpResponse:
        file = request.FILES.get('file')
        key = request.POST.get('key')

        if not file or not key:
            messages.error(request, message="File dan kunci tidak boleh kosong ...")
            return render(request, template_name="encryption.html")

        new_file = File.objects.create(
            file=file,
            filename=file.name,
            extension=file.name.split(".")[-1],
            size=file.size
        )

        file_checksum = compute_checksum(new_file.file.path)

        encrypted_file = encrypt(new_file.file.path, key)
        write_bytes_to_file(encrypted_file, new_file.file.path)

        template_context = {
            "checksum": file_checksum,
            "filename": new_file.filename,
            "extension": new_file.extension,
            "success": True
        }
        return render(request, template_name="encryption.html", context=template_context)
