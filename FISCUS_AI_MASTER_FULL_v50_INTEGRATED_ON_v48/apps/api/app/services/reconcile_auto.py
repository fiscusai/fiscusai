
from typing import List, Dict, Any, Tuple
from datetime import datetime, timedelta

def auto_match(transactions: List[Dict[str,Any]], invoices: List[Dict[str,Any]], rules: Dict[str,Any]):
    desc_rules = [r.lower() for r in rules.get("desc_rules", [])]
    tol_days = int(rules.get("tolerance_days", 5))
    tol_amt = float(rules.get("amount_tolerance", 1.0))
    matches, partials, unmatched = [], [], []

    inv_map = { (i.get("id") or i.get("number")): i for i in invoices }
    # helper to parse date
    def d(dstr):
        try:
            return datetime.fromisoformat(dstr.replace("Z","+00:00")).date()
        except Exception:
            return None

    for t in transactions:
        tdesc = (t.get("description") or "").lower()
        tdate = d(t.get("date") or "")
        tamt = float(t.get("amount") or 0)
        found = None
        # 1) description hint
        for key, inv in inv_map.items():
            if any(rule in tdesc for rule in desc_rules) or (inv.get("number","").lower() in tdesc):
                # date tolerance
                idate = d(inv.get("date") or "")
                date_ok = True
                if tdate and idate:
                    date_ok = abs((tdate - idate).days) <= tol_days
                amt_ok = abs(float(inv.get("amount") or 0) - tamt) <= tol_amt
                if amt_ok and date_ok:
                    found = ("full", inv); break
                # partial if smaller amount and near
                if tamt < float(inv.get("amount") or 0) and date_ok:
                    found = ("partial", inv); break
        if found:
            ftype, inv = found
            diff = float(inv.get("amount") or 0) - tamt
            item = {
                "tx_id": t.get("id"),
                "invoice_id": inv.get("id") or inv.get("number"),
                "type": ftype,
                "amount": tamt,
                "invoice_amount": float(inv.get("amount") or 0),
                "diff_amount": round(diff,2),
                "org": inv.get("org") or inv.get("organization_id"),
            }
            if ftype == "full":
                matches.append(item)
            else:
                partials.append(item)
        else:
            unmatched.append(t)
    return {"matches": matches, "partials": partials, "unmatched": unmatched}
