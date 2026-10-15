from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings

_url = settings.database_url or f"sqlite:///{Path(settings.output_dir) / 'agent.db'}"
Path(settings.output_dir).mkdir(parents=True, exist_ok=True)
engine = create_engine(_url, future=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def init_db() -> None:
    from app.db.models import Base
    Base.metadata.create_all(engine)
