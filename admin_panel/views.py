from django.shortcuts import render, redirect
from django.http import HttpRequest, JsonResponse
from admin_panel.forms import CustomizedUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group

from users.models import UserDataModel

FORBIDDEN_MSG = JsonResponse({
                "status": "403",
                "message": "forbidden",
            }, status=403
            )

# VIEWS

@login_required(login_url="/users/login/")
def collections(request : HttpRequest):
    if not request.user.is_superuser:
        return FORBIDDEN_MSG

    return render(request, "admin_panel/collections.html")

role_dict = {
    "0": "Employee",
    "1": "Manager",
    "2": "Director",
    "99": "System Admin",
}

@login_required(login_url="/users/login/")
def signup(request : HttpRequest):
    if not request.user.is_superuser:
        return FORBIDDEN_MSG

    if request.method == "POST":
        form = CustomizedUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user_obj : User = form.save(commit=False)

                data = form.cleaned_data
                selected_role = data.get("role")

                choices = dict(CustomizedUserCreationForm.RoleChoices.choices)
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

# def check_all_users(request : HttpRequest):
#     user_list = User.objects.all()

