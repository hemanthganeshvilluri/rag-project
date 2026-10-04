from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from models import load_models
from qdrant import vector_database, delete_collection
from backend.upload import router as upload_router
from backend.chat import router as chat_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    models = load_models()
    delete_collection()
    vector_db = vector_database(models['embed_model'])

    app.state.models = models
    app.state.vector_db = vector_db
    yield

app = FastAPI(title = 'RAG Application', lifespan = lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)
app.mount(
    "/static",
    StaticFiles(directory = 'frontend'),
    name = 'static'
)
app.include_router(upload_router)
app.include_router(chat_router)

@app.get('/')
def home():
    return FileResponse('frontend/index.html')
