from app.integrations import factory


def get_meetings(date: str) -> list[dict]:
    return factory.calendar().get_meetings(date)
