from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from dashboard.models import FormApprovalDataContainer

new_group, created = Group.objects.get_or_create(name='Employee')
ct = ContentType.objects.get_for_model(FormApprovalDataContainer)

permission = Permission.objects.get_or_create(
    codename='can_approve_form',
    name='Can add project',                               
    content_type=ct
)

new_group.permissions.add(permission)