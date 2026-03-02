from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required

from dashboard.models import FormApprovalDataContainer as FormData
from users.models import UserDataModel

import api.connect_api as AWISConnectAPI

import json

# Create your views here.

@login_required(login_url="/users/login/")
def dashboard(request : HttpRequest):

    user_data = UserDataModel.objects.filter(user=request.user).first()

    creator = FormData.objects.filter(form_creator=user_data)
    owner = FormData.objects.filter(form_owner=user_data)

    all_forms = creator.union(owner)

    return render(request, "dashboard/dashboard.html", {
        "user": request.user,
        "forms": all_forms,
    })

@login_required(login_url="/users/login/")
def approve_form_page(request : HttpRequest):

    all_forms = FormData.objects.all()

    return render(request, "dashboard/approve_page.html", {
        "user": request.user,
        "forms": all_forms,
    })

@login_required(login_url="/users/login/")
def selected_form_to_see_page(request : HttpRequest, form_id : int):
    selected_form = FormData.objects.filter(id=form_id).first()

    return render(request, "dashboard/selected_form_page.html", {
        "user": request.user,
        "form": selected_form,
        "data": json.dumps(selected_form.form.toAPICompatibleDictWithConvertedWarrants(), indent=4),
    })

@login_required(login_url="/users/login/")
def confirm_approve(request : HttpRequest, form_id : int):
    selected_form = FormData.objects.filter(id=form_id).first()
    if request.method == "POST":
        selected_form.approve_status = FormData.ApprovalStatus.APPROVED
        selected_form.save()

        # AWISConnectAPI.post_send_req_form("v1.1", request, selected_form.form.toAPICompatibleDictWithConvertedWarrants())

        return redirect(reverse("dashboard:success_page"))

    return render(request, "dashboard/confirmation_page.html", {
        "user": request.user,
        "action": "Approve",
        "form": selected_form,
    })
    

@login_required(login_url="/users/login/")
def confirm_reject(request : HttpRequest, form_id : int):
    selected_form = FormData.objects.filter(id=form_id).first()
    if request.method == "POST":
        selected_form.approve_status = FormData.ApprovalStatus.REJECTED
        selected_form.save()

        return redirect(reverse("dashboard:success_page"))
    
    return render(request, "dashboard/confirmation_page.html", {
        "user": request.user,
        "action": "Reject",
        "form": selected_form,
    })

@login_required(login_url="/users/login/")
def success_page(request : HttpRequest):
    return render(request, "dashboard/success_page.html", {
        "user": request.user,
    })