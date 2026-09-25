from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore

def vector_database(embed_model):
    collection_name = "documents"
    client = QdrantClient(
        path = "./qdrant_data"
    )
    if not client.collection_exists(collection_name):
        vector_size = len(
            embed_model.embed_query("test")
        )
        client.create_collection(
            collection_name = collection_name,
            vectors_config = VectorParams(
                size = vector_size,
                distance = Distance.COSINE
            )
        )
    vector_db = QdrantVectorStore(
        client = client,
        collection_name = collection_name,
        embedding = embed_model
    )

    return vector_db
