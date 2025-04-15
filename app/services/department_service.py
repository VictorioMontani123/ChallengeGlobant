import pandas as pd
from io import StringIO
from sqlalchemy.orm import Session
from app.models.department_model import Department
from sqlalchemy import text
from fastapi import HTTPException

# Servicio para manejar la carga de datos de departamentos
def process_upload_departments(file_contents: bytes, db: Session):
    data = StringIO(file_contents.decode("utf-8"))
    df = pd.read_csv(data, header=None, names=["id", "department"])
    
    # Verifica si ya existen departamentos con los mismos IDs
    result = db.execute(text("SELECT id FROM departments"))
    existing_ids = {row[0] for row in result.fetchall()}

    # Filtra los departamentos duplicados
    df_duplicates = df[df["id"].isin(existing_ids)]
    df_new = df[~df["id"].isin(existing_ids)]
    
    warning_msg = None
    if not df_duplicates.empty:
        warning_msg = f"{len(df_duplicates)} registros duplicados no insertados."
    
    # Inserta los nuevos departamentos
    if not df_new.empty:
        df_new.to_sql("departments", con=db.get_bind(), if_exists="append", index=False)
    
    return {
        "message": "Archivo CSV de Departments procesado.",
        "inserted": int(len(df_new)),
        "warning": warning_msg
    }

# Servicio para obtener todos los departamentos
def get_departments(db: Session):
    departments = db.query(Department).all()
    return [{"id": dept.id, "department": dept.department} for dept in departments]