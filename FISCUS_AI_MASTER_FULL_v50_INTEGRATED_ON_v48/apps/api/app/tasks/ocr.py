import time
def process(key: str):
    # TODO: Gerçek OCR uygulanacak alan
    time.sleep(1)
    print(f"[OCR] processed: {key}")
    return {"key": key, "status": "ok"}