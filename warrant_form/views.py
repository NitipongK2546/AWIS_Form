from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from warrant_form.forms import ArrayWarrantForm, MainJSONWarrantForm

# Create your views here.

# def index(request : HttpRequest):
#     return JsonResponse({
#         "success": "yes"
#     })

def index(request : HttpRequest):
    ## SUB_FORM HAS TO PASS -> MAIN_FORM WILL PASS...
    ## Well, just check both...
    if request.method == "POST":
        main_form = MainJSONWarrantForm(request.POST, prefix="main_form")
        sub_form = ArrayWarrantForm(request.POST, prefix="sub_form")

        if main_form.is_valid() and sub_form.is_valid():
            # both forms are valid
            main_form.save()
            sub_form.save()
            return redirect("/success-dayo")
        else:
            return redirect("#")
    else:
        main_form = MainJSONWarrantForm(prefix="main_form")
        sub_form = ArrayWarrantForm(prefix="sub_form")

        return render(request, "warrant_form/index.html", {
            "main_form": main_form,
            "sub_form": sub_form
        })

def form_submission(request : HttpRequest):
    main_form = MainJSONWarrantForm(prefix="main_form")
    sub_form = ArrayWarrantForm(prefix="sub_form")




    return JsonResponse({
        "ERROR": "WOW"
    })