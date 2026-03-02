from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout 
from django.http import HttpRequest

import warrant_form.connect_api as AWISConnectAPI

# Create your views here.

def user_login(request : HttpRequest):
    if request.user.is_authenticated:
        return redirect("awis:index")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, form.get_user())
                # AWISConnectAPI.post_login_authorize("v1.1", request)

            return redirect("awis:index")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})

# def signup(request : HttpRequest):
#     if request.method == "POST":
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("awis:login")
#     else:
#         form = UserCreationForm()
#     return render(request, "users/signup.html", {"form": form})

def custom_logout(request : HttpRequest): 
    logout(request) 
    return redirect("awis:login")