from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from app.services.department_service import process_upload_departments, get_departments
from app.db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter()

# Endpoint para cargar departamentos desde un archivo CSV
@router.post("/upload_departments", tags=["department"])
async def upload_departments(csv_file: UploadFile = File(...), db: Session = Depends(get_db)):
    contents = await csv_file.read() # PARA ESTO PODRIAMOS GENERAR UNA FUNCION EN EL SERVICES O UTILS.
    result = process_upload_departments(contents, db)
    return result

# Endpoint para obtener todos los departamentos
@router.get("/get_departments", tags=["department"])
def get_departments_list(db: Session = Depends(get_db)):
    return get_departments(db)