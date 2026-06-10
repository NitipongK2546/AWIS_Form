from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpRequest, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.conf import settings

from dashboard.models import FormAwaitingApproval 
from dashboard.models import VisualReqformData
from dashboard.warrant_wrapper import VisualWarrantData
from warrant_form.model_draftform import FormDraftContainer

import _log_utils.file_logger as FileLogger
from _log_utils.file_logger import AccessType

from users.permissions.perms import PermissionList, PermissionType, perm_str_list
from users.permissions.decorators import perm_req_log

from . import _permissions as DashboardPerm
from .forms_filter import DashboardFilterForm, StatisticFilterForm

from . import views_main_utils as utils

@login_required
def dashboard(request : HttpRequest):
    # If user can't access Dashboard page.
    if not request.user.has_perms(
        perm_str_list([PermissionType.VIEW,], 
                PermissionList.DASHBOARD,)
    ):
        return redirect("dashboard:statistics")

    # unsent_count = FormAwaitingApproval.objects.filter(
    #     approve_status=1
    # ).count()
    # sent_count = VisualReqformData.objects.filter(
    #     accept=99
    # ).count()

    # all_accepted = VisualReqformData.objects.filter(
    #     accept=1
    # )

    dashboard_list = []
    req_no_plaintiff_list = []


    banned_id_list = []

    filter_form = DashboardFilterForm(request.GET)
    drafts, form_unsent, form_already_sent = utils.get_dashboard_objs(request, filter_form)

    unreported_count = 0

    for visual_form in form_already_sent[0]:
        reqform = visual_form.form
        warrants = VisualWarrantData.objects.filter(
            warrant__in=reqform.warrants.all()
        )
        not_all_reported = warrants.filter(report_status=0).exists()
        if not_all_reported:
            unreported_count += 1

    utils.append_draft_data(dashboard_list, req_no_plaintiff_list, drafts[0], banned_id_list)  
    utils.append_unsent_form_data(dashboard_list, req_no_plaintiff_list, form_unsent[0], banned_id_list)
    
    utils.append_sent_form_data(dashboard_list, req_no_plaintiff_list, form_already_sent[0], banned_id_list)

    # dashboard_list.reverse()
    dashboard_list.sort(
        key=lambda x: x["last_update"],
        reverse=True
    )
    
    context = {
        "reqform_infos": dashboard_list,
        "user": request.user,
        "filter_form": filter_form,

        ############################################

        "draft_count": drafts[1],
        "unsent_count": form_unsent[1],
        "sent_count": form_already_sent[1],
        "unreported_count": unreported_count
    }

    # if request.user.has_perms(
    #     perm_str_list([PermissionType.VIEW, PermissionType.CREATE], PermissionList.REQFORM_AWAIT_APPROVAL)
    # ):
    #     context.update({
    #         "can_create_form": True,
    #     })
    
    # if request.user.has_perms(
    #     perm_str_list([PermissionType.VIEW, PermissionType.APPROVE], PermissionList.REQFORM_AWAIT_APPROVAL)
    # ):
    #     context.update({
    #         "can_approve_form": True,
    #     })


    return render(request, "dashboard/dashboard.html", context)

@perm_req_log(*DashboardPerm.VIEW_STATISTIC_PAGE)
def statistic_page_view(request : HttpRequest):


    form_failed_approval_count = FormAwaitingApproval.objects.filter(
        approve_status=0
    ).count()
    form_canceled_count = FormAwaitingApproval.objects.filter(
        approve_status=-1
    ).count()
    form_unsent_count = FormAwaitingApproval.objects.filter(
        approve_status=1
    ).count()
    form_sent_count = VisualReqformData.objects.filter(
        accept=99
    ).count()
    form_unaccepted_count = VisualReqformData.objects.filter(
        accept=0
    ).count()


    form_accepted = VisualReqformData.objects.filter(
        accept=1
    )

    unreported_count = 0
    all_reported_count = 0

    for visual_form in form_accepted:
        reqform = visual_form.form
        warrants = VisualWarrantData.objects.filter(
            warrant__in=reqform.warrants.all()
        )
        not_all_reported = warrants.filter(report_status=0).exists()
        if not_all_reported:
            unreported_count += 1
        else:
            all_reported_count += 1

    dashboard_list = []
    req_no_plaintiff_list = []

    dashboard_list = []
    req_no_plaintiff_list = []
    banned_id_list = []

    filter_form = StatisticFilterForm(request.GET)
    form_unsent, form_already_sent = utils.get_statistics_objs(request, filter_form)

    utils.append_unsent_form_data(dashboard_list, req_no_plaintiff_list, form_unsent, banned_id_list)
    utils.append_sent_form_data(dashboard_list, req_no_plaintiff_list, form_already_sent, banned_id_list)

    dashboard_list.sort(
        key=lambda x: x["last_update"],
        reverse=True
    )
    
    context = {
        "reqform_infos": dashboard_list,
        "user": request.user,
        "filter_form": filter_form,

        ############################################

        "canceled_form": form_canceled_count,
        "unsent_form": form_unsent_count,
        "unapproved_form": form_failed_approval_count,
        "sent_form": form_sent_count,
        "unaccepted_form": form_unaccepted_count,
        "unreported_form": unreported_count,
        "all_reported_form": all_reported_count,

        "total_count": form_sent_count + form_unsent_count + form_failed_approval_count + form_canceled_count + form_unaccepted_count + unreported_count + all_reported_count
    }

    return render(request, "history/statistic_page_view.html", context)