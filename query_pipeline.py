from retrieval import retrieval
from reranker import reranker
from context import context_format
from prompt_format import prompt_format
from generation import generation

def query_pipeline(query, vector_db, models):
    top_chunks = retrieval(query, vector_db)
    print("RETRIEVED CHUNKS:", len(top_chunks))
    for chunk in top_chunks:
        print(chunk.page_content[:200])
    rerank_chunks = reranker(
        query,
        top_chunks,
        models['rerank_model']
    )
    print("RERANKED CHUNKS:", len(rerank_chunks))
    context = context_format(rerank_chunks)
    print("CONTEXT:")
    print(context)
    prompt = prompt_format(query, context)
    answer = generation(
        prompt,
        models['llm']
    )
    return query, answer, rerank_chunks
