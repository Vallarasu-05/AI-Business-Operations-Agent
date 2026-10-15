SOURCE_PRIORITY = {
    "crm": 5,
    "internal_document": 4,
    "gmail": 4,
    "sheets": 4,
    "memory": 3,
    "company_website": 3,
    "web_search": 2,
}
EXTERNAL_SOURCES = {"web_search", "company_website"}


def priority(source: str) -> int:
    return SOURCE_PRIORITY.get(source, 1)
