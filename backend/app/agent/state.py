import operator
from typing import Annotated, TypedDict


class AgentState(TypedDict, total=False):
    user_request: str
    intent: dict
    meetings: list
    selected_meeting: dict
    customer: dict

    # raw research results (written by parallel nodes, one key each)
    crm_data: dict
    email_data: list
    document_data: list
    sheet_data: list
    web_data: list

    # reducers let parallel nodes append safely
    evidence: Annotated[list, operator.add]
    errors: Annotated[list, operator.add]

    validated_evidence: list
    conflicts: list
    memory: dict

    analysis: dict
    risks: list
    recommended_topics: list
    briefing: dict
    briefing_markdown: str
    quality: dict
    retries: int

    email_draft: dict
    approval_status: str
    delivery: dict
