from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required

from dashboard.models import FormApprovalDataContainer
from users.models import UserDataModel

import api.connect_api as AWISConnectAPI

import json

# Create your views here.

@login_required(login_url="/users/login/")
def dashboard(request : HttpRequest):

    user_data = UserDataModel.objects.filter(user=request.user).first()

    creator = FormApprovalDataContainer.objects.filter(form_creator=user_data)
    owner = FormApprovalDataContainer.objects.filter(form_owner=user_data)

    all_forms = creator.union(owner)

    return render(request, "dashboard/dashboard.html", {
        "forms": all_forms,
    })

@login_required(login_url="/users/login/")
def approve_form_page(request : HttpRequest):

    all_forms = FormApprovalDataContainer.objects.all()

    return render(request, "dashboard/approve_page.html", {
        "forms": all_forms,
    })

@login_required(login_url="/users/login/")
def selected_form_to_see_page(request : HttpRequest, form_id : int):
    selected_form = FormApprovalDataContainer.objects.filter(id=form_id).first()

    return render(request, "dashboard/selected_form_page.html", {
        "form": selected_form,
        "data": json.dumps(selected_form.form.toAPICompatibleDictWithConvertedWarrants(), indent=4),
    })

@login_required(login_url="/users/login/")
def confirm_approve(request : HttpRequest, form_id : int):
    selected_form = FormApprovalDataContainer.objects.filter(id=form_id).first()
    if request.method == "POST":
        selected_form.approve_status = 2
        selected_form.save()

        # AWISConnectAPI.post_send_req_form("v1.1", request, selected_form.form.toAPICompatibleDictWithConvertedWarrants())

        return redirect(reverse("dashboard:success_page"))

    return render(request, "dashboard/confirmation_page.html", {
        "action": "Approve",
        "form": selected_form,
    })
    

@login_required(login_url="/users/login/")
def confirm_reject(request : HttpRequest, form_id : int):
    selected_form = FormApprovalDataContainer.objects.filter(id=form_id).first()
    if request.method == "POST":
        selected_form.approve_status = 0
        selected_form.save()

        return redirect(reverse("dashboard:success_page"))
    
    return render(request, "dashboard/confirmation_page.html", {
        "action": "Reject",
        "form": selected_form,
    })

@login_required(login_url="/users/login/")
def success_page(request : HttpRequest):
    return render(request, "dashboard/success_page.html", {
    })