STEP 47 PATCH — Canary Deploy, Webhook Replay Guard, Grafana Dashboard, Restore Script, Status UI

Apply by copying these folders into repo root. Then:
- Include `csp_dashboard` router in FastAPI if not already.
- (Optional) Use `WebhookGuard` in your payment webhook handlers.
- Import Grafana dashboard JSON.
- Use canary manifests (NGINX or Istio) in your cluster.
