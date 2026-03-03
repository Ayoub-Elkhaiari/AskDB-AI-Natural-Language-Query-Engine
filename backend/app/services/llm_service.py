import os
import requests

OPENROUTER_URL = 'https://openrouter.ai/api/v1/chat/completions'
MODEL = 'meta-llama/llama-3-8b-instruct'


def _prompt(database_type: str, schema: str, user_question: str) -> str:
    if database_type == 'postgres':
        return (
            "You are a PostgreSQL SQL query generator.\n"
            "You MUST output ONLY a raw SQL query.\n"
            "The query MUST start directly with SELECT.\n"
            "Do NOT include explanations.\n"
            "Do NOT include markdown.\n"
            "Do NOT include backticks.\n"
            "Do NOT include comments.\n"
            "Do NOT include any text before or after the SQL.\n"
            "Only safe SELECT queries are allowed.\n"
            "If the request is not related to the schema, return: SELECT 1 WHERE FALSE;\n\n"
            f"Database schema:\n{schema}\n\n"
            f"User question:\n{user_question}"
        )

    return (
        "You are an expert MongoDB query generator.\n"
        "Only find() and aggregate() read operations are allowed.\n"
        "You MUST output a query starting with db.COLLECTION_PLACEHOLDER.find(...) "
        "or db.COLLECTION_PLACEHOLDER.aggregate([...]).\n"
        "Output properly formatted, multi-line MongoDB shell syntax.\n"
        "Do NOT return a single-line JSON object or raw array.\n"
        "Do NOT include explanations, comments, or markdown.\n"
        "If the request is not related to the schema, return db.COLLECTION_PLACEHOLDER.aggregate([]).\n\n"
        f"Database schema:\n{schema}\n\n"
        f"User Question:\n{user_question}"
    )
import time
# import requests


def generate_query(database_type: str, schema: str, user_question: str) -> str:
    api_key = os.getenv('OPENROUTER_API_KEY', '')
    if not api_key:
        raise ValueError('OPENROUTER_API_KEY is not configured.')

    payload = {
        'model': MODEL,
        'messages': [
            {'role': 'user', 'content': _prompt(database_type, schema, user_question)}
        ],
        'temperature': 0.2,
        'max_tokens': 300,
    }

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json',
    }

    for attempt in range(3):
        response = requests.post(
            OPENROUTER_URL,
            json=payload,
            headers=headers,
            timeout=60
        )

        if response.status_code == 429:
            time.sleep(2 ** attempt)
            continue

        response.raise_for_status()
        body = response.json()
        return body['choices'][0]['message']['content'] \
            .replace('```sql', '') \
            .replace('```json', '') \
            .replace('```', '') \
            .strip()

    raise Exception("Rate limit exceeded. Try again later.")

# def clean_mongo_output(raw_text: str) -> str:
#     """
#     Keep only the first [ ... ] block (MongoDB pipeline) from model output.
#     Returns a properly formatted JSON array as string.
#     """
#     start = raw_text.find('[')
#     end = raw_text.rfind(']') + 1
#     if start == -1 or end == -1:
#         return "[]"  # fallback for empty/invalid output
#     return raw_text[start:end].strip()


# def generate_query(database_type: str, schema: str, user_question: str) -> str:
#     api_key = os.getenv('OPENROUTER_API_KEY', '')
#     if not api_key:
#         raise ValueError('OPENROUTER_API_KEY is not configured.')

#     payload = {
#         'model': MODEL,
#         'messages': [
#             {'role': 'user', 'content': _prompt(database_type, schema, user_question)}
#         ],
#         'temperature': 0.2,
#         'max_tokens': 500,
#     }

#     headers = {
#         'Authorization': f'Bearer {api_key}',
#         'Content-Type': 'application/json',
#     }

#     for attempt in range(3):
#         response = requests.post(
#             OPENROUTER_URL,
#             json=payload,
#             headers=headers,
#             timeout=60
#         )

#         if response.status_code == 429:  # rate limit
#             time.sleep(2 ** attempt)
#             continue

#         response.raise_for_status()
#         body = response.json()
#         raw_query = body['choices'][0]['message']['content']
        
#         if database_type.lower() == 'mongodb':
#             return clean_mongo_output(raw_query)
#         return raw_query.strip()  # Postgres raw SQL

#     raise Exception("Rate limit exceeded. Try again later.")
