<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&height=220&color=0:0B1220,50:1E3A8A,100:22D3EE&text=Natural%20Scraping%20AI&fontColor=F8FAFC&fontSize=52&fontAlignY=38&desc=Agentic%20Web%20Scraper%20Pro&descAlignY=58&descSize=20" alt="Natural Scraping AI" width="100%"/>

### ⚡ Intelligent Extraction · Multi-Engine Automation · Structured Data

An async, full-stack scraping platform with background workers, three-tier browser fallback and premium Excel reports.

<br/>

![Python](https://img.shields.io/badge/Python-3.12-3B82F6?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0B1220?style=for-the-badge&logo=fastapi&logoColor=22D3EE)
![Next.js](https://img.shields.io/badge/Next.js-111827?style=for-the-badge&logo=nextdotjs&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-0B1220?style=for-the-badge&logo=celery&logoColor=22D3EE)
![Redis](https://img.shields.io/badge/Redis-111827?style=for-the-badge&logo=redis&logoColor=white)
![Playwright](https://img.shields.io/badge/Playwright-0B1220?style=for-the-badge&logo=playwright&logoColor=22D3EE)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-111827?style=for-the-badge&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-3B82F6?style=for-the-badge&logo=docker&logoColor=white)

<br/>

[**✨ Features**](#-features) &nbsp;•&nbsp; [**🏗️ Architecture**](#️-architecture) &nbsp;•&nbsp; [**🚀 Quick Start**](#-quick-start) &nbsp;•&nbsp; [**🔌 API**](#-api) &nbsp;•&nbsp; [**📊 Excel Reports**](#-vip-excel-reports) &nbsp;•&nbsp; [**🛡️ Responsible Use**](#️-responsible-scraping)

</div>

<br/>

## ✨ Features

<table>
<tr>
<td width="50%" valign="top">

### 🤖 Smart Scraping
- Async **Playwright** with rotating user agents
- **SeleniumBase** UC + CDP mode runs the batches
- **Nodriver** stealth browser for heavy, protected sites
- Auto retries, then automatic fallback

</td>
<td width="50%" valign="top">

### ⚙️ Background Workers
- **Celery** + **Redis** queue
- API never blocks while scraping
- Live task status for the dashboard
- Results kept in Redis for 1 hour

</td>
</tr>
<tr>
<td width="50%" valign="top">

### 🧠 Structured Data
- **BeautifulSoup4** parsers per website
- **Pydantic** models for products and properties
- **Pandas + NumPy** cleaning
- Optional **PostgreSQL** storage

</td>
<td width="50%" valign="top">

### 🖥️ Live Dashboard
- **Next.js** + Tailwind + Framer Motion
- Neural wire canvas background
- Live agent activity terminal
- Summary cards and one-click downloads

</td>
</tr>
</table>

<br/>

## 🌐 Supported Websites

| 🛒 E-Commerce | 🏠 Real Estate |
|:---|:---|
| Amazon | Zameen |
| eBay | Dubizzle |
| Etsy | Property Finder |
| AliExpress | Rightmove |
| Daraz | Zillow |
| Noon | |
| Walmart | |

> 📌 Each site has its own parser. Website layouts and anti-bot rules change over time, so extracted fields and results can vary by page and region.

<br/>

## 🏗️ Architecture

```mermaid
flowchart LR
    subgraph UI["🖥️ Presentation"]
        F["Next.js Dashboard"]
    end

    subgraph API["⚡ API Layer"]
        A["FastAPI :8800"]
    end

    subgraph Q["⚙️ Task Layer"]
        R[("Redis")]
        W["Celery Worker"]
    end

    subgraph B["🤖 Browser Layer"]
        P1["1. Playwright"]
        P2["2. Playwright Stealth"]
        P3["3. Nodriver"]
    end

    subgraph D["📊 Data Layer"]
        X["BeautifulSoup4 + Pydantic"]
        PD["Pandas + NumPy"]
        DB[("PostgreSQL")]
        XL["Excel + CSV"]
    end

    F -- "POST /scrape" --> A
    A -- "queue task" --> R
    R --> W
    W --> P1
    P1 -. "blocked or too short" .-> P2
    P2 -. "still failing" .-> P3
    P1 --> X
    P2 --> X
    P3 --> X
    X --> PD
    PD --> DB
    PD --> XL
    F -. "poll /scrape/status" .-> A
    A -. "result from Redis" .-> F
    XL -. "download" .-> F
```

**In short:** the dashboard sends URLs → FastAPI queues a Celery task through Redis → the worker scrapes → parsers structure the data → Pandas cleans it and saves Excel, CSV and (optionally) PostgreSQL → the dashboard polls the status and offers downloads.

<br/>

## 🛡️ Three-Tier Fallback

| Tier | Engine | File | Used when |
|:---:|---|---|---|
| **1** | Playwright (async) with random user agents, 2 attempts per URL | `scraping_main.py` | Default for every URL |
| **2** | Playwright with human-like mouse move and slow scroll | `scrp_retr.py` | Tier 1 returns too little HTML |
| **3** | Nodriver stealth browser with page scroll | `scraping_retr_2.py` | Tier 2 also falls short |

The whole run sits inside a SeleniumBase UC + CDP session that processes URLs in batches.

> ⚠️ Fallbacks improve success rates but cannot guarantee access to every website.

<br/>

## 🛠️ Tech Stack

| Layer | Tools |
|:---|:---|
| **Backend** | Python 3.12 · FastAPI 0.141 · Pydantic 2.13 · SQLAlchemy 2.0 |
| **Scraping** | Playwright 1.62 · SeleniumBase 4.56 · Nodriver · BeautifulSoup4 |
| **Queue** | Celery 5.6 · Redis |
| **Data** | Pandas 3.0 · NumPy 2.5 · openpyxl · PostgreSQL |
| **Frontend** | Next.js 16 · React 19 · Tailwind CSS 4 · Framer Motion · Lucide · Axios |
| **DevOps** | Docker · Docker Compose |

<br/>

## 📁 Project Structure

```text
Natural-Scraping-AI/
├── api_main.py               # FastAPI app and endpoints
├── tasks.py                  # Celery app + run_scraping task
├── scraping_main.py          # Main scraping engine (tier 1)
├── scrp_retr.py              # Fallback engine (tier 2)
├── scraping_retr_2.py        # Nodriver engine (tier 3)
├── extract_main.py           # Picks the right parser, validates data
├── sites_for_ecom.py         # E-commerce parsers
├── sites_for_real_estate.py  # Real estate parsers
├── pandas_save.py            # Cleaning, PostgreSQL, Excel, CSV
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

<br/>

## 🚀 Quick Start

### 🐳 Docker (recommended)

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

Open **http://localhost:3000** and start scraping.

```bash
docker compose ps         # check services
docker compose logs -f    # live logs
docker compose down       # stop everything
```

### 💻 Local setup

**Requirements:** Python 3.12, Node.js, Redis (PostgreSQL is optional).

```bash
# Backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

# Terminal 1: API
uvicorn api_main:app --port 8800

# Terminal 2: Worker
celery -A tasks.celery_app worker --loglevel=info

# Terminal 3: Frontend
cd scraper-frontend
npm install
npm run dev
```

<br/>

## ⚙️ Configuration

Create a `.env` file in the project root (all values are optional):

| Variable | Purpose | Default |
|---|---|---|
| `REDIS_URL` | Celery broker and result backend | `redis://localhost:6379/0` |
| `DB_URL` | PostgreSQL connection string. If empty, database saving is skipped | empty |

```env
REDIS_URL=redis://localhost:6379/0
DB_URL=postgresql://user:password@localhost:5432/dbname
```

> 🔐 Never commit real credentials. The Docker setup already sets `REDIS_URL` for you.

<br/>

## 🔌 API

Interactive docs are available at **`/docs`** while the backend is running.

| Method | Endpoint | Purpose |
|:---:|---|---|
| `POST` | `/scrape` | Queue a scraping task |
| `GET` | `/scrape/status/{task_id}` | Check status and get results |
| `GET` | `/scrape/downloads/{session_id}/{file_format}` | Download `xlsx` or `csv` |

<details>
<summary><b>📘 Request and response examples</b></summary>

<br/>

**Start a task** — `scrape_type` is `ecommerce` or `real_estate`

```bash
curl -X POST http://localhost:8800/scrape \
  -H "Content-Type: application/json" \
  -d '{"urls": ["https://www.daraz.pk/catalog/?q=shoes"], "scrape_type": "ecommerce"}'
```

```json
{
  "status": "Queued",
  "message": "Scraping task has started in the background.",
  "task_id": "<task_id>",
  "status_check_url": "/scrape/status/<task_id>"
}
```

**Check status**

```bash
curl http://localhost:8800/scrape/status/<task_id>
```

`status` is `PENDING`, `STARTED`, `SUCCESS` or `FAILURE`. On success the response includes `data` (the dashboard reads `user_session_id` from it), on failure it includes `error`.

**Download a report**

```bash
curl -O -J http://localhost:8800/scrape/downloads/<session_id>/xlsx
```

Use `csv` for CSV; any other value returns the Excel file.

**Errors:** `400` empty URL list or missing ID · `404` session or file not found · `500` queueing failed.

</details>

<br/>

## 📊 VIP Excel Reports

Every run produces a clean, ready-to-share **Excel** file and a **CSV** copy, saved in a per-session folder.

| Feature | Detail |
|---|---|
| 🟦 **Navy header** | Bold white text on dark navy |
| 🦓 **Zebra rows** | Alternating row colors for easy reading |
| 📏 **Auto widths** | Column sizes tuned per field type |
| 🔗 **Clickable links** | Product and property URLs open directly |
| ❄️ **Frozen header** | Header stays visible while scrolling |
| 🔍 **Auto filter** | Filter any column in one click |

<br/>

## 🖥️ Dashboard Experience

1. Choose **E-Commerce** or **Real Estate** mode
2. Paste one or more URLs and launch the agent
3. Watch live status and the **agent activity terminal**
4. Review summary cards: total items, average price, execution time
5. Download the **Excel** or **CSV** report

<br/>

## 🗄️ Data Pipeline

`Raw HTML` → `BeautifulSoup parser` → `Pydantic model` → `Pandas cleaning` → `Excel + CSV` (+ `PostgreSQL` when `DB_URL` is set)

When a database URL is configured, rows are appended to the `scraped_products` table.

<br/>

## 🛡️ Responsible Scraping

- Scrape only data you are allowed to collect, and respect website terms and `robots.txt`
- Keep request rates reasonable
- Handle personal data carefully
- Keep API keys and passwords out of Git
- Anti-bot protections and CAPTCHAs can still block requests, and site layout changes can break parsers

<br/>

## 🧰 Troubleshooting

| Problem | Try this |
|---|---|
| Task stays `PENDING` | Make sure Redis and the Celery worker are running |
| Dashboard cannot reach API | Backend must run on port `8800` |
| Browser fails to start | Run `playwright install chromium` |
| No data saved to PostgreSQL | Check that `DB_URL` is set correctly |
| Docker issues | Run `docker compose logs -f` |

<br/>

## 🧭 Roadmap

- [x] Multi-engine scraping with fallback
- [x] Celery + Redis background processing
- [x] E-commerce and real estate parsers
- [x] Excel and CSV reports
- [x] Live Next.js dashboard
- [ ] Scheduled scraping *(planned)*
- [ ] Authentication and user roles *(planned)*
- [ ] More websites and export formats *(planned)*

<br/>

## 🤝 Contributing

1. Fork the repository
2. Create a branch: `git checkout -b feature/my-feature`
3. Commit and test your changes
4. Open a pull request

<br/>

## 👨‍💻 Author

**Created & developed by Mr Faizan**

Full-stack engineering across async scraping, browser automation, distributed processing and data engineering.

[![GitHub](https://img.shields.io/badge/GitHub-mrfaizan--dev-0B1220?style=for-the-badge&logo=github&logoColor=22D3EE)](https://github.com/mrfaizan-dev)

<br/>

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&section=footer&height=140&color=0:22D3EE,50:1E3A8A,100:0B1220" alt="footer" width="100%"/>

### ⚡ Natural Scraping AI

**Intelligent Extraction • Distributed Automation • Data Intelligence**

*Crafted with dedication by Mr Faizan.*

</div>
