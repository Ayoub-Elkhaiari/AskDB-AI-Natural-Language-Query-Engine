from .db_manager import DBManager


def extract_postgres_schema() -> str:
    schema_lines = []
    with DBManager.pg_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
                """
            )
            tables = [row[0] for row in cur.fetchall()]
            for table in tables:
                schema_lines.append(f"Table: {table}")
                cur.execute(
                    """
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_schema = 'public' AND table_name = %s
                    ORDER BY ordinal_position;
                    """,
                    (table,),
                )
                columns = cur.fetchall()
                for col_name, data_type in columns:
                    schema_lines.append(f"  - {col_name}: {data_type}")
    return "\n".join(schema_lines)


def extract_mongo_schema() -> str:
    db = DBManager.mongo_db()
    lines = []
    for collection_name in db.list_collection_names():
        lines.append(f"Collection: {collection_name}")
        sample = db[collection_name].find_one()
        if sample:
            for key, value in sample.items():
                lines.append(f"  - {key}: {type(value).__name__}")
    return "\n".join(lines)
