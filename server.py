# server.py
try:
    from app.main import app           # apps/api/app/main.py içindeki 'app'
except ModuleNotFoundError:
    from FISCUS_AI_MASTER_FULL_v50_INTEGRATED_ON_v48.apps.api.app.main import app
