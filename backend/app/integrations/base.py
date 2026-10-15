from typing import Protocol


class CalendarProvider(Protocol):
    def get_meetings(self, date: str) -> list[dict]: ...


class CRMProvider(Protocol):
    def find_company(self, name: str | None = None, email: str | None = None,
                     domain: str | None = None) -> dict | None: ...
    def get_context(self, company_id: str) -> dict: ...


class GmailProvider(Protocol):
    def search_emails(self, addresses: list[str], company_names: list[str]) -> list[dict]: ...


class DriveProvider(Protocol):
    def search_documents(self, names: list[str]) -> list[dict]: ...


class SheetsProvider(Protocol):
    def get_pipeline(self, names: list[str]) -> list[dict]: ...
