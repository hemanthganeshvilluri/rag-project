def embedding(chunks, vector_db):
    vector_db.add_documents(chunks)
    return vector_db