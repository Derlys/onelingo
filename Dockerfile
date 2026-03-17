FROM python:3.9

# Creamos el usuario 'user' para cumplir con la seguridad de Hugging Face
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

WORKDIR /app

# Copiamos primero los requerimientos para aprovechar el cache de Docker
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copiamos el resto de los archivos
COPY --chown=user . /app

# EL CAMBIO CLAVE: Ejecutamos el archivo directamente con Python
# Ya no usamos 'uvicorn', usamos el comando estándar de Python
CMD ["python", "app.py"]