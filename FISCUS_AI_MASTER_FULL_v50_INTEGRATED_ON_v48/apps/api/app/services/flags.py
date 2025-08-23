import os

def get_flags():
    # Simple env-driven flags
    return {
        "AI_PANEL_ENABLED": os.getenv("FF_AI_PANEL", "1") == "1",
        "BILLING_ENABLED": os.getenv("FF_BILLING", "1") == "1",
        "RECON_RULES_ENABLED": os.getenv("FF_RECON_RULES", "1") == "1",
    }
