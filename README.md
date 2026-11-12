<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&height=220&color=0:0B1220,50:1E3A8A,100:22D3EE&text=Natural%20Scraping%20AI&fontColor=F8FAFC&fontSize=52&fontAlignY=38&desc=Agentic%20Web%20Scraper%20Pro&descAlignY=58&descSize=20" alt="Natural Scraping AI" width="100%" />

### ⚡ Intelligent Extraction · Multi-Engine Automation · Structured Data

An asynchronous, full-stack web scraping platform with multi-engine browser automation, intelligent fallback, background workers, structured data processing, and professional Excel reports.

<br />

![Python](https://img.shields.io/badge/Python-3.12-3B82F6?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0B1220?style=for-the-badge&logo=fastapi&logoColor=22D3EE)
![Next.js](https://img.shields.io/badge/Next.js-111827?style=for-the-badge&logo=nextdotjs&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-0B1220?style=for-the-badge&logo=celery&logoColor=22D3EE)
![Redis](https://img.shields.io/badge/Redis-111827?style=for-the-badge&logo=redis&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-0B1220?style=for-the-badge&logo=playwright&logoColor=22D3EE)
![SeleniumBase](https://img.shields.io/badge/SeleniumBase-1E3A8A?style=for-the-badge&logo=selenium&logoColor=white)
![BeautifulSoup4](https://img.shields.io/badge/BeautifulSoup4-0B1220?style=for-the-badge&logo=python&logoColor=22D3EE)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-111827?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-3B82F6?style=for-the-badge&logo=docker&logoColor=white)

<br />

[**⚡ Overview**](#-project-overview) &nbsp;•&nbsp; [**✨ Features**](#-features) &nbsp;•&nbsp; [**🏗️ Architecture**](#️-architecture) &nbsp;•&nbsp; [**🚀 Quick Start**](#-quick-start) &nbsp;•&nbsp; [**🔌 API**](#-api) &nbsp;•&nbsp; [**📊 Excel Reports**](#-vip-excel-reports) &nbsp;•&nbsp; [**🛡️ Responsible Use**](#️-responsible-scraping)

</div>

<br />

## ⚡ Project Overview

**Natural Scraping AI** is a full-stack, asynchronous web scraping platform built to extract, validate, clean, and export structured data from E-Commerce and Real Estate websites.

It combines multiple browser automation engines with automatic fallback, background task processing, structured data validation, and a live dashboard—turning submitted website URLs into organized, downloadable datasets.

### 🔄 How It Works

`Website URLs` → `Next.js Dashboard` → `FastAPI` → `Celery + Redis` → `Browser Automation & Fallback` → `Data Extraction & Validation` → `Pandas Processing` → `Excel / CSV / PostgreSQL`

### 🎯 Core Capabilities

- **Multi-Engine Scraping:** Playwright, SeleniumBase UC/CDP, and Nodriver with a tiered fallback workflow.
- **Background Processing:** Celery + Redis for asynchronous scraping tasks and task-status tracking.
- **Structured Extraction:** BeautifulSoup4, Pydantic v2, and Pandas for parsing, validation, and data cleaning.
- **Live Dashboard:** Next.js interface to submit jobs, monitor progress, review summaries, and download reports.
- **Data Export:** Professionally formatted Excel and CSV reports, with optional PostgreSQL storage.
- **Website Coverage:** Dedicated E-Commerce and Real Estate parsers for supported websites.

### 🚀 Quick Launch

Run the complete platform with Docker Compose:

```bash
git clone https://github.com/mrfaizan-dev/Natural-Scraping-AI.git
cd Natural-Scraping-AI
docker compose up --build
```

Open **http://localhost:3000** to access the dashboard.

> **Prerequisite:** Docker Desktop with Docker Compose. Detailed Docker and Windows local setup instructions are available in [Quick Start](#-quick-start).

<br />

## ✨ Features

<table>
<tr>
<td width="50%" valign="top">

### 🤖 Smart Scraping

- Async **Playwright** with rotating user agents
- **SeleniumBase** UC + CDP mode processes URL batches
- **Nodriver** browser for supported sites that need another fallback
- Automatic retries and multi-tier fallback

</td>
<td width="50%" valign="top">

### ⚙️ Background Workers

- **Celery** + **Redis** task queue
- Long-running scraping jobs execute in the worker
- Task status is available to the dashboard
- Results are retained in Redis for 1 hour

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🧠 Structured Data

- **BeautifulSoup4** parsers for supported websites
- **Pydantic v2** models for products and properties
- **Pandas + NumPy** data cleaning
- Optional **PostgreSQL** storage

</td>
<td width="50%" valign="top">

### 🖥️ Live Dashboard

- **Next.js** + Tailwind CSS + Framer Motion
- Animated neural-wire canvas background
- Live task and activity status
- Summary cards and one-click downloads

</td>
</tr>
</table>

<br />

## 🌐 Supported Websites

| 🛒 E-Commerce | 🏠 Real Estate |
|:---|:---|
| Amazon | Zameen |
| eBay | Dubizzle |
| Etsy | Property Finder |
| AliExpress | Rightmove |
| Daraz | Zillow |
| Noon | — |
| Walmart | — |

> 📌 Each supported website has its own parser. Website layouts, access restrictions, and anti-bot rules can change, so extracted fields and results may vary by page and region.

<br />

## 🏗️ Architecture

```mermaid
%%{init: {"theme":"base","themeVariables":{"fontSize":"16px","lineColor":"#22D3EE","primaryTextColor":"#F8FAFC","edgeLabelBackground":"#0B1220"},"flowchart":{"nodeSpacing":35,"rankSpacing":50,"curve":"basis","padding":14}}}%%
flowchart TB
    UI["🖥️ Next.js Dashboard<br/>Submit URLs · Live Status · Downloads"]

    subgraph API["⚡ API LAYER"]
        A["FastAPI · Port 8800"]
    end

    subgraph TASKS["⚙️ TASK LAYER"]
        direction LR
        R[("Redis<br/>Broker & Results")] --> W["Celery Worker"]
    end

    subgraph BROWSER["🤖 BROWSER AUTOMATION LAYER"]
        direction LR
        P1["① Playwright"] -. "Fallback" .-> P2["② Playwright Retry"]
        P2 -. "Fallback" .-> P3["③ Nodriver"]
    end

    subgraph DATA["📊 DATA LAYER"]
        direction LR
        X["BeautifulSoup4<br/>+ Pydantic"] --> PD["Pandas<br/>+ NumPy"]
        PD --> DB[("PostgreSQL<br/>Optional")]
        PD --> XL["Excel<br/>+ CSV"]
    end

    UI ==>|"POST /scrape"| A
    A ==>|"Queue task"| R
    W ==>|"Run scraping"| P1
    P1 --> X
    P2 --> X
    P3 --> X
    A -.->|"Status & download endpoints"| UI

    classDef ui fill:#1E3A8A,stroke:#22D3EE,stroke-width:2px,color:#F8FAFC
    classDef api fill:#0B1220,stroke:#3B82F6,stroke-width:2px,color:#F8FAFC
    classDef task fill:#111827,stroke:#22D3EE,stroke-width:2px,color:#F8FAFC
    classDef browser fill:#1E293B,stroke:#64748B,stroke-width:2px,color:#F8FAFC
    classDef data fill:#0F172A,stroke:#3B82F6,stroke-width:2px,color:#F8FAFC

    class UI ui
    class A api
    class R,W task
    class P1,P2,P3 browser
    class X,PD,DB,XL data
```

**In short:** The dashboard submits URLs to FastAPI. FastAPI queues a background task through Celery and Redis. The worker runs the browser automation workflow, extracts and validates data, and processes it with Pandas. The platform then creates Excel and CSV reports and can optionally store records in PostgreSQL. The dashboard polls task status and provides report downloads.

<br />

## 🛡️ Three-Tier Fallback

| Tier | Engine | File | Used When |
|:---:|---|---|---|
| **1** | Playwright (async), with rotating user agents and 2 attempts per URL | `scraping_main.py` | Default engine for each URL |
| **2** | Playwright retry with mouse movement and slow scrolling | `scrp_retr.py` | Tier 1 returns insufficient HTML |
| **3** | Nodriver browser with page scrolling | `scraping_retr_2.py` | Tier 2 also returns insufficient content |

The scraping run is orchestrated through a SeleniumBase UC + CDP session that processes URLs in batches.

> ⚠️ Fallbacks can improve access and extraction success, but cannot guarantee access to every website. CAPTCHAs, login requirements, rate limits, and website changes may still prevent scraping.

<br />

## 🛠️ Tech Stack

| Layer | Tools |
|:---|:---|
| **Backend** | Python 3.12 · FastAPI 0.141 · Pydantic 2.13 · SQLAlchemy 2.0 |
| **Scraping & Automation** | Playwright 1.62 · SeleniumBase 4.56 · Nodriver · BeautifulSoup4 |
| **Task Queue** | Celery 5.6 · Redis |
| **Data Processing** | Pandas 3.0 · NumPy 2.5 · openpyxl · PostgreSQL |
| **Frontend** | Next.js 16 · React 19 · Tailwind CSS 4 · Framer Motion · Lucide · Axios |
| **DevOps** | Docker · Docker Compose |

<br />

## 📁 Project Structure

```text
Natural-Scraping-AI/
├── api_main.py               # FastAPI app and endpoints
├── tasks.py                  # Celery app + run_scraping task
├── scraping_main.py          # Main scraping engine (tier 1)
├── scrp_retr.py              # Playwright fallback engine (tier 2)
├── scraping_retr_2.py        # Nodriver fallback engine (tier 3)
├── extract_main.py           # Selects parsers and validates extracted data
├── sites_for_ecom.py         # E-Commerce website parsers
├── sites_for_real_estate.py  # Real Estate website parsers
├── pandas_save.py            # Cleaning, PostgreSQL, Excel, and CSV
├── pydantic_v2_main.py       # Settings + Product / RealEstate models
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── scraper-frontend/         # Next.js dashboard
    ├── app/
    │   ├── page.js
    │   ├── layout.js
    │   └── globals.css
    └── package.json
```

<br />

## 🚀 Quick Start

### 🐳 Docker (Recommended)

Docker Compose starts the frontend, FastAPI backend, Celery worker, and Redis service together.

```bash
git clone https://github.com/mrfaizan-dev/Natural-Scraping-AI.git
cd Natural-Scraping-AI
docker compose up --build
```

| Service | Container | Port |
|---|---|:---:|
| 🖥️ Frontend | `nextjs_frontend` | **3000** |
| ⚡ Backend | `fastapi_backend` | **8800** |
| ⚙️ Worker | `celery_worker` | — |
| 🧠 Redis | `redis_container` | — |

Open **http://localhost:3000** to use the dashboard. FastAPI's interactive API documentation is available at **http://localhost:8800/docs**.

Useful Docker commands:

```bash
docker compose ps          # Check running services
docker compose logs -f     # Follow service logs
docker compose logs -f celery_worker  # Follow worker logs
docker compose down        # Stop and remove containers
```

### 💻 Local Setup (Windows PowerShell)

**Requirements:** Python 3.12, Node.js, Docker Desktop (for Redis), and optionally PostgreSQL.

#### 1. Clone the repository and create the Python environment

```powershell
git clone https://github.com/mrfaizan-dev/Natural-Scraping-AI.git
cd Natural-Scraping-AI

python -m venv venv
.\venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt
playwright install chromium
```

#### 2. Start Redis

Redis is required by Celery. Start a local Redis container:

```powershell
docker run -d --name natural-scraping-redis -p 6379:6379 redis:7-alpine
```

If the container already exists, start it with:

```powershell
docker start natural-scraping-redis
```

#### 3. Run the backend services in separate terminals

Keep the Python virtual environment activated in each backend terminal.

**Terminal 1 — FastAPI:**

```powershell
uvicorn api_main:app --host 127.0.0.1 --port 8800 --reload
```

**Terminal 2 — Celery worker:**

```powershell
celery -A tasks.celery_app worker --loglevel=info --pool=solo
```

**Terminal 3 — Next.js frontend:**

```powershell
cd scraper-frontend
npm install
npm run dev
```

Open **http://localhost:3000**. The backend API is available at **http://127.0.0.1:8800**, with interactive docs at **/docs**.

> 💡 On Windows, `--pool=solo` is used for the Celery worker. For a Linux environment, use the standard worker command: `celery -A tasks.celery_app worker --loglevel=info`.

<br />

## ⚙️ Configuration

Create a `.env` file in the project root. The following settings are supported by the project:

| Variable | Purpose | Default |
|---|---|---|
| `REDIS_URL` | Celery broker and result backend | `redis://localhost:6379/0` |
| `DB_URL` | Optional PostgreSQL connection string | Empty (database saving disabled) |

Example `.env`:

```env
REDIS_URL=redis://localhost:6379/0
DB_URL=postgresql://user:password@localhost:5432/dbname
```

> 🔐 Never commit real credentials. The Docker Compose setup configures the Redis URL for its services.

<br />

## 🔌 API

Interactive API documentation is available at **`http://localhost:8800/docs`** while the backend is running.

| Method | Endpoint | Purpose |
|:---:|---|---|
| `POST` | `/scrape` | Queue a scraping task |
| `GET` | `/scrape/status/{task_id}` | Check task status and retrieve results |
| `GET` | `/scrape/downloads/{session_id}/{file_format}` | Download an Excel or CSV report |

<details>
<summary><b>📘 Request and response examples</b></summary>

<br />

**Start a task** — `scrape_type` accepts `ecommerce` or `real_estate`.

```bash
curl -X POST http://localhost:8800/scrape \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://www.daraz.pk/catalog/?q=shoes"], "scrape_type": "ecommerce"}'
```

Example response:

```json
{
  "status": "Queued",
  "message": "Scraping task has started in the background.",
  "task_id": "<task_id>",
  "status_check_url": "/scrape/status/<task_id>"
}
```

**Check task status:**

```bash
curl http://localhost:8800/scrape/status/<task_id>
```

The task status can be `PENDING`, `STARTED`, `SUCCESS`, or `FAILURE`. A successful response includes the result data; a failed response includes an error message.

**Download an Excel report:**

```bash
curl -O -J http://localhost:8800/scrape/downloads/<session_id>/xlsx
```

Use `csv` in place of `xlsx` to download the CSV report.

**Common HTTP errors:** `400` — empty URL list or missing required ID · `404` — session or file not found · `500` — task queueing failed.

</details>

<br />

## 📊 VIP Excel Reports

Every successful run produces a clean, ready-to-share **Excel** report and a **CSV** copy, saved in a per-session folder.

| Feature | Detail |
|---|---|
| 🟦 **Navy header** | Bold white text on a dark navy background |
| 🦓 **Zebra rows** | Alternating row colors for easier reading |
| 📏 **Auto widths** | Column widths adjusted for field content |
| 🔗 **Clickable links** | Product and property URLs open directly |
| ❄️ **Frozen header** | Header remains visible while scrolling |
| 🔍 **Auto filter** | Filter records directly in Excel |

<br />

## 🖥️ Dashboard Experience

1. Choose **E-Commerce** or **Real Estate** mode.
2. Paste one or more website URLs and launch a scraping task.
3. Monitor task progress and the live activity terminal.
4. Review summary cards, including total items, average price, and execution time.
5. Download the generated **Excel** or **CSV** report.

<br />

## 🗄️ Data Pipeline

```text
Website URLs
    ↓
Browser Automation
    ↓
Raw HTML
    ↓
BeautifulSoup4 Parsers
    ↓
Pydantic Validation
    ↓
Pandas + NumPy Cleaning
    ↓
Excel + CSV Reports
    ↓
Optional PostgreSQL Storage
```

When `DB_URL` is configured, the application can store extracted records in the `scraped_products` table.

<br />

## 🛡️ Responsible Scraping

- Scrape only data you are authorized to collect, and respect website terms and `robots.txt`.
- Keep request rates reasonable and avoid unnecessary load on target websites.
- Handle personal and sensitive data carefully.
- Keep API keys, passwords, and other credentials out of Git.
- Anti-bot protections, CAPTCHAs, login requirements, and website changes may prevent access or affect parser accuracy.

<br />

## 🧰 Troubleshooting

| Problem | What to Check |
|---|---|
| Task stays `PENDING` | Make sure Redis is running and the Celery worker has started successfully. |
| Dashboard cannot reach API | Confirm that FastAPI is running on port `8800` and the frontend API configuration points to it. |
| Browser fails to start | Run `playwright install chromium` inside the active virtual environment. |
| No data is saved to PostgreSQL | Check the `DB_URL` value, database availability, and table permissions. |
| Docker services fail | Run `docker compose logs -f` and inspect the failing service. |
| Redis connection error | Confirm Redis is running and `REDIS_URL` points to the correct host and port. |

<br />

## 🧭 Roadmap

- [x] Multi-engine scraping with automatic fallback
- [x] Celery + Redis background processing
- [x] E-Commerce and Real Estate parsers
- [x] Excel and CSV reporting
- [x] Live Next.js dashboard
- [ ] Scheduled scraping
- [ ] Authentication and user roles
- [ ] Additional website parsers and export formats

<br />

## 🤝 Contributing

Contributions, suggestions, and bug reports are welcome.

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-feature`.
3. Commit your changes and test them.
4. Open a pull request with a clear description.

<br />

## 👨‍💻 Author

**Created & developed by Mr Faizan**

Full-stack engineering across asynchronous scraping, browser automation, distributed task processing, and data engineering.

[![GitHub](https://img.shields.io/badge/GitHub-mrfaizan--dev-0B1220?style=for-the-badge&logo=github&logoColor=22D3EE)](https://github.com/mrfaizan-dev)

<br />

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&section=footer&height=140&color=0:22D3EE,50:1E3A8A,100:0B1220" alt="Natural Scraping AI footer" width="100%" />

### ⚡ Natural Scraping AI

**Intelligent Extraction • Distributed Automation • Data Intelligence**

*Crafted with dedication by Mr Faizan.*

</div>
