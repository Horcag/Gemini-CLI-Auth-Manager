---
name: gemini-account-lifecycle
description: Manage the lifecycle of Google accounts used with the Gemini CLI. Use this skill when a user creates new accounts, sees "No project ID returned" errors, or encounters "0.0%" quota on fresh accounts. It covers initialization steps and trust-building requirements for heavy models.
---

# Gemini Account Lifecycle Management

Google accounts used with the Gemini CLI go through an initialization and trust-building process before they gain full access to all models.

## Initializing a New Account

Newly registered Google accounts may return an error: `Error: No project ID returned` when checking quotas or using API-based tools. This is because the underlying "Cloud Code Assist" project hasn't been created yet.

### Step-by-Step Initialization
1.  **Switch to the New Account**:
    `gchange <new_account_email>`
2.  **Start Gemini CLI Interactively**:
    `gemini`
3.  **Accept Terms of Service**:
    If prompted, type `Y` or `Enter` to agree to the Gemini CLI Terms of Service.
4.  **Perform a Test Query**:
    Ask a simple question like `hello`.
5.  **Wait for Response**:
    Google initializes the hidden internal project during this first successful interactive query. 
6.  **Verify Quota**:
    Run `gchange doctor` or `View Quota` menu option to confirm the Project ID is now detected.

## Understanding Quota Limits (Pro vs. Flash)

New accounts often have different default quotas:
-   **Flash / Flash-Lite Models**: Usually available immediately at ~100% capacity.
-   **Pro Models (1.5 Pro, 3.1 Pro)**: Often show **0.0%** quota on "fresh" accounts.

### Why 0.0% Quota?
Google's anti-abuse system limits "heavy" (Pro) models for newly registered accounts to prevent account farming.

### How to Gain Pro Access:
1.  **Trust (Age/Activity)**: Use the account naturally for a few days (search, Gmail, YouTube). Accounts with a linked phone number gain trust faster.
2.  **Subscription**: Activating a "Gemini Advanced" trial or a paid Workspace subscription immediately unlocks full Pro quotas.
3.  **Region**: Quotas vary by region; some regions have lower availability for Pro models.

## Safe Registration Tips

To avoid chain-bans or phone verification loops when creating multiple accounts:
1.  **Mobile Data**: Use LTE/4G from a phone instead of home Wi-Fi when registering.
2.  **Incognito Mode**: Use a clean incognito window for each registration.
3.  **Avoid Gmail Sub-addressing**: While `email+alias@gmail.com` works for incoming mail, Google's anti-fraud system links these accounts instantly. Use distinct recovery emails or phone numbers.
