def test_list_invoices_q_sort(client):
    # seed
    from app.routers.v2_invoices import INMEM
    INMEM.clear()
    INMEM.extend([
        {"id":"1","number":"INV-001","customer":"Aurea","date":"2025-08-01","total":100},
        {"id":"2","number":"INV-010","customer":"Legera","date":"2025-08-05","total":80},
        {"id":"3","number":"INV-002","customer":"Tributa","date":"2025-08-03","total":120},
    ])
    r = client.get("/v2/invoices/?q=INV-0")
    assert r.status_code == 200 and len(r.json()) == 3
    r = client.get("/v2/invoices/?q=Aurea")
    assert len(r.json()) == 1
    r = client.get("/v2/invoices/?sort=total:desc")
    js = r.json()
    assert js[0]["total"] >= js[-1]["total"]
