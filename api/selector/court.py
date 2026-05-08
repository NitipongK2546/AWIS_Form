from api.models import ExternalSelectorData
from _request_utils.connect_api import get_court_list as _api_get_court_list

import hashlib
import json

def _fetchCourtAndCreateHash():
    try:
        court_list = _api_get_court_list("v1")
        court_list_str = json.dumps(court_list).encode()
        hash_obj = hashlib.sha1(court_list_str)
        hash_hex_str = hash_obj.hexdigest()
    except:
        return None, None

    return court_list, hash_hex_str

def checkCourtDifferent():
    court_list, hash_hex_str = _fetchCourtAndCreateHash()

    court_data_obj = ExternalSelectorData.objects.filter(name="court_list").first()

    if not hash_hex_str:
        return "ERROR"

    if not court_data_obj:
        return True

    if court_data_obj.isHashDifferent(hash_hex_str):
        return True

    return False

def replaceCourtData(court_selector : ExternalSelectorData, hash_hex_str : str ,court_list : dict):
    court_selector.replaceData({
        "hash_hex_str": hash_hex_str,
        "data": court_list,
    })
    

def getCourtData():
    court_data_obj = ExternalSelectorData.objects.filter(name="court_list").first()

    if not court_data_obj:
        court_list, hash_hex_str = _fetchCourtAndCreateHash()
        
        new_court_data_obj = ExternalSelectorData.objects.create(**{
            "name": "court_list",
            "hash_hex_str": hash_hex_str,
            "data": court_list,
        })
    
        return new_court_data_obj.data
    
    return court_data_obj.data
    