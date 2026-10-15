from app.integrations.google.auth import service


def export_doc_text(file_id: str) -> str:
    data = service("drive", "v3").files().export(fileId=file_id, mimeType="text/plain").execute()
    return data.decode("utf-8", "ignore") if isinstance(data, bytes) else str(data)
