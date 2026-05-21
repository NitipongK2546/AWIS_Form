from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.conf import settings

from dashboard.models import FormAwaitingApproval 
from dashboard.models import VisualReqformData
from dashboard.warrant_wrapper import VisualWarrantData

from warrant_form.model_reqform import WarrantDataModel
from warrant_form.model_draftform import FormDraftContainer

from users.models import UserDataModel

import _log_utils.file_logger as FileLogger
from _log_utils.file_logger import AccessType

import _request_utils.connect_api as AWISConnectAPI

from datetime import datetime
from django.utils import timezone

from users.permissions.perms import PermissionList, PermissionType, perm_str, perm_str_list
from users.permissions.decorators import perm_req_log

from . import _permissions as DashboardPerm
from .forms_filter import DashboardFilterForm

def append_replace_id(target_list : list[dict], id_list : list[str],incoming_dict : dict, id : str):
    if id not in id_list:
        id_list.append(id)
        target_list.append(incoming_dict)
    else:
        # If ID is in ID_list
        target_obj_index = id_list.index(id)
        target_list.pop(target_obj_index)
        id_list.pop(target_obj_index)
        target_list.append(incoming_dict)


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


@login_required
def dashboard(request : HttpRequest):

    drafts = FormDraftContainer.objects.all()
    draft_count = drafts.count()
    approved = FormAwaitingApproval.objects.filter(
        approve_status=1
    ).count()
    accepted = VisualReqformData.objects.filter(
        accept=99
    ).count()

    dashboard_list = []
    req_no_plaintiff_list = []

    filter_form = DashboardFilterForm(request.GET)
    if filter_form.is_valid():
        data = filter_form.cleaned_data
        filter_data = _format_filter(data)
    else:
        filter_data = {}

    form_unsent = []
    form_already_sent = []

    wanted_status = filter_data.pop("status", None)
    if isinstance(wanted_status, str):
        wanted_status = int(wanted_status)

    if wanted_status in [10, 11, 12]:
        compare_val = {
            10: 1,
            11: 0,
            12: 2,
        }

        filter_data.update({
            "approve_status": compare_val.get(wanted_status)
        })
        form_unsent = FormAwaitingApproval.objects.filter(**filter_data).exclude(approve_status=-1)
    
    elif wanted_status in [20, 21, 22, 23, 24, 25]:
        compare_val = {
            20: 99,
            21: 0,
            22: 1,
            23: 1,
            24: 1,
            25: 1,
        }

        filter_data.update({
            "accept": compare_val.get(wanted_status)
        })
        form_already_sent = VisualReqformData.objects.filter(**filter_data)
    else:
        form_unsent = FormAwaitingApproval.objects.filter(**filter_data).exclude(approve_status=-1)
        form_already_sent = VisualReqformData.objects.filter(**filter_data)

              
    for reqform in form_unsent:
        append_replace_id(
            target_list=dashboard_list,
            id_list=req_no_plaintiff_list,
            incoming_dict = {
                "reqno": reqform.form.getReqno(),
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
        )

    for reqform in form_already_sent:  
        append_replace_id(
            target_list=dashboard_list,
            id_list=req_no_plaintiff_list,
            incoming_dict = {
                "reqno": reqform.form.getReqno(),
                "last_update": reqform.form.last_update_date,
                "req_no_plaintiff": reqform.form.req_no_plaintiff,
                "req_name": reqform.form.req_name,
                "accused": reqform.form.accused,
                "req_date": reqform.form.req_date,            
                "status": reqform.get_accept_display(),
                "status_int":  reqform.accept,
                "status_choice": color_val_sent.get(reqform.accept),
                "action": "report"
            },
            id=reqform.form.req_no_plaintiff,
        )

    # dashboard_list.reverse()
    dashboard_list.sort(
        key=lambda x: x["last_update"],
        reverse=True
    )
    
    context = {
        "reqform_infos": dashboard_list,
        "user": request.user,
        "draft_count": draft_count,
        "approve_form": approved,
        "accept_form": accepted,
        "filter_form": filter_form,
    }

    if request.user.has_perms(
        perm_str_list([PermissionType.VIEW, PermissionType.CREATE], PermissionList.REQFORM_AWAIT_APPROVAL)
    ):
        context.update({
            "can_create_form": True,
        })
    
    if request.user.has_perms(
        perm_str_list([PermissionType.VIEW, PermissionType.APPROVE], PermissionList.REQFORM_AWAIT_APPROVAL)
    ):
        context.update({
            "can_approve_form": True,
        })


    return render(request, "dashboard/dashboard.html", context)

@perm_req_log(*DashboardPerm.VIEW_STATISTIC_PAGE)
def statistic_page_view(request : HttpRequest):

    drafts = FormDraftContainer.objects.all()
    draft_count = drafts.count()
    form_unsent_count = FormAwaitingApproval.objects.filter(
        approve_status=1
    ).count()
    form_sent_count = VisualReqformData.objects.filter(
        accept=99
    ).count()
    form_accepted_count = VisualReqformData.objects.filter(
        accept=1
    ).count()

    dashboard_list = []
    req_no_plaintiff_list = []

    filter_form = DashboardFilterForm(request.GET)
    if filter_form.is_valid():
        data = filter_form.cleaned_data
        filter_data = _format_filter(data)
    else:
        filter_data = {}

    form_unsent = FormAwaitingApproval.objects.filter(**filter_data)
    form_already_sent = VisualReqformData.objects.filter(**filter_data)

    for reqform in form_unsent:
        append_replace_id(
            target_list=dashboard_list,
            id_list=req_no_plaintiff_list,
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
            },
            id=reqform.form.req_no_plaintiff,
        )

    for reqform in form_already_sent:
        append_replace_id(
            target_list=dashboard_list,
            id_list=req_no_plaintiff_list,
            incoming_dict = {
                "reqno": reqform.form.getReqno(),
                "req_year": reqform.form.req_year,
                "last_update": reqform.form.last_update_date,
                "req_no_plaintiff": reqform.form.req_no_plaintiff,
                "req_name": reqform.form.req_name,
                "accused": reqform.form.accused,
                "req_date": reqform.form.req_date,            
                "status": reqform.get_accept_display(),
                "status_int":  reqform.accept,
                "status_choice": color_val_sent.get(reqform.accept),
            },
            id=reqform.form.req_no_plaintiff,
        )

    dashboard_list.reverse()
    
    context = {
        "reqform_infos": dashboard_list,
        "user": request.user,
        "filter_form": filter_form,
        "draft_count": draft_count,
        "unsent_form": form_unsent_count,
        "sent_form": form_sent_count,
        "accepted_form": form_accepted_count,
        "total_count": form_sent_count + form_unsent_count + form_accepted_count,
    }

    return render(request, "history/statistic_page_view.html", context)