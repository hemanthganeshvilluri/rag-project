from element_type_formatting import similar_to_header, remove_numbered_headers
from docling_core.types.doc import SectionHeaderItem, TextItem, ListItem, TableItem, PictureItem

def identifying_structure(doc):
    elements = []
    for element, _ in doc.iterate_items():
        text = getattr(element, "text", None)
        if isinstance(element, SectionHeaderItem):
            element_type = "header"
        elif isinstance(element, TextItem):
            if similar_to_header(element):
                element_type = "header"
            else:
                element_type = "text"
        elif isinstance(element, ListItem):
            element_type = "list_item"
        elif isinstance(element, TableItem):
            element_type = "table"
        elif isinstance(element, PictureItem):
            element_type = "image"
        else:
            element_type = "other"
        if element_type == "header" and text:
            text = remove_numbered_headers(text)   
        elements.append({
            "type": element_type,
            "content": text
            })
    return elements
