import asyncio
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from statistics import mean

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.application.campaigns import (
    _persist_candidates,
    _research_campaign_company,
    create_campaign,
)
from app.domain.models import (
    CampaignCompany,
    Company,
    Opportunity,
    OpportunityScore,
    ProspectingCampaign,
    ResearchRun,
)
from app.infrastructure.database import SessionLocal
from app.modules.discovery.providers import CompanyCandidate, DiscoveryCriteria

RUN_LABEL = "Day 1 Vertical Tournament 2026-08-18"
OUTPUT_DIR = Path(__file__).resolve().parents[3]
REPORT_JSON = OUTPUT_DIR / "day1_vertical_tournament_report.json"
REPORT_MD = OUTPUT_DIR / "day1_vertical_tournament_report.md"
EDUCATION_BENCHMARK = OUTPUT_DIR / "market_validation_01_full.json"
BLOCKED_DOMAINS = {
    "altamirainmuebles.com": "crawl_tcp_connect_hang",
    "aon.es": "crawl_tls_read_hang",
    "hla.es": "crawl_tcp_connect_hang",
    "centromedicoteknon.com": "crawl_tcp_connect_hang",
}


@dataclass(frozen=True)
class Candidate:
    name: str
    domain: str


VERTICALS: dict[str, dict] = {
    "Real Estate": {
        "industry": "Real Estate",
        "candidates": [
            Candidate("Tecnocasa", "tecnocasa.es"),
            Candidate("Redpiso", "redpiso.es"),
            Candidate("Donpiso", "donpiso.com"),
            Candidate("RE/MAX Espana", "remax.es"),
            Candidate("Century 21 Espana", "century21.es"),
            Candidate("Keller Williams Espana", "kellerwilliamsespana.es"),
            Candidate("Coldwell Banker Espana", "coldwellbanker.es"),
            Candidate("Engel and Volkers Spain", "engelvoelkers.com"),
            Candidate("Lucas Fox", "lucasfox.com"),
            Candidate("aProperties", "aproperties.es"),
            Candidate("GILMAR", "gilmar.es"),
            Candidate("Forcadell", "forcadell.com"),
            Candidate("Vivendex", "vivendex.com"),
            Candidate("Monapart", "monapart.com"),
            Candidate("Finques Feliu", "finquesfeliu.es"),
            Candidate("Amat Immobiliaris", "amatimmobiliaris.com"),
            Candidate("Comprarcasa", "comprarcasa.com"),
            Candidate("Alfa Inmobiliaria", "alfainmo.com"),
            Candidate("Look and Find", "lookandfind.es"),
            Candidate("Adaix", "adaix.com"),
            Candidate("Huspy", "huspy.com"),
            Candidate("Housfy", "housfy.com"),
            Candidate("Clikalia", "clikalia.es"),
            Candidate("Solvia", "solvia.es"),
            Candidate("Servihabitat", "servihabitat.com"),
            Candidate("Aliseda Inmobiliaria", "alisedainmobiliaria.com"),
            Candidate("Altamira", "altamirainmuebles.com"),
            Candidate("Hipoges", "hipoges.com"),
            Candidate("Tinsa", "tinsa.es"),
            Candidate("CBRE Espana", "cbre.es"),
        ],
    },
    "Insurance": {
        "industry": "Insurance",
        "candidates": [
            Candidate("Mapfre", "mapfre.es"),
            Candidate("AXA Espana", "axa.es"),
            Candidate("Allianz Espana", "allianz.es"),
            Candidate("Generali Espana", "generali.es"),
            Candidate("Zurich Espana", "zurich.es"),
            Candidate("Occident", "occident.com"),
            Candidate("Santalucia", "santalucia.es"),
            Candidate("Reale Seguros", "reale.es"),
            Candidate("Mutua Madrilena", "mutua.es"),
            Candidate("Linea Directa", "lineadirecta.com"),
            Candidate("Verti", "verti.es"),
            Candidate("Caser", "caser.es"),
            Candidate("DKV Seguros", "dkv.es"),
            Candidate("Adeslas", "adeslas.es"),
            Candidate("Nationale-Nederlanden Espana", "nnseguros.es"),
            Candidate("ASISA", "asisa.es"),
            Candidate("FIATC", "fiatc.es"),
            Candidate("Helvetia", "helvetia.es"),
            Candidate("Plus Ultra Seguros", "plusultra.es"),
            Candidate("Seguros RGA", "segurosrga.es"),
            Candidate("Aon Espana", "aon.es"),
            Candidate("Marsh Espana", "marsh.com"),
            Candidate("Howden Iberia", "howdengroup.com"),
            Candidate("Willis Towers Watson Espana", "wtwco.com"),
            Candidate("Lockton", "lockton.com"),
            Candidate("Ribesalat", "ribesalat.com"),
            Candidate("Alkora", "alkora.com"),
            Candidate("E2K Global", "e2kglobal.com"),
            Candidate("Cojebro", "cojebro.com"),
            Candidate("CenterBrok", "centerbrok.es"),
        ],
    },
    "Private Clinics": {
        "industry": "Private Clinics",
        "candidates": [
            Candidate("Quironsalud", "quironsalud.com"),
            Candidate("HM Hospitales", "hmhospitales.com"),
            Candidate("Ribera Salud", "riberasalud.com"),
            Candidate("IMED Hospitales", "imedhospitales.com"),
            Candidate("Viamed Salud", "viamedsalud.com"),
            Candidate("Hospiten", "hospiten.com"),
            Candidate("HLA Grupo Hospitalario", "hla.es"),
            Candidate("Sanitas Hospitales", "sanitas.es"),
            Candidate("Adeslas Dental", "adeslasdental.es"),
            Candidate("Vitaldent", "vitaldent.com"),
            Candidate("Dental Company", "dentalcompany.es"),
            Candidate("Cleardent", "cleardent.es"),
            Candidate("Dorsia", "dorsia.es"),
            Candidate("Clinicas Londres", "clinicaslondres.es"),
            Candidate("Corporacion Capilar", "corporacioncapilar.es"),
            Candidate("Clinica Baviera", "clinicabaviera.com"),
            Candidate("Miranza", "miranza.es"),
            Candidate("IVI RMA", "ivi-rmainnovation.com"),
            Candidate("Eugin", "eugin.es"),
            Candidate("Ginemed", "ginemed.es"),
            Candidate("Eva Fertility Clinics", "evafertilityclinics.es"),
            Candidate("Clinica Tambre", "clinicatambre.com"),
            Candidate("Instituto Bernabeu", "institutobernabeu.com"),
            Candidate("CRA Barcelona", "cra.barcelona"),
            Candidate("FisioClinics", "fisioclinics.com"),
            Candidate("Fisiohogar", "fisiohogar.com"),
            Candidate("Clinica Cemtro", "clinicacemtro.com"),
            Candidate("Teknon", "teknon.es"),
            Candidate("Centro Medico Teknon", "centromedicoteknon.com"),
            Candidate("Clinica Universidad de Navarra", "cun.es"),
        ],
    },
    "Professional Services": {
        "industry": "Professional Services",
        "candidates": [
            Candidate("CE Consulting", "ceconsulting.es"),
            Candidate("GD Asesoria", "gdasesoria.com"),
            Candidate("Gesdocument", "gesdocument.com"),
            Candidate("Aselec Consultores", "aselecconsultores.com"),
            Candidate("Ayuda T Pymes", "ayudatpymes.com"),
            Candidate("TaxDown", "taxdown.es"),
            Candidate("Declarando", "declarando.es"),
            Candidate("Billin", "billin.net"),
            Candidate("Anfix", "anfix.com"),
            Candidate("Grant Thornton Espana", "grantthornton.es"),
            Candidate("BDO Espana", "bdo.es"),
            Candidate("KPMG Espana", "kpmg.com"),
            Candidate("Deloitte Espana", "deloitte.com"),
            Candidate("EY Espana", "ey.com"),
            Candidate("PwC Espana", "pwc.es"),
            Candidate("Ayming Espana", "ayming.es"),
            Candidate("AFI", "afi.es"),
            Candidate("Izertis", "izertis.com"),
            Candidate("Seidor", "seidor.com"),
            Candidate("Plain Concepts", "plainconcepts.com"),
            Candidate("Cuatrecasas", "cuatrecasas.com"),
            Candidate("Garrigues", "garrigues.com"),
            Candidate("Uria Menendez", "uria.com"),
            Candidate("Perez-Llorca", "perezllorca.com"),
            Candidate("ECIJA", "ecija.com"),
            Candidate("Broseta", "broseta.com"),
            Candidate("RocaJunyent", "rocajunyent.com"),
            Candidate("Andersen Spain", "es.andersen.com"),
            Candidate("Lener", "lener.es"),
            Candidate("Baker McKenzie Spain", "bakermckenzie.com"),
        ],
    },
}


