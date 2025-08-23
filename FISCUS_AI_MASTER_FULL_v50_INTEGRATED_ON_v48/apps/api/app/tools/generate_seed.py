import json, random
from datetime import date, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parents[1] / "data"
INV = BASE / "demo_invoices.json"

def rand_date(start: date, days: int) -> str:
    return (start + timedelta(days=random.randint(0, days))).isoformat()

def main(n=500, orgs=('ORG-ALPHA','ORG-BETA')):
    start = date(2024,8,1)
    items = []
    for i in range(n):
        total = round(random.uniform(250, 15000), 2)
        vat = round(total * random.choice([0.1, 0.18]), 2)
        items.append({
            "id": f"I-{1000+i}",
            "number": f"INV-{1000+i}",
            "customer": random.choice(["Aurea Ltd.","Legera A.Ş.","Tributa Tech","Faber SRL"]),
            "date": rand_date(start, 365+31),
            "total": total,
            "vat": vat,
            "organization_id": random.choice(orgs)
        })
    INV.write_text(json.dumps(items, indent=2), encoding="utf-8")
    print(f"Wrote {len(items)} invoices to {INV}")

if __name__ == "__main__":
    main()
