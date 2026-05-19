from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, JsonResponse, Http404

from dashboard.models import FormAwaitingApproval 
from dashboard.models import VisualReqformData
from dashboard.warrant_wrapper import VisualWarrantData

from warrant_form.model_reqform import WarrantDataModel, ReqformDataModel
from warrant_form.model_draftform import FormDraftContainer

from users.models import UserDataModel

import _log_utils.file_logger as FileLogger
from _log_utils.file_logger import AccessType

from users.permissions.perms import PermissionList, PermissionType, perm_str, perm_str_list
from users.permissions.decorators import perm_req_log

from . import _permissions as DashboardPerm

def reqform_info(request : HttpRequest, req_no_plaintiff : str):

    reqform = ReqformDataModel.objects.filter(
        req_no_plaintiff=req_no_plaintiff
    ).first()

    status = None
    status_int = None
    action = None
    warrants = None

    form_already_sent = VisualReqformData.objects.filter(
        form__req_no_plaintiff=req_no_plaintiff
    ).first()

    form_not_sent = FormAwaitingApproval.objects.filter(
        form__req_no_plaintiff=req_no_plaintiff
    ).first()

    if form_already_sent:
        status = form_already_sent.get_accept_display()
        status_int = form_already_sent.accept
        action = "report"

        warrants = VisualWarrantData.objects.filter(
            warrant__in=reqform.warrants.all()
        )

    elif form_not_sent:
        status = form_not_sent.get_approve_status_display()
        status_int = form_not_sent.approve_status
        action = "approve"

        warrants = reqform.warrants.all()

    else:
        status = "ร่าง"

    return render(request, "dashboard/reqform_info_page.html", {
        "reqform": reqform,
        "warrants": warrants,
        "status": status,
        "status_int": status_int,
        "action": action,
    })
