from pydantic import BaseModel


class Customer(BaseModel):
    company_id: str | None
    name: str
    domain: str | None = None
    industry: str | None = None
    employees: int | None = None
    aliases: list[str] = []
    emails: list[str] = []
    matched_via: str = ""
    confidence: float = 0.0
