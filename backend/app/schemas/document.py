from pydantic import BaseModel


class Document(BaseModel):
    id: str
    name: str
    text: str
