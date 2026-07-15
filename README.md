# LexiSQL

> **Status: work in progress / experiment.** LexiSQL is an early exploration of a natural-language-to-SQL agent. The Python backend wires up a Gemini LLM and a LangChain SQL toolkit against a MySQL database, but the end-to-end question → SQL → results flow is **not yet functional** — the code that would run a user's question is commented out, and the frontend is still an unmodified Next.js starter. Treat this repo as a scaffold and a proof-of-plumbing, not a usable product.

## Overview

LexiSQL aims to let a user ask a database question in plain English and get an answer back as executed SQL. The `agent/` directory contains a Python script that connects to a local MySQL database, builds a LangChain `SQLDatabase` over it, and initializes Google Gemini models (both the `google-generativeai` SDK and `langchain_google_genai`) along with a `SQLDatabaseToolkit`. As currently written, running the script only connects, constructs the toolkit, and prints the available SQL tools; it does not accept a question or return an answer. The `client/` directory is a fresh `create-next-app` scaffold with no LexiSQL-specific UI yet.

## Current state (honest scope)

- **Agent (`agent/app.py`)**: Executes top to bottom on import/run. It:
  - loads environment variables via `python-dotenv`,
  - opens a `mysql.connector` connection and a SQLAlchemy engine to a local `stepout_db` database,
  - wraps the engine in a LangChain `SQLDatabase`,
  - configures a Gemini `GenerativeModel` (`gemini-pro`) and a `ChatGoogleGenerativeAI` (`gemini-1.5-pro`) with temperature/safety settings,
  - builds a `SQLDatabaseToolkit(db, llm)` and **prints its tools** (`print(toolkit.get_tools())`).
- **Not wired up**: the functions that would make it useful are commented out — `read_sql_query()` (execute cleaned SQL and pretty-print results with `tabulate`), the English-to-SQL prompt, and `generate_gemini_response()` (send question to Gemini, then execute the returned SQL). `genai.configure(...)` is also commented out. So there is no request/response loop, no CLI or HTTP interface, and no connection between the client and the agent.
- **Hardcoded credentials**: the MySQL host/user/password/database are hardcoded to a local dev setup (`localhost`, `root`, database `stepout_db`). These would need to be replaced for any other environment.
- **Client (`client/`)**: default Next.js 15 App Router starter page (`src/app/page.tsx` is the create-next-app boilerplate). No pages, API routes, or agent integration have been added.
- **`agent/vanna.ai`**: an empty placeholder file (likely a note referencing the [Vanna](https://vanna.ai) NL-to-SQL library as inspiration).

## Intended architecture (as sketched in code)

The plumbing present in `app.py` implies the following planned flow, which is only partially assembled today:

```
English question
   → Gemini LLM (google-generativeai / langchain_google_genai)
   → SQL generated (guided by LangChain SQLDatabaseToolkit + schema introspection)
   → SQL cleaned + executed against MySQL (mysql.connector / SQLAlchemy)
   → results formatted (tabulate) and returned
```

The LangChain SQL tools already instantiated (`InfoSQLDatabaseTool`, `ListSQLDatabaseTool`, `QuerySQLCheckerTool`, `QuerySQLDatabaseTool` via the toolkit) are the building blocks intended for schema discovery and query validation/execution. A separate, simpler path is also stubbed: prompt Gemini directly for SQL, strip Markdown code fences, and run it through `mysql.connector`.

## Tech stack

**Agent (`agent/requirements.txt`)**
- `google-generativeai` — Gemini SDK
- `langchain` + `langchain_google_genai` — LLM orchestration and SQL toolkit (`langchain_community` SQL utilities are imported in code)
- `mysql-connector-python` + SQLAlchemy — MySQL connectivity (imported in code)
- `python-dotenv` — environment/config loading
- `tabulate` — tabular result formatting

**Client (`client/`)**
- Next.js 15 (App Router, Turbopack dev), React 19
- TypeScript, Tailwind CSS 3, ESLint (`eslint-config-next`)

## Getting started

**Agent**
```bash
cd agent
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# set GOOGLE_API_KEY (e.g. in a .env file)
# ensure a local MySQL is running with the database referenced in app.py,
# and update the hardcoded credentials to match your setup
python app.py     # currently just connects and prints the LangChain SQL tools
```

**Client**
```bash
cd client
pnpm install       # (a pnpm-lock.yaml is checked in)
pnpm dev           # Next.js dev server on http://localhost:3000
```

## Usage

There is no working query interface yet. Running `agent/app.py` verifies that the Gemini models and the MySQL-backed LangChain toolkit initialize, and prints the tool list. To turn this into a usable NL-to-SQL agent you would need to uncomment/finish the query functions in `app.py` (or route them through the LangChain toolkit) and build a real UI in `client/`.

## Project structure

```
LexiSQL/
├── agent/                      # Python NL-to-SQL experiment (WIP)
│   ├── app.py                  # Gemini + LangChain SQL toolkit setup; main flow commented out
│   ├── requirements.txt        # google-generativeai, langchain, tabulate, dotenv
│   └── vanna.ai                # empty placeholder file
└── client/                     # Next.js 15 starter (unmodified create-next-app)
    ├── package.json            # next 15, react 19, tailwind
    ├── next.config.ts
    ├── tailwind.config.ts
    └── src/app/
        ├── layout.tsx          # default starter layout
        ├── page.tsx            # default create-next-app landing page
        └── globals.css
```
