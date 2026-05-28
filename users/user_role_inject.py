from django.http import HttpRequest

def inject_user_role(request : HttpRequest):
    current_role = request.user.groups.first()
    if current_role:
        current_role = current_role.name
    elif request.user.is_superuser:
        current_role = "SUPERUSER"
    else:
        current_role = "ERROR: NO ROLE/GROUP ASSIGNED."

    return {
        "user_role": current_role
    }