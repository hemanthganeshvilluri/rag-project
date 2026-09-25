from retrieval import retrieval
from reranker import reranker
from context import context_format
from prompt_format import prompt_format
from generation import generation

def query_pipeline(query, vector_db, models):
    top_chunks = retrieval(query, vector_db)
    rerank_chunks = reranker(query, top_chunks, models['rerank_model'])
    context = context_format(rerank_chunks)
    prompt = prompt_format(query, context)
    answer = generation(prompt, models['llm'])
    return query, answer, rerank_chunks