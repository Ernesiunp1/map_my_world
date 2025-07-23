# Usa una imagen ligera de Python
FROM python:3.11-slim

# Evita interacción al instalar dependencias
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Establece el directorio de trabajo
WORKDIR /app

# Instala las dependencias
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia el resto del código
COPY . .

# Expone el puerto (opcional, útil si otros desarrolladores leen el Dockerfile)
EXPOSE 8000

# Comando por defecto
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
