from docxtpl import DocxTemplate
from warrant_form.code_handler import ThaiCountryAreaCode

def clean_data_for_docx(incoming_context : dict) -> dict:
    bool_key_dict : dict[str, int] = {
        "cause_type_id": 2,
        "have_req": 2,
        "charge_type": 2,
    }

    for bool_key, total_num in bool_key_dict.items():
        for num in range(total_num):
            # Example: cause_type_id_1
            # ✓ (U+2713)
            key = f"{bool_key}_{num + 1}"
            int_value = incoming_context.get(key)
            if int_value == 1:
                incoming_context.update({key: "✓"})
            elif int_value == 0:
                incoming_context.pop(key)

    return incoming_context

def set_year_to_buddhist_era(incoming_context : dict) -> dict:
    year_list = ['req_year', 'scene_date_year']
    for year in year_list:
        year_value = incoming_context.get(year, None)
        incoming_context.update({year: year_value + 543})

    return incoming_context

def setup_codes_to_text(incoming_context : dict) -> dict:
    all_codes_field = ['acc_province', 'acc_district', 'acc_sub_district',
                        'req_province', 'req_district', 'req_sub_district',]
    
    code_dict = ThaiCountryAreaCode().getCodeDict()
    for code_key in all_codes_field:
        area_code = incoming_context.get(code_key, None)

        area_text = code_dict.get(area_code, None)

        incoming_context.update({code_key: area_text})

    return incoming_context
    

def doc_create_with_context(incoming_context : dict):
    doc = DocxTemplate("warrant_form/warrrant_form.docx")

    context = clean_data_for_docx(incoming_context)
    incoming_context = setup_codes_to_text(incoming_context)
    incoming_context = set_year_to_buddhist_era(incoming_context)

    doc.render(context)

    doc.save("warrant_form/output.docx")
