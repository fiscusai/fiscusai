from typing import List, Dict
from statistics import mean, stdev
def summarize(invoices: List[Dict], expenses: List[Dict]) -> str:
    total_rev = sum(i['total'] for i in invoices if i['status'] in ('sent','paid'))
    total_exp = sum(e['amount'] for e in expenses); profit = total_rev - total_exp
    return f"Toplam gelir: ₺{total_rev:,.2f}, gider: ₺{total_exp:,.2f}, kâr: ₺{profit:,.2f}".replace(',', '.')
def anomaly(expenses: List[Dict]) -> List[Dict]:
    if len(expenses) < 3: return []; amounts = [e['amount'] for e in expenses]
    mu = mean(amounts); sd = stdev(amounts) if len(amounts)>1 else 0
    return [{"id":e["id"],"amount":e["amount"],"reason":"Olası aykırı harcama (2σ)"} for e in expenses if sd and abs(e["amount"]-mu)>2*sd]
def forecast_cash(invoices: List[Dict], expenses: List[Dict]) -> List[Dict]:
    net = sum(i['total'] for i in invoices if i['status'] in ('sent','paid')) - sum(e['amount'] for e in expenses)
    avg = net/3 if net else 0; return [{"period":"P1","cash":avg},{"period":"P2","cash":avg},{"period":"P3","cash":avg}]
