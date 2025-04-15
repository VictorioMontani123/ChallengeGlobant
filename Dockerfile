# Imagen base
FROM python:3.12-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar dependencias y requerimientos
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Exponer puerto por donde corre la API
EXPOSE 8000

# Comando para correr FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]