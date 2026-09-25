def reranker(query, top_chunks, rerank_model):
    rerank_data = [[query, doc.page_content] for doc in top_chunks]
    rerank_scores = rerank_model.predict(rerank_data)

    sort_rerank_chunks = sorted(
        zip(top_chunks, rerank_scores),
        key = lambda x: x[1],
        reverse = True
    )
    return [doc for doc, score in sort_rerank_chunks[:3]]