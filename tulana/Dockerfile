# Tulana Studio
FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
      fonts-indic fonts-noto-core fontconfig && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# every module the application imports at runtime
COPY config.py pdflib.py db.py library.py sources.py fetcher.py app.py ./
COPY sources.json share_gradio.py check_sources.py ./
COPY selftest.py ./
COPY static/ static/
COPY docs/ docs/
COPY README.md .
ENV TULANA_DATA_DIR=/app/data TULANA_STATE_DIR=/app/state \
    TULANA_HOST=0.0.0.0 TULANA_PORT=7862
EXPOSE 7862
CMD ["python3", "app.py"]
