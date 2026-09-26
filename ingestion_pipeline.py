from ingestion import ingestion
from format import formatting_documents
from chunking import chunking
from vectordb import embedding

def ingestion_pipeline(files, models, vector_db):
    documents = ingestion(
        files,
        models['converter']
    )
    print("DOCUMENTS:", len(documents))
    formatted_docs = formatting_documents(
        documents,
        models['processor'],
        models['model']
    )
    print("FORMATTED ELEMENTS:", len(formatted_docs))
    chunks = chunking(
        formatted_docs,
        models['text_splitter']
    )
    print("CHUNKS:", len(chunks))
    for chunk in chunks[:3]:
        print("CHUNK:", chunk.page_content[:200])
        print("METADATA:", chunk.metadata)
    result = embedding(
        chunks,
        vector_db
    )
    print("INDEXING COMPLETE")
    return result
