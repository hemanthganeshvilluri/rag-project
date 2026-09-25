from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import load_models
from qdrant import vector_database
from backend.upload import router as upload_router
from backend.chat import router as chat_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    models = load_models()
    vector_db = vector_database(models['embed_model'])

    app.state.models = models
    app.state.vector_db = vector_db
    yield

app = FastAPI(title = 'RAG Application', lifespan = lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://127.0.0.1:5500"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)
app.include_router(upload_router)
app.include_router(chat_router)

@app.get('/')
def home():
    return {'message': 'Application Running Successfully...!'}