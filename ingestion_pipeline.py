from ingestion import ingestion
from format import formatting_documents
from chunking import chunking
from vectordb import embedding

def ingestion_pipeline(files, models, vector_db):
    documents = ingestion(files, models['converter'])
    formatted_docs = formatting_documents(documents, models['processor'], models['model'])
    chunks = chunking(formatted_docs, models['text_splitter'])
    result = embedding(chunks, vector_db)
    return result