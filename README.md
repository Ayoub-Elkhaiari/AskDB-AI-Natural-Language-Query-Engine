# AskDB-AI: Natural Language Query Engine

AskDB-AI is a full-stack AI-powered query assistant that converts natural language questions into **read-only database queries (Security Service)** for:

- **PostgreSQL** (`SELECT` only)
- **MongoDB** (`find` / `aggregate` only)

It uses **OpenRouter LLMs** to generate queries from your prompt and current database schema, then lets you:

- review generated query,
- edit it,
- execute it, or
- reject/clear it.

---

## ✨ Features

- Natural language → SQL/Mongo query generation via OpenRouter
- Dynamic schema extraction for both PostgreSQL and MongoDB
- Query approval flow before execution
- Editable Monaco query editor in frontend
- Strict read-only safety validation
- Seeded sample data in both databases
- Full Dockerized local setup (`postgres`, `mongo`, `backend`, `frontend`)

---

## 🧱 Tech Stack

### Backend
- Django
- Django REST Framework
- django-cors-headers
- psycopg2-binary
- pymongo
- requests
- python-dotenv

### Frontend
- React (Vite)
- Axios
- TailwindCSS
- Monaco Editor

### Infrastructure
- Docker + Docker Compose
- PostgreSQL 16
- MongoDB 7

### LLM Provider
- OpenRouter
- Models used: `openai/gpt-oss-120b:free`, `google/gemma-3-27b-it:free`, `meta-llama/llama-3-8b-instruct`

---

## 🏗️ Architecture

```text
Frontend (React)
   ↓
Django REST API
   ↓
Service Layer (schema, LLM, security, execution)
   ↓
PostgreSQL / MongoDB
   ↓
OpenRouter API
```

---

## 📁 Project Structure

```text
.
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── scripts/
│   │   └── start.sh
│   └── app/
│       ├── core/
|       |    └──  ....
│       ├── api/
│       │   ├── management/commands/seed_databases.py
|       |   ├── apps.py
|       |   ├── urls.py
|       |   └── views.py
│       └── services/
|            └── db_manager.py
|            ├── llm_service.py
|            ├── query_service.py
|            ├── schema_service.py
|            └── security_service.py
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   └── src/
|        └── ....
├── docker-compose.yml
├── .env
└── README.md
```

---

## 🚀 Quick Start

### 1) Prerequisites
- Docker Desktop (or Docker Engine + Compose plugin)
- Git

### 2) Clone repository

```bash
git clone https://github.com/Ayoub-Elkhaiari/AskDB-AI-Natural-Language-Query-Engine.git
cd AskDB-AI-Natural-Language-Query-Engine
```

### 3) Configure environment
Create/modify `.env` in project root:
I already included a placeholder for the OpenRouter API key to illustrate the expected format in .env file. Replace the placeholder with your actual key when configuring the project.

```env
DJANGO_SECRET_KEY=your-secret-key
DEBUG=1
OPENROUTER_API_KEY=your-openrouter-api-key
```

> ⚠️ Never commit real API keys. If exposed, rotate immediately.

### 4) Start all services

```bash
docker compose up --build
```

### 5) Open apps
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/api

---

## 🔌 API Endpoints

### 1) Generate Query
`POST /api/generate-query/`

Request:

```json
{
  "database": "postgres",
  "question": "Show the top 5 users by total order value"
}
```

Response:

```json
{
  "schema": "...",
  "generated_query": "SELECT ..."
}
```

### 2) Execute Query
`POST /api/execute-query/`

Request:

```json
{
  "database": "postgres",
  "query": "SELECT * FROM users LIMIT 5;"
}
```

Response:

```json
{
  "results": [
    {"id": 1, "name": "..."}
  ]
}
```

---

## 🗃️ Seeded Data

On backend startup, the seeder initializes:

### PostgreSQL
- `users` table (15 rows)
- `orders` table (30 rows)

### MongoDB
- `customers` collection (15 documents)
- `purchases` collection (30 documents)

---

## 🔐 Safety Rules

Before execution, queries are validated to block destructive operations.

Blocked keywords include:
- `INSERT`
- `UPDATE`
- `DELETE`
- `DROP`
- `ALTER`
- `TRUNCATE`

```
if not re.match(r"^\s*SELECT\b", query, re.IGNORECASE):
            raise ValueError("Only SELECT queries are allowed for PostgreSQL.")
```
```
 if not ('find(' in normalized or 'aggregate(' in normalized):
            raise ValueError("Only find/aggregate read operations are allowed for MongoDB.")
```

Allowed:
- PostgreSQL: `SELECT`
- MongoDB: `find` / `aggregate`

---

## 🖥️ Frontend Usage Flow

1. Select database (`PostgreSQL` or `MongoDB`)
2. Enter natural language question
3. Click **Generate Query**
4. Inspect generated schema + query
5. Edit query if needed
6. Click **Execute** to run, or **Reject** to clear
7. Review results in table output

---

## 🧪 Useful Commands

### See running services
```bash
docker compose ps
```

### View backend logs
```bash
docker compose logs -f backend
```

### Restart stack cleanly
```bash
docker compose down -v
docker compose up --build
```

---

## 🛠️ Troubleshooting

### `no configuration file provided: not found`
Run compose from the repo directory that contains `docker-compose.yml`.

### Frontend shows `Network Error`
Usually backend is not running or not reachable on `localhost:8000`.

Check:
```bash
docker compose ps
docker compose logs backend --tail=200
```

### Backend fails with Django system check errors
Pull latest changes and rebuild containers:
```bash
docker compose down -v
docker compose up --build
```

### Backend fails with `stat /app/scripts/start.sh: no such file or directory`
```bash
docker compose down -v
docker compose up --build
```

### Query generation fails
- Confirm `OPENROUTER_API_KEY` is valid in `.env`
- Check backend logs for OpenRouter response details

---

## 📌 Security Notes

- Keep `.env` private and excluded from source control in production.
- Rotate OpenRouter keys if exposed.
- This project enforces read-only query execution by design.

---

## 🎥 Demo Video


```md
Watch demo here: 
```
![Image](https://github.com/user-attachments/assets/b5d0344f-3e73-4665-8135-06d3387fdd96)
