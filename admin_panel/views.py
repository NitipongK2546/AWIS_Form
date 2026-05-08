from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, JsonResponse, HttpResponseForbidden

from awis_custom_settings.settings import RoleChoices, RoleList

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User, Group

from users.models import UserDataModel

import _log_utils.file_logger as FileLogger
from _log_utils.file_logger import AccessType

from users.permissions.perms import PermissionList, PermissionType, perm_str, perm_str_list

from users.permissions.decorators import perm_req_log

import requests
from requests.exceptions import ConnectionError

from users.models import UserAccess
import os

FORBIDDEN_MSG = JsonResponse({
                "status": "403",
                "message": "forbidden",
            }, status=403
            )

# VIEWS

@perm_req_log([PermissionType.VIEW], PermissionList.ADMIN_PANEL, AccessType.VIEW)
def collections(request : HttpRequest):
    if not request.user.is_staff:
        return FORBIDDEN_MSG
    
    FileLogger.createNormalLog(request, AccessType.VIEW, PermissionList.ADMIN_PANEL,)

    return render(request, "admin_panel/collections.html")


def check_all_users(request : HttpRequest):
    all_users = UserDataModel.objects.all()

    user_display_list = [
        {
            "id": user.pk, 
            "full_name": user.get_full_name(), 
            "group_perm": user.groups.all() if not user.is_superuser else "SUPERUSER",
            "user_perm": user.get_user_permissions() if not user.is_superuser else "SUPERUSER",
        }
        for user in all_users
    ]

    return render(request, "admin_panel/user_list.html", {
        "user_list": user_display_list
    })

ORG_API_FETCH_USERS = os.getenv("ORG_API_FETCH_USERS")

@perm_req_log([PermissionType.CREATE], PermissionList.ADMIN_PANEL, AccessType.CREATE)
def admin_select_users(request : HttpRequest):
    try:
        response = requests.get(ORG_API_FETCH_USERS, timeout=5)
        users = response.json()

        if request.method == "POST":
            selected_ids = request.POST.getlist("selected_users")
            for uid in selected_ids:
                user_data = next((u for u in users if str(u["USR_ID"]) == uid), None)
                if user_data and not UserAccess.objects.filter(user_id=uid).exists():
                    add_user_to_access(user_data)
            return render(request, "admin_panel/success.html", {
                "status": "success"
            })

        
        dept_filter = request.GET.get("dept")
        position_filter = request.GET.get("position")
        id_filter = request.GET.get("id")
        name_filter = request.GET.get("name")
        
        if dept_filter: 
            users = [u for u in users if dept_filter.lower() in u["Dept"].lower()]
        
        if position_filter:
            users = [u for u in users if position_filter.lower() in u["Position"].lower()]
        
        if id_filter:
            users = [u for u in users if str(u.get("USR_ID", "")).startswith(id_filter)]

        if name_filter:
            full_name = lambda u: f"{u.get('USR_PREFIX','')}{u.get('USR_FNAME','')} {u.get('USR_LNAME','')}"
            users = [u for u in users if name_filter.lower() in full_name(u).lower()]
            
        return render(request, "admin_panel/select_users.html", {"users": users})
    except ConnectionError:
        return render(request, "admin_panel/select_users.html", {
            "users": {},
            "connect_error": True,
        })

    except Exception as e:
        FileLogger.createErrorLog(request, AccessType.CREATE, PermissionList.USER_ACCESS, {
            "message": str(e)
        })
        return render(request, "admin_panel/select_users.html", {
            "users": {},
            "error": str(e),
        })

################################################################################

def add_user_to_access(user_data : dict, is_sys_admin : bool = False):
    uid = user_data["USR_ID"]
    if not UserAccess.objects.filter(user_id=uid).exists():
        new_user_access = UserAccess.objects.create(
            user_id=uid,
            username=f"{user_data['USR_PREFIX']}{user_data['USR_FNAME']}",
            fullname=f"{user_data['USR_PREFIX']}{user_data['USR_FNAME']} {user_data['USR_LNAME']}",
            department=user_data["Dept"]
        )
        if is_sys_admin:
            new_user_access.role = 99
            new_user_access.save()

        user = UserDataModel.objects.filter(
            username=f"{user_data['USR_PREFIX']}{user_data['USR_FNAME']}"
        ).first()

        if not user:
            new_user = UserDataModel.objects.create_user(
                username=f"{user_data['USR_PREFIX']}{user_data['USR_FNAME']}",
                api_uid=user_data['USR_ID'],
                first_name=user_data['USR_FNAME'],
                last_name=user_data['USR_LNAME'],
            )

            if is_sys_admin:
                group_name = RoleList.getSystemAdminRoleValue()
            else:
                group_name = RoleList.getDefaultRoleValue()

            group = Group.objects.get(name=group_name)

            new_user.groups.add(group)
            

            new_user.set_unusable_password()
            new_user.save()

        return True
    return False

##############################################################################

@perm_req_log([PermissionType.VIEW], PermissionList.USER_ACCESS, AccessType.VIEW)
def access_list(request : HttpRequest):
    # ดึงข้อมูลทั้งหมดจาก UserAccess
    allowed_users = UserAccess.objects.all()

    current_user_access = UserAccess.objects.filter(user_id=request.user.api_uid).first()
    current_user_model = request.user

    return render(request, "admin_panel/access_list.html", {
        "allowed_users": allowed_users,
        "user_access": current_user_access,
        "user_model": current_user_model,
    })

