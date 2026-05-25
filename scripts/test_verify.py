import sys
from pathlib import Path

# Ensure project root is on sys.path so imports work when running from scripts/
sys.path.append(str(Path(__file__).resolve().parent.parent))

from verifier import verify_claim

print(verify_claim("OpenAI reached 200 million users in 2025"))
print(verify_claim("Unknown claim with 12345 number"))
print(verify_claim("This is a vague statement without numbers"))
