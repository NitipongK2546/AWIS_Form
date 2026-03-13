import os
import django
from django.contrib.contenttypes.models import ContentType
from dashboard.models import VisualReqformData, FormAwaitingApproval
from django.contrib.auth.models import Group, Permission

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_awis.settings")
django.setup()