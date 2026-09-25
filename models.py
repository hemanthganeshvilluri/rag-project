from docling.document_converter import DocumentConverter
from transformers import AutoModelForMultimodalLM, AutoProcessor
from langchain_huggingface import HuggingFaceEmbeddings
from sentence_transformers import CrossEncoder
from langchain_ollama import OllamaLLM
from langchain_text_splitters import RecursiveCharacterTextSplitter
import torch
import os

def load_models():
    converter = DocumentConverter()

    hf_token = os.getenv("HF_TOKEN")
    processor = AutoProcessor.from_pretrained('google/gemma-3-4b-it', token = hf_token)
    model = AutoModelForMultimodalLM.from_pretrained('google/gemma-3-4b-it', dtype = torch.bfloat16, device_map = 'auto', token = hf_token)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 950, chunk_overlap = 125)

    embed_model = HuggingFaceEmbeddings(model_name = 'Qwen/Qwen3-Embedding-0.6B')

    rerank_model = CrossEncoder('Qwen/Qwen3-Reranker-0.6B')

    llm = OllamaLLM(
        model = 'gemma2:2b',
        base_url = 'http://172.20.240.1:11434'
    )
    return {
        'converter': converter,
        'processor': processor,
        'model': model,
        'text_splitter': text_splitter,
        'embed_model': embed_model,
        'rerank_model': rerank_model,
        'llm': llm
    }
