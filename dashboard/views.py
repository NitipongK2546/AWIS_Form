from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required

from dashboard.models import FormApprovalDataContainer
from users.models import UserDataModel

import api.connect_api as AWISConnectAPI

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