from pydantic import BaseModel


class Item(BaseModel):
    text: str
    evidence_ids: list[str] = []


class Topic(BaseModel):
    topic: str
    why: str
    suggested_question: str
    evidence_ids: list[str] = []


class Analysis(BaseModel):
    summary: str
    requirements: list[Item] = []
    open_issues: list[Item] = []
    objections: list[Item] = []
    pending_decisions: list[Item] = []
    previous_discussions: list[Item] = []
    opportunities: list[Item] = []
