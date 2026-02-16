from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, JsonResponse

from formtools.wizard.views import SessionWizardView, CookieWizardView

from warrant_form.models import WarrantDataModel, MainAWISDataModel
from warrant_form.forms import WarrantForm, MainAWISForm

import requests
from requests import RequestException
import json

import datetime
# from django.utils import timezone 
# from django.utils.timezone import datetime 

from django.forms.models import model_to_dict

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

ALL_FORMS = [
    ("awis_req_form", MainAWISForm),
    ("warrant_form", WarrantForm),
]

class AWISFormWizard(CookieWizardView):
    form_list = ALL_FORMS
    template_name = "warrant_form/wizard.html"

    def done(self, form_list, **kwargs):
        awis_req_form : MainAWISForm = form_list[0]
        warrant_form : WarrantForm = form_list[1]

        awis_req_obj : MainAWISDataModel = awis_req_form.save(commit=False)
        warrant_obj : WarrantDataModel = warrant_form.save()

        awis_req_obj.save()

        return redirect("awis:success")

def index(request : HttpRequest):
    ## SUB_FORM HAS TO PASS -> MAIN_FORM WILL PASS...
    ## Well, just check both...
    main_form = MainAWISForm(prefix="main_form")
    sub_form = WarrantForm(prefix="sub_form")

    return render(request, "warrant_form/index.html", {
        "main_form": main_form,
        "sub_form": sub_form
    })
        

def form_submission(request : HttpRequest):
    # The expected outcome.
    if request.method == "POST":
        main_form = MainAWISForm(request.POST, prefix="main_form")
        sub_form = WarrantForm(request.POST, prefix="sub_form")

        if main_form.is_valid():
            try:
                # Create object from the form, but don't commit to database yet.
                # warrant_obj : WarrantDataModel = sub_form.save(commit=False)

                main_awis_obj : MainAWISDataModel = main_form.save(commit=False)
                # main_awis_obj.warrants = warrant_obj

                ## Send an API request to see if it works or not, then save.
                # api_request_submit_data(main_awis_obj, "test_auth_token")

                dict_main_awis = model_to_dict(main_awis_obj)
                # dict_warrant = model_to_dict(warrant_obj)

                

                dict_main_awis.pop("id")
                # dict_main_warrant.update({
                #     "warrants": 
                # })
                # buddhist_date_half = dict_main_awis.get("scene_date_datehalf")
                # time_half = dict_main_awis.get("scene_date_timehalf")

                # if buddhist_date_half and time_half:
                #     # First, we have to convert Year: B.E. to A.D.
                #     BUDDHIST_ERA_YEAR_DIFF = 543
                #     iso_date_half = buddhist_date_half

                #     # Leave a space between date and time.
                #     full_datetime = f"{date_half} {time_half}"
                #     dict_main_awis.update({"scene_date": full_datetime})

                print(dict_main_awis)
                # print(dict_warrant)

                # SAVE THE FORM
                # The form, not the obj.
                main_form.save()

                return redirect(reverse("awis:success"))
            
            except Exception as e:
                print("@***EXCEPTION OCCURED:", e + "***")

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
        return redirect(reverse("awis:main_page"))

    # Not POST request.   
    else:
        return redirect(reverse("awis:main_page"))

def success_page(request : HttpRequest):
    return JsonResponse({
        "status_code": "200",
        "message": "success"
    })