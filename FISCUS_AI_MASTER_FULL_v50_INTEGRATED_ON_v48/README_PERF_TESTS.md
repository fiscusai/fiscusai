# Test & Load Test

## Pytest (API)
```bash
pytest -q
```

## k6 (smoke)
```bash
# Install k6, then:
API_URL=http://localhost:8000 k6 run perf/smoke.js
```