class StaticProvider:
    provider_name = "day1-static-real-domains"

    def __init__(self, vertical: str) -> None:
        self.vertical = vertical

    async def discover(self, criteria: DiscoveryCriteria) -> list[CompanyCandidate]:
        rows = VERTICALS[self.vertical]["candidates"][: criteria.target_company_count]
        industry = VERTICALS[self.vertical]["industry"]
        return [
            CompanyCandidate(
                name=row.name,
                domain=row.domain,
                website_url=f"https://{row.domain}",
                industry=industry,
                country=criteria.country,
                city=criteria.city_or_region,
                source=self.provider_name,
                source_url="manual-curated-real-company-domain-list",
                metadata={"vertical": self.vertical, "run_label": RUN_LABEL},
            )
            for row in rows
        ]


def existing_campaign(name: str) -> ProspectingCampaign | None:
    with SessionLocal() as db:
        return db.scalar(select(ProspectingCampaign).where(ProspectingCampaign.name == name))


async def ensure_campaign(vertical: str) -> int:
    name = f"{RUN_LABEL} - {vertical}"
    with SessionLocal() as db:
        campaign = db.scalar(select(ProspectingCampaign).where(ProspectingCampaign.name == name))
        if campaign is None:
            opportunity = db.scalar(select(Opportunity).order_by(Opportunity.id.asc()))
            if opportunity is None:
                raise RuntimeError("Default opportunity is not seeded")
            campaign = create_campaign(
                db,
                name=name,
                country="Spain",
                city_or_region="Spain",
                industries=[VERTICALS[vertical]["industry"]],
                employee_min=None,
                employee_max=None,
                opportunity_id=opportunity.id,
                target_company_count=30,
            )
            print(f"created campaign {campaign.id}: {campaign.name}", flush=True)
        else:
            print(
                f"reusing campaign {campaign.id}: {campaign.name} ({campaign.status})", flush=True
            )
        campaign_id = campaign.id
    if existing_campaign(name).status != "COMPLETED":
        await run_resumable_campaign(campaign_id, StaticProvider(vertical))
    return campaign_id


