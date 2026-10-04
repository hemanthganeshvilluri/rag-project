from image_descripter import generate_text
def formatting_documents(elements, processor, model):
    results = []
    for element in elements:
        if element["type"] == "header":
            content = f"# {element['content']}"
        elif element["type"] == "text":
            content = element["content"]
        elif element["type"] == "list_item":
            content = f"- {element['content']}"
        elif element["type"] == 'image':
            image = element['element'].get_image(element['document'])
            if image:
                content = generate_text(image, processor, model)
            else:
                content = ""
        elif element['type'] == 'table':
            table_df = element["element"].export_to_dataframe(element["document"])
            content = table_df.to_markdown(index=False)
        else:
            continue
        results.append({
            "content": content,
            "type": element["type"],
            "source": element["source"],
            "page_no": element["page_no"]
        })
    return results
