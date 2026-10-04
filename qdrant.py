from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_qdrant import QdrantVectorStore

COLLECTION_NAME = "documents"
QDRANT_PATH = "./qdrant_data"
def vector_database(embed_model):
    client = QdrantClient(
        path=QDRANT_PATH
    )
    if not client.collection_exists(COLLECTION_NAME):
        vector_size = len(
            embed_model.embed_query("test")
        )
        client.create_collection(
            collection_name = COLLECTION_NAME,
            vectors_config = VectorParams(
                size = vector_size,
                distance = Distance.COSINE
            )
        )
    vector_db = QdrantVectorStore(
        client=client,
        collection_name=COLLECTION_NAME,
        embedding=embed_model
    )
    return vector_db


def delete_collection():
    client = QdrantClient(
        path=QDRANT_PATH
    )
    if client.collection_exists(COLLECTION_NAME):
        client.delete_collection(
            collection_name=COLLECTION_NAME
        )
        print(
            f"Deleted Qdrant collection: {COLLECTION_NAME}"
        )
    else:
        print(
            f"Collection does not exist: {COLLECTION_NAME}"
        )
