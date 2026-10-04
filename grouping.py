def grouping_by_headers(elements):
    groups = []
    current_group = []
    current_section = None
    for element in elements:
        if element["type"] == "header":
            if current_group:
                groups.append({
                    "content": current_group,
                    "section": current_section,
                    "source": current_group[0]["source"],
                    "page_no": current_group[0]["page_no"]
                })
            current_section = element["content"]
            current_group = [element]
        else:
            current_group.append(element)
    if current_group:
        groups.append({
            "content": current_group,
            "section": current_section,
            "source": current_group[0]["source"],
            "page_no": current_group[0]["page_no"]
        })
    return groups
