from docxtpl import DocxTemplate

def doc_create_with_context(incoming_context : dict):
    doc = DocxTemplate("warrant_form/warrrant_form.docx")

    context = incoming_context

    doc.render(context)

    doc.save("warrant_form/output.docx")
