# Gemini CLI Auth Manager

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows-yellow.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Version](https://img.shields.io/badge/version-2.3-brightgreen.svg)

**Gemini CLI Auth Manager** is a lightweight tool designed for the Google Gemini CLI environment. It supports instant multi-account switching, **automatic rotation on quota exhaustion**, and **unified account pool management**!

> 📖 [中文版本 (Chinese Version)](./README-CN.md)

---

## ✨ Features

- **Instant Switching**: Switch between multiple accounts in seconds.
- **Auto-Backup**: Automatically saves your credentials upon switching.
- **🆕 Gemini 3.1 Series Support**: Fully compatible with the latest `gemini-3.1-pro` and `gemini-3.1-flash-lite` models.
- **🆕 Intelligent Rotation Strategies**:
  - `gemini3.1-series-only` (Default): Monitors all 3.1 models.
  - `gemini3.1-pro-only`: Focuses exclusively on Pro model quota.
  - `custom`: Supports regex-based model matching.
- **Quota Pre-check**: Real-time quota monitoring via Google API, auto-switches before exhaustion (Default threshold: 10%).
- **Native OAuth Login**: One-click browser login to officially authenticate and capture accounts directly.
- **Interactive Menu**: Visual configuration interface (`gchange menu`).
- **Slash Command**: Seamlessly integrated as `/change` in Gemini CLI.

---

## 🚀 Installation

```bash
git clone https://github.com/Besty0728/Gemini-CLI-Auth-Manager.git
cd gemini-auth-manager
python install.py
```

### Dependencies
- Python 3.8+
- `requests` library (`pip install requests`)

---

## 🛠 Usage

### 1. Slash Commands (Inside Gemini CLI)
| Command | Description |
| :--- | :--- |
| `/change <n>` | Switch to account #n |
| `/change next` | Switch to the next available account |
| `/change menu` | Open the interactive management menu |
| `/change strategy` | View or change rotation strategy |
| `/change config` | Quick view of auto-switch configuration |

### 2. Terminal Commands (CMD/PowerShell)
| Command | Description |
| :--- | :--- |
| `gchange` | List all accounts and status |
| `gchange <n>` | Fast switch to account #n |
| `gchange menu` | Open interactive menu (Recommended) |
| `gchange pool login` | Add a new account via OAuth |

---

## ⚙️ Configuration

Settings are stored in `~/.gemini/auth_config.json`.

| Key | Default | Description |
| :--- | :--- | :--- |
| `strategy` | `gemini3.1-series-only` | `conservative`, `gemini3.1-pro-only`, `gemini3.1-series-only`, `custom` |
| `threshold` | `10` | Switch account when remaining quota < 10% |
| `model_pattern` | `gemini-3.1.*` | Regex pattern for model monitoring |
| `auto_restart` | `false` | Automatically restart CLI after a switch (Windows only) |

---

## 📂 Project Structure

```text
~/.gemini/
├── gemini_cli_auth_manager.py  # Core script
├── auth_config.json            # Configuration file
├── google_accounts.json        # Account index metadata
├── auth_profiles/              # Account credentials storage
│   ├── user1@gmail.com/
│   └── ...
├── hooks/
│   ├── quota_pre_check.py      # BeforeAgent Hook
│   └── quota_auto_switch.py    # AfterAgent Hook
└── commands/
    └── change.toml             # Slash command config
```

---

## 📅 Changelog

### [v2.3] - 2026-03-22
- **✨ Enhancement**: Fully updated UI and internal logic to version 2.3.
- **✨ Optimization**: Improved response speed and accuracy of quota monitoring.
- **🛠 Fix**: Resolved several residual references and display issues from v2.2.
- **🚀 Installer**: Upgraded installer for more reliable hook configurations.

### [v2.2] - 2026-02-15
- **🆕 Gemini 3.1 Support**: Added auto-rotation support for `gemini-3.1-pro` and `gemini-3.1-flash-lite`.
- **🆕 Smart Strategies**: Introduced rotation strategies like `gemini3.1-series-only`.
- **⚡ Auto-Rotation**: Implemented automatic account switching based on quota pre-checks.

---

## ❤️ Credits
Developed by Besty. Feel free to submit Issues or PRs!
