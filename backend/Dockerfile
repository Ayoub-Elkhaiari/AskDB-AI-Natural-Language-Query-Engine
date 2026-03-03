FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app /app
COPY scripts /app/scripts

RUN chmod +x /app/scripts/start.sh

EXPOSE 8000
CMD ["/app/scripts/start.sh"]
