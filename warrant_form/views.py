from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required, permission_required

from warrant_form.forms import WarrantForm, AWISFormStep1, DisabledWarrantForm, DisabledFormStep1
# from warrant_form.doc_create import doc_create_with_context
from warrant_form.model_warrant import WarrantDataModel
from warrant_form.model_reqform import ReqformDataModel


from dashboard.models import FormAwaitingApproval as VisualFormApprovalData
from dashboard.warrant_wrapper import VisualWarrantData
from users.models import UserDataModel

from django.utils import timezone

import json

from users import PermissionList, PermissionType, perm_str

##############################################################################
# FORM VIEWS

@login_required
def plain_form(request : HttpRequest):    
   
    return redirect(reverse("forms:step1"))
        

@login_required
def success_page(request : HttpRequest):
    return JsonResponse({
        "status_code": "200",
        "message": "success"
    })

##############################################################################

@permission_required(perm_str(PermissionType.CREATE, PermissionList.REQFORM_AWAIT_APPROVAL))
def step1_reqform(request : HttpRequest):
    static_data = {
        "court_code": "0000011",
        "police_station_id": "TCCT0001",
        "req_no_plaintiff": "tcctd20260304002",
        "create_uid": 10000010,
    }
    if request.method == "POST":
        form = AWISFormStep1(request.POST, prefix="main_form",)

        if form.is_valid():
            
            data = form.cleaned_data
            acc_info = dupeNeccesary(data, ["acc_full_name"])
            acc_info.update({
                "cause_text": data.get("accused")
            })

            form_data = dupeNeccesary(data, ["accused", "plaintiff", "court_name"])

            request.session.update({
                "step1": form_data,
                "step1_cleaned": data,
                "acc_info": acc_info 
            })

            return redirect(reverse("forms:step2"))
        else:
            # print(form.errors.as_text)
            return render(request, "warrant_form/awis_step1.html", {
                "form": form,
                "step": 1,
            })
    

    form = AWISFormStep1(initial=static_data, prefix="main_form")
    context = {
        "form": form,
        "step": 1,
    }
        
    old_data : dict = request.session.get("step1")

    if old_data:
        static_data.update(old_data)

        context.update({
            "req_province": old_data.get("req_province"),
            "req_district": old_data.get("req_district"),
            "req_sub_district": old_data.get("req_sub_district"),
            "acc_province": old_data.get("acc_province"),
            "acc_district": old_data.get("acc_district"),
            "acc_sub_district": old_data.get("acc_sub_district"),
        })
    # print(static_data)

    return render(request, "warrant_form/awis_step1.html", context)

@permission_required(perm_str(PermissionType.CREATE, PermissionList.REQFORM_AWAIT_APPROVAL))
def step2_warrantform(request : HttpRequest):
    if request.method == "POST":
        try:
            form = WarrantForm(request.POST)

            if form.is_valid():
                warrant_data = form.cleaned_data

                form_data = dupeNeccesary(warrant_data, ["acc_full_name",])

                request.session.update({
                    "step2": [form_data],
                    "step2_cleaned": [warrant_data],
                })
        except Exception as e:
            print(e)
            pass

        return redirect(reverse("forms:step3"))
            
    if not request.session.get("step1"):
        return redirect(reverse("forms:step1"))
    
    initial_data = {
        "woa_date_timehalf": timezone.datetime.now().time(),
        "acc_card_type": 1,
        "woa_refno": "tcctd20260304002",
    }

    old_data : list[dict] = request.session.get("step2")

    if old_data:
        initial_data.update(request.session.get("step2")[0])
    else:
        initial_data.update(request.session.get("acc_info"))

    form = WarrantForm(initial=initial_data)
    context = {
        "form": form,
        "step": 2,
    }

    # print(request.session.get("acc_info"))
    
    context.update({
        "acc_province": request.session.get("acc_info").get("acc_province"),
        "acc_district": request.session.get("acc_info").get("acc_district"),
        "acc_sub_district": request.session.get("acc_info").get("acc_sub_district"),
    })

    return render(request, "warrant_form/awis_step2.html", context)

@permission_required(perm_str(PermissionType.CREATE, PermissionList.REQFORM_AWAIT_APPROVAL))
def step3_confirm_form(request : HttpRequest):
    if request.method == "POST":
        try:
            reqform_data : dict = request.session.get("step1_cleaned")
            warrant_data : list[dict] = request.session.get("step2_cleaned")

            reqform : ReqformDataModel = ReqformDataModel.objects.create(**reqform_data)

            for item_dict in warrant_data:
                warrant : WarrantDataModel = WarrantDataModel.objects.create(
                    **item_dict
                )
                if reqform:
                    reqform.warrants.add(warrant)

            user_obj = UserDataModel.objects.get(id=request.user.id)
            VisualFormApprovalData.objects.create(
                form=reqform, 
                form_creator=user_obj, 
                form_owner=user_obj, 
                approve_status=VisualFormApprovalData.ApprovalStatus.PENDING
            )

            request.session.pop("step1", None)
            request.session.pop("step1_cleaned", None)
            request.session.pop("acc_info", None)
            request.session.pop("step2", None)
            request.session.pop("step2_cleaned", None)

            return redirect("dashboard:dashboard")
        except Exception as e:
            print(e)
            ReqformDataModel.objects.filter(pk=reqform.pk).first().delete()
            WarrantDataModel.objects.filter(pk=warrant.pk).first().delete()

    if not request.session.get("step2"):
        return redirect(reverse("forms:step2"))
    
    form = DisabledFormStep1(initial=request.session.get("step1"), prefix="main_form",)

    warrants : list[dict] = request.session.get("step2")

    # print(request.session.get("step1"))
    # print(request.session.get("step2"))

    old_data_1 = request.session.get("step1")

    warrant_list = []
    for item in warrants:
        warrant_form = DisabledWarrantForm(initial=item)
        warrant_list.append(
            warrant_form
        )

    return render(request, "warrant_form/awis_step3.html", {
        "user": request.user,
        "form": form,
        "warrant_list": warrant_list,
        "disabled": True,
        "req_province": old_data_1.get("req_province"),
        "req_district": old_data_1.get("req_district"),
        "req_sub_district": old_data_1.get("req_sub_district"),
        "acc_province": old_data_1.get("acc_province"),
        "acc_district": old_data_1.get("acc_district"),
        "acc_sub_district": old_data_1.get("acc_sub_district"),
    })

##########################################################################

def dupeNeccesary(incoming_dict : dict, field_list : list):
        dupe = field_list
        new_dict = incoming_dict.copy()

        for field in dupe:
            new_dict.update({f"{field}_1": incoming_dict.get(field)})
            new_dict.update({f"{field}_2": incoming_dict.get(field)})

        if incoming_dict.get("cause_type_id"):
            new_dict.update({f"cause_type_id_{incoming_dict.get("cause_type_id")}": 1})
            new_dict.update({f"cause_text_{incoming_dict.get("cause_type_id")}": incoming_dict.get("cause_text")})

        if incoming_dict.get("have_req"):
            new_dict.update({f"have_req_{incoming_dict.get("have_req") + 1}": 1})


        return new_dict