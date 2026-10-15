from pydantic import BaseModel


class Attendee(BaseModel):
    name: str
    email: str


class Meeting(BaseModel):
    event_id: str
    title: str
    date: str
    start: str
    end: str
    location: str | None = None
    attendees: list[Attendee]
