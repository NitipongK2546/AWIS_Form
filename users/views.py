from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout , authenticate
from django.http import HttpRequest
from django.core.mail import send_mail

import pyotp
from .models import OTPCollection

from api.internal.endpoints import login_via_api
from .forms import UserAuthForm
from .models import UserDataModel

import _log_utils.file_logger as FileLogger
from _log_utils.file_logger import AccessType

from .permissions import PermissionList, PermissionType

import os
from dotenv import load_dotenv

##########################################

load_dotenv()

def user_login(request : HttpRequest):
    if request.user.is_authenticated:
        return redirect("dashboard:dashboard")
    if request.method == "POST":
        form = UserAuthForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user : UserDataModel = authenticate(request, username=data.get("username"), password=data.get("password"))
            if user is not None:
                if not (os.getenv("PRODUCTION") == "YES"):
                    login(request, user)
                    FileLogger.createNormalLog(user.api_uid, AccessType.LOGIN, PermissionList.LOGIN_PAGE,)
                    if user.is_superuser:
                        return redirect("admin_panel:collections")
                    return redirect("dashboard:dashboard")
            else:
                result_user_id = login_via_api(request)
                if result_user_id:
                    user = UserDataModel.objects.get(api_uid=result_user_id)
                    login(request, user)
                    return redirect("dashboard:dashboard")

                return render(request, "users/login.html", {"form": form})
                    
                # PRODUCTION
                send_email_otp(user)

                return redirect("users:verify_otp")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})

# def insert_userID_

def send_email_otp(user : UserDataModel):
    otp_obj, created = OTPCollection.objects.get_or_create(user=user)
    if not otp_obj.secret:
        otp_obj.secret = pyotp.random_base32()
        otp_obj.save()

    totp = pyotp.TOTP(otp_obj.secret, interval=300)
    otp_code = totp.now()

    send_mail(
        subject="Your OTP Code",
        message=f"Your OTP code is {otp_code}. It expires in 5 minutes.",
        from_email=os.getenv("EMAIL_HOST_USER"),
        recipient_list=[user.email],
        fail_silently=False,
    )

def verify_email_otp(user : UserDataModel, entered_code : str):
    otp_obj = OTPCollection.objects.get(user=user)
    totp = pyotp.TOTP(otp_obj.secret, interval=300)
    return totp.verify(entered_code)

def verify_otp_view(request: HttpRequest):
    if request.method == "POST":
        entered_code = request.POST.get("otp")
        if verify_email_otp(request.user, entered_code):
            request.session['otp_verified'] = True

            otp_obj = OTPCollection.objects.get(user=request.user)
            otp_obj.delete()

            login(request, request.user)

            return redirect("dashboard:dashboard")
        else:
            return render(request, "users/verify_otp.html", {"error": "Invalid or expired OTP"})
    return render(request, "users/verify_otp.html")


def custom_logout(request : HttpRequest): 
    logout(request) 
    return redirect("users:login")