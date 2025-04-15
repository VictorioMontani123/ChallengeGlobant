from io import StringIO
import pandas as pd
from datetime import datetime
from sqlalchemy import text
from app.models.employee_model import Employee
from sqlalchemy.orm import Session
from app.schemas.employee_schema import EmployeeCreate
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import math
from app.sql.employee_queries import get_employees_per_quarter_query, get_departments_above_average
from fastapi.responses import JSONResponse

def load_employees_from_csv(file_contents: bytes, db: Session):
    data = StringIO(file_contents.decode("utf-8"))
    df = pd.read_csv(data, header=None, names=["id", "name","datetime","department_id","job_id"])

    before_drop = len(df)
    df = df.dropna(subset=["name", "datetime", "department_id", "job_id"]) #Elimino de forma rapida los null
    after_drop = len(df)
    removed_rows = before_drop - after_drop

    # Verifica si ya existen jobs con los mismos IDs
    result = db.execute(text("SELECT id FROM hired_employees"))
    existing_ids = {row[0] for row in result.fetchall()}

    # Filtra los jobs duplicados
    df_duplicates = df[df["id"].isin(existing_ids)]
    df_new = df[~df["id"].isin(existing_ids)]

    warning_msg = None
    if not df_duplicates.empty:
        warning_msg = f"{len(df_duplicates)} registros duplicados no insertados."
    
    # Inserta los nuevos departamentos
    if not df_new.empty:
        df_new.to_sql("hired_employees", con=db.get_bind(), if_exists="append", index=False)
    
    return {
        "message": "Archivo CSV de Employees procesado.",
        "inserted": int(len(df_new)),
        "warning": warning_msg,
        "removed_rows": f"filas con alguna columna en null : {removed_rows}"  
    }

def get_employees(db: Session, skip: int = 0, limit: int = 100):
    # Recupera los empleados desde la base de datos con paginación
    return db.query(Employee).offset(skip).limit(limit).all()

def insert_employees_batch(file_contents: bytes, db: Session, batch_size: int = 1000):
    if batch_size <= 0:
        raise ValueError("batch_size must be a positive integer.")

    data = StringIO(file_contents.decode("utf-8"))
    df = pd.read_csv(data, header=None, names=["id", "name", "datetime", "department_id", "job_id"])
    total_employees = len(df)

    if total_employees == 0:
        raise ValueError("You must send at least 1 employee.")

    num_batches = math.ceil(total_employees / batch_size)
    errores = []

    print(f"El archivo tiene {total_employees} empleados. Se dividirá en {num_batches} lote(s) de hasta {batch_size} empleados.")

    for i in range(num_batches):
        start = i * batch_size
        end = start + batch_size
        df_batch = df.iloc[start:end]

        db_employees = [
            Employee(
                id=row.id,
                name=row.name,
                datetime=row.datetime,
                department_id=row.department_id,
                job_id=row.job_id
            ) for _, row in df_batch.iterrows()
        ]

        try:
            db.add_all(db_employees)
            db.commit()
        except IntegrityError as ie:
            db.rollback()
            errores.append(f"Lote {i + 1}: Falló por conflicto de clave (posiblemente ID duplicado).")
        except SQLAlchemyError as e:
            db.rollback()
            errores.append(f"Lote {i + 1}: Error de base de datos inesperado: {str(e)}")

    if errores:
        return {
            "message": f"{total_employees} empleados procesados en {num_batches} lote(s).",
            "errores": errores
        }

    return {
        "message": f"{total_employees} empleados cargados exitosamente en {num_batches} lote(s) de hasta {batch_size} empleados."
    }

def get_employees_per_quarter(db: Session, year: int = 2021):
    query = get_employees_per_quarter_query(year)
    result = db.execute(text(query)).fetchall()
    columns = ['department', 'job', 'Q1', 'Q2', 'Q3', 'Q4']
    df = pd.DataFrame(result, columns=columns)
    print(df)
    data = df.to_dict(orient="records")
    return JSONResponse(content=data)

def get_number_employees_hired(db: Session, year: int = 2021):
    query = get_departments_above_average(year)
    result = db.execute(text(query)).fetchall()
    columns = ['id', 'department', 'hired']
    df = pd.DataFrame(result, columns=columns)
    print(df)
    data = df.to_dict(orient="records")
    return JSONResponse(content=data)
