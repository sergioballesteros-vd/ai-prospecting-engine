import pytest

from app.infrastructure.settings import Settings
from app.modules.research.llm import (
    OpenAICompanyAnalysisProvider,
    StructuredCompanyAnalysis,
    StubCompanyAnalysisProvider,
)
from app.modules.research.website import ExtractedPage, detect_evidence, normalize_domain


def test_normalize_domain_accepts_urls_and_strips_www() -> None:
    assert normalize_domain("https://www.example.com/path") == "example.com"
    assert normalize_domain("HTTP://WWW.Example.com/") == "example.com"


def test_normalize_domain_rejects_invalid_domain() -> None:
    with pytest.raises(ValueError):
        normalize_domain("localhost")


def test_detect_evidence_records_source_and_excerpt() -> None:
    pages = [
        ExtractedPage(
            url="https://example.com/contact",
            title="Contact",
            text="Talk to our sales team through this contact form. We also use HubSpot.",
            status_code=200,
        )
    ]

    evidence = detect_evidence(pages)

    assert {item.signal_type for item in evidence} >= {"HAS_SALES_TEAM", "USES_HUBSPOT"}
    assert all(item.source_url == "https://example.com/contact" for item in evidence)
    assert all(item.content_excerpt for item in evidence)


@pytest.mark.asyncio
async def test_stub_analysis_references_existing_evidence_ids() -> None:
    class Company:
        name = "Example"
        domain = "example.com"

    class Evidence:
        id = 10
        signal_type = "USES_HUBSPOT"
        confidence = 0.8

    analysis = await StubCompanyAnalysisProvider().analyze_company(Company(), [Evidence()])

    assert analysis.observedSignals[0].evidenceIds == [10]
    assert analysis.possibleAutomationOpportunities[0].evidenceIds == [10]


@pytest.mark.asyncio
async def test_openai_analysis_uses_configured_model_and_reasoning_effort() -> None:
    class Company:
        name = "Example"
        domain = "example.com"

    class Evidence:
        id = 10
        signal_type = "USES_HUBSPOT"
        source_url = "https://example.com"
        content_excerpt = "We use HubSpot."
        confidence = 0.8

    class Responses:
        kwargs: dict

        async def parse(self, **kwargs):
            self.kwargs = kwargs

            class Response:
                output_parsed = StructuredCompanyAnalysis(
                    summary="Evidence-backed summary.",
                    observedSignals=[],
                    possibleAutomationOpportunities=[],
                    unknowns=[],
                    recommendedBuyerRoles=[],
                )

            return Response()

    class Client:
        responses = Responses()

    provider = OpenAICompanyAnalysisProvider(
        Settings(
            LLM_PROVIDER="openai",
            OPENAI_API_KEY="openai-key",
            APP_API_TOKEN="app-token",
        )
    )
    provider.client = Client()

    await provider.analyze_company(Company(), [Evidence()])

    assert provider.client.responses.kwargs["model"] == "gpt-5.4-mini"
    assert provider.client.responses.kwargs["reasoning"] == {"effort": "low"}
