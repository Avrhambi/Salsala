FROM python:3.12-slim

# Install system deps needed by pytesseract and psycopg
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    tesseract-ocr-heb \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model used by hebrew_nlp service
RUN python -m spacy download xx_ent_wiki_sm

COPY . .

EXPOSE 8000

CMD ["uvicorn", "server.entry_point:app", "--host", "0.0.0.0", "--port", "8000"]
