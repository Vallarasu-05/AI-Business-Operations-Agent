from app.integrations import factory


def find_company(name=None, email=None, domain=None):
    return factory.crm().find_company(name=name, email=email, domain=domain)


def get_context(company_id: str) -> dict:
    return factory.crm().get_context(company_id)
