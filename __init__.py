# Bu klasör bir Python paketi olarak tanınsın diye __init__.py dosyası.
# Gerekirse burada import kısayolları tanımlanabilir.

# Örnek: main.py’deki FastAPI app’i üst seviyeden import edilebilir olsun.
try:
    from .main import app
except ImportError:
    # Bu klasörde main yoksa sessizce geç
    pass
