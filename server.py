# server.py örnek yapı
from fastapi import FastAPI

app = FastAPI()  # Bu 'app' object'i önemli!

@app.get("/")
async def root():
    return {"message": "FISCUS AI API"}