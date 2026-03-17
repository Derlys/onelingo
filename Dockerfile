FROM python:3.9-slim

# Establece el directorio de trabajo
WORKDIR /app

# Copia los archivos de requerimientos
COPY requirements.txt .

# Instala las librerías como root (más estable en Railway)
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código
COPY . .

# Exponemos el puerto 8080 (opcional pero buena práctica)
EXPOSE 8080

# Comando para arrancar la app
CMD ["python", "app.py"]