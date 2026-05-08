from admin_panel.views import add_user_to_access

import os
from dotenv import load_dotenv

load_dotenv()

def add_initial_admin_user():
    user_data = {
        "USR_ID": int(os.getenv("INIT_ADMIN_ID")),
        "USR_PREFIX": os.getenv("INIT_ADMIN_PREFIX"),
        "USR_FNAME": os.getenv("INIT_ADMIN_FNAME"),
        "USR_LNAME": os.getenv("INIT_ADMIN_LNAME"),
        "Dept": os.getenv("INIT_ADMIN_DEPT"),
        "Position": os.getenv("INIT_ADMIN_POSITION"),
    }

    result = add_user_to_access(user_data, True)

    print("System Admin Setup Success.")

print("[Create Initial User as System Admin]")
add_initial_admin_user()