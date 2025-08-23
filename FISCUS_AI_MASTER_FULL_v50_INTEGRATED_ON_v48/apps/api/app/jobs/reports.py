from time import sleep
from pathlib import Path

def generate_daily_report():
    # Simulate heavy work
    sleep(1)
    out = Path(__file__).resolve().parents[1] / "data" / "daily_report.txt"
    out.write_text("Daily report OK", encoding="utf-8")
    return {"ok": True, "file": str(out)}
