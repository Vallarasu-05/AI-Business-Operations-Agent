from app.integrations.google.auth import service
from app.integrations.google.docs import export_doc_text


class GoogleDrive:
    def search_documents(self, names: list[str], limit: int = 10) -> list[dict]:
        drive = service("drive", "v3")
        q = " or ".join(f"name contains '{n.replace(chr(39), '')}'" for n in names if n)
        files = drive.files().list(q=f"({q}) and trashed=false", pageSize=limit,
                                   fields="files(id,name,mimeType)").execute().get("files", [])
        out = []
        for f in files:
            if f["mimeType"] == "application/vnd.google-apps.document":
                out.append({"id": f["id"], "name": f["name"], "text": export_doc_text(f["id"])})
            # TODO: download + extract PDFs/DOCX (see rag.ingestion.extract_text)
        return out
