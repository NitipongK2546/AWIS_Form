from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, JsonResponse

from awis_custom_settings.settings import RoleChoices, RoleList

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User, Group

from users.models import UserDataModel

import _log_utils.file_logger as FileLogger
from _log_utils.file_logger import AccessType

from users.permissions.perms import PermissionList, PermissionType, perm_str, perm_str_list

from users.permissions.decorators import perm_req_log

import requests
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

# @permission_required(perm_str(PermissionType.CREATE, PermissionList.ADMIN_PANEL), raise_exception=True)
# def signup(request : HttpRequest):
#     if not request.user.is_staff:
#         return FORBIDDEN_MSG

#     if request.method == "POST":
#         form = CustomizedUserCreationForm(request.POST)
#         if form.is_valid():
#             try:
#                 user_obj : User = form.save(commit=False)

#                 data = form.cleaned_data
#                 selected_role = data.get("role")

#                 choices = dict(RoleChoices.choices)
#                 selected_role_string = choices.get(int(selected_role))

#                 # print(choices)
#                 # print(selected_role)
#                 # print(selected_role_string)

#                 selected_group = Group.objects.get(name=selected_role_string)

#                 # print(selected_group)

#                 user_obj.is_active = False
#                 user_obj.save()

#                 user_obj.groups.add(selected_group)
#                 UserDataModel.objects.create(user=user_obj, role=selected_role,)

#                 return redirect("admin_panel:collections")
#             except Exception as e:
#                 raise Exception(e)
#     else:
#         form = CustomizedUserCreationForm()
#     return render(request, "admin_panel/signup.html", {"form": form})

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
        response = requests.get(ORG_API_FETCH_USERS)
        users = response.json()

        if request.method == "POST":
            selected_ids = request.POST.getlist("selected_users")
            for uid in selected_ids:
                user_data = next((u for u in users if str(u["USR_ID"]) == uid), None)
                if user_data and not UserAccess.objects.filter(user_id=uid).exists():
                    UserAccess.objects.create(
                        user_id=user_data["USR_ID"],
                        username=f"{user_data['USR_PREFIX']}{user_data['USR_FNAME']}",
                        fullname=f"{user_data['USR_PREFIX']}{user_data['USR_FNAME']} {user_data['USR_LNAME']}",
                        department=user_data["Dept"]
                    )
            return redirect("admin_panel:access_list")

        return render(request, "admin_panel/select_users.html", {"users": users})
    except Exception as e:
        FileLogger.createErrorLog(request, AccessType.CREATE, PermissionList.USER_ACCESS, {
            "message": str(e)
        })

################################################################################

def add_user_to_access(user_data : dict):
    uid = user_data["USR_ID"]
    if not UserAccess.objects.filter(user_id=uid).exists():
        UserAccess.objects.create(
            user_id=uid,
            username=f"{user_data['USR_PREFIX']}{user_data['USR_FNAME']}",
            fullname=f"{user_data['USR_PREFIX']}{user_data['USR_FNAME']} {user_data['USR_LNAME']}",
            department=user_data["Dept"]
        )

        user = UserDataModel.objects.create_user(
            username=f"{user_data['USR_PREFIX']}{user_data['USR_FNAME']}",
            api_uid=user_data['USR_ID'],
            first_name=user_data['USR_FNAME'],
            last_name=user_data['USR_LNAME'],
        )

        group_name = RoleList.getDefaultRoleValue()
        group = Group.objects.get(name=group_name)

        user.groups.add(group)

        user.set_unusable_password()
        user.save()

        return True
    return False

@perm_req_log([PermissionType.CREATE], PermissionList.USER_ACCESS, AccessType.CREATE)
def add_specific_user(request: HttpRequest):
    user_data = {
        "USR_ID": int(os.getenv("TEST_ID")),
        "USR_PREFIX": os.getenv("TEST_PREFIX"),
        "USR_FNAME": os.getenv("TEST_FNAME"),
        "USR_LNAME": os.getenv("TEST_LNAME"),
        "Dept": os.getenv("TEST_DEPT"),
        "Position": os.getenv("TEST_POSITION"),
    }

    added = add_user_to_access(user_data)

    if added:
        return redirect("admin_panel:access_list")
    else:
        return redirect("admin_panel:access_list")

##############################################################################

@perm_req_log([PermissionType.VIEW], PermissionList.USER_ACCESS, AccessType.VIEW)
def access_list(request):
    # ดึงข้อมูลทั้งหมดจาก UserAccess
    allowed_users = UserAccess.objects.all()

    return render(request, "admin_panel/access_list.html", {
        "allowed_users": allowed_users
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


# @perm_req_log([PermissionType.VIEW], PermissionList.ADMIN_PANEL, AccessType.VIEW)
# def view_all_logs(request : HttpRequest):
#     filter = request.GET
#     query_form = LogQuery(data=filter)

#     logs = FileLogger.getOrFilterLogs(filter)

#     return render(request, "admin_panel/log_list.html", {
#         "normal_logs": logs.get("normal"),
#         "errors_logs": logs.get("errors"),
#         "denied_logs": logs.get("denied"),
#         "query": query_form,
#     })

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