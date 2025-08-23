from pydantic import BaseModel
class CustomerIn(BaseModel): name: str; email: str | None = None; tax_no: str | None = None
