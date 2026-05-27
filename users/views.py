from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout , authenticate
from django.http import HttpRequest
from django.core.mail import send_mail

import pyotp
from .models import OTPCollection

from .forms import UserAuthForm
from .models import UserDataModel

import _log_utils.file_logger as FileLogger
from _log_utils.file_logger import AccessType

from .permissions import PermissionList, PermissionType

from _request_utils.connect_api import login_via_api
# from _request_utils.authenticate_user import erp_login_authorize

import os
from dotenv import load_dotenv

##########################################

load_dotenv()

def _login_via_erp(request: HttpRequest, form_data : dict, form : UserAuthForm):
    def _block_no_user_access():
        deny_reason = {
            "message": f"{response_data.get("message")} ({form_data.get("username")})",
        }

        FileLogger.createAccessDeniedLog(request, AccessType.LOGIN, PermissionList.LOGIN_PAGE, deny_reason,)

        return render(request, "users/login.html", {
            "form": form,
            "error": True,
            "reason": response_data.get("message")
        })
    
    def _block_wrong_username_password():
        deny_reason = {
            "message": f"Wrong username or password? ({form_data.get("username")})",
        }

        FileLogger.createAccessDeniedLog(request, AccessType.LOGIN, PermissionList.LOGIN_PAGE, deny_reason,)
        
        return render(request, "users/login.html", {
            "form": form,
            "error": True,
            "reason": "ชื่อหรือรหัสผ่านผิด"
        })
    
    try:
        response_data = login_via_api(request)
        if response_data.get("status") != 200:
            return _block_no_user_access()
        
        result_user_id = response_data.get("id")
        if not result_user_id:
            return _block_wrong_username_password()

        # result_user_id exist
        user = UserDataModel.objects.get(api_uid=result_user_id)
        login(request, user)

        FileLogger.createNormalLog(request, AccessType.LOGIN, PermissionList.LOGIN_PAGE,)

        return redirect("dashboard:dashboard")
    
    except:
        return render(request, "users/login.html", {
            "form": form,
            "error": True,
            "reason": "เชื่อมกับระบบ ERP ไม่ได้"
        })
    
def _block_django_non_superuser(request : HttpRequest, form : UserAuthForm):
    FileLogger.createAccessDeniedLog(request, AccessType.LOGIN, PermissionList.LOGIN_PAGE, remark="บัญชี Django ไม่มีสิทธิเข้าถึง ยกเว้น Superuser")

    return render(request, "users/login.html", {
        "form": form,
        "error": True,
        "reason": "บัญชีนี้ไม่มีสิทธิเข้าถึงระบบ AWIS แบบนี้ได้"
    })


def user_login(request : HttpRequest):
    if request.user.is_authenticated:
        return redirect("dashboard:dashboard")
    if request.method == "POST":
        form = UserAuthForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            user : UserDataModel | None = authenticate(
                request, 
                username=form_data.get("username"), 
                password=form_data.get("password")
            )

            # User cannot be authenticated via Django Auth.
            # Login via ERP
            if not user:
                return _login_via_erp(request, form_data, form)
            
            # User exists in the database itself, but not Superuser.
            if not user.is_superuser:
                return _block_django_non_superuser(request, form)

            # User is guaranteed to be Django Superuser.
            login(request, user)

            FileLogger.createNormalLog(request, AccessType.LOGIN, PermissionList.LOGIN_PAGE,)

            return redirect("dashboard:dashboard")

            # send_email_otp(user)
            # return redirect("users:verify_otp")

    form = UserAuthForm()    
    return render(request, "users/login.html", {
        "form": form
    })

#########################################################################

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