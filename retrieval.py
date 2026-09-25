def retrieval(query, vector_db):
    top_chunks = vector_db.similarity_search(query, k = 10)
    return top_chunks