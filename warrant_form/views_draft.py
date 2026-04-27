from django.shortcuts import render, redirect
from django.urls import reverse

from django.http import HttpRequest, JsonResponse, Http404
from .model_draftform import ReqformDraftDataModel, WarrantDraftDataModel, FormDraftContainer
from warrant_form.forms import ReqformDraftModelForm, FormDraftContainerModelForm, WarrantDraftDataModelForm

from dashboard.models import FormAwaitingApproval

from warrant_form.model_reqform import ReqformDataModel
from warrant_form.model_warrant import WarrantDataModel

from django.forms.models import model_to_dict


def create_draft_main_local_page(request : HttpRequest):
    
    draft_container = FormDraftContainer.objects.create(
        form_owner=request.user,
        form_creator=request.user,
    )

    reqform_obj = ReqformDraftDataModel.objects.create(
        draft_container=draft_container
    )

    # return render(request, "drafts/awis_draft_main_local.html", {
    #     "draft_container": draft_container,
    # })

    return redirect("forms:view-draft-container", container_id=draft_container.pk)


def view_draft_main_local_page(request : HttpRequest, container_id : int):
    draft_container = FormDraftContainer.objects.filter(pk=container_id).first()

    if draft_container:
        return render(request, "drafts/awis_draft_main_local.html", {
            "draft_container": draft_container,
        })
    
    raise Http404()

def delete_draft_main_local_page(request : HttpRequest, container_id : int):
    draft_container = FormDraftContainer.objects.filter(pk=container_id).first()

    if draft_container:
        if request.method == "POST":
            draft_container.delete()

            return redirect("dashboard:dashboard")

        return render(request, "dashboard/confirmation_page.html", {
            "action": "Delete Draft",
        })
    
    raise Http404()


#####################################################################

# def create_reqform_draft(request : HttpRequest):
#     if request.method == "POST":
#         draft_form = ReqformDraftModelForm(request.POST)
#         draft_form.save()

#         return redirect("dashboard:dashboard")
    
#     preadded_field = {
#         "court_code": "0000011",
#         "police_station_id": "TCCT0001",
#         "req_no_plaintiff": "tcctd20260304002",
#         "create_uid": request.user.api_uid
#     }

#     draft_form = ReqformDraftModelForm(initial=preadded_field)

#     return render(request, "warrant_form/awis_draft_step1.html", {
#         "draft_form": draft_form,
#     })


def edit_reqform_draft(request : HttpRequest, container_id : int):
    draft_container = FormDraftContainer.objects.filter(pk=container_id).first()

    if draft_container:

        reqform_form = ReqformDraftModelForm(instance=draft_container.reqform_draft)

        if request.method == "POST":
            reqform_form = ReqformDraftModelForm(request.POST, instance=draft_container.reqform_draft)
            reqform_form.save()

            draft_container.save()

            return redirect("forms:view-draft-container", container_id=draft_container.pk)

        return render(request, "drafts/awis_draft_step1.html", {
            "draft_form": reqform_form,
        })
    
    raise Http404()

###############################################################################

def create_warrant_draft(request : HttpRequest, container_id : int):
    draft_container = FormDraftContainer.objects.filter(pk=container_id).first()

    if draft_container:
        WarrantDraftDataModel.objects.create(
            draft_container=draft_container
        )
        draft_container.save()

        return redirect("forms:view-draft-container", container_id=draft_container.pk)
    
    raise Http404()

def edit_warrant_draft(request : HttpRequest, container_id : int, warrant_id : int):
    draft_container = FormDraftContainer.objects.filter(pk=container_id).first()

    if draft_container:

        warrant_form = WarrantDraftDataModelForm(instance=draft_container.warrant_drafts.get(pk=warrant_id))

        if request.method == "POST":
            warrant_form = WarrantDraftDataModelForm(request.POST, instance=draft_container.warrant_drafts.get(pk=warrant_id))
            warrant_form.save()

            draft_container.save()

            return redirect("forms:view-draft-container", container_id=draft_container.pk)

        return render(request, "drafts/awis_draft_step1.html", {
            "draft_form": warrant_form,
        })
    
    raise Http404()

def delete_warrant_draft(request : HttpRequest, container_id : int, warrant_id : int):
    draft_container = FormDraftContainer.objects.filter(pk=container_id).first()

    if draft_container:

        warrant_form = WarrantDraftDataModel.objects.get(pk=warrant_id)
        warrant_form.delete()

        draft_container.save()

        return redirect("forms:view-draft-container", container_id=draft_container.pk)

        # return render(request, "dashboard/confirmation_page.html", {
        #     "action": "Delete Warrant inside Draft",
        # })
    
    raise Http404()

###############################################################################

def create_reqform_from_draft(request : HttpRequest, container_id : int):
    selected_draft = FormDraftContainer.objects.filter(pk=container_id).first()

    if selected_draft:
        if request.method == "POST":
            try:
                # reqform = AWISFormStep1(selected_draft.convertBacktoFormView())
                reqform_obj = ReqformDataModel.objects.create(\
                    **model_to_dict(selected_draft.reqform_draft, exclude=["id", "draft_container"]))

                for draft in selected_draft.warrant_drafts.all():
                    warrant = WarrantDataModel.objects.create(
                        **model_to_dict(draft, exclude=["id", "draft_container"])
                    )
                    reqform_obj.warrants.add(warrant)

                FormAwaitingApproval.objects.create(form=reqform_obj, form_owner=request.user, form_creator=request.user, approve_status=1)


                return redirect("dashboard:dashboard")
            except Exception as e:
                if reqform_obj:
                    reqform_obj.delete()

                return JsonResponse({"error": str(e)}, json_dumps_params={"ensure_ascii": False})

        return render(request, "dashboard/confirmation_page.html", {
            "action": "Create Reqform from Draft",
        })
    
    raise Http404()

################################################################################

