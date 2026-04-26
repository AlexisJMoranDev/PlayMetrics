# ---- Seleccionar version de python más compatible ----
FROM python:3.12-slim

# ---- decimos a Docker en qué carpeta de la "caja virtual" vamos a trabajar ----
WORKDIR /app

# ---- Dependencias para LightGBM ----
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*
# ---- copiamos e instalamos todas las librerias ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

#---- abrimos el puerto 5000 ---- 
EXPOSE 5000

# ---- arrancar contenedor ----
CMD ["flask", "--app", "main.py", "run", "--host=0.0.0.0"]