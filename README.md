# Globant Data Engineering Challenge

Este proyecto es una solución al desafío de Data Engineering propuesto por Globant. El objetivo principal es desarrollar una API REST para cargar datos desde archivos CSV a una base de datos SQL, realizar consultas analíticas sobre los datos y aplicar buenas prácticas de desarrollo.

---

## 📁 Estructura de archivos

- `/app/`
  - `main.py`: Archivo principal con los endpoints de la API.
  - `models/`
    - `base.py`: Define el `Base` de SQLAlchemy.
    - `models.py`: Contiene los modelos `Department`, `Job` y `HiredEmployee`.
  - `services/`: Lógica para carga de CSV y consultas SQL.
- `/data/`: Carpeta con los archivos CSV entregados.
- `requirements.txt`: Dependencias del proyecto.
- `README.md`: Este archivo.
- `Dockerfile` (opcional).
- `/test/` (opcional): Tests unitarios.

---

## 🧪 Archivos CSV

El desafío proporciona tres archivos CSV con las siguientes estructuras:

### `hired_employees.csv`
| id | name | datetime | department_id | job_id |
|----|------|----------|----------------|--------|

### `departments.csv`
| id | department |
|----|------------|

### `jobs.csv`
| id | job |
|----|-----|

---

## 🚀 Funcionalidades

### 1. API REST para carga de CSVs

Permite subir los archivos CSV y guardarlos en una base de datos SQL utilizando SQLAlchemy.

#### Endpoint:  
**POST** `/upload_csv/{type}`

- `{type}` puede ser: `departments`, `jobs`, `hired_employees`.

#### Ejemplo de uso:

```bash
curl -X POST -F "file=@data/departments.csv" http://localhost:8000/upload_csv/departments
```


### 🧱 Tecnologías utilizadas
Python 3.10+

FastAPI – Framework web para construir la API.

SQLAlchemy – ORM para interactuar con la base de datos.

SQLite (o PostgreSQL) – Motor de base de datos.

Uvicorn – Servidor ASGI para correr la API.

Docker (opcional) – Para contenerizar la aplicación.

Pytest (opcional) – Para pruebas unitarias.

### Instalación y ejecución local

# CLONE
```
git clone https://github.com/tu-usuario/globant-data-challenge.git
cd globant-data-challenge
```
# Crear entorno virtual e instalar dependencias:
```
python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate
pip install -r requirements.txt
```
# Ejecutar API
```
uvicorn app.main:app --reload
```
