#!/usr/bin/env bash
set -e

python - <<'PY'
import os
import time
import psycopg2
from pymongo import MongoClient

pg_host = os.getenv('POSTGRES_HOST', 'postgres')
pg_port = int(os.getenv('POSTGRES_PORT', '5432'))
pg_db = os.getenv('POSTGRES_DB', 'nlq_postgres')
pg_user = os.getenv('POSTGRES_USER', 'postgres')
pg_password = os.getenv('POSTGRES_PASSWORD', 'postgres')
mongo_uri = os.getenv('MONGO_URI', 'mongodb://mongo:27017/')

for _ in range(30):
    try:
        conn = psycopg2.connect(
            host=pg_host,
            port=pg_port,
            dbname=pg_db,
            user=pg_user,
            password=pg_password,
        )
        conn.close()
        break
    except Exception:
        time.sleep(2)
else:
    raise RuntimeError('PostgreSQL is not ready in time')

for _ in range(30):
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        break
    except Exception:
        time.sleep(2)
else:
    raise RuntimeError('MongoDB is not ready in time')
PY

python manage.py migrate --noinput
python manage.py seed_databases
python manage.py runserver 0.0.0.0:8000
