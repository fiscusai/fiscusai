import os

SENTRY_DSN = os.getenv("SENTRY_DSN", "")

def enable_sentry():
    if not SENTRY_DSN:
        return False
    try:
        import sentry_sdk
        from sentry_sdk.integrations.fastapi import FastApiIntegration
        from sentry_sdk.integrations.logging import LoggingIntegration
        sentry_logging = LoggingIntegration(level=None, event_level=None)
        sentry_sdk.init(dsn=SENTRY_DSN, integrations=[FastApiIntegration(), sentry_logging], traces_sample_rate=0.05)
        return True
    except Exception:
        return False
