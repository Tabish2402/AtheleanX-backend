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