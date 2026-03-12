from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required

from warrant_form.forms import WarrantForm, AWISFormStep1, DisabledWarrantForm, DisabledFormStep1
# from warrant_form.doc_create import doc_create_with_context
from warrant_form.model_warrant import WarrantDataModel
from warrant_form.model_reqform import ReqformDataModel


from dashboard.models import VisualFormApprovalData
from dashboard.warrant_wrapper import VisualWarrantData
from users.models import UserDataModel

import json

##############################################################################
# FORM VIEWS

@login_required(login_url="/users/login/")
def plain_form(request : HttpRequest):    
    main_form = VisualFormApprovalData(prefix="main_form")
    sub_form = WarrantForm(prefix="sub_form")

    context = {
        "main_form": main_form,
        "sub_form": sub_form
    }

    # if request.GET.get("status") == "error":
    #     context.update({"status": "error"})

    return render(request, "warrant_form/plain-reqform.html", context)

@login_required(login_url="/users/login/")
def plain_form_submission(request : HttpRequest):
    # The expected outcome.
    if request.method == "POST":
        main_form = VisualFormApprovalData(request.POST, prefix="main_form")
        sub_form = WarrantForm(request.POST, prefix="sub_form")

        if main_form.is_valid():
            awis_obj : VisualFormApprovalData = main_form.save(commit=False)
            warrant_obj : WarrantDataModel = sub_form.save()

            cleaned_dict = awis_obj.toAPICompatibleDict()
            warrant_dict = warrant_obj.toAPICompatibleDict()

            warrants_list = [warrant_dict,]

            cleaned_dict.update({"warrants": warrants_list})

            awis_obj.save()
            awis_obj.warrants.add(warrant_obj)

<<<<<<< HEAD
                # doc_create_with_context(form_awis_obj.toDocumentCompatibleDict())

                # MainAWISDataModel.objects.create(**cleaned_dict)

                return redirect(reverse("awis:success"))
                # sub_form = WarrantForm(prefix="sub_form")
=======
            # print(awis_obj.toAPICompatibleDictWithConvertedWarrants())

            user_obj, success = UserDataModel.objects.get_or_create(user=request.user, role=0)
>>>>>>> dev
            
            VisualFormApprovalData.objects.create(form=awis_obj, form_creator=user_obj, form_owner=user_obj, approve_status=1)

            ###################################################################

            # success = AWISConnectAPI.post_send_req_form("v1.1", request, cleaned_dict)
            
            # if not success:
            #     raise Exception("Form submission failed.")

            return redirect(reverse("forms:success"))
        
###############################################################################
        

@login_required(login_url="/users/login/")
def success_page(request : HttpRequest):
    return JsonResponse({
        "status_code": "200",
        "message": "success"
    })

##############################################################################

@login_required(login_url="/users/login/")
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
        
    old_data : dict = request.session.get("step1")

    if old_data:
        static_data.update(old_data)

    form = AWISFormStep1(initial=static_data, prefix="main_form")
    return render(request, "warrant_form/awis_step1.html", {
        "form": form,
        "step": 1,
    })

@login_required(login_url="/users/login/")
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
    
    initial_data = {}

    if request.session.get("step2"):
        initial_data.update(request.session.get("step2")[0])
    else:
        initial_data.update(request.session.get("acc_info"))

    form = WarrantForm(initial=initial_data)

    return render(request, "warrant_form/awis_step2.html", {
        "form": form,
        "step": 2,
    })

def step3_confirm_form(request : HttpRequest):
    if request.method == "POST":
        try:
            reqform_data = request.session.get("step1_cleaned")
            warrant_data = request.session.get("step2_cleaned")[0]

            reqform : ReqformDataModel = ReqformDataModel.objects.create(**reqform_data)

            warrant : WarrantDataModel = WarrantDataModel.objects.create(
                **warrant_data
            )

            if reqform:
                reqform.warrants.add(warrant)

                # Fix below/above for more than 1 warrant

            # data = reqform.toAPICompatibleDictWithConvertedWarrants()

            # print(json.dumps(data, indent=2, ensure_ascii=False))

            user_obj, success = UserDataModel.objects.get_or_create(user=request.user, role=0)
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
        except:
            ReqformDataModel.objects.filter(pk=reqform.pk).first().delete()
            WarrantDataModel.objects.filter(pk=warrant.pk).first().delete()
    
    form = DisabledFormStep1(initial=request.session.get("step1"), prefix="main_form",)

    warrants : list[dict] = request.session.get("step2")

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
    })

##########################################################################

def dupeNeccesary(incoming_dict : dict, field_list : list):
        dupe = field_list
        new_dict = incoming_dict.copy()

        for field in dupe:
            new_dict.update({f"{field}_1": incoming_dict.get(field)})
            new_dict.update({f"{field}_2": incoming_dict.get(field)})

        return new_dict