<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.136-009688?logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/ChromaDB-Vector_DB-FF6B6B" />
  <img src="https://img.shields.io/badge/LLM-OpenAI_Compatible-7C3AED" />
  <img src="https://img.shields.io/badge/License-MIT-green" />
</div>

---

# 🤖 AI Job Agent

### Semantic RAG-Powered Autonomous Job Discovery Engine

AI Job Agent is a **production-grade Retrieval-Augmented Generation (RAG)** platform that autonomously scrapes thousands of job listings from multiple sources, embeds them into a vector database, and semantically matches them to your resume. It generates AI-powered match explanations, personalized cover letters, and delivers real-time alerts — all through a professional editorial-grade web interface.

> **"Stop searching. Jobs find you."**

---

## 🧠 How the RAG Pipeline Works

```
                          ┌──────────────────────┐
                          │     YOUR RESUME      │
                          │     (PDF Upload)     │
                          └──────────┬───────────┘
                                     │
                    ┌────────────────▼────────────────┐
                    │        RETRIEVAL ENGINE          │
                    │                                  │
                    │  pypdf → Skills → Profile        │
                    │  sentence-transformers (384d)     │
                    │  ChromaDB Vector Search          │
                    │  Cosine Similarity Ranking        │
                    └────────────────┬────────────────┘
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         │                           │                           │
         ▼                           ▼                           ▼
┌─────────────────┐    ┌─────────────────────┐    ┌─────────────────┐
│  KNOWLEDGE BASE  │    │    HYBRID RANKING    │    │   GENERATION    │
│                  │    │                      │    │                 │
│  RemoteOK        │    │  60% Semantic Sim    │    │  Match Explain  │
│  Greenhouse (20) │    │  40% Keyword Overlap │    │  Cover Letter   │
│  Lever           │    │  + Experience Boost  │    │  Job Summary    │
│  WeWorkRemotely  │    │                      │    │  (Groq/Llama)   │
│                  │    │                      │    │                 │
│  2,800+ jobs/run │    └─────────────────────┘    └─────────────────┘
└─────────────────┘
```

---

## 🏗 Full System Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                     INGESTION PIPELINE                            │
│                                                                   │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐      │
│  │ SCRAPERS  │──►│NORMALIZER│──►│  DOMAIN  │──►│ENRICHMENT│      │
│  │           │   │          │   │  FILTER  │   │          │      │
│  │ RemoteOK  │   │Validate  │   │70+ Tech  │   │Tech Stack│      │
│  │ Greenhouse│   │Required  │   │Signals   │   │Experience│      │
│  │ Lever     │   │Fields    │   │Word-Bound│   │Level     │      │
│  │ WWR       │   │          │   │ary Check │   │Detection │      │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘      │
│                                                      │           │
│       ┌──────────┐    ┌──────────┐    ┌──────────┐   │           │
│       │  ALERTS  │◄───│ DEDUP    │◄───│ SCORING  │◄──┘           │
│       │          │    │          │    │          │               │
│       │Telegram  │    │By Link   │    │User Prefs│               │
│       │Top-5     │    │Early-Term│    │Priority  │               │
│       │Candidate │    │          │    │Keywords  │               │
│       │Profile   │    └──────────┘    └──────────┘               │
│       └──────────┘                                               │
│                                                      │           │
│       ┌──────────────────────────────────────────┐   │           │
│       │           DUAL DATABASE WRITE             │◄──┘           │
│       │                                           │               │
│       │  ┌────────────────┐  ┌────────────────┐  │               │
│       │  │  PostgreSQL     │  │   ChromaDB      │  │               │
│       │  │  (Source Truth) │  │  (Vector Index) │  │               │
│       │  │  Job Data       │  │  384-dim Embed  │  │               │
│       │  └────────────────┘  └────────────────┘  │               │
│       └──────────────────────────────────────────┘               │
└──────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                             │
│                                                                   │
│  ┌────────────────┐  ┌────────────────┐  ┌────────────────┐     │
│  │   FastAPI       │  │   React 19     │  │   Background    │     │
│  │   Backend       │  │   Frontend     │  │   Scheduler     │     │
│  │                 │  │                │  │                 │     │
│  │ JWT Auth        │  │ Editorial UI   │  │ APScheduler     │     │
│  │ Email Verify    │  │ Playfair+Inter │  │ Every 12 hrs    │     │
│  │ Profile Mgmt    │  │ Cream+Navy     │  │ Auto-Cleanup    │     │
│  │ Apply Tracking  │  │ Responsive     │  │ Email Alerts    │     │
│  │ Semantic Search │  │ Dash+Jobs+Prof │  │ Scraper Run     │     │
│  └────────────────┘  └────────────────┘  └────────────────┘     │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🛠 Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Backend Framework** | FastAPI 0.136 | High-performance async API |
| **Frontend** | React 19 + Vite + Tailwind | Modern SPA with custom design system |
| **Database** | PostgreSQL 16 | ACID-compliant source of truth |
| **ORM** | SQLAlchemy 2.0 | Type-safe database operations |
| **Vector Database** | ChromaDB (Persistent) | 384-dim embedding storage & search |
| **Embedding Model** | `all-MiniLM-L6-v2` | 384-dimensional semantic vectors |
| **LLM Integration** | Groq / OpenAI / Ollama | Match explanation + cover letters |
| **Authentication** | JWT + bcrypt + OAuth2 | Secure, stateless auth |
| **Scraping** | Playwright + requests + BS4 | Headless browser + API calls |
| **Notifications** | Telegram Bot API + Gmail SMTP | Multi-channel alerts |
| **Scheduling** | APScheduler | Automated pipeline execution |
| **PDF Parsing** | pypdf | Resume text extraction |

