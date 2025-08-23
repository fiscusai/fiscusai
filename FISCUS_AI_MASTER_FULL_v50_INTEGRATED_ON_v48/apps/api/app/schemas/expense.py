from pydantic import BaseModel
from datetime import date
class ExpenseIn(BaseModel): title: str; amount: float; date: date; category: str | None = None
