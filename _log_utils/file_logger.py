import os
from enum import Enum

from users.models import LogSystem, UserDataModel
from django.utils import timezone
from users.permissions import PermissionList

from django.http import HttpRequest

LOG_DIR = "_log_output/"
ALL_LOG_NAME = "all_access_log.txt"

NORMAL_LOG = "access_log.txt"
ERROR_LOG = "error_log.txt"
ACCESS_DENIED_LOG = "access_denied_log.txt"

class AccessType(Enum):
    VIEW = "View"
    CREATE = "Create"
    EDIT = "Edit"
    DELETE = "Delete"
    APPROVE = "Approve"
    REJECT = "Reject"
    LOGIN = "Login"

os.makedirs(LOG_DIR, exist_ok=True)

def exportLogAsFile(filename : str = ALL_LOG_NAME):
    all_logs = list(LogSystem.objects.all())

    with open(LOG_DIR + filename, mode="w", encoding="utf-8") as file:
        for log in all_logs:
            user_obj : UserDataModel = UserDataModel.objects.get(api_uid=log.user_id)
            file.write(f"[{log.time_logged.astimezone(timezone.get_current_timezone())}]: {user_obj.username} ({user_obj.first_name} {user_obj.last_name}) {log.action} the {log.system}\n")

def getUserLog(user_id : int):
    all_logs = LogSystem.objects.filter(user_id=user_id)

    return all_logs

#############################################################################

def _createLog(request : HttpRequest, action : AccessType, system : PermissionList, relevant_info = None, remark : str = None, filename : str = ERROR_LOG, ) -> LogSystem:
    if relevant_info:
        if not isinstance(relevant_info, list):
            if isinstance(relevant_info, str):
                relevant_info = [relevant_info]
            else:
                relevant_info = list(relevant_info)

        relevant_info_str : list[str] = [str(info) for info in relevant_info]
    else:
        relevant_info_str = []
    
    user : UserDataModel = request.user
    user_id = user.api_uid

    time_logged : timezone.datetime = timezone.now()
    log_obj = LogSystem.objects.create(user_id=user_id, action=action.value, system=system.value, time_logged=time_logged, relevant_info=relevant_info_str)

    return log_obj  

########################################################################

def createNormalLog(request : HttpRequest, action : AccessType, system : PermissionList, access_info : list = None, remark : str = None,):
    
    log_obj = _createLog(request, action, system, access_info, remark, NORMAL_LOG,)

    with open(LOG_DIR + NORMAL_LOG, mode="a", encoding="utf-8") as file:
        prepared_text = log_obj.toStrExtra()
        if remark:
            prepared_text = prepared_text + f" ({remark})"

        file.write(f"{prepared_text}\n")

    return log_obj 

def createAccessDeniedLog(request : HttpRequest, action : AccessType, system : PermissionList, denied_reason : list = None, remark : str = None,):

    log_obj = _createLog(request, action, system, denied_reason, remark, NORMAL_LOG,)

    with open(LOG_DIR + ACCESS_DENIED_LOG, mode="a", encoding="utf-8") as file:
        prepared_text = log_obj.toStrFailed("ACCESS DENIED")
        if remark:
            prepared_text = prepared_text + f" ({remark})"

        file.write(f"{prepared_text}\n")

    return log_obj  
    

def createErrorLog(request : HttpRequest, action : AccessType, system : PermissionList, error_reason : list = None, remark : str = None,):

    log_obj = _createLog(request, action, system, error_reason, remark, NORMAL_LOG,)

    with open(LOG_DIR + ERROR_LOG, mode="a", encoding="utf-8") as file:
        prepared_text = log_obj.toStrFailed("ERROR")
        if remark:
            prepared_text = prepared_text + f" ({remark})"

        file.write(f"{prepared_text}\n")

    return log_obj
    
