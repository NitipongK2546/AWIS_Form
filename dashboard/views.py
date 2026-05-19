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

def getFormAwaitViaReqno(reqno : str):
    return FormAwaitingApproval.objects.filter(form__reqno=reqno).first()

def getFormAwaitViaPlaintiff(req_no_plaintiff : str):
    return FormAwaitingApproval.objects.filter(form__req_no_plaintiff=req_no_plaintiff).first()

def isNotUserAndNotHaveApprovePerm(form : FormAwaitingApproval, user_data : UserDataModel):

    is_not_user = not (user_data in (form.form_creator, form.form_owner))

    not_has_approve_perm = not (user_data.has_perm(perm_str(PermissionType.VIEW, PermissionList.REQFORM_AWAIT_APPROVAL)))

    # print(is_not_user)

    return is_not_user and not_has_approve_perm

#######################################################################

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

# I will seperate dashboard + index, just in case.
def index(request : HttpRequest):
    return redirect("dashboard:dashboard")

from .forms_filter import DashboardFilterForm

@login_required
def dashboard(request : HttpRequest):
    def _format_filter(incoming_dict : dict):
        filter = {}

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

    form_unsent = FormAwaitingApproval.objects.filter(**filter_data)
    form_already_sent = VisualReqformData.objects.filter(**filter_data)

    for reqform in form_unsent:
        append_replace_id(
            target_list=dashboard_list,
            id_list=req_no_plaintiff_list,
            incoming_dict = {
                "reqno": reqform.form.getReqno(),
                "req_no_plaintiff": reqform.form.req_no_plaintiff,
                "req_name": reqform.form.req_name,
                "accused": reqform.form.accused,
                "req_date": reqform.form.req_date,            
                "status": reqform.get_approve_status_display(),
                "status_int":  reqform.approve_status,
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
                "req_no_plaintiff": reqform.form.req_no_plaintiff,
                "req_name": reqform.form.req_name,
                "accused": reqform.form.accused,
                "req_date": reqform.form.req_date,            
                "status": reqform.get_accept_display(),
                "status_int":  reqform.accept,
                "action": "report"
            },
            id=reqform.form.req_no_plaintiff,
        )

    dashboard_list.reverse()
    # dashboard_list.sort(
    #     key=lambda x: x["req_date"]
    # )
    
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

############################################################################

@perm_req_log(*DashboardPerm.REQFORM_AWAIT_APPROVAL_PAGE)
def approve_table_page(request):
    written_form = FormAwaitingApproval.objects.filter(form_creator=request.user)
    owned_form = FormAwaitingApproval.objects.filter(form_owner=request.user)
    form_awaiting_approval = written_form.union(owned_form)

    return render(request, "dashboard/approve_table_page.html", {
        "forms": form_awaiting_approval,
    })

##############################################################################

from warrant_form.views_reqform import view_form

@perm_req_log(*DashboardPerm.APPROVE_REQFORM)
def reqform_approve_page(request : HttpRequest, req_no_plaintiff : str):
    def handle_form_approved():
        try:
            if settings.ENABLE_API:
                AWISConnectAPI.post_send_req_form("v1.1", request, selected_form.form.toAPICompatibleDict())

            selected_form.approve_status = FormAwaitingApproval.ApprovalStatus.APPROVED
            selected_form.date_approved = timezone.now()
            selected_form.save()

            for warrant in selected_form.form.warrants.all():
                VisualWarrantData.objects.create(
                    warrant=warrant,
                    judge_name=selected_form.form.judge_name,
                )
            
            VisualReqformData.objects.create(
                form=selected_form.form,
                accept=VisualReqformData.AcceptStatus.WAITING,
            )

            FileLogger.createNormalLog(request, AccessType.APPROVE, PermissionList.REQFORM_AWAIT_APPROVAL, selected_form.getLogInfoDict(),)

            return redirect("dashboard:dashboard")
        except Exception as e:
            print(str(e))
            return redirect("dashboard:dashboard")

    def handle_form_rejected():
        selected_form.approve_status = FormAwaitingApproval.ApprovalStatus.REJECTED
        selected_form.save()

        FileLogger.createNormalLog(request, AccessType.REJECT, PermissionList.REQFORM_AWAIT_APPROVAL, selected_form.getLogInfoDict())

        return redirect("dashboard:dashboard")
        
    selected_form = getFormAwaitViaPlaintiff(req_no_plaintiff)

    if request.method == "POST":
        if request.POST.get("confirm_approve") and request.POST.get("confirm_reject"):
            # ไม่ควรเกิดขึ้น หาก Javascript ทำงาน
            return render(request, "errors/400.html", {
                "reason": "ท่านเลือกที่จะอนุมัติและปฎิเสธพร้อมกัน"
            }, status=400)

        if request.POST.get("confirm_approve"):
            return handle_form_approved()
        elif request.POST.get("confirm_reject"):
            return handle_form_rejected()

        else:
            # ไม่ควรเกิดขึ้น หาก input ยังอยู่
            return render(request, "errors/400.html", {
                "reason": "ไม่ได้รับข้อมูลว่าอนุมัติหรือปฏิเสธ"
            }, status=400)
        
    return view_form(request, req_no_plaintiff, selected_html="approve_form_view.html")

