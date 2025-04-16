# Imagen base de Python 3.12 con slim para reducir el tamaño de la imagen
FROM python:3.12-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar solo el archivo de dependencias primero para aprovechar el caché de Docker
COPY requirements.txt .

# Instalar las dependencias desde requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código del proyecto
COPY . .

# Exponer el puerto donde se correrá la API (8000 por defecto)
EXPOSE 8000

# Comando para iniciar FastAPI con Uvicorn (el servidor ASGI recomendado para FastAPI)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
