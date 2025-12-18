FROM python:3.9-slim

# Configurar directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código Python y datasets
COPY python/ /app/python/
COPY csvs/ /app/csvs/

# Crear directorio para reportes
RUN mkdir -p /app/reports

# Exponer puerto
EXPOSE 5000

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PORT=5000
ENV CSV_DIR=/app/csvs

# Establecer directorio de trabajo de la app
WORKDIR /app/python

# Comando de inicio
CMD ["python", "app.py"]
