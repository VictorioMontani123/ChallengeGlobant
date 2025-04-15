import pandas as pd
from io import StringIO
from sqlalchemy.orm import Session
from app.models.job_model import Job
from sqlalchemy import text
from fastapi import HTTPException

def load_jobs_from_csv(file_contents: bytes, db: Session):
    data = StringIO(file_contents.decode("utf-8"))
    df = pd.read_csv(data, header=None, names=["id", "job"])
    
     # Verifica si ya existen jobs con los mismos IDs
    result = db.execute(text("SELECT id FROM jobs"))
    existing_ids = {row[0] for row in result.fetchall()}

    # Filtra los jobs duplicados
    df_duplicates = df[df["id"].isin(existing_ids)]
    df_new = df[~df["id"].isin(existing_ids)]

    warning_msg = None
    if not df_duplicates.empty:
        warning_msg = f"{len(df_duplicates)} registros duplicados no insertados."
    
    # Inserta los nuevos departamentos
    if not df_new.empty:
        df_new.to_sql("jobs", con=db.get_bind(), if_exists="append", index=False)
    
    return {
        "message": "Archivo CSV de jobs procesado.",
        "inserted": int(len(df_new)),
        "warning": warning_msg
    }

def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    # Recupera los trabajos desde la base de datos con paginación (opcional)
    return db.query(Job).offset(skip).limit(limit).all()