from langchain_core.documents import Document

def chunking(documents, text_splitter):
    chunks = []
    for elements in documents:
        if elements['type'] == 'table':
            chunks.append({
                'text': elements['content'].to_string(index = False),
                'type': elements['type'],
                'source': elements['source'],
                'section': elements['section'],
                'page_no': elements['page_no']
            })
        else:
            chunks.append({
                'text': elements['content'],
                'type': elements['type'],
                'source': elements['source'],
                'section': elements['section'],
                'page_no': elements['page_no']
            })
    final_chunks = []
    for chunk in chunks:
        if chunk['type'] in ['table', 'image', 'heading']:
            text = chunk['text']
            final_chunks.append(
                Document(
                    page_content = text,
                    metadata = {
                        'type': chunk['type'],
                        'source': chunk['source'],
                        'section': chunk['section'],
                        'page_no': chunk['page_no']
                    }
                )
            )
        else:
            text = chunk['text']
            splitted_text = text_splitter.split_text(text)
            for st in splitted_text:
                final_chunks.append(
                    Document(
                        page_content = st,
                        metadata = {
                            'type': chunk['type'],
                            'source': chunk['source'],
                            'section': chunk['section'],
                            'page_no': chunk['page_no']
                        }
                    )
                )
    return final_chunks