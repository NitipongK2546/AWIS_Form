import os
from enum import Enum
from django.db.models import TextChoices
from django.core.exceptions import ValidationError

from users.models import LogSystem, UserDataModel
from django.utils import timezone
from users.permissions import PermissionList

from django.http import HttpRequest
from django.contrib.auth.models import AnonymousUser

from django.http import QueryDict

from urllib import parse

LOG_DIR = "_log_output/"

EXPORT_LOG_DIR = "exported/"

NORMAL_LOG = "access_log.txt"
ERROR_LOG = "error_log.txt"
ACCESS_DENIED_LOG = "access_denied_log.txt"

class AccessType(TextChoices):
    VIEW = "View"
    CREATE = "Create"
    EDIT = "Edit"
    DELETE = "Delete"
    APPROVE = "Approve"
    REJECT = "Reject"
    LOGIN = "Login"

os.makedirs(LOG_DIR, exist_ok=True)

def exportLogAsFile(export_dir : str = EXPORT_LOG_DIR):
    all_logs = getOrFilterLogs(as_text=True)
    os.makedirs(LOG_DIR + export_dir, exist_ok=True)

    with open(LOG_DIR + export_dir + NORMAL_LOG, mode="w", encoding="utf-8") as file:
        prepared_text = all_logs.get("normal")
        for line in prepared_text:
            file.write(f"{line}\n")

    with open(LOG_DIR + export_dir + ACCESS_DENIED_LOG, mode="w", encoding="utf-8") as file:
        prepared_text = all_logs.get("denied")
        for line in prepared_text:
            file.write(f"{line}\n")

    with open(LOG_DIR + export_dir + ERROR_LOG, mode="w", encoding="utf-8") as file:
        prepared_text = all_logs.get("errors")
        for line in prepared_text:
            file.write(f"{line}\n")

def getCleanedFilter(query : QueryDict):
    def cleanQuery():
        allowed_keys = ["action", "user_id"]
        for key in query:
            if not any(query.get(key)):
                continue
            
            if key == "reqno":
                filter.update({f"relevant_info__form__reqno": query.getlist(key),})
            elif key in allowed_keys:
                filter.update({f"{key}__in": query.getlist(key)})

    def cleanDate():
        start_obj = None
        end_obj = None
        try:
            if query.get("start_year") and query.get("start_month") and query.get("start_day"):
                start_obj = timezone.datetime(
                    int(query.get("start_year")), int(query.get("start_month")), int(query.get("start_day")), tzinfo=timezone.get_current_timezone()
                )
            if query.get("end_year") and query.get("end_month") and query.get("end_day"):
                end_obj = timezone.datetime(
                    int(query.get("end_year")),  int(query.get("end_month")), (int(query.get("end_day")) + 1),
                    tzinfo=timezone.get_current_timezone()
            )
            if start_obj and end_obj:
                if start_obj > end_obj:
                    raise ValidationError("Start Date is after the End Date")
                
                filter.update({
                    "time_logged__range": (start_obj, end_obj),
                })

        except Exception as e:
            print(e)

    filter = {}

    cleanQuery()
    cleanDate()

    return filter

def deleteLogViaFilter(query : QueryDict = {}):
    filter = getCleanedFilter(query)

    queried_log = LogSystem.objects.filter(
        **filter
    )

    queried_log.delete()

def getOrFilterLogs(query : QueryDict = {}, as_text : bool = False):
    filter = getCleanedFilter(query)

    # print(filter)

    queried_log = LogSystem.objects.filter(
        **filter
    )

    log_collections : dict[str, list] = {
        "normal": [],
        "errors": [],
        "denied": [],
    }

    for log in queried_log:
        if not as_text:
            user_obj = UserDataModel.objects.filter(api_uid=log.user_id).first()

            data_dict = {
                "time_logged": log.time_logged,
                "user_id": log.user_id,
                "username": user_obj.username,
                "fullname": f"{user_obj.first_name} {user_obj.last_name}",
                "action": log.action,
                "system": log.system,
                "relevant_info": log.getRelevantDataObj(log.type),
                "url_path": parse.unquote(log.url_path),
                "remark": log.remark,
            }

            log_collections[log.type].append(data_dict)
        else:
            log_collections[log.type].append((log.toStrType(log.type, True)))

    return log_collections


def getUserLog(user_id : int):
    all_logs = LogSystem.objects.filter(user_id=user_id)

    return all_logs

#############################################################################

def _createLog(request : HttpRequest, action : AccessType, system : PermissionList, type : str, relevant_info : dict = None, remark : str = None, filename : str = ERROR_LOG, user_bypass : UserDataModel = None) -> LogSystem:
    # if relevant_info:
    #     if not isinstance(relevant_info, list):
    #         if isinstance(relevant_info, str):
    #             relevant_info = [relevant_info]
    #         else:
    #             relevant_info = list(relevant_info)

    #     relevant_info_str : list[str] = [info for info in relevant_info]
    # else:
    #     relevant_info_str = []
    if not relevant_info:
        relevant_info = {}
    
    if isinstance(request.user, AnonymousUser):
        if user_bypass:
            user : UserDataModel = user_bypass
        else:
            user = None
    else:
        user : UserDataModel = request.user

    user_id = user.api_uid

    time_logged : timezone.datetime = timezone.now()
    log_obj = LogSystem.objects.create(
        user_id=user_id, action=action.value, system=system.value, time_logged=time_logged, relevant_info=relevant_info, 
        type=type, url_path=request.get_full_path(), remark=remark
    )

    return log_obj  

########################################################################

def createNormalLog(request : HttpRequest, action : AccessType, system : PermissionList, access_info : dict = None, remark : str = None, user_bypass : UserDataModel = None):
    
    log_obj = _createLog(request, action, system, "normal", access_info, remark, NORMAL_LOG, user_bypass)

    with open(LOG_DIR + NORMAL_LOG, mode="a", encoding="utf-8") as file:
        prepared_text = str(log_obj)
        if remark:
            prepared_text = prepared_text + f" ({remark})"

        file.write(f"{prepared_text}\n")

    return log_obj 

def createAccessDeniedLog(request : HttpRequest, action : AccessType, system : PermissionList, denied_reason : dict = None, remark : str = None, user_bypass : UserDataModel = None):

    log_obj = _createLog(request, action, system, "denied", denied_reason, remark, NORMAL_LOG, user_bypass)

    with open(LOG_DIR + ACCESS_DENIED_LOG, mode="a", encoding="utf-8") as file:
        prepared_text = str(log_obj)
        if remark:
            prepared_text = prepared_text + f" ({remark})"

        file.write(f"{prepared_text}\n")

    return log_obj  
    

def createErrorLog(request : HttpRequest, action : AccessType, system : PermissionList, error_reason : dict = None, remark : str = None, user_bypass : UserDataModel = None):

    log_obj = _createLog(request, action, system, "errors", error_reason, remark, NORMAL_LOG, user_bypass)

    with open(LOG_DIR + ERROR_LOG, mode="a", encoding="utf-8") as file:
        prepared_text = log_obj.toStrFailed("ERROR",)
        if remark:
            prepared_text = prepared_text + f" ({remark})"

        file.write(f"{prepared_text}\n")

    return log_obj
    
