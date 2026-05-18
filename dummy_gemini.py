import json
import time
from pathlib import Path

# Simulate some startup delay that a real CLI would have
time.sleep(0.5)

ACCOUNTS_JSON = Path(r"C:\Users\nikit\.gemini\google_accounts.json")
if ACCOUNTS_JSON.exists():
    with open(ACCOUNTS_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
        active = data.get('active', 'unknown')
        
    with open(r"C:\Users\nikit\Gemini-CLI-Auth-Manager\ping_log.txt", 'a', encoding='utf-8') as log_f:
        log_f.write(f"Pinged account: {active}\n")
