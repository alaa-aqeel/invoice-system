from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, forms
from django.views import View
# Create your views here.


class LoginView(View):
    """Login View """

    
    def get(self, request):
        """Dispaly login page"""

        # render login template 
        return render(request, "login.html", {"form": forms.AuthenticationForm})

    def post(self, request):
        """Post login"""
        # get username and password 
        username = request.POST.get("username")
        password = request.POST.get('password')

        # Check and get user by username and password 
        user = authenticate(username=username, password=password)
        if user is not None:
            # create login session for user 
            login(request, user)

            # redirect to dashboard 
            return redirect(reverse("dashboard"))
        # flash message 
        messages.error(request, "Username or Password is incorect !!")

        # back to login page 
        return redirect(reverse("login"))