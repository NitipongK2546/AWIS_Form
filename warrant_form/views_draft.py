from django.shortcuts import render, redirect
from django.urls import reverse

from django.http import HttpRequest, JsonResponse, Http404
from .model_draftform import ReqformDraftDataModel
from warrant_form.forms import ReqformDraftModelForm

def create_reqform_draft(request : HttpRequest):
    if request.method == "POST":
        draft_form = ReqformDraftModelForm(request.POST)
        draft_form.save()

        return redirect("dashboard:dashboard")
    
    preadded_field = {
        "court_code": "0000011",
        "police_station_id": "TCCT0001",
        "req_no_plaintiff": "tcctd20260304002",
        "create_uid": request.user.api_uid
    }

    draft_form = ReqformDraftModelForm(initial=preadded_field)

    return render(request, "warrant_form/awis_draft_step1.html", {
        "draft_form": draft_form,
    })


def edit_reqform_draft(request : HttpRequest, draft_id : int):
    old_draft = ReqformDraftDataModel.objects.filter(pk=draft_id).first()

    if old_draft:
        if request.method == "POST":
            draft_form = ReqformDraftModelForm(request.POST, instance=old_draft)
            draft_form.save()

            return redirect("dashboard:dashboard")

        draft_form = ReqformDraftModelForm(instance=old_draft)

        return render(request, "warrant_form/awis_draft_step1.html", {
            "draft_form": draft_form,
        })
    
    raise Http404()

def delete_reqform_draft(request : HttpRequest, draft_id : int):
    selected_draft = ReqformDraftDataModel.objects.filter(pk=draft_id).first()

    if selected_draft:
        if request.method == "POST":
            selected_draft.delete()

            return redirect("dashboard:dashboard")

        return render(request, "dashboard/confirmation_page.html", {
            "action": "Delete Draft",
        })
    
    raise Http404()

# def create_reqform_from_draft(request : HttpRequest, draft_id : int):
#     selected_draft = ReqformDraftDataModel.objects.filter(pk=draft_id).first()

#     if selected_draft:
#         if request.method == "POST":
#             try:



#             return redirect("dashboard:dashboard")

#         return render(request, "dashboard/confirmation_page.html", {
#             "action": "Create Reqform from Draft",
#         })
    
#     raise Http404()


    
