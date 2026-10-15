from app.integrations import factory


def search_documents(names: list[str]) -> list[dict]:
    return factory.drive().search_documents(names)
