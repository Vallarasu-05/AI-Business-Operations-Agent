from pydantic import BaseModel


class EmailMessage(BaseModel):
    thread_id: str
    subject: str
    sender: str
    to: list[str]
    date: str
    body: str
