from langchain_core.documents import Document
def chunking(groups, text_splitter):
    final_chunks = []
    for group in groups:
        text = group["content"]
        if not text:
            continue
        split_texts = text_splitter.split_text(text)
        for chunk in split_texts:
            final_chunks.append(
                Document(
                    page_content=chunk,
                    metadata={
                        "source": group["source"],
                        "page_no": group["page_no"],
                        "type": group["type"]
                    }
                )
            )
    return final_chunks
