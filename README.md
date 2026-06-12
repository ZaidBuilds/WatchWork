<div align="center">

# Action Engine

**Turn saved learning content into tracked execution plans.**

[![CI](https://github.com/zaidbuilds/action-engine/actions/workflows/ci.yml/badge.svg)](https://github.com/zaidbuilds/action-engine/actions/workflows/ci.yml)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Next.js 15](https://img.shields.io/badge/next.js-15-black.svg)](https://nextjs.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

</div>

---

## What it does

Action Engine is a local-first system that converts saved YouTube videos into actionable task plans.

1. **Capture** — Chrome extension grabs the current video
2. **Plan** — AI generates a structured action plan with tasks
3. **Execute** — Dashboard tracks progress and enforces completion before new captures

No copy-paste links. No endless watch-later lists. Just execution.

---

## Features

| Feature | Description |
|---------|-------------|
| **Browser Capture** | One-click YouTube capture via Chrome extension |
| **AI Planning** | OpenAI-powered structured action plan generation |
| **Task Tracking** | Check off tasks, track completion percentage |
| **Gatekeeper Mode** | Blocks new captures until current plan reaches threshold |
| **JWT Auth** | Secure user registration and login |
| **Rate Limiting** | Daily capture limits per user |
| **Webhooks** | Event-driven notifications for integrations |
| **Background Jobs** | Non-blocking transcript + plan processing |
| **Responsive UI** | Mobile-first dashboard with sidebar navigation |

---

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   YouTube   │────▶│   Chrome    │────▶│   FastAPI   │
│    Page     │     │  Extension  │     │     API     │
└─────────────┘     └─────────────┘     └──────┬──────┘
                                               │
                    ┌──────────────────────────┼──────────────────────────┐
                    │                          │                          │
              ┌─────▼─────┐             ┌──────▼──────┐            ┌─────▼─────┐
              │ Transcript │             │   OpenAI    │            │  SQLite   │
              │  Extractor │             │   Planner   │            │ Database  │
              └───────────┘             └─────────────┘            └───────────┘
                                               │
                                       ┌───────▼───────┐
                                       │   Next.js     │
                                       │   Dashboard   │
                                       └───────────────┘
```

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| **API** | Python 3.12, FastAPI, SQLModel, Alembic |
| **Web** | Next.js 15, React, TypeScript, Tailwind CSS |
| **Extension** | Chrome MV3, Vanilla JS |
| **Database** | SQLite (dev), PostgreSQL (prod) |
| **AI** | OpenAI GPT-4.1-mini |
| **Auth** | JWT (PyJWT + passlib/bcrypt) |
| **Testing** | pytest, FastAPI TestClient |
| **CI/CD** | GitHub Actions |
| **Container** | Docker, Docker Compose |

---

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 20+
- OpenAI API key

### 1. Clone the repo

```bash
git clone https://github.com/zaidbuilds/action-engine.git
cd action-engine
```

### 2. Start the API

```bash
cd apps/api
python -m venv .venv
source .venv/bin/activate  # Windows: .\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### 3. Start the Web Dashboard

```bash
cd apps/web
npm install
npm run dev
```

Open http://localhost:3000 and register an account.

### 4. Load the Extension

1. Open Chrome → `chrome://extensions`
2. Enable **Developer mode**
3. Click **Load unpacked** → select `apps/extension`
4. Open any YouTube video and click **Send to Action Engine**

---

## Testing

```bash
cd apps/api
python -m pytest -v
```

**39 tests** covering:
- Authentication (register, login, JWT)
- Content ingestion (capture, dedup, rate limits)
- Background jobs (process, status, auth)
- Settings (CRUD, validation)
- Webhooks (CRUD, event filtering)
- Security (URL validation)

---

## Deployment

### Docker Compose (Recommended)

```bash
# Set environment variables
export OPENAI_API_KEY=your-key
export JWT_SECRET=your-secret

# Start services
docker compose up -d
```

- API: http://localhost:8000
- Web: http://localhost:3000

### Manual Deployment

**API** (Railway, Render, Fly.io):
```bash
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Web** (Vercel):
```bash
cd apps/web
npm run build
# Deploy to Vercel
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | Database connection string | `sqlite:///./action_engine.sqlite3` |
| `OPENAI_API_KEY` | OpenAI API key | — |
| `OPENAI_MODEL` | Model to use | `gpt-4.1-mini` |
| `JWT_SECRET` | Secret for JWT signing | `change-me-in-production` |
| `FREE_DAILY_INGEST_LIMIT` | Daily capture limit | `10` |
| `FRONTEND_ORIGIN` | Allowed CORS origin | `http://localhost:3000` |

---

## Project Structure

```
action-engine/
├── apps/
│   ├── api/              # FastAPI backend
│   │   ├── app/
│   │   │   ├── main.py           # App entry, middleware, routers
│   │   │   ├── models.py         # SQLModel database models
│   │   │   ├── schemas.py        # Pydantic request/response
│   │   │   ├── auth.py           # JWT + password hashing
│   │   │   ├── config.py         # Settings via pydantic-settings
│   │   │   ├── worker.py         # Background job processor
│   │   │   ├── events.py         # Event bus
│   │   │   ├── routers/          # API endpoints
│   │   │   └── services/         # Business logic
│   │   ├── tests/                # pytest test suite
│   │   ├── alembic/              # Database migrations
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── web/              # Next.js dashboard
│   │   ├── app/                  # App router pages
│   │   ├── components/           # React components
│   │   ├── lib/                  # API client, auth context
│   │   ├── Dockerfile
│   │   └── package.json
│   └── extension/        # Chrome MV3 extension
│       ├── manifest.json
│       ├── popup.js
│       ├── content-script.js
│       └── options.html
├── docker-compose.yml
├── .github/workflows/ci.yml
└── docs/                 # Documentation
```

---

## Scale Path

This MVP is designed to grow:

1. **Swap SQLite → PostgreSQL** — Change `DATABASE_URL`, run migrations
2. **Add Redis + Celery** — Move background jobs to a queue
3. **Source connectors** — YouTube playlist sync, podcast feeds
4. **Agent review** — AI critic validates plans before saving
5. **Analytics** — Google Sheets logging for usage insights

---

## Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Run tests (`python -m pytest -v`)
4. Commit (`git commit -m 'feat: add amazing feature'`)
5. Push (`git push origin feature/amazing`)
6. Open a Pull Request

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

<div align="center">

**Built by [zaidbuilds](https://github.com/zaidbuilds)**

</div>