@perm_req_log(*DashboardPerm.REJECT_REQFORM)
def confirm_reject(request : HttpRequest, req_no_plaintiff : str):
    selected_form = getFormAwaitViaPlaintiff(req_no_plaintiff)
    if request.method == "POST":
        selected_form.approve_status = FormAwaitingApproval.ApprovalStatus.REJECTED
        selected_form.save()

        FileLogger.createNormalLog(request, AccessType.REJECT, PermissionList.REQFORM_AWAIT_APPROVAL, selected_form.getLogInfoDict())
  
        return redirect(reverse("dashboard:success_page"))
    
    return render(request, "dashboard/confirmation_page.html", {
        "user": request.user,
        "action": "Reject",
        "form": selected_form,
    })


###########################################################################

@perm_req_log(*DashboardPerm.REQFORM_SUBMITTED_PAGE)
def accept_table_page(request):
    form_sent = VisualReqformData.objects.all()

    output_list = []
    for obj in form_sent:
        data_dict = {
            "accept": obj.get_accept_display,
            "accept_date": convert_time(obj.accept_date),
            "req_no_plaintiff": obj.getReqNoPlaintiff(),
            "reqno": obj.getReqNo(),
        }

        output_list.append(data_dict)

    return render(request, "dashboard/accept_table_page.html", {
        "forms_sent": output_list,
    })

@perm_req_log(*DashboardPerm.WARRANT_SUBMITTED_PAGE)
def warrant_status_page(request, req_no_plaintiff : str):

    reqform = getFormAwaitViaPlaintiff(req_no_plaintiff)

    # warrants : list[VisualWarrantData] = VisualWarrantData.objects.filter(warrant_data.reqforms.first().reqno)

    warrants = reqform.form.warrants

    warrants_list = []
    for warrant_data in warrants.all():
        warrant_wrap = VisualWarrantData.objects.filter(warrant=warrant_data).first()

        data_dict = {
            "woa_no_and_year": warrant_data.get_woa_no_and_year(),
            "woa_type": f"{warrant_data.get_woa_type_text()} | {warrant_data.get_fault_type_text()}",
            "woa_refno": warrant_data.woa_refno,

            "court_injunction": warrant_wrap.get_court_injunction_display(), 
            "judge_name": warrant_wrap.judge_name,
            "injunction_date": convert_time(warrant_wrap.injunction_date),
            "file_path": warrant_wrap.file_path,
            "because": warrant_wrap.because,

            "court_injunction_int": warrant_wrap.court_injunction, 
            "req_no_plaintiff": req_no_plaintiff,

            "report_status": warrant_wrap.report_status
        }

        warrants_list.append(data_dict)

    return render(request, "dashboard/warrant_status_page.html", {
        "warrants": warrants_list
    })


#######################################################3
#
# FORM APPROVE SECTION
#

# @permission_required(perm_str(PermissionType.APPROVE, PermissionList.REQFORM_AWAIT_APPROVAL), raise_exception=True)
# def approve_form_page(request : HttpRequest):

#     written_form = FormAwaitingApproval.objects.filter(form_creator=request.user)
#     owned_form = FormAwaitingApproval.objects.filter(form_owner=request.user)
#     form_awaiting_approval = written_form.union(owned_form)

#     return render(request, "dashboard/approve_page.html", {
#         "user": request.user,
#         "forms": form_awaiting_approval,
#     })

@login_required
def success_page(request : HttpRequest):
    return render(request, "dashboard/success_page.html", {
        "user": request.user,
    })

################################################################################

from .forms_report_warrant import ReportWarrantForm
import warrant_form.forms_central as CentralForm

