from app.integrations import factory


def search_emails(addresses: list[str], company_names: list[str]) -> list[dict]:
    return factory.gmail().search_emails(addresses, company_names)
