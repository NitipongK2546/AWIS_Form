from docxtpl import DocxTemplate
from warrant_form.code_handler import ThaiCountryAreaCode

def multiple_checkboxes(incoming_context : dict) -> dict:
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
    

def doc_create_with_context(incoming_context : dict):
    doc = DocxTemplate("warrant_form/resources/warrant_template.docx")

    context = bool_to_checkbox(incoming_context)

    doc.render(context)

    doc.save("warrant_form/resources/output.docx")
