from langchain_core.documents import Document
def grouping_by_headers(elements):
    groups = []
    current_group = []
    for element in elements:
        if element["type"] == "header":
            if current_group:
                groups.append(current_group)
            current_group = [element]
        else:
            current_group.append(element)
    if current_group:
        groups.append(current_group)
    return groups
