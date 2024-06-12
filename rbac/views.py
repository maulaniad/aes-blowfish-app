from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View

# Create your views here.

class RBACView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, template_name="rbac.html")
