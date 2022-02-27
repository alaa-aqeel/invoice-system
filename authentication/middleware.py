from django.shortcuts import redirect 
from django.urls import reverse 
from django.conf import settings
from django.contrib.auth.decorators import login_required


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):# {

        if request.path == settings.LOGIN_URL :  # check is path for login page 
            if not request.user.is_authenticated:
                return None
            else:
                return redirect(reverse("dashboard"))

        if request.user.is_authenticated :
            return None

        return login_required(view_func)(request, *view_args, **view_kwargs)
    # }