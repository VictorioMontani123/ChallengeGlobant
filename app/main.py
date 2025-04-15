from fastapi import FastAPI
from app.db.init_db import init_db
from app.routers import department_router, job_router, employee_router

app = FastAPI(title="Globant Data Engineering Challenge")

# Inicializa la base de datos
init_db()

# Incluir routers
app.include_router(department_router.router)
app.include_router(job_router.router)
app.include_router(employee_router.router)

@app.get("/")
def read_root():
    return {"message": "API is running"}