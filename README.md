# Task API

A CRUD API for managing a to-do list, built with FastAPI and SQLAlchemy. Tasks are stored in PostgreSQL, and the whole stack (API, database, pgAdmin) runs in Docker Compose.

## Run

```bash
docker compose -f postgresql.yaml up -d
```

| Service  | URL / Port                                     |
|----------|------------------------------------------------|
| API      | http://localhost:8000 (Swagger UI at `/docs`)  |
| Postgres | `localhost:5000` (mapped to 5432 in container) |

Stop with `docker compose -f postgresql.yaml down`. Data lives in the `postgres_data` volume and survives this; add `-v` to wipe it.

## Endpoints

| Method | Path          | Description             | Body (JSON)                            | Success | Error                                  |
|--------|---------------|-------------------------|----------------------------------------|---------|----------------------------------------|
| GET    | `/tasks`      | List all tasks          | none                                   | 200     | none                                   |
| GET    | `/tasks/{id}` | Get a single task       | none                                   | 200     | 200 with `{"error": ...}` if not found |
| POST   | `/tasks`      | Create a task           | `{"title": str, "done": bool = false}` | 201     | 400 if `title` is empty                |
| PUT    | `/tasks/{id}` | Partially update a task | `{"title"?: str, "done"?: bool}`       | 200     | 400 if id doesn't exist                |
| DELETE | `/tasks/{id}` | Delete a task           | none                                   | 200     | 404 if id doesn't exist                |

## Example

```
$ curl -i -X POST http://localhost:8000/tasks \
    -H "Content-Type: application/json" \
    -d '{"title":"Buy groceries"}'

HTTP/1.1 201 Created
date: Fri, 30 Oct 2026 12:00:00 GMT
server: uvicorn
content-length: 45
content-type: application/json

{"id":1,"title":"Buy groceries","done":false}
```

## Persistence check

1. Create a task:
   ```bash
   curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"persist me"}'
   ```
2. Destroy and recreate every container (the volume is kept):
   ```bash
   docker compose -f postgresql.yaml down
   docker compose -f postgresql.yaml up -d
   ```
3. Read it back:
   ```bash
   curl -i http://localhost:8000/tasks
   ```

Result:

```json
[
  {
    "id": 2,
    "title": "Buy groceries",
    "done": false,
    "created_at": "2026-10-30T13:16:07.291475Z",
    "updated_at": "2026-10-30T13:16:07.291475Z"
  },
  {
    "id": 3,
    "title": "Finish project report",
    "done": false,
    "created_at": "2026-10-30T13:16:07.291475Z",
    "updated_at": "2026-10-30T13:16:07.291475Z"
  },
  {
    "id": 4,
    "title": "Call the dentist",
    "done": true,
    "created_at": "2026-10-30T13:16:07.291475Z",
    "updated_at": "2026-10-30T13:16:07.291475Z"
  }
]
```
