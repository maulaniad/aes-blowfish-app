from time import time

from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from database.models import File, Transaction
from core.blowfish import Blowfish
from core.checksum import compute_checksum
from helpers.dates import dt_now
from helpers.enums import TransactionStatus
from helpers.functions import (write_bytes_to_file,
                               generate_random_chars,
                               generate_search_code,
                               format_size,
                               paginate,
                               encrypt_file,
                               decrypt_file)
from helpers.types import ARCHIVES

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

        aes_key: bytes = generate_random_chars(type=bytes, length=16)  # type: ignore
        aes_iv: bytes = generate_random_chars(type=bytes, length=16)   # type: ignore

        start_time = time()

        new_file = File.objects.create(
            file=file,
            filename=file.name,
            extension=file.name.split(".")[-1],
            size=file.size,
            aes_key=aes_key,
            secret_key=make_password(key)
        )

        file_checksum = compute_checksum(new_file.file.path)

        encrypted_file = encrypt_file(new_file.file.file, aes_key, aes_iv)
        write_bytes_to_file(encrypted_file, new_file.file.path)

        end_time = time()

        blowfish_engine = Blowfish(key)
        blowfish_validation_key = generate_random_chars(type=str)

        new_transaction = Transaction.objects.create(
            key=blowfish_engine.encrypt(blowfish_validation_key),
            vector=aes_iv,
            name=generate_search_code(new_file.extension),
            status=TransactionStatus.ENCRYPTED,
            user=request.user,
            file=new_file
        )

        template_context = {
            'elapsed_time': round(end_time - start_time, 2),
            'checksum': file_checksum,
            'validation_key': blowfish_validation_key,
            'oid': new_file.oid,
            'size': format_size(new_file.size),
            'name': new_transaction.name,
            'extension': "archive" if new_file.extension in ARCHIVES else new_file.extension,
            'success': True
        }
        return render(request, template_name="encryption.html", context=template_context)


class DecryptionView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 10))
        search = request.GET.get('search', "")

        list_data = Transaction.objects.filter(
            user=request.user,
            name__icontains=search,
            date_deleted__gt=dt_now()
        ).order_by('-date_created')

        data, meta = paginate(list_data, page, page_size)
        template_context = {
            'data': data,
            'meta': meta,
            'active_search': search
        }

        return render(request, template_name="decryption.html", context=template_context)

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        operation = kwargs['operation']
        object_id = request.POST.get('oid', None)
        secret_key = request.POST.get('key', None)

        if not object_id:
            messages.error(request, message="Transaksi atau File tidak ada ...")
            return redirect(to="app:decryption")

        if operation == "decrypt":
            return self._decrypt(request, object_id, secret_key)

        return self._delete(request, object_id)

    def _decrypt(self, request: HttpRequest, object_id: str, secret_key: str | None) -> HttpResponse:
        try:
            transaction = Transaction.objects.get(oid=object_id)
        except Transaction.DoesNotExist:
            messages.error(request, message="Transaksi atau File tidak ada ...")
            return redirect(to="app:decryption")

        if not check_password(secret_key, transaction.file.secret_key):
            messages.error(request, message="Kunci tidak sesuai ...")
            return redirect(to="app:decryption")

        blowfish_engine = Blowfish(secret_key)
        decrypted_key = blowfish_engine.decrypt(list(map(ord, transaction.key))).decode("utf-8")

        decrypted_file = decrypt_file(transaction.file.file, transaction.file.aes_key, transaction.vector)
        write_bytes_to_file(decrypted_file, transaction.file.file.path)

        transaction.status = TransactionStatus.DECRYPTED.value
        transaction.save()

        messages.success(request, message=f"Dekripsi Berhasil! ... Blowfish Validation Key: {decrypted_key}")
        return redirect(to="app:decryption")

    def _delete(self, request: HttpRequest, object_id: str) -> HttpResponse:
        try:
            transaction = Transaction.objects.get(oid=object_id)
        except Transaction.DoesNotExist:
            messages.error(request, message="Transaksi atau File tidak ada ...")
            return redirect(to="app:decryption")

        transaction.file.date_deleted = dt_now()
        transaction.file.save()
        transaction.date_deleted = dt_now()
        transaction.save()

        messages.success(request, message="File berhasil dihapus ...")
        return redirect(to="app:decryption")
