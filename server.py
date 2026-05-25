import ast
import io
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from extractor import extract_claims
from utils import extract_pdf_text
from verifier import verify_claim

load_dotenv()

app = FastAPI(
    title="TruthLayer AI Backend",
    description="API backend for PDF fact-checking and claim verification",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIST = BASE_DIR / "frontend" / "dist"

DATA_DIR = BASE_DIR / "data"
KB_PATH = DATA_DIR / "knowledge.json"


@app.get("/kb")
def get_kb():
    if not KB_PATH.exists():
        return []
    try:
        import json

        with open(KB_PATH, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            return data
    except Exception:
        raise HTTPException(status_code=500, detail="Unable to read knowledge base")


@app.post("/kb")
def save_kb(payload: list = Body(...)):
    # payload expected to be a list of objects {claim,evidence,source}
    try:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        import json

        with open(KB_PATH, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, ensure_ascii=False)
        return {"status": "ok", "count": len(payload)}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unable to save knowledge base: {exc}")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/factcheck")
async def factcheck(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Please upload a PDF file.")

    pdf_bytes = await file.read()

    try:
        text = extract_pdf_text(pdf_bytes)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Unable to read PDF: {exc}")

    claims_text = extract_claims(text)
    try:
        claims = ast.literal_eval(claims_text)
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Claim extraction failed to return a valid list: {exc}",
        )

    if not isinstance(claims, list):
        raise HTTPException(
            status_code=500,
            detail="Claim extraction output was not a Python list.",
        )

    results = []
    for claim in claims:
        verification = verify_claim(claim)
        results.append(
            {
                "claim": claim,
                "status": verification["status"],
                "confidence": verification["confidence"],
                "evidence": verification["evidence"],
                "source": verification["source"],
            }
        )

    return {"results": results}


if FRONTEND_DIST.exists():
    app.mount("/assets", StaticFiles(directory=str(FRONTEND_DIST / "assets")), name="assets")


@app.get("/")
async def root():
    if FRONTEND_DIST.exists():
        return FileResponse(FRONTEND_DIST / "index.html")
    raise HTTPException(status_code=404, detail="Not Found")


@app.get("/{full_path:path}")
async def spa_fallback(full_path: str):
    if FRONTEND_DIST.exists():
        return FileResponse(FRONTEND_DIST / "index.html")
    raise HTTPException(status_code=404, detail="Not Found")
