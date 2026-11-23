
# AI Text Analyzer API

A REST API built with FastAPI that uses an external AI model to analyze text. It identifies sentiment (`positive`, `neutral`, or `negative`), generates a short summary, and stores the original text and analysis results in PostgreSQL.

This is an educational backend project focused on asynchronous API integration, database persistence, migrations, and error handling.

## Tech Stack

- Python and FastAPI
- PostgreSQL
- SQLAlchemy (async)
- Alembic
- HTTPX
- Docker and Docker Compose
- Pytest

## Features

- Analyze submitted text with an external AI service.
- Return a sentiment classification and a short summary.
- Save the original text, sentiment, summary, and record metadata in PostgreSQL.
- Retrieve saved analyses individually or as a collection.
- Handle upstream AI service failures and timeouts with appropriate HTTP errors.

## API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `POST` | `/analysis` | Analyze text and save the result |
| `GET` | `/analyses` | Retrieve saved analyses |
| `GET` | `/analyses/{id}` | Retrieve an analysis by ID |

Interactive API documentation is available at `/docs` when the FastAPI server is running.

## Getting Started

### Requirements

- Docker and Docker Compose
- Credentials and endpoint for the configured AI provider

### Configuration

Create a `.env` file in the project root:

```dotenv
AI_API_KEY=your_api_key_here
AI_URL=your_ai_service_url_here
DATABASE_URL=your_local_postgresql_connection_url
DATABASE_URL_DOCKER=your_docker_postgresql_connection_url
```

Never commit real API keys or your `.env` file to GitHub.

The database URLs must match the PostgreSQL credentials configured in Docker Compose.

### Run the Application

```bash
docker compose up --build
```

The API is configured to run on port `8000`.

Open the interactive API documentation:

http://localhost:8000/docs

### Database Migrations

The database schema is managed using Alembic.

Apply migrations:

```bash
alembic upgrade head
```

Run this command in an environment where Alembic can connect to the configured PostgreSQL database. Depending on your Docker setup, you may need to run it inside the API container.

## Testing

The project includes Pytest tests covering:

- External AI service failures.
- AI request timeouts.
- API-level error handling.
- Verification that failed AI requests do not create database records.

Run tests from the project root:

```bash
pytest -v
```

External AI requests are mocked using HTTPX.

**Note:** The current educational test setup does not use a fully isolated test database. Check the database configuration before running database-writing tests.

## Current Limitations

This project is an educational MVP and is not production-ready.

- Tests do not yet use a separate test database.
- Docker Compose does not include a database health check.
- The Compose configuration uses development database credentials.
- The API depends on an external AI provider.
- Production security and infrastructure hardening are outside the current scope.

## Project Status

The educational MVP is complete.

The project demonstrates practical experience with FastAPI, asynchronous HTTP requests, PostgreSQL persistence, SQLAlchemy, Alembic migrations, Docker Compose, and API error handling.
