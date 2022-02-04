from django.shortcuts import redirect 
from django.urls import reverse 
from django.conf import settings
from django.contrib.auth.decorators import login_required


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):

        response = self.get_response(request)

        return response


    def process_view(self, request, view_func, view_args, view_kwargs):
        # is page login 
        is_login_page = request.path == settings.LOGIN_URL

        if is_login_page :  # is login page 
            # and not authenticated 
            if not request.user.is_authenticated:
                return None

            # if authenticated 
            else:
                return redirect(reverse("dashboard"))


        # if authenticated
        if request.user.is_authenticated :
            return None

                
        return login_required(view_func)(request, *view_args, **view_kwargs)