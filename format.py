from docling_core.types.doc import DoclingDocument, TextItem, SectionHeaderItem, ListItem, TableItem, PictureItem
from image_descripter import generate_text
def formatting_documents(documents, processor, model):
    results = []
    for file in documents:
        source = file['source']
        doc: DoclingDocument = file['document']
        curr_section = None
        for element, _ in doc.iterate_items():
            page_no = element.prov[0].page_no if (hasattr(element, 'prov') and element.prov) else None
            if isinstance(element, SectionHeaderItem):
                text = element.text
                curr_section = text
                results.append({
                    'content': text,
                    'type': 'heading',
                    'section': curr_section,
                    'source': source,
                    'page_no': page_no
                })
            elif isinstance(element, TextItem):
                text = element.text
                results.append({
                    'content': text,
                    'type': 'text',
                    'section': curr_section,
                    'source': source,
                    'page_no': page_no
                })
            elif isinstance(element, ListItem):
                text = element.text
                results.append({
                    'content': text,
                    'type': 'list_item',
                    'section': curr_section,
                    'source': source,
                    'page_no': page_no
                })
            elif isinstance(element, TableItem):
                table_df = element.export_to_dataframe(doc)
                results.append({
                    'content': table_df,
                    'type': 'table',
                    'section': curr_section,
                    'source': source,
                    'page_no': page_no
                })
            elif isinstance(element, PictureItem):
                image = element.get_image(doc)
                if image:
                    image_to_text = generate_text(image, processor, model)
                else:
                    image_to_text = ""
                results.append({
                    'content': image_to_text,
                    'type': 'image',
                    'section': curr_section,
                    'source': source,
                    'page_no': page_no
                }) 
    return results
