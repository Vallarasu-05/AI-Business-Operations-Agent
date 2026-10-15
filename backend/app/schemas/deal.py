from pydantic import BaseModel


class Deal(BaseModel):
    id: str
    name: str
    amount: float
    currency: str = "INR"
    stage: str
    close_date: str | None = None
    probability: float | None = None
