import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.application import campaigns
from app.domain.models import Base, Evidence, Opportunity
from app.modules.discovery.providers import CompanyCandidate, DiscoveryCriteria
from app.modules.research.website import evidence_fingerprint


class FakeProvider:
    provider_name = "fake"

    async def discover(self, criteria: DiscoveryCriteria) -> list[CompanyCandidate]:
        return [
            CompanyCandidate(
                name="Training One",
                domain="https://www.training-one.example/",
                website_url="https://www.training-one.example/",
                industry=criteria.industries[0],
                country=criteria.country,
                city=criteria.city_or_region,
                source="fake",
                source_url="memory://fake",
                metadata={"index": 1},
            ),
            CompanyCandidate(
                name="Training One Duplicate",
                domain="training-one.example",
                website_url="https://training-one.example",
                industry=criteria.industries[0],
                country=criteria.country,
                city=criteria.city_or_region,
                source="fake",
                source_url="memory://fake",
                metadata={"index": 2},
            ),
            CompanyCandidate(
                name="Training Fail",
                domain="training-fail.example",
                website_url="https://training-fail.example",
                industry=criteria.industries[0],
                country=criteria.country,
                city=criteria.city_or_region,
                source="fake",
                source_url="memory://fake",
                metadata={"index": 3},
            ),
        ]


@pytest.mark.asyncio
async def test_campaign_deduplicates_domains_tracks_partial_failures_and_scores(
    monkeypatch,
) -> None:
    db = _session()
    opportunity = _opportunity()
    db.add(opportunity)
    db.commit()
    campaign = campaigns.create_campaign(
        db,
        name="Training companies in Madrid",
        country="Spain",
        city_or_region="Madrid",
        industries=["training companies"],
        employee_min=10,
        employee_max=150,
        opportunity_id=opportunity.id,
        target_company_count=10,
    )

    async def fake_research(
        session: Session, company_id: int, campaign_id: int | None = None
    ) -> None:
        company = session.get(campaigns.Company, company_id)
        if company and "fail" in company.domain:
            raise RuntimeError("website timeout")
        session.add_all(
            [
                _evidence(company_id, "HAS_CRM", 0.8),
                _evidence(company_id, "MULTIPLE_CONTACT_FORMS", 0.75),
                _evidence(company_id, "HAS_SALES_TEAM", 0.7),
            ]
        )
        session.commit()

    monkeypatch.setattr(campaigns, "SessionLocal", lambda: db)
    monkeypatch.setattr(campaigns, "research_company", fake_research)

    await campaigns.run_campaign(campaign.id, provider=FakeProvider())
    refreshed = campaigns.campaign_detail(db, campaign.id)
    stats = campaigns.campaign_stats(refreshed)

    assert refreshed.status == "COMPLETED"
    assert stats["discovered"] == 2
    assert stats["researched"] == 1
    assert stats["failed"] == 1
    assert stats["qualified"] == 1
    assert any(entry.error == "website timeout" for entry in refreshed.companies)
    successful = [entry for entry in refreshed.companies if entry.research_state == "RESEARCHED"][0]
    assert successful.company.opportunity_scores[0].total_score > 0


def test_campaign_state_starts_as_draft() -> None:
    db = _session()
    opportunity = _opportunity()
    db.add(opportunity)
    db.commit()

    campaign = campaigns.create_campaign(
        db,
        name="Training companies in Madrid",
        country="Spain",
        city_or_region="Madrid",
        industries=["training companies"],
        employee_min=10,
        employee_max=150,
        opportunity_id=opportunity.id,
        target_company_count=20,
    )

    assert campaign.status == "DRAFT"
    assert campaign.started_at is None
    assert campaign.completed_at is None


def test_discovery_provider_abstraction() -> None:
    provider = FakeProvider()

    assert provider.provider_name == "fake"
    assert callable(provider.discover)


def _session() -> Session:
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine, expire_on_commit=False)()


def _opportunity() -> Opportunity:
    return Opportunity(
        name="Sales Operations Automation",
        market={
            "country": "Spain",
            "company_size": {"min": 10, "max": 150},
            "industries": ["training companies"],
        },
        desired_signals=["HAS_CRM"],
        excluded_industries=["energy"],
        weights={"icp": 0.30, "pain": 0.30, "value": 0.20, "intent": 0.10, "reachability": 0.10},
    )


def _evidence(company_id: int, signal_type: str, confidence: float) -> Evidence:
    return Evidence(
        company_id=company_id,
        signal_type=signal_type,
        source_url="https://training-one.example",
        content_excerpt=f"Public evidence for {signal_type}",
        fingerprint=evidence_fingerprint(
            signal_type, "https://training-one.example", f"Public evidence for {signal_type}"
        ),
        confidence=confidence,
        evidence_metadata={"test": True},
    )
