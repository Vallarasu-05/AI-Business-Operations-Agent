from datetime import datetime
from sqlalchemy import JSON, DateTime, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class AgentRun(Base):
    __tablename__ = "agent_runs"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    request: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    steps: Mapped[list] = mapped_column(JSON, default=list)
    briefing: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    quality: Mapped[dict | None] = mapped_column(JSON, nullable=True)


class Approval(Base):
    __tablename__ = "approvals"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(String(64))
    decision: Mapped[str] = mapped_column(String(16))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
