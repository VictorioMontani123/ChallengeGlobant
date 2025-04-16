from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.job_service import load_jobs_from_csv, get_jobs  # Asegúrate de importar la función 'get_jobs'

router = APIRouter(prefix="/jobs", tags=["Jobs"])  # Solo en el APIRouter

@router.post("/load")
async def load_jobs(csv_file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await csv_file.read()
    result = load_jobs_from_csv(contents, db)
    return  result 


# Endpoint para obtener todos los jobs
@router.get("/list")
def get_jobs_list(db: Session = Depends(get_db)):
    return get_jobs(db)
