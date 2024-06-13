from django.conf import settings
from django.http import (HttpRequest,
                         HttpResponse,
                         HttpResponseRedirect)
from django.middleware.security import SecurityMiddleware
from django.urls import reverse

# Create your custom middlewares here.

SAFE_ROUTES = ('authentication:login',
               'authentication:register',
               'authentication:reset_password',
               'errors')

class AuthenticationMiddleware:
    def __init__(self, get_response) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)

        is_authenticated = request.session.get('is_authenticated', None)

        if request.path == "/" and not is_authenticated:
            return HttpResponseRedirect(redirect_to=reverse("authentication:login"))

        if self.is_safe_route(request.path) and is_authenticated:
            return HttpResponseRedirect(redirect_to=reverse("app:dashboard"))

        if not self.is_safe_route(request.path) and not is_authenticated:
            return HttpResponseRedirect(redirect_to=reverse("authentication:login"))

        return response

    def is_safe_route(self, path: str) -> bool:
        if path == "/":
            return True

        if path in (settings.MEDIA_ROOT, settings.STATIC_ROOT):
            return True

        return path in [reverse(route) for route in SAFE_ROUTES]


class CustomSecurityMiddleware(SecurityMiddleware):
    def process_response(self, request, response):
        response['Cross-Origin-Opener-Policy'] = 'same-origin'
        response['Cross-Origin-Embedder-Policy'] = 'require-corp'
        return response
