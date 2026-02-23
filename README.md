# AtheLeanX Backend 🏋️‍♂️🧠

Backend service for **AtheLeanX**, an AI-powered fitness planning platform.

This backend handles:
- Authentication & authorization
- AI-powered workout and diet generation
- Conversational AI fitness coach
- Data persistence using PostgreSQL
- A structured API consumed by a React frontend

> ⚠️ This is **not** a chatbot backend.  
> AI is treated as deterministic infrastructure, not a UI feature.

---

## 🚀 What is AtheLeanX?

AtheLeanX is a full-stack fitness application that provides:
- Personalized workout plans
- Personalized diet plans
- Context-aware AI coaching

Key design principles:
- Users **never write prompts**
- AI outputs are **schema-driven**
- All AI responses are **validated and stored**
- Plans persist across sessions and devices

---

## 🧠 Architecture Overview

### Core Principles
- AI is infrastructure, not UI
- Strict schema validation using Pydantic
- Deterministic plan generation
- Clear separation of concerns

### AI Layers

#### 1. Plan Generation
- Workout and diet plans
- AI returns **strict JSON only**
- Validated via Pydantic schemas
- Stored in PostgreSQL using JSONB

#### 2. AI Coach
- Conversational fitness coach
- Uses latest workout and diet plans as context
- Returns plain text responses
- Chat history is persisted

---

## 🔁 AI Mode Switching

The backend supports two AI modes:

| Mode | Description |
|---|---|
| `mock` | Deterministic fake AI (development & testing) |
| `openrouter` | Real LLM via OpenRouter |

Switching AI mode does **not** affect:
- API endpoints
- Schemas
- Frontend logic
- Database models

```env
AI_MODE=mock   # or openrouter
```
---

## 🧩 Tech Stack

- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL (Supabase)
- **ORM**: SQLAlchemy
- **Migrations**: Alembic
- **Authentication**: JWT (Bearer tokens)
- **Password Hashing**: Argon2
- **AI Providers**:
  - Mock AI (default)
  - OpenRouter (OpenAI-compatible)
- **Server**: Uvicorn

---
## 🔐 Authentication

### Endpoints
- `POST /auth/signup` — Create a user (**does not log in**)
- `POST /auth/login` — Authenticate and receive JWT
- `GET /auth/me` — Get current user (**protected**)

### Notes
- JWT is required for all protected endpoints
- Tokens must be sent as:
 ---
 - Signup and login are intentionally separate

---

## 🤖 GenAI Endpoints

### Workout Generation
- `POST /generate/workout`
- Deterministic
- Schema-driven JSON response
- Stored as structured JSON (`JSONB`)

### Diet Generation
- `POST /generate/diet`
- Deterministic
- Schema-driven JSON response
- Stored as structured JSON (`JSONB`)

### AI Coach
- `POST /coach/chat`
- `GET /coach/history`
- Context-aware (uses latest workout & diet)
- Plain text responses
- Chat history persisted per user

---

## 🗄️ Database Design

- PostgreSQL (Supabase)
- JSONB used for AI-generated plans
- Relational tables for:
- Users
- Workout plans
- Diet plans
- Coach chat messages
- Alembic manages all schema migrations

---

## 🌍 Environment Variables

Example `.env` file:

```env
DATABASE_URL=postgresql+psycopg2://...
JWT_SECRET=supersecret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

AI_MODE=mock
OPENROUTER_API_KEY=sk-...
```
