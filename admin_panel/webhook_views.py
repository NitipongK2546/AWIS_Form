from api.models import APISecret
from django.http import HttpRequest
from django.shortcuts import render, redirect

from users.permissions import perm_str, PermissionList, PermissionType

def api_secret_page(request : HttpRequest):

    request.session.pop("api_key", "")

    all_api_keys = APISecret.objects.all()

    context = {
        "api_keys": all_api_keys
    }

    if request.method == "POST":
        api_key = APISecret.createAPIKey(request, {
            "name": "delete_user_access",
            "reason": "Delete UserAccess via Webhook",
            "permission": [
                perm_str(PermissionType.DELETE, PermissionList.USER_ACCESS)
            ]
        })

        context.update({
            "api_key": api_key
        })

        request.session.update({
            "api_key": api_key
        })

        return redirect("admin_panel:create_api_secret")
        

    return render(request, "api_page/api_page.html", context)


def generate_api_secret(request : HttpRequest):
    return render(request, "api_page/api_key_page.html", {
        "api_key": request.session.get("api_key", "No API Key, Error.")
    })