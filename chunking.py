from langchain_core.documents import Document
def chunking(groups, text_splitter):
    final_chunks = []
    for group in groups:
        text = "\n\n".join(
            element["content"]
            for element in group
            if element["content"]
        )
        if not text:
            continue
        split_texts = text_splitter.split_text(text)
        for chunk in split_texts:
            final_chunks.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "source": group[0]["source"],
                        "page_no": group[0]["page_no"]
                    }
                )
            )
    return final_chunks
