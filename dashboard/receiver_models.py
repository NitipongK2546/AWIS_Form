from django import forms
from django.utils import timezone

class ReceivedReqFormStatus(forms.Form):
    accept = forms.IntegerField()
    accept_date = forms.CharField(max_length=19)

    court_code = forms.CharField(max_length=7)

    plaintiff = forms.CharField(max_length=400)
    police_station_id = forms.CharField(max_length=5)

    req_case_type_id = forms.IntegerField()
    req_date = forms.CharField(max_length=19)
    req_no = forms.IntegerField()
    req_no_plaintiff = forms.CharField(max_length=50)
    req_year = forms.IntegerField()
    
    def toDictWithConvertedType(self) -> dict[str, object]:
        output_dict = {
            "court_code": self.court_code,
            "req_year": self.req_year,
            "req_no": self.req_no,
            "police_station_id": self.police_station_id,
            "plaintiff": self.plaintiff,
        }

        date_format = "%Y-%m-%d %H:%M:%S"

        new_req_date = timezone.datetime.strptime(
            self.req_date, date_format
        )
        output_dict.update({"req_date": new_req_date})

        new_accept_date = timezone.datetime.strptime(
            self.accept_date, date_format
        )
        output_dict.update({"accept_date_date": new_accept_date})

        #############################################################

        output_dict.update({"accept": self.accept})

        output_dict.update({"req_no_plaintiff": self.req_no_plaintiff})

        return output_dict
