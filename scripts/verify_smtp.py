"""Verify Gmail SMTP credentials by sending a test email to yourself.
Run locally with the same env vars GitHub Actions uses:
    set GMAIL_USER=noha@nozaklabs.com         (Windows cmd)
    set GMAIL_APP_PASSWORD=xxxxxxxxxxxxxxxx
    python scripts/verify_smtp.py

PowerShell:
    $env:GMAIL_USER="noha@nozaklabs.com"
    $env:GMAIL_APP_PASSWORD="xxxxxxxxxxxxxxxx"
    python scripts/verify_smtp.py

Unix/macOS:
    export GMAIL_USER=noha@nozaklabs.com
    export GMAIL_APP_PASSWORD=xxxxxxxxxxxxxxxx
    python scripts/verify_smtp.py
"""

from __future__ import annotations

import os
import smtplib
import sys
from datetime import datetime, timezone
from email.message import EmailMessage


def main() -> int:
    user = os.environ.get("GMAIL_USER")
    pw   = os.environ.get("GMAIL_APP_PASSWORD")

    if not user or not pw:
        print("❌ Missing GMAIL_USER or GMAIL_APP_PASSWORD in environment.")
        return 1

    msg = EmailMessage()
    msg["Subject"] = "🛰️ Radar SMTP verification"
    msg["From"]    = user
    msg["To"]      = user
    msg.set_content(
        f"If you're reading this, Gmail SMTP works.\n"
        f"Sent at {datetime.now(timezone.utc).isoformat()} UTC.\n"
        f"Next: merge v2-email-digest, then trigger the workflow manually."
    )

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, timeout=15) as smtp:
            smtp.login(user, pw)
            smtp.send_message(msg)
    except smtplib.SMTPAuthenticationError:
        print("❌ Authentication failed. Common causes:")
        print("   • App Password is wrong or revoked")
        print("   • 2FA isn't enabled on the Google account")
        print("   • You pasted your real Google password, not the 16-char app password")
        return 2
    except (smtplib.SMTPException, OSError) as e:
        print(f"❌ SMTP send failed: {type(e).__name__}: {e}")
        return 3

    print(f"✅ Test email sent to {user}. Check inbox (and spam).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
