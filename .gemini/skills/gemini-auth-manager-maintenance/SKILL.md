---
name: gemini-auth-manager-maintenance
description: Troubleshoot and maintain the Gemini-CLI-Auth-Manager tool. Trigger this skill when the user reports identical quotas across different accounts, when terminal auto-restart fails after switching accounts, when gemini CLI repeatedly asks for login despite switching, or when the user wants to cleanly remove or reset an account profile. Use it to check for shared Google Project IDs, clear local quota caches, and perform safe account deletions.
---

# Gemini-CLI-Auth-Manager Maintenance

This skill provides procedures for troubleshooting and maintaining the Gemini-CLI-Auth-Manager.

## Automated Diagnostics (Doctor Command)

The `doctor` command is the first step for any system inconsistency. It checks environment variables, scans for corrupted JSON files, clears stuck caches, and validates profile credentials.

**Command**: `gchange doctor` or `python gemini_cli_auth_manager.py doctor`

### What it performs:
1.  **System Environment Check**: Compares `GEMINI_CLIENT_ID` in the Windows Registry/Environment against `auth_config.json`.
2.  **Corrupted JSON Scan**: Scans `~/.gemini/` for empty or malformed files that crash the CLI.
3.  **Cache Validation**: Resets `mcp-oauth-tokens-v2.json` and `quota_cache.json` if they are unreadable.
4.  **Profile Integrity**: Checks `auth_profiles/` for missing or empty `oauth_creds.json`.

## Troubleshooting Persistent Login Prompts

If `gemini` CLI keeps asking to "Sign in with Google" even after you switch accounts via the manager:

### 1. Client ID Mismatch
The manager often uses a **custom Client ID** to avoid standard rate limits. If the `gemini` CLI uses its default ID, it will reject tokens issued under the custom ID.

**Solution**: Ensure the environment variables match your `auth_config.json`.
```powershell
# Set variables globally in Windows
setx GEMINI_CLIENT_ID "your_custom_client_id"
setx GEMINI_CLIENT_SECRET "your_custom_client_secret"
```
**Crucial**: You MUST restart the terminal for `setx` changes to take effect.

### 2. Checking Active Tokens
Verify which account a token *actually* belongs to (to catch accidental duplicate logins):
```python
# Run this to see the email associated with the current token
import requests
token = "..." # from ~/.gemini/oauth_creds.json
resp = requests.get("https://www.googleapis.com/oauth2/v3/userinfo", 
                    headers={"Authorization": f"Bearer {token}"})
print(resp.json().get("email"))
```

## Troubleshooting Identical Quotas

If multiple accounts show the same quota percentages, they might be linked to the same Google Cloud Project ID or the tokens are actually for the same email.

### 1. Check Project IDs
Use this Python snippet to find the Project ID associated with an account's token:

```python
import json, os, requests
from pathlib import Path

def get_project_id(email):
    p = Path(os.path.expanduser('~/.gemini/auth_profiles')) / email / 'oauth_creds.json'
    if not p.exists():
        return "Profile not found"
    
    with open(p, 'r') as f:
        creds = json.load(f)
        token = creds.get('access_token')
        
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    url = 'https://cloudcode-pa.googleapis.com/v1internal:loadCodeAssist'
    payload = {
        'metadata': {
            'ideType': 'GEMINI_CLI',
            'platform': 'WINDOWS_AMD64',
            'pluginType': 'GEMINI'
        }
    }
    
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=10)
        return resp.json().get('cloudaicompanionProject')
    except Exception as e:
        return f"Error: {e}"
```

If the Project IDs match, the accounts are sharing quotas. The user may need to re-login to force Google to assign a new project.

### 2. Silent Token Refresh (No Popup)
To refresh a token without spawning terminal windows, the manager uses direct HTTP requests to `https://oauth2.googleapis.com/token` with the `refresh_token`.

## Windows-Specific Troubleshooting

### 1. Fixing 'charmap' Encoding Errors
If hooks or scripts fail with `UnicodeEncodeError: 'charmap' codec can't encode characters` when printing emojis/UTF-8:
1.  **System-wide fix**: `setx PYTHONIOENCODING "utf-8"` (Restart terminal after).
2.  **Script-level fix**:
    ```python
    import sys
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    ```

### 2. Fixing 'WinError 2' in Hooks
Hooks (like `quota_pre_check.py`) may fail to find `gchange` because it's a `.bat` alias.
**Solution**: Use the absolute path to the manager script and the current Python executable.
```python
manager_script = Path(os.path.expanduser("~/.gemini/gemini_cli_auth_manager.py"))
subprocess.run([sys.executable, str(manager_script), "next"])
```

### 3. Fixing CLI Startup Crash (SyntaxError: Unexpected end of JSON)
The `gemini` CLI scans ALL `.json` files in `~/.gemini/`. Corrupted or empty files (e.g., failed backups) will cause a crash.
**Action**: Delete all corrupted `.json` files in the root of `~/.gemini/`.
`Remove-Item ~/.gemini/oauth_creds.backup.*.json -Force`

## Safe Account Removal (Reset)

To completely remove or reset an account:

1.  **Command**: `gchange pool remove <email>`
2.  **Manual Cleanup**:
    *   `Remove-Item -Recurse -Force ~/.gemini/auth_profiles/<target_email>`
    *   Remove entry from `~/.gemini/google_accounts.json`.
