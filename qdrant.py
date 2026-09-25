from langchain_qdrant import QdrantVectorStore

def vector_database(embed_model):

    try:
        vector_db = QdrantVectorStore.from_existing_collection(
            embedding = embed_model,
            path = './qdrant_data',
            collection_name = 'documents'
        )

    except Exception:
        vector_db = QdrantVectorStore.from_documents(
            documents = [],
            embedding = embed_model,
            path = './qdrant_data',
            collection_name = 'documents'
        )

    return vector_db