from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, HttpResponseForbidden, JsonResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings

from warrant_form.forms import WarrantForm, AWISFormStep1, DisabledFormStep1, DisabledWarrantForm

from dashboard.models import VisualFormApprovalData as FormData
from dashboard.models import VisualFinalizedFormData as FormSent
from dashboard.warrant_wrapper import VisualWarrantData

from warrant_form.model_reqform import ReqformDataModel, WarrantDataModel
from users.models import UserDataModel

import _request_utils.connect_api as AWISConnectAPI

import json

# Create your views here.

@login_required(login_url="/users/login/")
def dashboard(request : HttpRequest):

    user_data = UserDataModel.objects.filter(user=request.user).first()

    creator = FormData.objects.filter(form_creator=user_data)
    owner = FormData.objects.filter(form_owner=user_data)
    waiting_approval_forms = creator.union(owner)

    form_sent = FormSent.objects.all()

    warrants : list[VisualWarrantData] = VisualWarrantData.objects.all()

    output_list = []
    for obj in form_sent:
        data_dict = {
            "id": obj.form.id,
            "recive_date": obj.recive_date,
            "accept": obj.get_accept_display,
            "accept_date": obj.accept_date,
            "req_no_plaintiff": obj.getReqNoPlaintiff(),
            "reqno": obj.getReqNo(),
        }

        output_list.append(data_dict)

    warrants_list = []
    for warrant_wrap in warrants:
        warrant_data = warrant_wrap.warrant
        data_dict = {
            "court_injunction": warrant_wrap.get_court_injunction_display, 
            "reqno": warrant_data.reqforms.all().first().reqno,
            "woa_no": f"{warrant_data.woa_no}/{warrant_data.woa_date.year + 543}",
            "woa_year": warrant_data.woa_date.year + 543,
            "woa_type": warrant_data.woa_type,
            "woa_refno": warrant_data.woa_refno,
            "judge_name": warrant_wrap.judge_name,
            "injunction_date": warrant_wrap.injunction_date.strftime("%d/%m/%Y, %H:%M น."),
            "file_path": warrant_wrap.file_path,
            "because": warrant_wrap.because,
        }

        warrants_list.append(data_dict)

    return render(request, "dashboard/dashboard.html", {
        "user": request.user,
        "forms": waiting_approval_forms,
        "forms_sent": output_list,
        "warrants": warrants_list,
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
def view_form(request : HttpRequest, form_id : int):
    if not request.user.has_perm("dashboard.can_approve_form"):
        return HttpResponseForbidden("403 Forbidden: No Permission")

    selected_form = FormData.objects.filter(id=form_id).first().form

    warrants : list[WarrantDataModel] = selected_form.warrants.all()

    warrant_list = []
    for item in warrants:
        dict_item = item.convertBacktoFormView()
        form = DisabledWarrantForm(initial=dict_item)
        warrant_list.append(
            form
        )
    
    form = DisabledFormStep1(initial=selected_form.convertBacktoFormView(), prefix="main_form")
    
    return render(request, "warrant_form/view_all.html", {
        "user": request.user,
        "form": form,
        "warrant_list": warrant_list,
        "disabled": True,
    })

# def edit_form(request : HttpRequest, form_id : int):
#     if not request.user.has_perm("dashboard.can_approve_form"):
#         return HttpResponseForbidden("403 Forbidden: No Permission")

#     selected_form = FormData.objects.filter(id=form_id).first().form

#     print(selected_form.convertBacktoFormView())
    
#     form = AWISFormStep1(initial=selected_form.convertBacktoFormView(), prefix="main_form")
    
#     return render(request, "warrant_form/awis_step1.html", {
#         "user": request.user,
#         "form": form,
#     })

@login_required(login_url="/users/login/")
def confirm_approve(request : HttpRequest, form_id : int):
    if not request.user.has_perm("dashboard.can_approve_form"):
        return HttpResponseForbidden("403 Forbidden: No Permission")

    selected_form = FormData.objects.filter(id=form_id).first()
    if request.method == "POST":
        try:
            selected_form.approve_status = FormData.ApprovalStatus.APPROVED
            selected_form.save()

            if settings.ENABLE_API:
                dict = AWISConnectAPI.post_send_req_form("v1.1", request, selected_form.form.toAPICompatibleDictWithConvertedWarrants())
            
            FormSent.objects.create(
                form=selected_form.form,
                accept=FormSent.AcceptStatus.WAITING,
            )

            print(json.dumps(selected_form.form.toAPICompatibleDictWithConvertedWarrants(), indent=2, ensure_ascii=False))
                  
            # print(f"Result: {json.dumps(dict)}")

            return redirect(reverse("dashboard:success_page"))
        except Exception as e:
            print(e)

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
def edit_form(request : HttpRequest, form_id : int):
    if not request.user.has_perm("dashboard.can_approve_form"):
        return HttpResponseForbidden("403 Forbidden: No Permission")
    
    selected_form = FormData.objects.filter(id=form_id).first()
    current_user = request.user

    if not ((current_user == selected_form.form_creator.user) or (current_user == selected_form.form_owner.user)):
        return JsonResponse({
            "status": 403,
            "message": "Not the owner or creator."
        }, status=403)
    
    # if selected_form.approve_status == FormData.ApprovalStatus.APPROVED:
    #     return JsonResponse({
    #         "status": 405,
    #         "message": "API already sent. Can't edit anymore."
    #     }, status=405)

    if request.method == "POST":
        main_form = AWISFormStep1(request.POST, prefix="main_form")
        sub_form = WarrantForm(request.POST, prefix="sub_form")

        if main_form.is_valid() and sub_form.is_valid():
            awis_obj : ReqformDataModel = main_form.save(commit=False)
            warrant_obj : WarrantDataModel = sub_form.save()

            awis_obj.save()
            awis_obj.warrants.add(warrant_obj)
            
            selected_form.form.delete()
            
            # The old object is replaced by the new one.
            selected_form.form = awis_obj
            # Enable approval again.
            selected_form.approve_status = FormData.ApprovalStatus.PENDING

            selected_form.save()

            return redirect(reverse("dashboard:success_page"))
        else:
            print(main_form.errors.as_text())
            print(sub_form.errors.as_text())
    
    form_obj : ReqformDataModel = selected_form.form.convertBacktoFormView()
    warrants_list : list[WarrantDataModel] = selected_form.form.warrants.all()[0].toAPICompatibleDict()

    # warrants_list = [warrant.toAPICompatibleDict() for warrant in warrants_list][0]

    main_form = AWISFormStep1(initial=form_obj, prefix="main_form",)
    sub_form = WarrantForm(initial=warrants_list, prefix="sub_form")

    return render(request, "warrant_form/awis_step1.html", {
        # "main_form": main_form,
        "sub_form": sub_form,
        "user": request.user,
        "action": "Edit",
        "form": main_form,
    })