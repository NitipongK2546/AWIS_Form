import csv

def set_up_codes() -> list:
    CSV_PATH = "warrant_form/codes.csv"
    province_choices = []
    district_choices = []
    sub_district_choices = []

    with open(CSV_PATH, mode='r', newline='', encoding='utf-8') as csv_file:
        code_table = csv.reader(csv_file, delimiter=",")

        current_province_code = ""
        current_district_code = ""
        current_sub_district_code = ""

        for row in code_table:
            if row[0]:
                current_province_code = row[0]
                province_choices.append((current_province_code, row[0 + 3]))
                continue
            if row[1]:
                current_district_code = current_province_code + row[1]
                district_choices.append((current_district_code, row[1 + 3]))
                continue
            if row[2]:
                current_sub_district_code = current_district_code + row[2]
                sub_district_choices.append((current_sub_district_code, row[2 + 3]))
                continue

    return province_choices, district_choices, sub_district_choices

class ThaiCountryAreaCode:
    province_choices = []
    district_choices = []
    sub_district_choices = []

    def __init__(self):
        self.province_choices, self.district_choices, self.sub_district_choices = set_up_codes()

    def getProvinceChoices(self):
        return self.province_choices
    
    def getDistrictChoices(self):
        return self.district_choices
    
    def getSubDistrictChoices(self):
        return self.sub_district_choices
    
    def getCodeDict(self):
        output_dict = {}
        [output_dict.update({code:text}) for code, text in self.province_choices]
        [output_dict.update({code:text}) for code, text in self.district_choices]
        [output_dict.update({code:text}) for code, text in self.sub_district_choices]

        return output_dict