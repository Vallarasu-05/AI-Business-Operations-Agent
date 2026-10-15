from app.integrations import factory


def get_pipeline(names: list[str]) -> list[dict]:
    return factory.sheets().get_pipeline(names)
