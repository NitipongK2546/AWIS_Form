from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout 
from django.http import HttpRequest
from django.core.mail import send_mail
import _request_utils.connect_api as AWISConnectAPI
import pyotp
from django.core.mail import send_mail
from .models import OTPCollection

def user_login(request : HttpRequest):
    if request.user.is_authenticated:
        return redirect("dashboard:dashboard")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user is not None:
                login(request, user)
                # if user.is_superuser:
                #     return redirect("admin_panel:collections")
                send_email_otp(user)

                return redirect("users:verify_otp")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})

def custom_logout(request : HttpRequest): 
    logout(request) 
    return redirect("users:login")

def send_email_otp(user):
    otp_obj, created = OTPCollection.objects.get_or_create(user=user)
    if not otp_obj.secret:
        otp_obj.secret = pyotp.random_base32()
        otp_obj.save()

    totp = pyotp.TOTP(otp_obj.secret, interval=300)
    otp_code = totp.now()

    send_mail(
        subject="Your OTP Code",
        message=f"Your OTP code is {otp_code}. It expires in 5 minutes.",
        from_email="plowitzaaa@gmail.com",
        recipient_list=[user.email],
    )

def verify_email_otp(user, entered_code):
    otp_obj = OTPCollection.objects.get(user=user)
    totp = pyotp.TOTP(otp_obj.secret, interval=300)
    return totp.verify(entered_code)

def verify_otp_view(request: HttpRequest):
    if request.method == "POST":
        entered_code = request.POST.get("otp")
        if verify_email_otp(request.user, entered_code):
            request.session['otp_verified'] = True
            return redirect("dashboard:dashboard")
        else:
            return render(request, "users/verify_otp.html", {"error": "Invalid or expired OTP"})
    return render(request, "users/verify_otp.html")