from fastapi import Request, UploadFile, File, APIRouter
from ingestion_pipeline import ingestion_pipeline
from pathlib import Path
import shutil

router = APIRouter()

@router.post('/upload')
async def upload_file(req: Request, file: UploadFile = File(...)):
    file_dir = Path('uploads')
    file_dir.mkdir(exist_ok = True)
    file_path = file_dir / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    models = req.app.state.models
    vector_db = req.app.state.vector_db
    ingestion_pipeline(file_path, models, vector_db)
    return {
        'message': 'File Uploaded Successfully...!',
        'file': file.filename
    }
