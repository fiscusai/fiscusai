# Webhook Receiver Example

A minimal FastAPI server that validates `X-Webhook-Signature` and prints events.

```
pip install fastapi uvicorn
WEBHOOK_SECRET=your-secret uvicorn app:app --reload --port 8081
```
Then set `WEBHOOK_URL=http://localhost:8081/webhook/fiscus` in main project.