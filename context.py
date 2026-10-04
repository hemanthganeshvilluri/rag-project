def context_format(re_ranked_chunks):
    context = ''
    for i, chunk in enumerate(re_ranked_chunks, 1):
        context += f"""
context {i}:
{chunk.page_content}
Source: {chunk.metadata['source']}
Section: {chunk.metadata['section']}
Page_no: {chunk.metadata['page_no']}
"""
    return context
