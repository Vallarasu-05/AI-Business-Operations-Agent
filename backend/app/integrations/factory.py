"""Chooses the provider implementation from DATA_MODE. The agent never knows which one it uses."""
from app.config import settings


def calendar():
    if settings.is_mock:
        from app.integrations.mock.calendar import MockCalendar
        return MockCalendar()
    from app.integrations.google.calendar import GoogleCalendar
    return GoogleCalendar()


def crm():
    if settings.is_mock:
        from app.integrations.mock.crm import MockCRM
        return MockCRM()
    from app.integrations.hubspot.crm import HubSpotCRM
    return HubSpotCRM()


def gmail():
    if settings.is_mock:
        from app.integrations.mock.gmail import MockGmail
        return MockGmail()
    from app.integrations.google.gmail import GoogleGmail
    return GoogleGmail()


def drive():
    if settings.is_mock:
        from app.integrations.mock.drive import MockDrive
        return MockDrive()
    from app.integrations.google.drive import GoogleDrive
    return GoogleDrive()


def sheets():
    if settings.is_mock:
        from app.integrations.mock.sheets import MockSheets
        return MockSheets()
    from app.integrations.google.sheets import GoogleSheets
    return GoogleSheets()
