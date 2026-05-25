# TruthLayer AI

AI-powered PDF fact-checking application with a React frontend and FastAPI backend.

## Features
- Upload PDFs
- Extract factual claims using Gemini
- Verify claims using live web search
- Download CSV fact-check reports

## Tech Stack
- React + Vite
- FastAPI
- Offline claim extraction and verification
- Python

## Setup

1. Copy `.env.example` to `.env` and add your Gemini API key:
   ```bash
   copy .env.example .env
   ```
2. Install backend dependencies:
   ```bash
   python -m pip install -r requirement.txt
   ```
3. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   cd ..
   ```
4. Build the React app:
   ```bash
   cd frontend
   npm run build
   cd ..
   ```
5. Start the unified app:
   ```bash
   uvicorn server:app --host 0.0.0.0 --port 8000
   ```

Then open the app at `http://localhost:8000`.

## Offline mode

This project supports an offline mode that does not require Internet access. When offline, the app uses a local knowledge base to verify claims and falls back to simple heuristics when no matching evidence is found.

- Add facts to the local knowledge base at `data/knowledge.json`. The file should be a JSON array of objects with keys: `claim`, `evidence`, `source`.

Example `data/knowledge.json`:

```json
[
   {
      "claim": "OpenAI reached 200 million users in 2025",
      "evidence": "OpenAI reported reaching 200 million users in public communications in 2025.",
      "source": "local"
   }
]
```

With `data/knowledge.json` populated, the app will run and verify using only local data and heuristics — no external network calls are required.

## Usage

- Open the app in the browser at `http://localhost:8000`.
- Upload a PDF file.
- Review extracted claims, verification status, evidence, and source.
- Download a CSV fact-check report.
- Use the Local Knowledge Base editor to add or update `claim`, `evidence`, and `source` entries for offline verification.
