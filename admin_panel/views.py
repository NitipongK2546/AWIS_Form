from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, JsonResponse
from admin_panel.forms import CustomizedUserCreationForm

from awis_custom_settings.settings import RoleChoices

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User, Group

from users.models import UserDataModel

from users.permissions.perms import PermissionList, PermissionType, perm_str

import requests
from users.models import UserAccess
import os

FORBIDDEN_MSG = JsonResponse({
                "status": "403",
                "message": "forbidden",
            }, status=403
            )

# VIEWS

@permission_required(perm_str(PermissionType.VIEW, PermissionList.ADMIN_PANEL), raise_exception=True)
def collections(request : HttpRequest):
    if not request.user.is_staff:
        return FORBIDDEN_MSG

    return render(request, "admin_panel/collections.html")

@permission_required(perm_str(PermissionType.CREATE, PermissionList.ADMIN_PANEL), raise_exception=True)
def signup(request : HttpRequest):
    if not request.user.is_staff:
        return FORBIDDEN_MSG

    if request.method == "POST":
        form = CustomizedUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user_obj : User = form.save(commit=False)

                data = form.cleaned_data
                selected_role = data.get("role")

                choices = dict(RoleChoices.choices)
                selected_role_string = choices.get(int(selected_role))

                # print(choices)
                # print(selected_role)
                # print(selected_role_string)

                selected_group = Group.objects.get(name=selected_role_string)

                # print(selected_group)

                user_obj.is_active = False
                user_obj.save()

                user_obj.groups.add(selected_group)
                UserDataModel.objects.create(user=user_obj, role=selected_role,)

                return redirect("admin_panel:collections")
            except Exception as e:
                raise Exception(e)
    else:
        form = CustomizedUserCreationForm()
    return render(request, "admin_panel/signup.html", {"form": form})

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

@permission_required(perm_str(PermissionType.CREATE, PermissionList.ADMIN_PANEL), raise_exception=True)
def admin_select_users(request):
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

def add_user_to_access(user_data):
    uid = user_data["USR_ID"]
    if not UserAccess.objects.filter(user_id=uid).exists():
        UserAccess.objects.create(
            user_id=uid,
            username=f"{user_data['USR_PREFIX']}{user_data['USR_FNAME']}",
            fullname=f"{user_data['USR_PREFIX']}{user_data['USR_FNAME']} {user_data['USR_LNAME']}",
            department=user_data["Dept"]
        )
        return True
    return False

def add_specific_user(request: HttpRequest):
    user_data = {
        "USR_ID": 9644,
        "USR_PREFIX": "นาย",
        "USR_FNAME": "ชลสิทธิ์",
        "USR_LNAME": "มูลคร",
        "Dept": "ฝ่ายเทคโนโลยีดิจิทัล",
        "Position": "เจ้าหน้าที่พัฒนาโปรแกรม",
    }

    added = add_user_to_access(user_data)

    if added:
        return redirect("admin_panel:access_list")
    else:
        return redirect("admin_panel:access_list")

def access_list(request):
    # ดึงข้อมูลทั้งหมดจาก UserAccess
    allowed_users = UserAccess.objects.all()

    return render(request, "admin_panel/access_list.html", {
        "allowed_users": allowed_users
    })
    
def update_role(request, user_id, role_value):
    user = get_object_or_404(UserAccess, user_id=user_id)
    if int(role_value) in [choice[0] for choice in RoleChoices.choices]:
        user.role = int(role_value)
        user.save()
    return redirect("admin_panel:access_list")

def delete_access(request, user_id):
    user = get_object_or_404(UserAccess, user_id=user_id)
    user.delete()
    return redirect("admin_panel:access_list")