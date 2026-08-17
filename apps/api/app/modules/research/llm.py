from typing import Protocol

from openai import AsyncOpenAI
from pydantic import BaseModel, Field

from app.domain.models import Company, Evidence
from app.infrastructure.settings import Settings


class ObservedSignal(BaseModel):
    signalType: str
    reasoning: str
    confidence: float = Field(ge=0, le=1)
    evidenceIds: list[int]


class PossibleAutomationOpportunity(BaseModel):
    problem: str
    reasoning: str
    confidence: float = Field(ge=0, le=1)
    evidenceIds: list[int]


class StructuredCompanyAnalysis(BaseModel):
    summary: str
    observedSignals: list[ObservedSignal]
    possibleAutomationOpportunities: list[PossibleAutomationOpportunity]
    unknowns: list[str]
    recommendedBuyerRoles: list[str]


class CompanyAnalysisProvider(Protocol):
    provider_name: str
    model_name: str

    async def analyze_company(
        self, company: Company, evidence: list[Evidence]
    ) -> StructuredCompanyAnalysis: ...


class StubCompanyAnalysisProvider:
    provider_name = "stub"
    model_name = "deterministic-local"

    async def analyze_company(
        self, company: Company, evidence: list[Evidence]
    ) -> StructuredCompanyAnalysis:
        observed = [
            ObservedSignal(
                signalType=item.signal_type,
                reasoning="Detected from public website evidence.",
                confidence=item.confidence,
                evidenceIds=[item.id],
            )
            for item in evidence[:8]
        ]
        evidence_ids = [item.id for item in evidence[:3]]
        opportunities = []
        if evidence_ids:
            opportunities.append(
                PossibleAutomationOpportunity(
                    problem="Lead routing or follow-up process complexity",
                    reasoning=(
                        "Public signals suggest acquisition or contact workflows may exist. "
                        "This should be validated with the company before making any claim."
                    ),
                    confidence=0.45,
                    evidenceIds=evidence_ids,
                )
            )
        return StructuredCompanyAnalysis(
            summary=(
                f"{company.name} has public website evidence that can be reviewed for possible "
                "automation or integration opportunities. The analysis is limited to observable "
                "website content and does not assert internal process problems."
            ),
            observedSignals=observed,
            possibleAutomationOpportunities=opportunities,
            unknowns=[
                "Current CRM or operational system configuration",
                "Lead volume and response-time requirements",
                "Whether existing processes are manual or automated",
            ],
            recommendedBuyerRoles=["CEO", "COO", "Head of Sales", "Head of Operations"],
        )


class OpenAICompanyAnalysisProvider:
    provider_name = "openai"

    def __init__(self, settings: Settings) -> None:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai")
        self.model_name = settings.openai_model
        self.reasoning_effort = settings.openai_reasoning_effort
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def analyze_company(
        self, company: Company, evidence: list[Evidence]
    ) -> StructuredCompanyAnalysis:
        evidence_payload = [
            {
                "id": item.id,
                "signalType": item.signal_type,
                "sourceUrl": item.source_url,
                "excerpt": item.content_excerpt,
                "confidence": item.confidence,
            }
            for item in evidence[:30]
        ]
        response = await self.client.responses.parse(
            model=self.model_name,
            input=[
                {
                    "role": "system",
                    "content": (
                        "Analyze only the supplied public evidence. Never invent internal company "
                        "processes. Distinguish observation from inference. Every observed signal "
                        "and possible opportunity must reference evidenceIds. Prefer uncertainty."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        f"Company: {company.name}\nDomain: {company.domain}\n"
                        f"Evidence: {evidence_payload}"
                    ),
                },
            ],
            reasoning={"effort": self.reasoning_effort},
            text_format=StructuredCompanyAnalysis,
        )
        return response.output_parsed


def provider_from_settings(settings: Settings) -> CompanyAnalysisProvider:
    if settings.llm_provider == "openai":
        return OpenAICompanyAnalysisProvider(settings)
    return StubCompanyAnalysisProvider()