async def run_resumable_campaign(campaign_id: int, provider: StaticProvider) -> None:
    db = SessionLocal()
    try:
        campaign = db.get(ProspectingCampaign, campaign_id)
        if campaign is None:
            raise RuntimeError(f"Campaign not found: {campaign_id}")
        campaign.status = "RUNNING"
        campaign.started_at = campaign.started_at or datetime.now(UTC)
        campaign.completed_at = None
        db.commit()

        criteria = DiscoveryCriteria(
            country=campaign.country,
            city_or_region=campaign.city_or_region,
            industries=campaign.industries,
            employee_min=campaign.employee_min,
            employee_max=campaign.employee_max,
            target_company_count=campaign.target_company_count,
        )
        candidates = await provider.discover(criteria)
        entries = _persist_candidates(db, campaign, candidates)
        for entry in entries:
            entry = db.get(CampaignCompany, entry.id)
            if entry is None or entry.research_state == "RESEARCHED":
                continue
            company = db.get(Company, entry.company_id)
            if company is not None and company.domain in BLOCKED_DOMAINS:
                entry.research_state = "FAILED"
                entry.error = BLOCKED_DOMAINS[company.domain]
                entry.updated_at = datetime.now(UTC)
                db.add(
                    ResearchRun(
                        company_id=company.id,
                        campaign_id=campaign.id,
                        provider="research",
                        model="unknown",
                        input_tokens=0,
                        output_tokens=0,
                        estimated_cost=0,
                        execution_time_ms=0,
                        status="FAILED",
                        error=entry.error,
                        diagnostics={"crawl_failures": 1, "error": entry.error},
                    )
                )
                db.commit()
                print(f"skipped blocked domain {company.domain}", flush=True)
                continue
            await _research_campaign_company(db, campaign, entry)

        campaign.status = "COMPLETED"
        campaign.completed_at = datetime.now(UTC)
        db.commit()
    except Exception:
        db.rollback()
        campaign = db.get(ProspectingCampaign, campaign_id)
        if campaign is not None:
            campaign.status = "FAILED"
            campaign.completed_at = datetime.now(UTC)
            db.commit()
        raise
    finally:
        db.close()


