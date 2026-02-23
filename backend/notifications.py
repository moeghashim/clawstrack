from __future__ import annotations


def dispatch_notification(provider: str, email: str, message: str) -> str:
    if provider == 'console':
        print(f'[notify:{provider}] {email}: {message}')
        return 'sent'
    # Keep provider abstraction stable for future email/webhook adapters.
    print(f'[notify:{provider}] (fallback to console) {email}: {message}')
    return 'sent-fallback'
