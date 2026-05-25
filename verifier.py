from search import search_web
import re
from datetime import datetime


def calculate_confidence(claim, evidence):
    claim_words = [w for w in re.findall(r"\w+", claim.lower()) if len(w) > 2]
    evidence_lower = evidence.lower()
    if not claim_words:
        return 10
    matches = sum(1 for w in claim_words if w in evidence_lower)
    token_score = matches / len(claim_words)

    # small bonus if numeric data appears in both
    nums_claim = re.findall(r"\d[\d,\.]*", claim)
    nums_evidence = re.findall(r"\d[\d,\.]*", evidence)
    num_bonus = 0
    if nums_claim and nums_evidence:
        common = set(nums_claim).intersection(set(nums_evidence))
        if common:
            num_bonus = 0.15

    confidence = int((token_score + num_bonus) * 100)
    return max(5, min(confidence, 99))


def _extract_numbers_and_years(text):
    nums = re.findall(r"\d[\d,\.]*", text)
    years = [int(n) for n in nums if len(n) == 4 and n.isdigit()]
    return nums, years


def verify_claim(claim, offline=True):
    # Try local KB search first
    results = search_web(claim, offline=offline)
    if results:
        best = results[0]
        evidence = best.get("body", "") or best.get("title", "")
        confidence = calculate_confidence(claim, evidence)
        status = "Verified" if confidence >= 70 else ("Inaccurate" if confidence >= 40 else "False")
        return {
            "status": status,
            "confidence": f"{confidence}%",
            "evidence": evidence,
            "source": best.get("link", "local"),
        }

    # No local evidence: fallback heuristic
    nums, years = _extract_numbers_and_years(claim)
    now = datetime.utcnow().year
    if years:
        max_year = max(years)
        if max_year > now:
            return {
                "status": "Inaccurate",
                "confidence": "25%",
                "evidence": f"Claim contains future year {max_year}. Offline heuristic flagged as inaccurate.",
                "source": "offline-heuristic",
            }
    if nums:
        return {
            "status": "Unverified",
            "confidence": "30%",
            "evidence": f"Numbers detected: {', '.join(nums)}. No offline evidence available.",
            "source": "offline-heuristic",
        }

    return {
        "status": "Unverified",
        "confidence": "10%",
        "evidence": "No offline evidence available.",
        "source": "offline-heuristic",
    }
