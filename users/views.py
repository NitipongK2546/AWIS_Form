from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout 
from django.http import HttpRequest

import request_utils.connect_api as AWISConnectAPI

# Create your views here.

def user_login(request : HttpRequest):
    if request.user.is_authenticated:
        return redirect("dashboard:dashboard")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, form.get_user())
                if user.is_superuser:
                    return redirect("admin_panel:collections")

                return redirect("dashboard:dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})

def custom_logout(request : HttpRequest): 
    logout(request) 
    return redirect("users:login")