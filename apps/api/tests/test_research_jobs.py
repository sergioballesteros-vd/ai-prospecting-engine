from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.application.research_jobs import create_research_job, get_research_job
from app.domain.models import Base, Company


def test_research_job_state_is_persisted(monkeypatch) -> None:
    db = _session()
    company = Company(
        name="Example",
        domain="example.com",
        website_url="https://example.com",
    )
    db.add(company)
    db.commit()

    monkeypatch.setattr("app.application.research_jobs.SessionLocal", lambda: _SameSession(db))

    job = create_research_job(company.id, db)
    loaded = get_research_job(job.id)

    assert loaded is not None
    assert loaded.id == job.id
    assert loaded.company_id == company.id
    assert loaded.status == "queued"


def _session() -> Session:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, expire_on_commit=False)()


class _SameSession:
    def __init__(self, db: Session) -> None:
        self.db = db

    def __enter__(self) -> Session:
        return self.db

    def __exit__(self, *args: object) -> None:
        return None
