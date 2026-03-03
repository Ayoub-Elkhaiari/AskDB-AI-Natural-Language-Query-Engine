import os
from pymongo import MongoClient
import psycopg2


class DBManager:
    @staticmethod
    def pg_connection():
        return psycopg2.connect(
            host=os.getenv('POSTGRES_HOST', 'postgres'),
            port=int(os.getenv('POSTGRES_PORT', 5432)),
            dbname=os.getenv('POSTGRES_DB', 'nlq_postgres'),
            user=os.getenv('POSTGRES_USER', 'postgres'),
            password=os.getenv('POSTGRES_PASSWORD', 'postgres'),
        )

    @staticmethod
    def mongo_client():
        uri = os.getenv('MONGO_URI', 'mongodb://mongo:27017/')
        return MongoClient(uri)

    @staticmethod
    def mongo_db():
        client = DBManager.mongo_client()
        return client[os.getenv('MONGO_DB', 'nlq_mongo')]
