from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest

from dashboard.models import FormApprovalDataContainer

# Create your views here.

def dashboard(request : HttpRequest):

    all_forms = FormApprovalDataContainer.objects.all()

    return render(request, "dashboard/dashboard.html", {
        "forms": all_forms,
    })