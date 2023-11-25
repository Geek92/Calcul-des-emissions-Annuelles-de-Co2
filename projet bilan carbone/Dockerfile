FROM python:3.10
WORKDIR /app
COPY ./app /app
COPY ./requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 80

# Commande pour démarrer l'application FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
