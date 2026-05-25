import requests
import json

# Test GET /kb
r = requests.get('http://127.0.0.1:8000/kb')
print(f'GET /kb Status: {r.status_code}')
ct = r.headers.get('content-type')
print(f'Content-Type: {ct}')
data = r.json()
print(f'KB entries: {len(data)}')
for entry in data:
    print(f'  - {entry["claim"][:60]}')

# Test POST /kb with new entry
new_kb = data + [
    {
        'claim': 'Test claim: AI is advancing rapidly',
        'evidence': 'AI models are improving every year',
        'source': 'test'
    }
]
r = requests.post('http://127.0.0.1:8000/kb', json=new_kb)
print(f'\nPOST /kb Status: {r.status_code}')
print(f'Response: {r.json()}')

# Test GET /kb again to verify persistence
r = requests.get('http://127.0.0.1:8000/kb')
data = r.json()
print(f'\nGET /kb after POST - KB entries: {len(data)}')
if len(data) > 2:
    print('✓ Persistence verified - new entry saved')
