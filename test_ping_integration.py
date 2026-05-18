import os
import sys
import json
import time
from pathlib import Path
import subprocess

# Set up paths
TEST_DIR = Path(__file__).parent.absolute()
GEMINI_DIR = Path(os.path.expanduser("~/.gemini"))
ACCOUNTS_JSON = GEMINI_DIR / "google_accounts.json"
CONFIG_FILE = GEMINI_DIR / "auth_config.json"
PING_LOG = TEST_DIR / "ping_log.txt"
DUMMY_GEMINI = TEST_DIR / "dummy_gemini.py"

# Add src to path so we can import the module
sys.path.insert(0, str(TEST_DIR / "src"))
from gemini_auth_manager.cli.main import handle_ping, load_config, save_config

def setup_test():
    # Clear log
    if PING_LOG.exists():
        PING_LOG.unlink()

    # Create dummy gemini script
    with open(DUMMY_GEMINI, "w", encoding="utf-8") as f:
        f.write(f"""import json
import time
from pathlib import Path

# Simulate some startup delay that a real CLI would have
time.sleep(0.5)

ACCOUNTS_JSON = Path(r"{str(ACCOUNTS_JSON)}")
if ACCOUNTS_JSON.exists():
    with open(ACCOUNTS_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
        active = data.get('active', 'unknown')
        
    with open(r"{str(PING_LOG)}", 'a', encoding='utf-8') as log_f:
        log_f.write(f"Pinged account: {{active}}\\n")
""")

    # Update config to use dummy script
    config = load_config()
    if "auto_switch" not in config:
        config["auto_switch"] = {}
    
    # Store old command to restore later
    old_cmd = config["auto_switch"].get("ping_command")
    
    # Set to python dummy_gemini.py
    config["auto_switch"]["ping_command"] = f'"{sys.executable}" "{str(DUMMY_GEMINI)}"'
    save_config(config)
    
    return old_cmd

def run_test():
    print("Running integration test for ping race condition...")
    old_cmd = setup_test()
    
    try:
        # Force ping all to ensure it pings everything
        print("Executing handle_ping(['all'])...")
        handle_ping(['all'])
        
        # Give background processes time to finish writing to log
        print("Waiting for background processes to complete...")
        time.sleep(2)
        
        if not PING_LOG.exists():
            print("ERROR: ping_log.txt was not created!")
            return False
            
        with open(PING_LOG, 'r', encoding='utf-8') as f:
            lines = f.read().splitlines()
            
        print("\n--- Ping Log Output ---")
        for line in lines:
            print(line)
        print("-----------------------\n")
        
        # Check if all accounts pinged were the same
        accounts_pinged = [line.split(": ")[1] for line in lines if ": " in line]
        
        if len(accounts_pinged) == 0:
            print("FAILED: No accounts logged.")
            return False
            
        unique_accounts = set(accounts_pinged)
        print(f"Total pings: {len(accounts_pinged)}")
        print(f"Unique accounts pinged: {len(unique_accounts)}")
        
        if len(unique_accounts) == 1 and len(accounts_pinged) > 1:
            print("\nFAILED: Race condition detected! Multiple pings went to the SAME account because the active account was switched before background processes read the credentials.")
            return False
        elif len(unique_accounts) == len(accounts_pinged):
            print("\nPASSED: Each ping went to a distinct account.")
            return True
        else:
            print("\nFAILED: Some pings went to duplicate accounts.")
            return False
            
    finally:
        # Restore config
        config = load_config()
        if old_cmd:
            config["auto_switch"]["ping_command"] = old_cmd
        else:
            del config["auto_switch"]["ping_command"]
        save_config(config)

if __name__ == '__main__':
    success = run_test()
    sys.exit(0 if success else 1)