def classify_company(
    evidence_count: int, avg_confidence: float, score: OpportunityScore | None
) -> str:
    if evidence_count == 0 or score is None:
        return "INSUFFICIENT"
    if evidence_count >= 10 and avg_confidence >= 0.60:
        return "STRONG"
    if evidence_count >= 5 and avg_confidence >= 0.50:
        return "USABLE"
    return "WEAK"


def contact_readiness(quality: str) -> str:
    if quality == "STRONG":
        return "CONTACT FIRST"
    if quality == "USABLE":
        return "WORTH REVIEWING"
    return "DO NOT CONTACT"


def has_any(text: str, needles: list[str]) -> bool:
    haystack = text.lower()
    return any(needle in haystack for needle in needles)


def joined_company_text(company: Company) -> str:
    parts = []
    for evidence in company.evidence:
        parts.append(evidence.signal_type)
        parts.append(evidence.content_excerpt)
        parts.append(json.dumps(evidence.evidence_metadata, ensure_ascii=True))
    for analysis in company.analyses:
        parts.append(analysis.summary)
        parts.append(json.dumps(analysis.observed_signals, ensure_ascii=True))
        parts.append(json.dumps(analysis.possible_automation_opportunities, ensure_ascii=True))
        parts.append(" ".join(analysis.unknowns))
    return "\n".join(parts)


