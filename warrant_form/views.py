from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, JsonResponse, HttpResponse

# from formtools.wizard.views import SessionWizardView, CookieWizardView

from warrant_form.models import WarrantDataModel, MainAWISDataModel
from warrant_form.forms import WarrantForm, MainAWISForm, SpecialAWISDataFormModelPartOne
from warrant_form.doc_create import doc_create_with_context

import requests
from requests import RequestException
import json

# from django.utils import timezone 
# from django.utils.timezone import datetime 

# Functions

def api_request_submit_data(warrant_form : MainAWISDataModel, auth_token):
    auth_header = {
        "Authorization": f"Bearer {auth_token}"
    }

    json_data = json.dumps(warrant_form)

    try:
        # Response is a json.
        response = requests.post("", data=json_data, headers=auth_header)
        data : dict = response.json()

        # success : bool = data.get("success", False)
        # message : str = data.get("message", "Error")

        return JsonResponse(data)

    except Exception as e:
        raise RequestException("The API request has failed.")

# VIEWS

def index(request : HttpRequest):    
    main_form = MainAWISForm(prefix="main_form")
    sub_form = WarrantForm(prefix="sub_form")

    context = {
        "form": main_form,
        "sub_form": sub_form
    }

    if request.GET.get("status") == "error":
        context.update({"status": "error"})

    return render(request, "warrant_form/awis_step1.html", context)
        

def form_submission(request : HttpRequest):
    # The expected outcome.
    if request.method == "POST":
        main_form = MainAWISForm(request.POST, prefix="main_form")
        sub_form = WarrantForm(request.POST, prefix="sub_form")

        if main_form.is_valid():
            try:
                # Create object from the form, but don't commit to database yet.
                # warrant_obj : WarrantDataModel = sub_form.save(commit=False)

                main_awis_obj : SpecialAWISDataFormModelPartOne = main_form.save(commit=False)
                # main_awis_obj.warrants = warrant_obj

                ## Send an API request to see if it works or not, then save.
                # api_request_submit_data(main_awis_obj, "test_auth_token")

                print(main_awis_obj.toAPICompatibleDict())

                doc_create_with_context(main_awis_obj.toAPICompatibleDict())

                # SAVE THE FORM
                # The form, not the obj.
                # main_form.save()

                return redirect(reverse("awis:success"))
                # sub_form = WarrantForm(prefix="sub_form")
            
            except Exception as e:
                print("@***EXCEPTION OCCURED:", e  ,"***")

        print(main_form.errors.as_text())
        # if main_form.is_valid() and sub_form.is_valid():
        #     try:
        #         # Create object from the form, but don't commit to database yet.
        #         warrant_obj : WarrantDataModel = sub_form.save(commit=False)

        #         main_awis_obj : MainAWISDataModel = main_form.save(commit=False)
        #         main_awis_obj.warrants = warrant_obj

        #         ## Send an API request to see if it works or not, then save.
        #         # api_request_submit_data(main_awis_obj, "test_auth_token")

        #         dict_main_awis = model_to_dict(main_awis_obj)
        #         dict_warrant = model_to_dict(warrant_obj)

        #         print(dict_main_awis)
        #         print(dict_warrant)

        #         dict_main_awis.pop("id")
        #         # dict_main_warrant.update({
        #         #     "warrants": 
        #         # })

        #         warrant_obj.save()
        #         main_awis_obj.save()

        #         return redirect(reverse("awis:success"))
            
        #     except Exception:
        #         pass
        
        # IF not valid, or exception occured.
        return redirect(reverse("awis:main_page", query={
            "status": "error",
        }))

    # Not POST request.   
    else:
        return redirect(reverse("awis:main_page"))

def success_page(request : HttpRequest):
    return JsonResponse({
        "status_code": "200",
        "message": "success"
    })