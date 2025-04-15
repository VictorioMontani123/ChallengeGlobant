from fastapi import APIRouter, File, UploadFile, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.employee_service import load_employees_from_csv, get_employees, insert_employees_batch,get_employees_per_quarter,get_number_employees_hired
from typing import List


router = APIRouter(prefix="/employees", tags=["Employees"])

@router.post("/load")
async def load_employees(csv_file: UploadFile = File(...),db: Session = Depends(get_db)):
    contents = await csv_file.read()
    result = load_employees_from_csv(contents, db)
    return result

@router.post("/employees/batch")
async def insert_employees_endpoint(csv_file: UploadFile = File(...),batch_size: int = Query(1000, gt=0),db: Session = Depends(get_db)):
    try:
        contents = await csv_file.read()
        result = insert_employees_batch(contents, db, batch_size)
        return result
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Endpoint para obtener todos los employees
@router.get("/get_employees", tags=["Employees"])
def get_employees_list(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    employees = get_employees(db, skip=skip, limit=limit)
    return employees

# GET POR QUARTER
@router.get("/employees-per-quarter")
def employees_per_quarter(year: int = 2021, db: Session = Depends(get_db)):
    return get_employees_per_quarter(db, year)


# GET POR QUARTER
@router.get("/number-employees-hired")
def number_employees_hired(year: int = 2021, db: Session = Depends(get_db)):
    return get_number_employees_hired(db, year)