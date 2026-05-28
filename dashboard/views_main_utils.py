from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.conf import settings

from dashboard.models import FormAwaitingApproval, VisualReqformData
from warrant_form.model_draftform import FormDraftContainer
from dashboard.warrant_wrapper import VisualWarrantData

from django.forms import Form
from django.utils import timezone

def append_replace_id(target_list : list[dict], id_list : list[str],incoming_dict : dict, id : str, banned_id_list : list[str]):
    if id in banned_id_list:
        return
    
    # print(id_list)
    # print()

    if id not in id_list:
        id_list.append(id)
        target_list.append(incoming_dict)
    else:
        # If ID is in ID_list
        target_obj_index = id_list.index(id)
        target_list[target_obj_index] = incoming_dict

        # target_list.pop(target_obj_index)
        # # id_list.pop(target_obj_index)
        # target_list.append(incoming_dict)


########################################################################

color_val_unsent = {
    1: 10,
    0: 11,
    2: 12,
    -1: 99,
}

color_val_sent = {
    99: 20,
    0: 22,
    1: 23,
}


def _format_filter(incoming_dict : dict):
    filter = {}

    if incoming_dict.get("status"):
        filter.update({
            "status": incoming_dict.get("status")
        })

    if incoming_dict.get("req_no_plaintiff"):
        filter.update({
            "form__req_no_plaintiff": incoming_dict.get("req_no_plaintiff"),
        })

    start_date = incoming_dict.get("start_date")
    end_date = incoming_dict.get("end_date")
    start_obj = None
    end_obj = None

    if start_date:
        start_obj = timezone.datetime.strftime(
            start_date,
            "%Y-%m-%d %H:%M:%S"
        )
    if end_date:
        end_obj = timezone.datetime.strftime(
            end_date,
            "%Y-%m-%d %H:%M:%S"
        )

    if start_obj and end_obj:
        filter.update({
            "form__req_date__range": (start_obj, end_obj),
        })
        
    return filter

def append_draft_data(target_list : list[dict], id_list : list[str], form_unsent : list[FormDraftContainer], banned_id_list : list[str]):
    for draft in form_unsent:
        chosen_id = draft.reqform_draft.req_no_plaintiff if draft.reqform_draft.req_no_plaintiff else draft.pk
        append_replace_id(
            target_list=target_list,
            id_list=id_list,
            incoming_dict = {
                "reqno": "-",
                "req_year": "-",
                "last_update": draft.last_edit,
                "req_no_plaintiff": draft.reqform_draft.req_no_plaintiff if draft.reqform_draft.req_no_plaintiff else "กำลังร่าง",
                "container_id": draft.pk,
                "req_name": draft.reqform_draft.req_name if draft.reqform_draft.req_name else "กำลังร่าง",
                "accused": draft.reqform_draft.accused if draft.reqform_draft.accused else "กำลังร่าง",
                "req_date": "-",            
                "status": "ร่างคำร้อง",
                "status_int": 1,
                "status_choice": 1,
                "action": "draft",
            },
            id=chosen_id,
            banned_id_list=banned_id_list,
        )

def append_unsent_form_data(target_list : list[dict], id_list : list[str], form_unsent : list[FormAwaitingApproval], banned_id_list : list[str]):
    for reqform in form_unsent:
        append_replace_id(
            target_list=target_list,
            id_list=id_list,
            incoming_dict = {
                "reqno": reqform.form.getReqno(),
                "req_year": reqform.form.req_year,
                "last_update": reqform.form.last_update_date,
                "req_no_plaintiff": reqform.form.req_no_plaintiff,
                "req_name": reqform.form.req_name,
                "accused": reqform.form.accused,
                "req_date": reqform.form.req_date,            
                "status": reqform.get_approve_status_display(),
                "status_int":  reqform.approve_status,
                "status_choice": color_val_unsent.get(reqform.approve_status),
                "action": "approve"
            },
            id=reqform.form.req_no_plaintiff,
            banned_id_list=banned_id_list,
        )

def append_sent_form_data(target_list : list[dict], id_list : list[str], form_already_sent : list[VisualReqformData], banned_id_list : list[str]):
    for visual_form in form_already_sent:  

        reqform = visual_form.form
        warrants = VisualWarrantData.objects.filter(
            warrant__in=reqform.warrants.all()
        )

        all_reported = not warrants.exclude(report_status=1).exists()

        data_dict = {
            "reqno": visual_form.form.getReqno(),
            "req_year": visual_form.form.req_year,
            "last_update": visual_form.form.last_update_date,
            "req_no_plaintiff": visual_form.form.req_no_plaintiff,
            "req_name": visual_form.form.req_name,
            "accused": visual_form.form.accused,
            "req_date": visual_form.form.req_date,            
            "status": visual_form.get_accept_display(),
            "status_int":  visual_form.accept,
            "status_choice": color_val_sent.get(visual_form.accept),
            "action": "report"
        }

        if all_reported:
            data_dict.update({
                "status": "รายงานหมายจับทั้งหมดแล้ว",
                # "status_int": 
                "status_choice": 25,
            })

        append_replace_id(
            target_list=target_list,
            id_list=id_list,
            incoming_dict = data_dict,
            id=visual_form.form.req_no_plaintiff,
            banned_id_list=banned_id_list,
        )

