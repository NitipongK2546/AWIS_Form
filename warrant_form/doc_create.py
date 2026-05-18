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

def clean_warrant(incoming_context : dict) -> dict:
    def bool_to_checkbox(incoming_context : dict):
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
    def setup_area_codes_to_text(incoming_context : dict) -> dict:
        all_codes_field = ['acc_province', 'acc_district', 'acc_sub_district',
                            'req_province', 'req_district', 'req_sub_district',]
        
        code_dict = CentralForm.thai_codes.getCodeDict()
        for code_key in all_codes_field:
            area_code = incoming_context.get(code_key, "ERROR")

            area_text = code_dict.get(area_code, "ERROR")

            incoming_context.update({code_key: area_text})

        return incoming_context
    
    def setup_nation_codes_to_text(incoming_context : dict):
        all_codes_field = ['acc_origin', 'acc_nation',]
        code_dict = CentralForm.nation_codes.getCodeDict()

        for code_key in all_codes_field:
            acc_code = incoming_context.get(code_key, "ERROR")

            acc_text = code_dict.get(str(acc_code), "ERROR")

            incoming_context.update({code_key: acc_text})
        
        return incoming_context

    def none_to_empty_string(incoming_context : dict):
        for key, item in incoming_context.items():
            if not item:
                incoming_context.update({
                    key: ""
                })

        return incoming_context

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
    
    context = bool_to_checkbox(context)
    context = setup_area_codes_to_text(context)
    context = setup_nation_codes_to_text(context)
    context = none_to_empty_string(context)
    context = split_card_id(context)

    return context

def clean_reqform(incoming_context : dict) -> dict:
    pass

def reqform_create(incoming_context : dict) -> dict:
    doc = DocxTemplate("warrant_form/resources/reqform_template.docx")

    context = clean_reqform(incoming_context)

    doc.render(context)

    return doc

def warrant_create(incoming_context : dict):
    doc = DocxTemplate("warrant_form/resources/warrant_template.docx")

    context = clean_warrant(incoming_context)

    doc.render(context)

    return doc

###############################################################################

from io import BytesIO
import tempfile
import subprocess
import os

from django.http import FileResponse

def create_pdf(incoming_context : dict):
    doc = warrant_create(incoming_context)

    with tempfile.TemporaryDirectory() as tmpdir:
        docx_path = os.path.join(tmpdir, "output.docx")
        pdf_path = os.path.join(tmpdir, "output.pdf")

        doc.save(docx_path)

        subprocess.run([
            "soffice",
            "--headless",
            "--convert-to", "pdf",
            "--outdir", tmpdir,
            docx_path
        ], check=True)

        with open(pdf_path, "rb") as f:
            pdf_bytes = BytesIO(f.read())

    pdf_bytes.seek(0)

    return FileResponse(
        pdf_bytes,
        as_attachment=False,
        filename="report.pdf",
        content_type="application/pdf"
    )
