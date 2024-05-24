from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View


class ErrorPageView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        try:
            error_code = kwargs['code']
        except KeyError:
            error_code = 404

        match error_code:
            case 200:
                return render(request, template_name="200.html", status=200)
            case 400:
                return render(request, template_name="400.html", status=400)
            case 401:
                return render(request, template_name="401.html", status=401)
            case 403:
                return render(request, template_name="403.html", status=403)
            case 404:
                return render(request, template_name="404.html", status=404)
            case _:
                return render(request, template_name="500.html", status=500)


def bad_request(request: HttpRequest, exception):
    messages.error(request, message=f"{exception}")
    return render(request, template_name="400.html", status=400)

def unauthorized(request: HttpRequest, exception):
    messages.error(request, message=f"{exception}")
    return render(request, template_name="401.html", status=401)

def forbidden(request: HttpRequest, exception):
    messages.error(request, message=f"{exception}")
    return render(request, template_name="403.html", status=403)

def not_found(request: HttpRequest, exception):
    messages.error(request, message=f"{exception}")
    return render(request, template_name="404.html", status=404)

def internal_server_error(request: HttpRequest):
    return render(request, template_name="500.html", status=500)
