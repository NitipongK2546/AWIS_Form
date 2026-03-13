import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project_awis.settings")

django.setup()

###############################################################################

import _scripts.create_superuser as create_superuser
import _scripts._permissions.full_setup_group_perm 

create_superuser.create_superuser()

###############################################################################