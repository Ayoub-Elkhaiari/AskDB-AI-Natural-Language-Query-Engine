import re

FORBIDDEN = ["INSERT", "UPDATE", "DELETE", "DROP", "ALTER", "TRUNCATE"]


def validate_query(database: str, query: str) -> None:
    upper = query.upper()
    if any(token in upper for token in FORBIDDEN):
        raise ValueError("Destructive operations are not allowed.")

    if database == 'postgres':
        if not re.match(r"^\s*SELECT\b", query, re.IGNORECASE):
            raise ValueError("Only SELECT queries are allowed for PostgreSQL.")
    elif database == 'mongo':
        normalized = query.replace(" ", "").lower()
        if not ('find(' in normalized or 'aggregate(' in normalized):
            raise ValueError("Only find/aggregate read operations are allowed for MongoDB.")
    else:
        raise ValueError("Unsupported database type.")
