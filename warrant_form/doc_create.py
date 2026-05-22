from docxtpl import DocxTemplate
import warrant_form.forms_central as CentralForm

# def multiple_checkboxes(incoming_context : dict) -> dict:
#     bool_key_dict : dict[str, int] = {
#         "cause_type_id": 2,
#         "have_req": 2,
#         "charge_type": 2,
#     }

#     for bool_key, total_num in bool_key_dict.items():
#         for num in range(total_num):
#             # Example: cause_type_id_1
#             # ✓ (U+2713)
#             key = f"{bool_key}_{num + 1}"
#             int_value = incoming_context.get(key)
#             if int_value == 1:
#                 incoming_context.update({key: "✓"})
#             elif int_value == 0:
#                 incoming_context.pop(key)

#     return incoming_context

def _setup_area_codes_to_text(incoming_context : dict) -> dict:
    all_codes_field = ['acc_province', 'acc_district', 'acc_sub_district',
                        'req_province', 'req_district', 'req_sub_district',]
    
    code_dict = CentralForm.thai_codes.getCodeDict()
    for code_key in all_codes_field:
        area_code = incoming_context.get(code_key, "ERROR")

        area_text = code_dict.get(area_code, "ERROR")

        incoming_context.update({code_key: area_text})

    return incoming_context

def _setup_nation_codes_to_text(incoming_context : dict):
    all_codes_field = ['acc_origin', 'acc_nation',]
    code_dict = CentralForm.nation_codes.getCodeDict()

    for code_key in all_codes_field:
        acc_code = incoming_context.get(code_key, "ERROR")

        acc_text = code_dict.get(str(acc_code), "ERROR")

        incoming_context.update({code_key: acc_text})
    
    return incoming_context

def _none_to_empty_string(incoming_context : dict):
    for key, item in incoming_context.items():
        if not item:
            incoming_context.update({
                key: ""
            })

    return incoming_context

def _bool_to_checkbox(incoming_context : dict):
    for key, item in incoming_context.items():
        if isinstance(item, bool):
            if item:
                incoming_context.update({
                    key: "✓"
                })
            else:
                incoming_context.update({
                    key: ""
                })

    return incoming_context

###########################################################

def clean_warrant(incoming_context : dict) -> dict:
    def split_card_id(incoming_context : dict):
        card_id_field = "acc_card_id"
        id_data = incoming_context.get(card_id_field)

        incoming_context.update({
            "th_id_1": id_data[0],
            "th_id_2_5": id_data[1:5],
            "th_id_6_10": id_data[5:10],
            "th_id_11_12": id_data[10:12],
            "th_id_13": id_data[-1],
        })

        return incoming_context
    
    context = incoming_context
    
    context = _bool_to_checkbox(context)
    context = _setup_area_codes_to_text(context)
    context = _setup_nation_codes_to_text(context)
    context = _none_to_empty_string(context)
    context = split_card_id(context)

    return context

def clean_reqform(incoming_context : dict) -> dict:

    context = incoming_context
    context = _bool_to_checkbox(context)
    context = _setup_area_codes_to_text(context)
    context = _setup_nation_codes_to_text(context)
    context = _none_to_empty_string(context)

    return context

###############################################################################

from io import BytesIO
import tempfile
import subprocess
import os

from django.http import FileResponse
from docxtpl import DocxTemplate
from pathlib import Path

TEMP_DIR = "temp/"

def _create_pdf(doc : DocxTemplate, filename : str):
    os.makedirs(TEMP_DIR, exist_ok=True)

    docx_path = TEMP_DIR + "output.docx"
    pdf_path = TEMP_DIR + "output.pdf"

    doc.save(str(docx_path))

    result = subprocess.run([
        "soffice",
        "--headless",
        "--nologo",
        "--nofirststartwizard",
        "--convert-to", "pdf",
        "--outdir", TEMP_DIR,
        docx_path
    ],
        capture_output=True, 
        check=True
    )

    with open(pdf_path, "rb") as f:
        pdf_bytes = BytesIO(f.read())

    pdf_bytes.seek(0)

    Path(docx_path).unlink(missing_ok=True) 
    Path(pdf_path).unlink(missing_ok=True) 

    return FileResponse(
        pdf_bytes,
        as_attachment=False,
        filename=filename,
        content_type="application/pdf"
    )

def create_reqform_pdf(incoming_context : dict):
    def reqform_create() -> dict:
        doc = DocxTemplate("warrant_form/resources/reqform_template.docx")

        context = clean_reqform(incoming_context)

        doc.render(context)

        return doc

    doc = reqform_create()

    response = _create_pdf(doc, "reqform.pdf")

    return response

def create_warrant_pdf(incoming_context : dict):
    def warrant_create():
        doc = DocxTemplate("warrant_form/resources/warrant_template.docx")

        context = clean_warrant(incoming_context)

        doc.render(context)

        return doc

    doc = warrant_create()

    response = _create_pdf(doc, "warrant.pdf")

    return response