---

## ✨ Key Features

### 🔍 Semantic Job Discovery (RAG)
- Upload your resume → AI extracts 16+ skills, domains, experience level
- Resume text is embedded into 384-dimensional vector using `sentence-transformers`
- ChromaDB performs cosine similarity search across all scraped jobs
- Hybrid ranking: 60% semantic similarity + 40% keyword overlap + experience boost
- Natural language search: *"python backend intern remote India"* finds exactly what you mean

### 📊 Multi-Source Scraping
| Source | Type | Companies | Jobs/Run |
|--------|------|-----------|:---:|
| RemoteOK | Web Scraping (Playwright) | All remote jobs | ~50 |
| Greenhouse | REST API | 20 companies (Stripe, Airbnb, Discord, Figma...) | ~2,300 |
| Lever | REST API | Spotify, Palantir | ~388 |
| We Work Remotely | Web Scraping (Playwright) | All remote jobs | ~48 |
| **Total** | | | **~2,800** |

### 🎯 Intelligent Filtering Pipeline
- **Domain Filter**: 70+ required tech signals with word-boundary checking (prevents "ai" matching "campaign")
- **Relevance Filter**: 15+ irrelevant keyword blocks (sales, legal, HR)
- **Enrichment**: Auto-detects tech stack (30+ technologies), experience level, years required
- **Scoring Engine**: Multi-signal with user preferences + priority keyword tiers + experience detection
- **Deduplication**: By unique apply link with early-termination optimization

### 🤖 LLM-Powered Features
- **Match Explanation**: *"This role matches you because you both have Python and FastAPI skills. It's entry-level, matching your student status."*
- **Cover Letter Generation**: 3-paragraph personalized drafts using Groq's Llama 3.1 (free tier)
- **Job Summarization**: Condenses 2,000+ word descriptions into 3-5 bullet points
- **OpenAI-Compatible Pattern**: Same code works with Groq (free), OpenAI (paid), or Ollama (local)

### 📱 Professional Web Interface
- **Editorial Design System**: Cream `#F8F4F1` + Navy `#14213D` + Orange `#E97B42` accents
- **Typography**: Playfair Display (headings) + Inter (body) — agency-quality
- **Responsive**: Mobile-first with smooth transitions
- **Dashboard**: Real-time pipeline stats, AI recommendations, applied job tracking
- **Jobs Page**: Semantic/KW toggle, AI-powered search, today's jobs filter
- **Profile Page**: Full professional profile with multi-resume upload + auto-fill