@perm_req_log([PermissionType.EDIT], PermissionList.USER_ROLE, AccessType.EDIT)
def update_role(request, user_id, role_value):
    user : UserAccess = get_object_or_404(UserAccess, user_id=user_id)
    django_user : UserDataModel = UserDataModel.objects.filter(api_uid=user_id).first()
    if int(role_value) in [choice[0] for choice in RoleChoices.choices]:
        user.role = int(role_value)

        group_name = user.get_role_display()
        group = Group.objects.get(name=group_name)

        django_user.groups.clear()
        django_user.groups.add(group)
        
        user.save()
        django_user.save()

        FileLogger.createNormalLog(request, AccessType.EDIT, PermissionList.USER_ROLE, django_user.getLogInfoDict())

    return redirect("admin_panel:access_list")

@perm_req_log([PermissionType.EDIT], PermissionList.ADMIN_ROLE, AccessType.EDIT)
def update_role_admin(request : HttpRequest, user_id, role_value):

    current_user = UserAccess.objects.filter(user_id=request.user.api_uid).first()
    current_user_model = request.user
    # System Admin or not Superuser
    # Here's hoping that me not writing a util function for something like this won't come to bite me later.
    # But really, how long would it take for someone to read this code again?
    # Haha.
    if current_user and (not current_user_model.is_superuser) and current_user.role != 99:
        return render(request, "errors/403.html", {
            "error": "Not Superuser or System Admin"
        })
    
    user : UserAccess = get_object_or_404(UserAccess, user_id=user_id)
    django_user : UserDataModel = UserDataModel.objects.filter(api_uid=user_id).first()
    if int(role_value) in [choice[0] for choice in RoleChoices.choices]:
        user.role = int(role_value)

        group_name = user.get_role_display()
        group = Group.objects.get(name=group_name)

        django_user.groups.clear()
        django_user.groups.add(group)
        
        user.save()
        django_user.save()

        FileLogger.createNormalLog(request, AccessType.EDIT, PermissionList.USER_ROLE, django_user.getLogInfoDict())

    return redirect("admin_panel:access_list")

@perm_req_log([PermissionType.DELETE], PermissionList.USER_ACCESS, AccessType.DELETE)
def delete_access(request, user_id):
    user = get_object_or_404(UserAccess, user_id=user_id)
    user.delete()

    # FileLogger.createNormalLogRequest(request, AccessType.DELETE, PermissionList.ADMIN_PANEL,)

    return redirect("admin_panel:access_list")

####################################################################

from .forms import LogQuery
from django.core.paginator import Paginator

@perm_req_log([PermissionType.VIEW], PermissionList.LOG_ACCESS, AccessType.VIEW)
def view_all_logs(request: HttpRequest):
    filter = request.GET
    query_form = LogQuery(data=filter)

    logs = FileLogger.getOrFilterLogs(filter)

    # Paginate each category separately
    normal_logs = logs.get("normal", [])
    errors_logs = logs.get("errors", [])
    denied_logs = logs.get("denied", [])

    # Get page numbers for each category (different query params)
    normal_page_number = request.GET.get("normal_page")
    errors_page_number = request.GET.get("errors_page")
    denied_page_number = request.GET.get("denied_page")

    normal_paginator = Paginator(normal_logs, 20)
    errors_paginator = Paginator(errors_logs, 20)
    denied_paginator = Paginator(denied_logs, 20)

    normal_page_obj = normal_paginator.get_page(normal_page_number)
    errors_page_obj = errors_paginator.get_page(errors_page_number)
    denied_page_obj = denied_paginator.get_page(denied_page_number)

    return render(request, "admin_panel/log_list.html", {
        "normal_page_obj": normal_page_obj,
        "errors_page_obj": errors_page_obj,
        "denied_page_obj": denied_page_obj,
        "query": query_form,
    })

@perm_req_log([PermissionType.CREATE], PermissionList.LOG_ACCESS, AccessType.CREATE)
def export_logs(request : HttpRequest):
    if request.method == "POST":
        FileLogger.exportLogAsFile()

        return redirect("admin_panel:view_logs")
    
    return render(request, "admin_panel/confirm_export_log.html", {
        "action": "Export Log"
    })

def delete_logs(request : HttpRequest):
    filter = request.GET

    if request.method == "POST":
        FileLogger.deleteLogViaFilter(filter)

        return redirect("admin_panel:view_logs")

    return render(request, "admin_panel/confirm_export_log.html", {
        "action": "Delete Log"
    })

from api.selector import court as CourtUtil
from .models import SelectedCourt

def edit_selected_courts(request : HttpRequest):
    court_list : list[dict] = CourtUtil.getCourtData().get("courts")

    if request.method == "POST":
        selected_codes = request.POST.getlist("selected_courts")

        for court in court_list:
            if len(selected_codes) == 0:
                break

            current_code = court.get("court_code") 
            if current_code in selected_codes:
                SelectedCourt.objects.get_or_create(
                    data=court
                )
                selected_codes.remove(current_code)

        return JsonResponse({
            "message": "Success"
        })


    return render(request, "module/court_table.html", {
        "court_list": court_list,
    })

def view_all_selected_courts(request : HttpRequest):
    all_selected_courts = SelectedCourt.objects.all()

    return render(request, "admin_panel/selected_court_list.html", {
        "court_list": all_selected_courts,
    })
