import json
from pathlib import Path
import re
from difflib import SequenceMatcher

DATA_DIR = Path(__file__).resolve().parent / "data"
KB_PATH = DATA_DIR / "knowledge.json"


def _load_local_knowledge():
    if not KB_PATH.exists():
        return []
    try:
        with open(KB_PATH, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def _token_overlap_score(a, b):
    a_tokens = set(re.findall(r"\w+", a.lower()))
    b_tokens = set(re.findall(r"\w+", b.lower()))
    if not a_tokens or not b_tokens:
        return 0.0
    inter = a_tokens.intersection(b_tokens)
    return len(inter) / max(len(a_tokens), len(b_tokens))


def _fuzzy_ratio(a, b):
    return SequenceMatcher(None, a, b).ratio()


def search_web(query, offline=True, min_score=0.18):
    """
    Offline-first search using local KB. Returns results sorted by a combined
    fuzzy/token-overlap score. `min_score` filters weak matches.
    """
    local_kb = _load_local_knowledge()
    if not local_kb:
        return []

    results = []
    q = query.strip()
    for entry in local_kb:
        claim = entry.get("claim", "")
        evidence = entry.get("evidence", "")
        combined = f"{claim} {evidence}"

        # Scoring: weighted combination of fuzzy match on claim and token overlap
        fuzzy = _fuzzy_ratio(q.lower(), claim.lower())
        overlap = _token_overlap_score(q, combined)
        score = 0.6 * fuzzy + 0.4 * overlap

        if score >= min_score:
            results.append({
                "title": claim[:120],
                "body": evidence,
                "link": entry.get("source", "local"),
                "trusted": True,
                "score": score,
            })

    results.sort(key=lambda r: r.get("score", 0), reverse=True)
    return results
