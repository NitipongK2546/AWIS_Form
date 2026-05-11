import users.models as UserCreation

import os
from dotenv import load_dotenv
load_dotenv()

print("[Special User Creation]")

email = os.getenv("SUPERUSER_EMAIL")
password = os.getenv("SUPERUSER_PASSWORD")

if email and password:
    UserCreation.create_superuser(**{
        "email": email,
        "password": password
    })

######################################################################

# UserCreation.create_court_user(
#     "testcourtuser7", "court@example.com", "testpass999999", "CourtUser", "Court"
# )