@perm_req_log(*DashboardPerm.CREATE_REPORT_WARRANT_SUBMITTED)
def report_update_warrant_arrest_yet(request : HttpRequest, req_no_plaintiff : str, woa_refno : str):
    selected_form = getFormAwaitViaPlaintiff(req_no_plaintiff)

    target_warrant : WarrantDataModel = selected_form.form.warrants.filter(woa_refno=woa_refno).first()

    current_user : UserDataModel = request.user

    report_form = ReportWarrantForm()

    if not target_warrant:
        raise Http404("ไม่พบข้อมูลดังกล่าว")
    
    context = {
        "court_code": CentralForm.court_codes.getValueOf(selected_form.form.court_code),
        "woa_no": target_warrant.get_woa_no_and_year(),
        "woa_type": target_warrant.get_woa_type_text(),
        "req_num_case_type_id": selected_form.form.get_req_case_type_id_display(),
        "arrest_report_uid": current_user.api_uid
    }

    api_data = {
        "court_code": selected_form.form.court_code,
        "woa_no": target_warrant.woa_no,
        "woa_type": target_warrant.woa_type,
        "woa_year": target_warrant.woa_year,
        "req_num_case_type_id": selected_form.form.req_case_type_id,
        "arrest_report_date": timezone.now().astimezone(timezone.get_current_timezone()).strftime("%Y-%m-%d %H:%M:%S"),
        "arrest_report_uid": current_user.api_uid
    }
    
    if request.method == "POST":
        report_form = ReportWarrantForm(data=request.POST)

        if report_form.is_valid():
            put_data = report_form.cleaned_data
            
            put_data = combine_date(put_data)

            put_data.update(api_data)

            try:
                if settings.ENABLE_API:
                    AWISConnectAPI.put_report_warrant_result("v1.1", request, put_data)
                else:
                    print(put_data)

                warrant_wrapper = VisualWarrantData.objects.filter(warrant=target_warrant).first()

                # Change status to reported.
                warrant_wrapper.report_status = 1
                warrant_wrapper.save()

                return redirect("dashboard:view_reqform_warrants", req_no_plaintiff)

            except:
                return render(request, "errors/500.html", {

                })

    context.update({
        "report_form": report_form,
    })
    
    return render(request, "dashboard/report_warrant.html", context)

@perm_req_log(*DashboardPerm.DELETE_REQFORM_SUBMITTED)
def unsend_reqform(request : HttpRequest, req_no_plaintiff : str):
    sent_form = VisualReqformData.objects.filter(form__req_no_plaintiff=req_no_plaintiff).first()

    unneeded_warrants = sent_form.form.warrants.all()

    warrant_results = VisualWarrantData.objects.filter(warrant__in=unneeded_warrants)

    if sent_form.accept == 1:
        return render(request, "errors/400.html", {
            "reason": "คำร้องดังกล่าวไม่สามารถยกเลิกการส่งได้แล้ว"
        }, status=403)

    if request.method == "POST":
        try:
            if settings.ENABLE_API:
                AWISConnectAPI.unsend_reqform_from_court("v1.1", request, req_no_plaintiff)

            form_await_approval = FormAwaitingApproval.objects.filter(
                form=sent_form.form
            ).first()
            
            form_await_approval.approve_status = FormAwaitingApproval.ApprovalStatus.PENDING

            form_await_approval.save()
            sent_form.delete()
            warrant_results.delete()
                
            return redirect("dashboard:success_page")

        except:
            return JsonResponse({
                "status": "Error",
            })
        
    return render(request, "dashboard/confirmation_page.html", {
        "action": "Unsend Reqform"
    })

###############################################################################

from warrant_form import doc_create

def download_warrant(request : HttpRequest, req_no_plaintiff : str, woa_refno : str):
    selected_form = getFormAwaitViaPlaintiff(req_no_plaintiff)

    target_warrant : WarrantDataModel = selected_form.form.warrants.filter(woa_refno=woa_refno).first()

    doc_data = target_warrant.convertToDocumentData()

    response = doc_create.create_pdf(doc_data)

    return response


###############################################################################

def combine_date(put_data : dict):
    day = put_data.get("arrest_date_day")
    month = put_data.get("arrest_date_month")
    year = put_data.get("arrest_date_year")

    put_data.update({
        "arrest_date": f"{year}-{month}-{day}"
    })
    
    put_data.pop("arrest_date_day")
    put_data.pop("arrest_date_month")
    put_data.pop("arrest_date_year")

    return put_data

def convert_time(datetime_obj : datetime):
    if datetime_obj:
        return datetime_obj
    else:
        return f"-"