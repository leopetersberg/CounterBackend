# Verwenden Sie das offizielle Python-Image als Basis
FROM python:3.8-slim

# Arbeitsverzeichnis im Container setzen
WORKDIR /app

# Abhängigkeiten installieren
COPY requirements.txt .
RUN pip install -r requirements.txt

# Quellcode kopieren
COPY . .

# Port freigeben
EXPOSE 800

# Anwendung starten
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
