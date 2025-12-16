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

# Copiar archivos de la aplicación
COPY app.py .
COPY preprocesar_vulnerabilidades.py .
COPY train_features.csv .
COPY test_features.csv .
COPY example_features.csv .

# Crear directorio para reportes
RUN mkdir -p reports

# Exponer puerto
EXPOSE 5000

# Variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Comando de inicio
CMD ["python", "app.py"]