def summarize_campaign(campaign_id: int, vertical: str) -> dict:
    with SessionLocal() as db:
        campaign = db.scalar(
            select(ProspectingCampaign)
            .where(ProspectingCampaign.id == campaign_id)
            .options(
                selectinload(ProspectingCampaign.companies)
                .selectinload(CampaignCompany.company)
                .selectinload(Company.evidence),
                selectinload(ProspectingCampaign.companies)
                .selectinload(CampaignCompany.company)
                .selectinload(Company.signals),
                selectinload(ProspectingCampaign.companies)
                .selectinload(CampaignCompany.company)
                .selectinload(Company.analyses),
                selectinload(ProspectingCampaign.companies)
                .selectinload(CampaignCompany.company)
                .selectinload(Company.sources),
                selectinload(ProspectingCampaign.companies)
                .selectinload(CampaignCompany.company)
                .selectinload(Company.opportunity_scores),
            )
        )
        if campaign is None:
            raise RuntimeError(f"Campaign not found: {campaign_id}")
        rows = []
        for entry in campaign.companies:
            company = entry.company
            score = next(
                (
                    item
                    for item in company.opportunity_scores
                    if item.opportunity_id == campaign.opportunity_id
                ),
                None,
            )
            evidence_count = len(company.evidence)
            signal_count = len(company.signals)
            pages = len(company.sources)
            avg_conf = (
                mean([item.confidence for item in company.evidence]) if company.evidence else 0
            )
            quality = classify_company(evidence_count, avg_conf, score)
            text = joined_company_text(company)
            opportunities = (
                company.analyses[-1].possible_automation_opportunities if company.analyses else []
            )
            rows.append(
                {
                    "company": company.name,
                    "domain": company.domain,
                    "research_state": entry.research_state,
                    "evidence_count": evidence_count,
                    "signal_count": signal_count,
                    "pages": pages,
                    "avg_confidence": round(avg_conf, 3),
                    "quality": quality,
                    "contact_readiness": contact_readiness(quality),
                    "total_score": score.total_score if score else 0,
                    "icp_score": score.icp_score if score else 0,
                    "pain_score": score.pain_score if score else 0,
                    "value_score": score.value_score if score else 0,
                    "intent_score": score.intent_score if score else 0,
                    "reachability_score": score.reachability_score if score else 0,
                    "confidence_score": score.confidence_score if score else 0,
                    "matched_signals": score.matched_signals if score else [],
                    "multi_systems": has_any(
                        text,
                        [
                            "crm",
                            "hubspot",
                            "salesforce",
                            "pipedrive",
                            "api",
                            "integracion",
                            "integration",
                        ],
                    ),
                    "multiple_locations": has_any(
                        text,
                        [
                            "MULTIPLE_LOCATIONS",
                            "delegaciones",
                            "oficinas",
                            "centros",
                            "clinicas",
                            "locations",
                        ],
                    ),
                    "commercial_indicators": has_any(
                        text,
                        ["sales", "comercial", "ventas", "lead", "contact form", "formulario"],
                    ),
                    "repetitive_workflows": has_any(
                        text,
                        [
                            "appointment",
                            "cita",
                            "booking",
                            "renewal",
                            "renovacion",
                            "document",
                            "onboarding",
                            "follow-up",
                        ],
                    ),
                    "multi_signal_opportunity": len(opportunities) > 0 and signal_count >= 2,
                    "why_now": has_any(
                        text,
                        [
                            "HIRING_SALES",
                            "HIRING_OPERATIONS",
                            "ACTIVE_GROWTH_SIGNAL",
                            "hiring",
                            "expansion",
                            "growth",
                        ],
                    ),
                }
            )
        researched = [row for row in rows if row["research_state"] == "RESEARCHED"]
        quality_counts = {key: 0 for key in ["STRONG", "USABLE", "WEAK", "INSUFFICIENT"]}
        contact_counts = {key: 0 for key in ["CONTACT FIRST", "WORTH REVIEWING", "DO NOT CONTACT"]}
        for row in rows:
            quality_counts[row["quality"]] += 1
            contact_counts[row["contact_readiness"]] += 1
        n = len(rows) or 1
        researched_n = len(researched) or 1
        return {
            "vertical": vertical,
            "campaign_id": campaign.id,
            "campaign_name": campaign.name,
            "status": campaign.status,
            "companies_researched": len(researched),
            "companies_discovered": len(rows),
            "useful_evidence_rate": round(
                100 * sum(1 for row in rows if row["evidence_count"] > 0) / n, 1
            ),
            "strong_rate": round(100 * quality_counts["STRONG"] / n, 1),
            "usable_rate": round(100 * quality_counts["USABLE"] / n, 1),
            "weak_rate": round(100 * quality_counts["WEAK"] / n, 1),
            "insufficient_rate": round(100 * quality_counts["INSUFFICIENT"] / n, 1),
            "quality_distribution": quality_counts,
            "contact_distribution": contact_counts,
            "avg_evidence_company": round(mean([row["evidence_count"] for row in rows]), 2)
            if rows
            else 0,
            "avg_signals_company": round(mean([row["signal_count"] for row in rows]), 2)
            if rows
            else 0,
            "avg_pages_company": round(mean([row["pages"] for row in rows]), 2) if rows else 0,
            "avg_confidence": round(mean([row["avg_confidence"] for row in rows]), 3)
            if rows
            else 0,
            "avg_score": round(mean([row["total_score"] for row in rows]), 2) if rows else 0,
            "contact_first_pct": round(100 * contact_counts["CONTACT FIRST"] / n, 1),
            "avg_pain_score": round(mean([row["pain_score"] for row in rows]), 2) if rows else 0,
            "avg_value_score": round(mean([row["value_score"] for row in rows]), 2) if rows else 0,
            "avg_intent_score": round(mean([row["intent_score"] for row in rows]), 2)
            if rows
            else 0,
            "avg_reachability_score": round(mean([row["reachability_score"] for row in rows]), 2)
            if rows
            else 0,
            "commercial_signals": {
                "multiple_operational_systems": sum(row["multi_systems"] for row in rows),
                "multiple_locations": sum(row["multiple_locations"] for row in rows),
                "commercial_sales_indicators": sum(row["commercial_indicators"] for row in rows),
                "observable_repetitive_workflows": sum(row["repetitive_workflows"] for row in rows),
                "automation_opportunity_multi_signal": sum(
                    row["multi_signal_opportunity"] for row in rows
                ),
                "genuine_why_now": sum(row["why_now"] for row in rows),
            },
            "top_companies": sorted(
                rows, key=lambda row: (row["total_score"], row["evidence_count"]), reverse=True
            )[:10],
            "companies": rows,
            "researched_denominator": researched_n,
        }


