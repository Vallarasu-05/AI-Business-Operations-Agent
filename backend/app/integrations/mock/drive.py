from pathlib import Path
from app.config import settings
from app.rag.ingestion import extract_text


class MockDrive:
    def search_documents(self, names: list[str]) -> list[dict]:
        prefixes = {n.split()[0].lower() for n in names if n}
        out = []
        for p in sorted((Path(settings.data_dir) / "sample_documents").iterdir()):
            if p.is_file() and any(p.name.lower().startswith(x) for x in prefixes):
                out.append({"id": p.name, "name": p.name, "text": extract_text(p)})
        return out
