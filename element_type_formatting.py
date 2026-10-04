import re

def remove_numbered_headers(text):
    return re.sub(r'^\d+(\.\d+)*[\s.)-]+', '', text.strip()).strip()

def is_numbered_heading(text):
    return bool(
        re.match(
            r"^\d+(\.\d+)*[\s.)-]+",
            text.strip()
        )
    )

def similar_to_header(element):
    text = element.text.strip()
    if not text:
        return False
    words = text.split()
    if len(words) > 10:
        return False
    if re.fullmatch(r"[\d.,%+\-]+", text):
        return False
    score = 0
    if element.formatting and element.formatting.bold:
        score += 2
    if len(words) <= 6:
        score += 1
    if text.isupper() and len(words) <= 6:
        score += 1
    if is_numbered_heading(text):
        score += 1
    return score >= 3