def education_summary() -> dict | None:
    if not EDUCATION_BENCHMARK.exists():
        return None
    payload = json.loads(EDUCATION_BENCHMARK.read_text())
    metrics = payload["metrics"]
    q = metrics["quality_distribution"]
    c = metrics["contact_distribution"]
    n = metrics["companies_researched"] or 1
    companies = payload["companies"]

    def avg_breakdown(key: str) -> float:
        values = [row.get("score_breakdown", {}).get(key, 0) for row in companies]
        return round(mean(values), 2) if values else 0

    return {
        "vertical": "Education",
        "campaign_id": None,
        "campaign_name": payload["campaign"]["name"],
        "status": "BENCHMARK",
        "companies_researched": metrics["companies_researched"],
        "companies_discovered": metrics["companies_discovered"],
        "useful_evidence_rate": round(100 * metrics["companies_with_useful_evidence"] / n, 1),
        "strong_rate": round(100 * q["STRONG"] / n, 1),
        "usable_rate": round(100 * q["USABLE"] / n, 1),
        "weak_rate": round(100 * q["WEAK"] / n, 1),
        "insufficient_rate": round(100 * q["INSUFFICIENT"] / n, 1),
        "quality_distribution": q,
        "contact_distribution": c,
        "avg_evidence_company": metrics["average_evidence_company"],
        "avg_signals_company": metrics["average_signals_company"],
        "avg_pages_company": metrics["average_pages_company"],
        "avg_confidence": metrics["average_confidence"],
        "avg_score": metrics["average_score"],
        "contact_first_pct": round(100 * c["CONTACT FIRST"] / n, 1),
        "avg_pain_score": avg_breakdown("pain"),
        "avg_value_score": avg_breakdown("value"),
        "avg_intent_score": avg_breakdown("intent"),
        "avg_reachability_score": avg_breakdown("reachability"),
        "commercial_signals": {
            "multiple_operational_systems": None,
            "multiple_locations": None,
            "commercial_sales_indicators": None,
            "observable_repetitive_workflows": None,
            "automation_opportunity_multi_signal": None,
            "genuine_why_now": sum(1 for row in companies if row.get("why_now_signals")),
        },
        "top_companies": companies[:10],
        "companies": companies,
    }


