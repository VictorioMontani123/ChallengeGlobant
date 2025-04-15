'''
init_db.py: Este archivo se usa para inicializar la base de datos 
y crear las tablas según los modelos que hayas definido. 
En tu caso, este archivo importará todos los modelos 
(departamentos, empleados, trabajos, etc.) 
para que las tablas sean creadas cuando se ejecute la función init_db.
'''
from app.models.base import Base
from app.db.session import engine
from app.models import department_model, employee_model, job_model

def init_db():
    # Crea todas las tablas en la base si no existen aún
    Base.metadata.create_all(bind=engine)