def get_dashboard_objs(request : HttpRequest , form_used_for_filter : Form):
    form_unsent = []
    form_already_sent = []
    drafts = []

    if form_used_for_filter.is_valid():
        data = form_used_for_filter.cleaned_data
        filter_data = _format_filter(data)
    else:
        filter_data = {}

    wanted_status = filter_data.pop("status", None)
    if isinstance(wanted_status, str):
        wanted_status = int(wanted_status)

    ##########################################################

    seven_days_ago = timezone.now() - timezone.timedelta(days=7)

    written_draft = FormDraftContainer.objects.filter(**filter_data).filter(form_creator=request.user, reqform_draft__reqformdatamodel__isnull=True)
    owned_draft = FormDraftContainer.objects.filter(**filter_data).filter(form_owner=request.user, reqform_draft__reqformdatamodel__isnull=True)
    available_drafts = written_draft.union(owned_draft)
    available_drafts_count = len(available_drafts)

    written_unsent = FormAwaitingApproval.objects.filter(form_creator=request.user).filter(**filter_data).exclude(form__last_update_date__lt=seven_days_ago)
    owned_unsent = FormAwaitingApproval.objects.filter(form_owner=request.user).filter(**filter_data).exclude(form__last_update_date__lt=seven_days_ago)

    written_unsent_without_approved = FormAwaitingApproval.objects.filter(form_creator=request.user).filter(**filter_data).exclude(form__last_update_date__lt=seven_days_ago).exclude(approve_status=2)
    owned_unsent_without_approved = FormAwaitingApproval.objects.filter(form_owner=request.user).filter(**filter_data).exclude(form__last_update_date__lt=seven_days_ago).exclude(approve_status=2)

    existing_approved_form = written_unsent.union(owned_unsent)
    
    available_unsent = written_unsent_without_approved.union(owned_unsent_without_approved)
    available_unsent_count = len(available_unsent)

    available_sent = VisualReqformData.objects.filter(**filter_data).filter(form__in=existing_approved_form.values("form"))
    available_sent_count = len(available_sent)

    if wanted_status in [1, ]:
        drafts = available_drafts
        
    elif wanted_status in [10, 11, 12, 99]:
        compare_val = {
            10: 1,
            11: 0,
            12: 2,
            99: -1,
        }

        filter_data.update({
            "approve_status": compare_val.get(wanted_status)
        })

        a = written_unsent_without_approved.filter(**filter_data)
        b = owned_unsent_without_approved.filter(**filter_data)

        form_unsent = a.union(b)

    elif wanted_status in [20, 21, 22, 23, 24, 25]:
        compare_val = {
            20: 99,
            21: 1,
            22: 0,
            23: 1,
            24: 1,
            25: 1,
        }

        filter_data.update({
            "accept": compare_val.get(wanted_status),
        })

        form_already_sent = available_sent.filter(**filter_data)

        if wanted_status in [23, 24, 25]:
            unreported = []
            full_reported = []
            for visual_form in form_already_sent:
                reqform = visual_form.form
                warrants = VisualWarrantData.objects.filter(
                    warrant__in=reqform.warrants.all()
                )
                not_all_reported = warrants.filter(report_status=0).exists()
                if not_all_reported:
                    unreported.append(visual_form)
                else:
                    full_reported.append(visual_form)

            if wanted_status in [23, 24]:
                form_already_sent = unreported
            else:
                form_already_sent = full_reported

    else:
        drafts = available_drafts
        form_unsent = available_unsent
        
        form_already_sent = available_sent

    return (
        (drafts, available_drafts_count), 
        (form_unsent, available_unsent_count), 
        (form_already_sent, available_sent_count)
    )

def get_statistics_objs(request : HttpRequest, form_used_for_filter : Form):
    form_unsent = []
    form_already_sent = []

    if form_used_for_filter.is_valid():
        data = form_used_for_filter.cleaned_data
        filter_data = _format_filter(data)
    else:
        filter_data = {}

    wanted_status = filter_data.pop("status", None)
    if isinstance(wanted_status, str):
        wanted_status = int(wanted_status)

    if wanted_status in [10, 11, 12, 99]:
        compare_val = {
            10: 1,
            11: 0,
            12: 2,
            99: -1,
        }

        filter_data.update({
            "approve_status": compare_val.get(wanted_status)
        })
        form_unsent = FormAwaitingApproval.objects.filter(**filter_data)
    
    elif wanted_status in [20, 21, 22, 23, 24, 25]:
        compare_val = {
            20: 99,
            21: 1,
            22: 0,
            23: 1,
            24: 1,
            25: 1,
        }

        filter_data.update({
            "accept": compare_val.get(wanted_status)
        })
        form_already_sent = VisualReqformData.objects.filter(**filter_data)

        if wanted_status in [23, 24, 25]:
            unreported = []
            full_reported = []
            for visual_form in form_already_sent:
                reqform = visual_form.form
                warrants = VisualWarrantData.objects.filter(
                    warrant__in=reqform.warrants.all()
                )
                not_all_reported = warrants.filter(report_status=0).exists()
                if not_all_reported:
                    unreported.append(visual_form)
                else:
                    full_reported.append(visual_form)

            if wanted_status in [23, 24]:
                form_already_sent = unreported
            else:
                form_already_sent = full_reported

    elif wanted_status in [99,]:
        compare_val = {
            99: -1,
        }
        filter_data.update({
            "approve_status": compare_val.get(wanted_status)
        })
        form_unsent = FormAwaitingApproval.objects.filter(**filter_data)
    else:
        form_unsent = FormAwaitingApproval.objects.filter(**filter_data)
        form_already_sent = VisualReqformData.objects.filter(**filter_data)

    return form_unsent, form_already_sent