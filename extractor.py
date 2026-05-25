import re


def fallback_claim_extraction(text: str) -> str:
    # Split into candidate sentences and score them by evidence-like features
    sentences = re.split(r"(?<=[.!?])\s+", text)
    candidates = []
    claim_pattern = re.compile(
        r"\b(?:\d[\d,]*(?:\.\d+)?(?:%| billion| million| trillion|k|m|bn|km|kg|years?|year|USD|\$|€|£)|\d{4})\b",
        re.IGNORECASE,
    )

    for sentence in sentences:
        s = sentence.strip()
        if not s or len(s) < 20:
            continue
        score = 0
        # presence of numbers/percent/years increases score
        if claim_pattern.search(s):
            score += 3
        # longer sentences that look like claims
        score += min(max(len(s) / 80, 0), 2)
        # presence of typical claim verbs
        if re.search(r"\b(reported|estimated|reaches|reached|is worth|is estimated|grew|declined|increased|decreased)\b", s, re.IGNORECASE):
            score += 2

        if score > 0:
            candidates.append((score, s.replace('"', "'")))

    # sort by score desc and dedupe
    candidates.sort(key=lambda x: x[0], reverse=True)
    seen = set()
    claims = []
    for _, sent in candidates:
        if sent in seen:
            continue
        seen.add(sent)
        claims.append(sent)
        if len(claims) >= 12:
            break

    # fallback: take first substantive sentence
    if not claims:
        for s in sentences:
            s2 = s.strip()
            if len(s2) > 30:
                claims = [s2.replace('"', "'")]
                break

    return repr(claims)


def extract_claims(text: str) -> str:
    return fallback_claim_extraction(text)
