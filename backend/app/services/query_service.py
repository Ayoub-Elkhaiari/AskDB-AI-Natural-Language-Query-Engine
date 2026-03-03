import json
import re
from psycopg2.extras import RealDictCursor
from bson import json_util
from .db_manager import DBManager


def execute_postgres(query: str):
    with DBManager.pg_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query)
            rows = cur.fetchall()
    return rows


def execute_mongo(query: str):
    db = DBManager.mongo_db()
    compact = query.strip()

    match_find = re.match(r"^db\.(\w+)\.find\((.*)\)$", compact, re.DOTALL)
    if match_find:
        collection = match_find.group(1)
        arg_text = match_find.group(2).strip() or "{}"
        criteria = json.loads(arg_text)
        docs = list(db[collection].find(criteria).limit(200))
        return json.loads(json_util.dumps(docs))

    match_agg = re.match(r"^db\.(\w+)\.aggregate\((.*)\)$", compact, re.DOTALL)
    if match_agg:
        collection = match_agg.group(1)
        arg_text = match_agg.group(2).strip() or "[]"
        pipeline = json.loads(arg_text)
        docs = list(db[collection].aggregate(pipeline))
        return json.loads(json_util.dumps(docs))

    raise ValueError("Mongo query must be db.<collection>.find({...}) or db.<collection>.aggregate([...]).")
