from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission

# permission_view, success = Permission.objects.get_or_create(
#     codename='',
#     content_type=ct
# )

# permission_add, success = Permission.objects.get_or_create(
#     codename='can_add_visual_form_approval_data',
#     content_type=ct
# )

# permission_update, success = Permission.objects.get_or_create(
#     codename='can_change_visual_form_approval_data',
#     content_type=ct
# )

# permission_delete, success = Permission.objects.get_or_create(
#     codename='can_delete_visual_form_approval_data',
#     content_type=ct
# )

# permission_approve, success = Permission.objects.get_or_create(
#     codename='can_approve_visual_form_approval_data',
#     content_type=ct
# )