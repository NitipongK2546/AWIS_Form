from django.http import HttpRequest, JsonResponse

from api import check_utils as UtilsHandle

# V1 ENDPOINTS

def update_status_req_warrant(request : HttpRequest) -> JsonResponse:
    if request.method != "PUT":
        # Wrong request method.
        return JsonResponse({
            "status": 405,
            "message": "Wrong Request Method"
        }, status=405)

    data = UtilsHandle.json_retrieval(request)

    # Failed.
    if isinstance(data, JsonResponse):
        return data
    
    # Data confirm to be dictionary.   
    # Sample
    # {
    #     "req_no_plaintiff": "123456789",
    #     "recive_date": "2006-01-02T00:00:00",
    #     "reqno": "จ.1/2569",
    #     "accept": 1,
    #     "accept_date": "2006-01-02T00:00:00"
    # }

    

def update_status_warrant(request : HttpRequest) -> JsonResponse:
    if request.method != "PUT":
        # Wrong request method.
        return JsonResponse({
            "status": 405,
            "message": "Wrong Request Method"
        }, status=405)

    data = UtilsHandle.json_retrieval(request)

    # Failed.
    if isinstance(data, JsonResponse):
        return data
    
    # Data confirm to be dictionary.   

    print(data)


        
    