### 🔔 Real-Time Alerts
- Telegram notifications for top-5 personalized matches per pipeline run
- Candidate profile-aware: alerts use hybrid matching against your resume
- Email confirmation on job application
- Falls back to keyword scoring when no resume profile exists

### 📈 Application Tracking
- Mark jobs as "Applied" with one click
- Dashboard shows recent applications with dates
- Applied jobs persist for 15 days (auto-cleanup)
- Unapplied jobs auto-delete after 5 days

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.10+** — [Download](https://www.python.org/downloads/)
- **Node.js 18+** — [Download](https://nodejs.org/)
- **PostgreSQL 16** — [Download](https://www.postgresql.org/download/)

### 1. Clone & Setup Backend

```bash
git clone https://github.com/aniketkag45/job-agent.git
cd job-agent

# Create virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Setup Environment Variables

```bash
cp .env.example .env
```

Fill in your `.env`:

```env
# Database
DATABASE_URL=postgresql://jobagent:jobagent123@localhost:5432/jobagent

# Auth
SECRET_KEY=your_random_secret_key_here

# Telegram Notifications
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# LLM (Groq — free, fast)
LLM_API_KEY=gsk_your_groq_key
LLM_BASE_URL=https://api.groq.com/openai/v1
LLM_MODEL=llama-3.1-8b-instant

# Email (Gmail SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SMTP_FROM_EMAIL=your_email@gmail.com

# Frontend URL (for email verification redirects)
FRONTEND_URL=http://localhost:5173
```

### 3. Setup PostgreSQL

```bash
# Create the database
psql -U postgres -c "CREATE DATABASE jobagent;"

# Initialize tables
python -c "from app.services.database import init_db; init_db()"
```

### 4. Setup Frontend

```bash
cd frontend
npm install
```

### 5. Launch

**Terminal 1 — Backend:**
```bash
uvicorn app.api.main:app --reload
```
→ API running at `http://localhost:8000` | Docs at `http://localhost:8000/docs`

**Terminal 2 — Frontend:**
```bash
cd frontend && npm run dev
```
→ Frontend at `http://localhost:5173`

### 6. Start Scraping

```bash
python scripts/run_job_pipeline.py
```

The pipeline runs automatically every 12 hours via APScheduler. First run fetches ~2,800 jobs.

---

## 🎯 Quick Feature Walkthrough

| Feature | How To Use |
|---------|-----------|
| **Semantic Search** | Jobs page → toggle "AI" → type "python backend intern remote" |
| **Personalized Matching** | Upload resume → Dashboard shows AI recommendations matched to YOUR skills |
| **Today's Jobs** | Jobs page → toggle "Today" → see only jobs from last 24 hours |
| **Hybrid Match Score** | `/jobs/for-me` — combines semantic similarity + your skills |
| **Apply Tracking** | Jobs page → click "Track" on any job → appears in Dashboard "Applied" section |
| **Cover Letters** | API: `GET /jobs/{id}/cover-letter`, requires LLM configured |
| **Match Explanation** | API: `GET /jobs/{id}/explain`, requires resume uploaded |

---

## 📁 Project Structure

```
job-agent/
├── app/
│   ├── api/                    # FastAPI application
│   │   ├── main.py             # App entry, middleware, CORS
│   │   └── routes/             # 5 route modules
│   │       ├── auth.py         # Signup, login, verify-email
│   │       ├── jobs.py         # CRUD, search, semantic, apply
│   │       ├── profile.py      # GET/PUT user profile
│   │       ├── resume.py       # Upload, list, activate, delete
│   │       └── agent_overview.py
│   ├── auth/                   # JWT, bcrypt, dependencies
│   ├── core/                   # Middleware, exceptions
│   ├── notifier/               # Telegram bot integration
│   ├── schemas/                # Pydantic models
│   ├── scraper/                # 4 job scrapers
│   │   ├── remoteok_scraper.py
│   │   ├── greenhouse_scraper.py
│   │   ├── lever_scraper.py
│   │   └── weworkremotely_scraper.py
│   ├── services/               # 20 business logic modules
│   │   ├── database.py         # SQLAlchemy ORM (6 models)
│   │   ├── embedding_service.py
│   │   ├── vector_store.py     # ChromaDB CRUD
│   │   ├── job_matcher.py      # Hybrid ranking engine
│   │   ├── llm_service.py      # OpenAI-compatible LLM
│   │   ├── email_service.py    # Gmail SMTP
│   │   ├── job_filter.py       # Multi-signal scoring
│   │   ├── job_domain_filter.py
│   │   └── ...                 # Enrichment, dedup, normalize
│   └── utils/
├── frontend/
│   └── src/
│       ├── pages/              # 8 pages (Dashboard, Jobs, Profile...)
│       ├── components/         # Navbar, JobCard, ResumeUpload
│       ├── sections/           # Landing page (Hero, Features, CTA...)
│       ├── context/            # Auth + SavedJobs state
│       └── api/                # Axios HTTP client
├── scripts/
│   └── run_job_pipeline.py     # Main scraper pipeline
├── config/
│   └── user_preferences.json
├── requirements.txt
└── README.md
```

---

## 🧪 Testing

```bash
# Test PostgreSQL connection
python -c "from app.services.database import engine; engine.connect(); print('OK')"

# Test embedding service
python -c "from app.services.embedding_service import generate_embedding; e=generate_embedding('test'); print(len(e))"

# Test vector store
python -c "from app.services.vector_store import get_collection_stats; print(get_collection_stats())"

# Run single scraper
python -c "from app.scraper.lever_scraper import fetch_lever_jobs; print(len(fetch_lever_jobs()))"

# Run full pipeline
python scripts/run_job_pipeline.py

# API health check
curl http://localhost:8000/
```

---

## 🔑 Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| `all-MiniLM-L6-v2` (384-dim) | Fast CPU inference (~50ms), strong semantic quality, 80MB model — perfect for single-server deployment |
| ChromaDB Persistent | Survives restarts, zero cloud cost, Python-native, no Docker dependency |
| Hybrid Ranking (60/40) | Pure semantic can't break ties between similar roles (0.52 vs 0.51). Keyword overlap adds explicit skill signal |
| OpenAI-Compatible LLM | One code pattern. Swap between Groq (free, 7B params), OpenAI (paid, GPT-4o), or Ollama (local) by changing 2 env vars |
| Lazy Singleton Models | Embedding model (100MB) loaded once at first use, not at import. Saves ~3s startup + memory |
| Playwright for Dynamic Sites | Modern job boards are JS-rendered SPAs. `requests` returns empty pages. Playwright handles full browser context |
| PostgreSQL over SQLite | MVCC enables concurrent scraper writes + API reads. JSONB for preference storage. Production-standard |

---

## 📊 Performance

| Metric | Value |
|--------|:---:|
| Jobs per pipeline run | **~2,800** |
| Pipeline duration | ~7 minutes |
| Semantic search latency | <100ms |
| Embedding generation | ~50ms per text |
| Vector DB query | ~5ms for top-10 |
| LLM explanation | ~2s (Groq) |

---

## 🗺 Roadmap

- [ ] **Google OAuth** — Social login integration
- [ ] **Docker Deployment** — One-command production deploy
- [ ] **Auto-Apply Engine** — Playwright form-filling for Greenhouse/Lever-style ATS
- [ ] **More Scrapers** — Expand Lever companies, add Indeed RSS, YC Jobs
- [ ] **Advanced Analytics** — Application funnel, response rate tracking
- [ ] **Slack/Discord Alerts** — Multi-channel notification support
- [ ] **Alembic Migrations** — Proper DB versioning
- [ ] **CI/CD Pipeline** — GitHub Actions for testing + deployment

---

## 🤝 Contributing

This is a learning project built to master full-stack AI engineering. If you have ideas, improvements, or want to collaborate:

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit your changes
4. Push and open a Pull Request

---

## 📄 License

MIT — built for learning, sharing, and growing. Use it, modify it, ship it.

---

<div align="center">
  <br/>
  <p><strong>Built with ❤️ by <a href="https://github.com/aniketkag45">Aniket Kag</a></strong></p>
  <p>AI Engineer • Full-Stack Developer • Builder</p>
  <br/>
</div>