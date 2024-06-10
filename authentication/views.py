from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from authentication.forms import RegisterForm, ResetPasswordForm
from database.models import User
from helpers.dates import dt_now

# Create your views here.

class LoginView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, template_name="login.html")

    def post(self, request: HttpRequest) -> HttpResponse:
        username = request.POST['username']
        password = request.POST['password']
        user_data = authenticate(request, username=username, password=password)

        if user_data:
            request.session['is_authenticated'] = True
            request.session['user'] = user_data.fullname       # type: ignore
            request.session['role'] = user_data.role.rolename  # type: ignore

            login(request, user_data)
            messages.success(request, message="Login Berhasil!")
            return redirect(to="app:dashboard")

        messages.error(request, message="Login Gagal ...")
        return redirect(to="authentication:login")


class RegisterView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, template_name="register.html")

    def post(self, request: HttpRequest) -> HttpResponse:
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, message="Registrasi Berhasil!")
            return redirect(to="authentication:login")

        messages.error(request, message="Registrasi Gagal ...")
        return redirect(to="authentication:register")


class ResetPasswordView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, template_name="reset_password.html")

    def post(self, request: HttpRequest) -> HttpResponse:
        post_type = request.POST.get('type', None)

        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            if post_type and post_type.lower() == "validation":
                return self._validation(request, form)

            return self._change_password(request, form)

        messages.error(request, message="Setel Ulang Kata Sandi Gagal ...")
        return redirect(to="authentication:reset_password")

    def _validation(self, request: HttpRequest, form: ResetPasswordForm) -> HttpResponse:
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        validation_filter = Q(username=username) | Q(email=email)
        user_data = User.objects.get(validation_filter, date_deleted__gt=dt_now())

        if user_data.password_changed:
            allowed_date = user_data.password_changed + timedelta(days=7)
            delta = allowed_date - dt_now()

            if delta.days > 0:
                context = {'delta': delta.days - 7}
                return render(request, template_name="reset_password.html", context=context)

        context = {
            'username': form.cleaned_data.get('username'),
            'email': form.cleaned_data.get('email'),
            'next': True
        }
        return render(request, template_name="reset_password.html", context=context)

    def _change_password(self, request: HttpRequest, form: ResetPasswordForm) -> HttpResponse:
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        new_password = form.cleaned_data.get('password')

        validation_filter = Q(username=username) | Q(email=email)
        user_data = User.objects.get(validation_filter, date_deleted__gt=dt_now())
        user_data.password = make_password(new_password)
        user_data.password_changed = dt_now()
        user_data.save()

        messages.success(request, message="Setel Ulang Kata Sandi Berhasil!")
        return redirect(to="authentication:login")


class LogoutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        request.session.pop('is_authenticated', None)
        request.session.pop('user', None)
        return redirect(to="authentication:login")
