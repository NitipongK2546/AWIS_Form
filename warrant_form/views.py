from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, JsonResponse, HttpResponseForbidden, HttpResponseNotAllowed

# from formtools.wizard.views import SessionWizardView, CookieWizardView

from warrant_form.models import WarrantDataModel, MainAWISDataModel
from warrant_form.forms import WarrantForm, MainAWISForm, SpecialAWISDataFormModelPartOne
from warrant_form.doc_create import doc_create_with_context

import json

import warrant_form.request_utils as RequestUtils

#############################################################################
# API REQUEST

def get_health_check(version : str) -> bool:
    base_url = RequestUtils.get_full_url_from_env()
    parameter = [version, "authorize"]

    response : JsonResponse = RequestUtils.get_request(
        base_url, 
        parameter_data=parameter
    )
    data : dict = response.json()
    
    # Response OK.
    if data.get("status") == "ok":
        return True
    
    return False

def post_login_authorize(version : str, request : HttpRequest, username : str, password : str) -> bool:

    if not get_health_check("v1"):
        return False
    
    base_url = RequestUtils.get_full_url_from_env()
    parameter = [version, "authorize"]

    post_data = {
        "username": username,
        "password": password,
    }
    response : JsonResponse = RequestUtils.post_request(
        base_url, 
        parameter_data=parameter, 
        post_data=post_data
    )
    data : dict = response.json()
    
    # Response OK.
    if data.get("token"):
        request.session["bearer_token"] = data.get("token")
        return True
    
    return False

def send_req_form(version : str, request : HttpRequest, post_data : dict) -> bool:

    if not get_health_check("v1"):
        return False

    base_url = RequestUtils.get_full_url_from_env()
    parameter = [version, "awis", "reqforms"]

    auth_token : str = RequestUtils.check_auth_token(request)
    response : JsonResponse = RequestUtils.post_request_with_auth(
        base_url, 
        parameter_data=parameter, 
        post_data=post_data, 
        auth_token=auth_token
    )
    data : dict = response.json()

    if data.get("status"):
        return True

##############################################################################
# FORM VIEWS

# def login(request : HttpRequest): 
#     if request.method != "POST":
#         return HttpResponseNotAllowed("Method is not POST.")

#     if login_authorize(request, "test", "test"):


#     return HttpResponseForbidden("Login Failed.")

def index(request : HttpRequest):    
    # health_check()
    main_form = MainAWISForm(prefix="main_form")
    sub_form = WarrantForm(prefix="sub_form")

    context = {
        "form": main_form,
        "main_form": main_form,
        "sub_form": sub_form
    }

    # if request.GET.get("status") == "error":
    #     context.update({"status": "error"})

    return render(request, "warrant_form/index.html", context)

def plain_form_submission(request : HttpRequest):
    # The expected outcome.
    if request.method == "POST":
        main_form = MainAWISForm(request.POST, prefix="main_form")
        sub_form = WarrantForm(request.POST, prefix="sub_form")

        if main_form.is_valid():
            awis_obj : MainAWISDataModel = main_form.save(commit=False)
            warrant_obj : WarrantDataModel = sub_form.save()

            cleaned_dict = awis_obj.toAPICompatibleDict()
            warrant_dict = warrant_obj.toAPICompatibleDict()

            warrants_list = [warrant_dict,]

            cleaned_dict.update({"warrants": warrants_list})

            ###################################################################

            success = send_req_form("v1.1", request, cleaned_dict)
            
            if not success:
                raise Exception("Form submission failed.")

            return redirect(reverse("awis:success"))
        

def form_submission(request : HttpRequest):
    # The expected outcome.
    if request.method == "POST":
        main_form = MainAWISForm(request.POST, prefix="main_form")
        # sub_form = WarrantForm(request.POST, prefix="sub_form")

        if main_form.is_valid():
            try:
                # Create object from the form, but don't commit to database yet.
                # warrant_obj : WarrantDataModel = sub_form.save(commit=False)

                form_awis_obj : SpecialAWISDataFormModelPartOne = main_form.save(commit=False)
                # main_awis_obj.warrants = warrant_obj

                ## Send an API request to see if it works or not, then save.

                cleaned_dict = form_awis_obj.toAPICompatibleDict()
                print(json.dumps(cleaned_dict, indent=4))

                # Uncomment to send API.
                # Please setup URL first.
                # api_request_submit_data(cleaned_dict, "test_auth_token")

                doc_create_with_context(form_awis_obj.toDocumentCompatibleDict())

                MainAWISDataModel.objects.create(**cleaned_dict)

                return redirect(reverse("awis:success"))
                # sub_form = WarrantForm(prefix="sub_form")
            
            except Exception as e:
                print("@***EXCEPTION OCCURED:", e  ,"***")

        print(main_form.errors.as_text())
        
        # IF not valid, or exception occured.
        return render(request, "warrant_form/awis_step1.html", {
            "form": main_form,
            "status": "error",
        })

    # Not POST request.   
    else:
        return redirect(reverse("awis:main_page"))

def success_page(request : HttpRequest):
    return JsonResponse({
        "status_code": "200",
        "message": "success"
    })