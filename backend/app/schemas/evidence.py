from pydantic import BaseModel


class Evidence(BaseModel):
    claim: str
    source: str  # crm | gmail | internal_document | sheets | web_search | memory
    source_id: str
    date: str | None = None
    confidence: float = 0.8
    topic: str = "general"
    value: float | str | None = None
    id: str | None = None


class Conflict(BaseModel):
    topic: str
    values: list[dict]
    groups: list[dict] = []
    note: str
    highest_priority_source: str | None = None