def market_score(row: dict) -> float:
    return round(
        row["contact_first_pct"] * 0.30
        + row["strong_rate"] * 0.25
        + row["useful_evidence_rate"] * 0.15
        + row["avg_score"] * 0.15
        + min(row["avg_evidence_company"] * 3, 100) * 0.10
        + row["avg_reachability_score"] * 0.05,
        2,
    )


def write_reports(summaries: list[dict]) -> None:
    ranked = sorted(
        [{**row, "market_priority_score": market_score(row)} for row in summaries],
        key=lambda row: row["market_priority_score"],
        reverse=True,
    )
    output = {
        "generated_at": datetime.now(UTC).isoformat(),
        "run_label": RUN_LABEL,
        "environment": {
            "database": "local sqlite",
            "llm_provider": "openai",
            "model": "gpt-5.4-mini",
            "production_api_blocker": (
                "Production API token in local .env was rejected by Render service."
            ),
        },
        "ranking": [
            {
                "rank": index + 1,
                "vertical": row["vertical"],
                "market_priority_score": row["market_priority_score"],
            }
            for index, row in enumerate(ranked)
        ],
        "summaries": ranked,
    }
    REPORT_JSON.write_text(json.dumps(output, indent=2, ensure_ascii=True))

    lines = [
        f"# {RUN_LABEL}",
        "",
        (
            "Production API was reachable but rejected the local APP_API_TOKEN, so this "
            "run used the same local engine configuration against SQLite: OpenAI "
            "provider, gpt-5.4-mini, unchanged research/scoring rules."
        ),
        "",
        "## Ranking",
        "",
        (
            "| Rank | Vertical | Priority | Researched | Useful evidence | STRONG | "
            "CONTACT FIRST | Avg score | Avg evidence |"
        ),
        "|---:|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for index, row in enumerate(ranked, 1):
        lines.append(
            f"| {index} | {row['vertical']} | {row['market_priority_score']} | "
            f"{row['companies_researched']} | {row['useful_evidence_rate']}% | "
            f"{row['strong_rate']}% | {row['contact_first_pct']}% | "
            f"{row['avg_score']} | {row['avg_evidence_company']} |"
        )
    lines.extend(["", "## Market Details", ""])
    for row in ranked:
        lines.extend(
            [
                f"### {row['vertical']}",
                "",
                f"- Status: {row['status']}",
                f"- Quality distribution: {row['quality_distribution']}",
                f"- Contact distribution: {row['contact_distribution']}",
                (
                    "- Avg Pain/Value/Intent/Reachability: "
                    f"{row['avg_pain_score']} / {row['avg_value_score']} / "
                    f"{row['avg_intent_score']} / {row['avg_reachability_score']}"
                ),
                f"- Commercial signals: {row['commercial_signals']}",
                "",
                "Top companies:",
            ]
        )
        for company in row["top_companies"][:5]:
            name = company.get("company") or company.get("company_name")
            domain = company.get("domain")
            score = company.get("total_score")
            evidence = company.get("evidence_count")
            lines.append(f"- {name} ({domain}): score {score}, evidence {evidence}")
        lines.append("")
    REPORT_MD.write_text("\n".join(lines))
    print(f"wrote {REPORT_JSON}", flush=True)
    print(f"wrote {REPORT_MD}", flush=True)


async def main() -> None:
    campaign_ids = []
    for vertical in VERTICALS:
        campaign_ids.append((vertical, await ensure_campaign(vertical)))
    summaries = []
    benchmark = education_summary()
    if benchmark:
        summaries.append(benchmark)
    for vertical, campaign_id in campaign_ids:
        summaries.append(summarize_campaign(campaign_id, vertical))
    write_reports(summaries)


if __name__ == "__main__":
    asyncio.run(main())
