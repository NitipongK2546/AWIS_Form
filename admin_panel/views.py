from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from admin_panel.forms import CustomizedUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

FORBIDDEN_MSG = JsonResponse({
                "status": "403",
                "message": "forbidden",
            }, status=403
            )

# VIEWS

@login_required(login_url="/users/login/")
def collections(request : HttpRequest):
    if not request.user.is_superuser:
        return FORBIDDEN_MSG

    return render(request, "admin_panel/collections.html")

@login_required(login_url="/users/login/")
def signup(request : HttpRequest):
    if not request.user.is_superuser:
        return FORBIDDEN_MSG

    if request.method == "POST":
        form = CustomizedUserCreationForm(request.POST)
        if form.is_valid():
            user_obj : User = form.save()

            user_obj.is_active = False

            user_obj.save()

            return redirect("admin_panel:collections")
    else:
        form = CustomizedUserCreationForm()
    return render(request, "users/signup.html", {"form": form})