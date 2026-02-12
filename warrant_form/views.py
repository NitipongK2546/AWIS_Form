from django.shortcuts import render
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
    main_form = MainJSONWarrantForm()
    sub_form = ArrayWarrantForm()

    return render(request, "warrant_form/index.html", {
        "main_form": main_form,
        "sub_form": sub_form
    })