from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout 
from django.http import HttpRequest, JsonResponse, HttpResponse
# from formtools.wizard.views import SessionWizardView, CookieWizardView
from warrant_form.models import WarrantDataModel, MainAWISDataModel
from warrant_form.forms import WarrantForm, MainAWISForm, SpecialAWISDataFormModelPartOne
from warrant_form.doc_create import doc_create_with_context

import json

import warrant_form.connect_api as AWISConnectAPI

##############################################################################
# FORM VIEWS
def user_login(request : HttpRequest):
    if request.user.is_authenticated:
        return redirect("awis:index")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("awis:index")
    else:
        form = AuthenticationForm()
    return render(request, "warrant_form/login.html", {"form": form})

def signup(request : HttpRequest):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("awis:login")
    else:
        form = UserCreationForm()
    return render(request, "warrant_form/signup.html", {"form": form})

def custom_logout(request : HttpRequest): 
    logout(request) 
    return redirect("awis:login")

# def login(request : HttpRequest): 
#     if request.method != "POST":
#         return HttpResponseNotAllowed("Method is not POST.")

#     if login_authorize(request, "test", "test"):


#     return HttpResponseForbidden("Login Failed.")

def index(request : HttpRequest):    
    main_form = WarrantForm(prefix="main_form")
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

            success = AWISConnectAPI.post_send_req_form("v1.1", request, cleaned_dict)
            
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