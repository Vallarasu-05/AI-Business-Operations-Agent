"""Small synthetic benchmark over the mock data. Extend /data and add cases to grow it."""
CUSTOMER_ID_CASES = [
    {"title": "ABC Corporation - Sales Meeting", "attendees": ["john.smith@abcmfg.com"], "expected": "12345"},
    {"title": "Catch up", "attendees": ["sarah.wilson@abcmfg.com"], "expected": "12345"},
    {"title": "Intro call with ABC Corp", "attendees": ["new.person@gmail.com"], "expected": "12345"},
    {"title": "XYZ Technologies - Product Discussion", "attendees": ["priya@xyztech.io"], "expected": "67890"},
    {"title": "Weekly sync", "attendees": ["priya@xyztech.io"], "expected": "67890"},
    {"title": "Unknown prospect", "attendees": ["someone@unknown-co.com"], "expected": None},
]
RETRIEVAL_CASES = [
    {"customer_id": "12345", "query": "total price payment", "relevant": {"ABC_Proposal.txt"}},
    {"customer_id": "12345", "query": "SAML SSO data residency SAP ERP", "relevant": {"ABC_Technical_Requirements.txt"}},
    {"customer_id": "12345", "query": "action items demo notes", "relevant": {"ABC_Meeting_Notes.txt"}},
    {"customer_id": "67890", "query": "analytics suite price", "relevant": {"XYZ_Proposal.txt"}},
]
