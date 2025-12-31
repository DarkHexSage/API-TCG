FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    sqlite3 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar y instalar requirements
COPY TCG-API/tcg-backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Copiar código
COPY TCG-API/tcg-backend/main.py .
COPY db_standardizer/tcg_unified.db .

EXPOSE 8000

# Correr directamente
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
