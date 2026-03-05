from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required

from warrant_form.forms import MainAWISForm, WarrantForm
from warrant_form.models import MainAWISDataModel, WarrantDataModel

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

#######################################################3
#
# FORM APPROVE SECTION
#

@login_required(login_url="/users/login/")
def approve_form_page(request : HttpRequest):
    if not request.user.has_perm("dashboard.can_approve_form"):
        return HttpResponseForbidden("403 Forbidden: No Permission")

    all_forms = FormData.objects.all()

    return render(request, "dashboard/approve_page.html", {
        "user": request.user,
        "forms": all_forms,
    })

@login_required(login_url="/users/login/")
def selected_form_to_see_page(request : HttpRequest, form_id : int):
    if not request.user.has_perm("dashboard.can_approve_form"):
        return HttpResponseForbidden("403 Forbidden: No Permission")
    
    selected_form = FormData.objects.filter(id=form_id).first()

    if selected_form.approve_status == FormData.ApprovalStatus.APPROVED:
        return JsonResponse({
            "status": 405,
            "message": "API already sent. Can't edit anymore.",
        }, status=405)

    return render(request, "dashboard/selected_form_page.html", {
        "user": request.user,
        "form": selected_form,
        "data": json.dumps(selected_form.form.toAPICompatibleDictWithConvertedWarrants(), indent=4, ensure_ascii=False),
    })

@login_required(login_url="/users/login/")
def confirm_approve(request : HttpRequest, form_id : int):
    if not request.user.has_perm("dashboard.can_approve_form"):
        return HttpResponseForbidden("403 Forbidden: No Permission")

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
    if not request.user.has_perm("dashboard.can_approve_form"):
        return HttpResponseForbidden("403 Forbidden: No Permission")

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

######################################################################
#EDIT THE FORM

@login_required(login_url="/users/login/")
def select_form_to_edit(request : HttpRequest, form_id : int):
    selected_form = FormData.objects.filter(id=form_id).first()
    current_user = request.user

    if not ((current_user == selected_form.form_creator.user) or (current_user == selected_form.form_owner.user)):
        return JsonResponse({
            "status": 403,
            "message": "Not the owner or creator."
        }, status=403)
    
    if selected_form.approve_status == FormData.ApprovalStatus.APPROVED:
        return JsonResponse({
            "status": 405,
            "message": "API already sent. Can't edit anymore."
        }, status=405)

    if request.method == "POST":
        main_form = MainAWISForm(request.POST, prefix="main_form")
        sub_form = WarrantForm(request.POST, prefix="sub_form")

        if main_form.is_valid():
            awis_obj : MainAWISDataModel = main_form.save(commit=False)
            warrant_obj : WarrantDataModel = sub_form.save()

            awis_obj.save()
            awis_obj.warrants.add(warrant_obj)
            
            # The old object is replaced by the new one.
            selected_form.form = awis_obj
            # Enable approval again.
            selected_form.approve_status = FormData.ApprovalStatus.PENDING

            selected_form.save()

            return redirect(reverse("dashboard:success_page"))
    
    form_obj : MainAWISDataModel = selected_form.form.toAPICompatibleDict("main_form")
    warrants_list : list[WarrantDataModel] = selected_form.form.warrants.all()[0].toAPICompatibleDict("sub_form")

    main_form = MainAWISForm(form_obj, prefix="main_form")
    sub_form = WarrantForm(warrants_list, prefix="sub_form")

    return render(request, "dashboard/reqform.html", {
        "main_form": main_form,
        "sub_form": sub_form,
        "user": request.user,
        "action": "Edit",
        "form": selected_form,
    })


################################################### View for Check Reqform Status
#

@login_required(login_url="/users/login/")
def view_reqforms_status(request : HttpRequest, req_no_plaintiff : str):

    # data = AWISConnectAPI.get_req_form_status("v1.1", request, req_no_plaintiff)
    data = None

    if not data:
        data = []
    
    return render(request, "dashboard/reqform_status.html", {
        "reqforms": data,
    })