import requests
import json

with open('test_doc.pdf', 'rb') as f:
    files = {'file': ('test_doc.pdf', f, 'application/pdf')}
    response = requests.post('http://127.0.0.1:8000/factcheck', files=files)
    
print(f"Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"Claims extracted: {len(data.get('results', []))}")
    for i, claim in enumerate(data.get('results', []), 1):
        print(f"\n{i}. {claim['claim'][:80]}")
        print(f"   Status: {claim['status']} ({claim['confidence']})")
        print(f"   Source: {claim['source']}")
else:
    print(f"Error: {response.text}")
