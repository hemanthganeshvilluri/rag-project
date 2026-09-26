from image_descripter import generate_text
def formatting_documents(documents, processor, model):
    results = []
    for file in documents:
        source = file['source']
        doc = file['document']
        curr_section = None
        for _, element in doc:
            print("ELEMENT TYPE:", type(element).__name__)
            if type(element).__name__ == 'SectionHeaderItem':
                text = element.text
                curr_section = text
                results.append({
                    'content': text,
                    'type': 'heading',
                    'section': curr_section,
                    'source': source,
                    'page_no': element.prov[0].page_no
                })
            elif type(element).__name__ == 'TextItem':
                text = element.text
                results.append({
                    'content': text,
                    'type': 'text',
                    'section': curr_section,
                    'source': source,
                    'page_no': element.prov[0].page_no
                })
            elif type(element).__name__ == 'TableItem':
                table = element.export_to_dataframe(doc)
                results.append({
                    'content': table,
                    'type': 'table',
                    'section': curr_section,
                    'source': source,
                    'page_no': element.prov[0].page_no
                })
            elif type(element).__name__ == "PictureItem":
                image = element.get_image(doc)
                image_to_text = generate_text(image, processor, model)
                results.append({
                    'content': image_to_text,
                    "type": 'image',
                    "section": curr_section,
                    "source": source,
                    "page_no": element.prov[0].page_no
            })
    return results
