# ruff: noqa: E501
import json
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path
from statistics import mean

from sqlalchemy import create_engine, text

ROOT = Path(__file__).resolve().parents[3]
DB_PATH = ROOT / "apps/api/prospecting_tournament.db"
TOURNAMENT_JSON = ROOT / "day1_vertical_tournament_report.json"

OUTPUTS = {
    "segmentation": ROOT / "professional_services_segmentation.md",
    "offer": ROOT / "professional_services_offer.md",
    "top10": ROOT / "professional_services_top10.md",
    "first5": ROOT / "professional_services_first5.md",
    "playbook": ROOT / "professional_services_discovery_playbook.md",
    "json": ROOT / "professional_services_deep_dive_report.json",
}

SEGMENTS = {
    "CE Consulting": ("Accounting / tax / gestoría advisory", 0.78, "Asesoría network evidence."),
    "GD Asesoria": (
        "Accounting / tax / gestoría advisory",
        0.45,
        "Name/domain suggest asesoría, but no useful evidence was captured.",
    ),
    "Gesdocument": (
        "Gestoría / business administration",
        0.45,
        "Name suggests document/business administration, but no useful evidence was captured.",
    ),
    "Aselec Consultores": (
        "Accounting / tax / gestoría advisory",
        0.72,
        "Consulting plus economist/lawyer and contact evidence.",
    ),
    "Ayuda T Pymes": (
        "Accounting / tax / gestoría advisory",
        0.82,
        "Public services for autónomos, companies, branches, associations and foundations.",
    ),
    "TaxDown": (
        "Tax/accounting platforms and tech-enabled advisory",
        0.88,
        "Tax software/service with consumer and enterprise fiscal workflows.",
    ),
    "Declarando": (
        "Tax/accounting platforms and tech-enabled advisory",
        0.65,
        "Tax/accounting positioning, but limited useful evidence captured.",
    ),
    "Billin": (
        "Tax/accounting platforms and tech-enabled advisory",
        0.82,
        "Billing/accounting product with gestoría directory and support stack.",
    ),
    "Anfix": (
        "Tax/accounting platforms and tech-enabled advisory",
        0.84,
        "Accounting/invoicing software for businesses, autónomos and asesorías.",
    ),
    "Grant Thornton Espana": (
        "Business consulting / audit / financial advisory",
        0.9,
        "Audit, advisory, tax/legal and professional-services evidence.",
    ),
    "BDO Espana": (
        "Business consulting / audit / financial advisory",
        0.9,
        "Audit, advisory, tax/legal and outsourcing evidence.",
    ),
    "KPMG Espana": (
        "Business consulting / audit / financial advisory",
        0.88,
        "Large professional-services network with broad advisory/tax/audit evidence.",
    ),
    "Deloitte Espana": (
        "Business consulting / audit / financial advisory",
        0.86,
        "Large professional-services network with broad advisory evidence.",
    ),
    "EY Espana": (
        "Business consulting / audit / financial advisory",
        0.88,
        "Large professional-services network with advisory and operations evidence.",
    ),
    "PwC Espana": (
        "Business consulting / audit / financial advisory",
        0.5,
        "Known professional-services firm, but no useful evidence was captured.",
    ),
    "Ayming Espana": (
        "Business consulting / audit / financial advisory",
        0.86,
        "Innovation financing, fiscal/compliance, sustainability and partner evidence.",
    ),
    "AFI": (
        "Business consulting / audit / financial advisory",
        0.86,
        "Financial consulting and education-arm evidence.",
    ),
    "Izertis": (
        "Technology consulting",
        0.92,
        "Software, cloud, cybersecurity, AI/data and Salesforce evidence.",
    ),
    "Seidor": (
        "Technology consulting",
        0.5,
        "Technology consulting candidate, but no useful evidence was captured.",
    ),
    "Plain Concepts": (
        "Technology consulting",
        0.92,
        "Software engineering, AI/data, cloud and case-study evidence.",
    ),
    "Cuatrecasas": ("Legal services", 0.92, "Multi-office law firm evidence."),
    "Garrigues": ("Legal services", 0.65, "Law firm candidate with limited useful evidence."),
    "Uria Menendez": ("Legal services", 0.45, "Law firm candidate, but no useful evidence captured."),
    "Perez-Llorca": ("Legal services", 0.92, "Multi-country law firm evidence."),
    "ECIJA": ("Legal services", 0.72, "Legal-services evidence, though smaller evidence set."),
    "Broseta": ("Legal services", 0.86, "Law firm with multilingual/contact evidence."),
    "RocaJunyent": ("Legal services", 0.45, "Law firm candidate, but no useful evidence captured."),
    "Andersen Spain": ("Legal services", 0.9, "Legal/services firm with Iberian/global evidence."),
    "Lener": ("Legal services", 0.88, "Legal/restructuring firm with offices/contact evidence."),
    "Baker McKenzie Spain": ("Legal services", 0.88, "Global law firm evidence; Spain-specificity is tentative."),
}

SUBTYPE_DECISION_SCORES = {
    "Accounting / tax / gestoría advisory": {
        "pain_frequency": 7,
        "pain_repeatability": 9,
        "evidence_quality": 6,
        "economic_value": 7,
        "buyer_reachability": 8,
        "explainability": 9,
        "technical_fit": 9,
        "delivery_ease": 9,
        "reuse": 9,
        "recurring_revenue": 8,
        "sales_cycle_simplicity": 8,
    },
    "Tax/accounting platforms and tech-enabled advisory": {
        "pain_frequency": 7,
        "pain_repeatability": 8,
        "evidence_quality": 6,
        "economic_value": 7,
        "buyer_reachability": 6,
        "explainability": 7,
        "technical_fit": 8,
        "delivery_ease": 6,
        "reuse": 7,
        "recurring_revenue": 7,
        "sales_cycle_simplicity": 5,
    },
    "Business consulting / audit / financial advisory": {
        "pain_frequency": 8,
        "pain_repeatability": 7,
        "evidence_quality": 8,
        "economic_value": 8,
        "buyer_reachability": 4,
        "explainability": 6,
        "technical_fit": 8,
        "delivery_ease": 5,
        "reuse": 6,
        "recurring_revenue": 7,
        "sales_cycle_simplicity": 3,
    },
    "Technology consulting": {
        "pain_frequency": 7,
        "pain_repeatability": 7,
        "evidence_quality": 7,
        "economic_value": 7,
        "buyer_reachability": 5,
        "explainability": 5,
        "technical_fit": 5,
        "delivery_ease": 4,
        "reuse": 5,
        "recurring_revenue": 5,
        "sales_cycle_simplicity": 3,
    },
    "Legal services": {
        "pain_frequency": 8,
        "pain_repeatability": 8,
        "evidence_quality": 7,
        "economic_value": 8,
        "buyer_reachability": 5,
        "explainability": 8,
        "technical_fit": 8,
        "delivery_ease": 7,
        "reuse": 8,
        "recurring_revenue": 7,
        "sales_cycle_simplicity": 5,
    },
    "Gestoría / business administration": {
        "pain_frequency": 6,
        "pain_repeatability": 9,
        "evidence_quality": 2,
        "economic_value": 7,
        "buyer_reachability": 7,
        "explainability": 9,
        "technical_fit": 9,
        "delivery_ease": 8,
        "reuse": 9,
        "recurring_revenue": 8,
        "sales_cycle_simplicity": 7,
    },
}

TOP10 = [
    "CE Consulting",
    "TaxDown",
    "Ayuda T Pymes",
    "Aselec Consultores",
    "Billin",
    "Anfix",
    "Grant Thornton Espana",
    "BDO Espana",
    "Ayming Espana",
    "AFI",
]

FIRST5 = [
    "CE Consulting",
    "Ayuda T Pymes",
    "Aselec Consultores",
    "TaxDown",
    "Billin",
]


def load_rows() -> dict[str, dict]:
    report = json.loads(TOURNAMENT_JSON.read_text())
    professional = next(row for row in report["summaries"] if row["vertical"] == "Professional Services")
    rows = {row["company"]: row for row in professional["companies"]}
    engine = create_engine(f"sqlite:///{DB_PATH}")
    with engine.connect() as conn:
        for row in conn.execute(
            text(
                """
                select co.name, co.domain, ca.summary, ca.observed_signals,
                       ca.possible_automation_opportunities, ca.recommended_buyer_roles
                from prospecting_campaigns pc
                join campaign_companies cc on cc.campaign_id = pc.id
                join companies co on co.id = cc.company_id
                left join company_analyses ca on ca.company_id = co.id
                where pc.name like '%Professional Services'
                """
            )
        ):
            item = rows[row._mapping["name"]]
            for key in [
                "summary",
                "observed_signals",
                "possible_automation_opportunities",
                "recommended_buyer_roles",
            ]:
                value = row._mapping[key]
                if isinstance(value, str) and value and key != "summary":
                    value = json.loads(value)
                item[key] = value or ([] if key != "summary" else "")
        for row in conn.execute(
            text(
                """
                select co.name, e.signal_type, e.confidence, e.source_url,
                       substr(e.content_excerpt, 1, 320) as excerpt
                from evidence e
                join companies co on co.id = e.company_id
                join campaign_companies cc on cc.company_id = co.id
                join prospecting_campaigns pc on pc.id = cc.campaign_id
                where pc.name like '%Professional Services'
                order by e.confidence desc, e.id asc
                """
            )
        ):
            rows[row._mapping["name"]].setdefault("evidence", []).append(dict(row._mapping))
    for name, row in rows.items():
        subtype, confidence, note = SEGMENTS[name]
        row["subtype"] = subtype
        row["subtype_confidence"] = confidence
        row["subtype_note"] = note
        row["unique_signal_count"] = len(row.get("matched_signals", []))
    return rows


def signal_families(row: dict) -> set[str]:
    text_blob = json.dumps(row, ensure_ascii=False).lower()
    signals = set()
    matched = set(row.get("matched_signals", []))
    if "HAS_CONTACT_FORM" in matched or "contact" in text_blob:
        signals.add("contact forms / inbound intake")
    if "MULTIPLE_PRODUCTS_OR_SERVICES" in matched or "servicios" in text_blob:
        signals.add("multiple service lines")
    if "MULTIPLE_LOCATIONS" in matched or "oficinas" in text_blob:
        signals.add("multiple offices")
    if "HAS_SUPPORT_FLOW" in matched or "CUSTOMER_SUCCESS" in text_blob:
        signals.add("support / client service flow")
    if "HIRING" in matched or "HIRING_OPERATIONS" in matched:
        signals.add("hiring / team growth")
    if matched & {"USES_HUBSPOT", "USES_SALESFORCE", "HAS_CRM_INDICATORS", "HAS_INTEGRATIONS"}:
        signals.add("CRM / integrations")
    if matched & {"USES_GOOGLE_TAG_MANAGER", "HAS_MARKETING_AUTOMATION_INDICATORS"}:
        signals.add("marketing automation / analytics")
    if any(word in text_blob for word in ["document", "fiscal", "tax", "legal", "audit"]):
        signals.add("document-heavy advisory work")
    if row.get("possible_automation_opportunities"):
        signals.add("repetitive workflow opportunity")
    return signals


PAIN_RULES = {
    "inbound request triage and routing": ["triage", "routing", "route", "inbound", "contact"],
    "document and data intake": ["document", "pdf", "data", "classification", "extract"],
    "client onboarding and case setup": ["onboarding", "case setup", "questionnaire", "intake"],
    "CRM / marketing follow-up synchronization": ["crm", "hubspot", "salesforce", "follow-up", "nurture"],
    "reporting and attribution": ["reporting", "analytics", "attribution", "tag", "dashboard"],
    "content and knowledge publishing": ["content", "publishing", "translation", "localization"],
    "cross-office / partner handoffs": ["office", "location", "partner", "handoff", "cross-border"],
    "support request deflection or routing": ["support", "help", "intercom", "zendesk"],
}


def pain_themes(row: dict) -> set[str]:
    text_blob = json.dumps(row.get("possible_automation_opportunities", []), ensure_ascii=False).lower()
    themes = {theme for theme, words in PAIN_RULES.items() if any(word in text_blob for word in words)}
    if row.get("possible_automation_opportunities") and not themes:
        themes.add("repetitive back-office workflow")
    return themes


def aggregate(rows: dict[str, dict]) -> dict[str, dict]:
    by_segment = defaultdict(list)
    for row in rows.values():
        by_segment[row["subtype"]].append(row)
    output = {}
    for subtype, items in by_segment.items():
        n = len(items)
        signal_counter = Counter()
        pain_counter = Counter()
        pain_conf = defaultdict(list)
        for item in items:
            signal_counter.update(signal_families(item))
            themes = pain_themes(item)
            pain_counter.update(themes)
            opps = item.get("possible_automation_opportunities") or []
            avg_opp_conf = mean([opp.get("confidence", 0) for opp in opps]) if opps else 0
            for theme in themes:
                pain_conf[theme].append(avg_opp_conf)
        output[subtype] = {
            "n": n,
            "useful_evidence_rate": pct(sum(1 for item in items if item["evidence_count"] > 0), n),
            "strong_rate": pct(sum(1 for item in items if item["quality"] == "STRONG"), n),
            "contact_first_rate": pct(
                sum(1 for item in items if item["contact_readiness"] == "CONTACT FIRST"), n
            ),
            "avg_evidence": avg(items, "evidence_count"),
            "avg_unique_signals": avg(items, "unique_signal_count"),
            "avg_pain": avg(items, "pain_score"),
            "avg_value": avg(items, "value_score"),
            "avg_reachability": avg(items, "reachability_score"),
            "avg_confidence": avg(items, "confidence_score"),
            "signals": signal_counter.most_common(),
            "pains": [
                {
                    "theme": theme,
                    "companies": count,
                    "pct": pct(count, n),
                    "supporting_signal_families": [
                        name for name, _ in signal_counter.most_common(5)
                    ],
                    "avg_confidence": round(mean(pain_conf[theme]), 2) if pain_conf[theme] else 0,
                    "economic_impact": economic_impact(theme, count, n),
                }
                for theme, count in pain_counter.most_common()
            ],
        }
    return dict(sorted(output.items()))


def avg(items: list[dict], key: str) -> float:
    return round(mean([item.get(key, 0) for item in items]), 2) if items else 0


def pct(count: int, total: int) -> float:
    return round(100 * count / total, 1) if total else 0


def economic_impact(theme: str, count: int, total: int) -> str:
    if theme in {"document and data intake", "client onboarding and case setup"}:
        return "HIGH" if count / max(total, 1) >= 0.4 else "MEDIUM"
    if theme in {"inbound request triage and routing", "CRM / marketing follow-up synchronization"}:
        return "MEDIUM" if count else "LOW"
    if theme in {"reporting and attribution", "content and knowledge publishing"}:
        return "MEDIUM"
    return "LOW"


def subtype_score_table() -> list[dict]:
    rows = []
    for subtype, scores in SUBTYPE_DECISION_SCORES.items():
        rows.append(
            {
                "subtype": subtype,
                **scores,
                "average": round(mean(scores.values()), 1),
            }
        )
    return sorted(rows, key=lambda row: row["average"], reverse=True)


def evidence_bullets(row: dict, max_items: int = 4) -> list[str]:
    signal_bullets = []
    for signal in row.get("observed_signals", []):
        signal_type = signal.get("signalType") or signal.get("signal_type")
        reasoning = signal.get("reasoning", "")
        confidence = signal.get("confidence", 0)
        evidence_ids = signal.get("evidenceIds") or signal.get("evidence_ids") or []
        if not signal_type or not reasoning:
            continue
        refs = ", ".join(f"#{item}" for item in evidence_ids[:5])
        signal_bullets.append(
            f"{signal_type} (confidence {confidence:.2f}, evidence {refs}): {reasoning}"
        )
        if len(signal_bullets) >= max_items:
            return signal_bullets

    seen = set()
    bullets = []
    for item in row.get("evidence", []):
        signal = item["signal_type"]
        if signal in seen:
            continue
        seen.add(signal)
        excerpt = " ".join((item["excerpt"] or "").split())
        bullets.append(f"{signal} ({item['source_url']}): {excerpt[:210]}")
        if len(bullets) >= max_items:
            break
    return bullets or ["No useful evidence captured in the existing campaign."]


def write_segmentation(rows: dict[str, dict], segments: dict[str, dict]) -> None:
    lines = [
        "# Professional Services Segmentation",
        "",
        "Source: existing Professional Services cohort from the completed tournament. No research was rerun.",
        "",
        "## Company Classification",
        "",
        "| Company | Domain | Sub-vertical | Confidence | Notes |",
        "|---|---|---|---:|---|",
    ]
    for name in sorted(rows):
        row = rows[name]
        lines.append(
            f"| {name} | {row['domain']} | {row['subtype']} | "
            f"{row['subtype_confidence']:.2f} | {row['subtype_note']} |"
        )
    lines.extend(["", "## Sub-vertical Metrics", ""])
    lines.append(
        "| Sub-vertical | N | Useful evidence | STRONG | CONTACT FIRST | "
        "Avg evidence | Avg signals | Pain | Value | Reachability | Confidence |"
    )
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for subtype, data in segments.items():
        lines.append(
            f"| {subtype} | {data['n']} | {data['useful_evidence_rate']}% | "
            f"{data['strong_rate']}% | {data['contact_first_rate']}% | "
            f"{data['avg_evidence']} | {data['avg_unique_signals']} | "
            f"{data['avg_pain']} | {data['avg_value']} | "
            f"{data['avg_reachability']} | {data['avg_confidence']} |"
        )
    lines.extend(["", "## Recurring Signals by Sub-vertical", ""])
    for subtype, data in segments.items():
        lines.append(f"### {subtype}")
        for signal, count in data["signals"]:
            lines.append(f"- {signal}: {count}/{data['n']}")
        lines.append("")
    lines.extend(["## Recurring Pain Hypotheses", ""])
    for subtype, data in segments.items():
        lines.append(f"### {subtype}")
        if not data["pains"]:
            lines.append("- No recurring pain hypothesis supported by existing evidence.")
        for pain in data["pains"]:
            signals = ", ".join(pain["supporting_signal_families"])
            lines.append(
                f"- {pain['theme']}: {pain['companies']} companies "
                f"({pain['pct']}%). Supporting signal families: {signals}. "
                f"Avg confidence {pain['avg_confidence']}; impact {pain['economic_impact']}."
            )
        lines.append("")
    lines.extend(["## Sub-vertical Decision Scores", ""])
    headers = [
        "Pain freq",
        "Repeatability",
        "Evidence",
        "Economic value",
        "Reachability",
        "Explainability",
        "Tech fit",
        "Delivery",
        "Reuse",
        "MRR",
        "Sales simplicity",
        "Avg",
    ]
    lines.append("| Sub-vertical | " + " | ".join(headers) + " |")
    lines.append("|---|" + "|".join(["---:"] * len(headers)) + "|")
    for row in subtype_score_table():
        score_values = [
            row["pain_frequency"],
            row["pain_repeatability"],
            row["evidence_quality"],
            row["economic_value"],
            row["buyer_reachability"],
            row["explainability"],
            row["technical_fit"],
            row["delivery_ease"],
            row["reuse"],
            row["recurring_revenue"],
            row["sales_cycle_simplicity"],
            row["average"],
        ]
        lines.append(f"| {row['subtype']} | " + " | ".join(map(str, score_values)) + " |")
    lines.extend(
        [
            "",
            "## Winning Sub-vertical",
            "",
            "**Accounting / tax / gestoría advisory**.",
            "",
            "This is not the highest raw OpportunityScore group. It is the best first-commercial "
            "target because the problem is easy to explain, the implementation can be small, "
            "buyers are closer to the owner/operator, and the workflow is repeatable across firms: "
            "client emails, documents, forms, and status requests arrive in messy formats and must "
            "be classified, routed, tracked, and copied into systems.",
            "",
            "## Secondary Sub-vertical",
            "",
            "**Legal services**.",
            "",
            "Legal services showed strong multi-office, multilingual, contact and knowledge-work "
            "signals. It is a good secondary market, especially for intake/routing and document "
            "workflow automation, but the likely sales cycle is slower and first implementation "
            "risk is higher than with owner-led advisory firms.",
        ]
    )
    OUTPUTS["segmentation"].write_text("\n".join(lines))


def write_offer() -> None:
    lines = [
        "# Initial Professional Services Offer",
        "",
        "## Target Customer",
        "",
        "Spanish accounting, tax, labour and gestoría firms with roughly 5-50 employees "
        "that receive recurring client emails, forms and documents and still depend on "
        "manual review, classification, follow-up or data copying.",
        "",
        "## Problem Hypothesis",
        "",
        "**Hypothesis, not confirmed:** advisory teams lose billable or response time because "
        "client requests and documents arrive through email/contact forms/phone follow-ups, "
        "then someone manually decides what it is, what is missing, who should handle it, and "
        "where the information must be logged.",
        "",
        "## Evidence Supporting the Hypothesis",
        "",
        "- CE Consulting exposes a broad asesoría network, offices, job/contact pages and GTM.",
        "- Ayuda T Pymes shows many service situations, support phone/contact flows, newsletter "
        "capture, partner/media signals and GTM.",
        "- Aselec has a contact form, customer-attention hours and advisory positioning.",
        "- TaxDown, Billin and Anfix show adjacent fiscal/accounting workflows, support tooling, "
        "HubSpot/Intercom/Zendesk/GTM and segment-specific onboarding or demo flows.",
        "",
        "## Current Likely Workflow",
        "",
        "Observed: public sites show contact forms, support/client attention channels, many "
        "service lines, and fiscal/accounting/document-heavy services.",
        "",
        "Assumption to validate: a human receives each request, reads the message/document, "
        "identifies the matter, checks missing information, sends a reply or reminder, and "
        "logs or forwards it to the correct advisor/system.",
        "",
        "## Desired Business Outcome",
        "",
        "- Reduce repetitive manual processing of client requests and documents.",
        "- Reduce copying between email, folders, spreadsheets, CRM or practice-management tools.",
        "- Shorten first-response time and reduce missed follow-ups.",
        "- Standardize intake so advisors receive cleaner, pre-classified work.",
        "",
        "## Sergio's Implementation",
        "",
        "A small workflow automation for one high-volume intake process:",
        "",
        "1. Connect one inbox or form destination.",
        "2. Classify incoming requests by service type, urgency and missing data.",
        "3. Extract structured fields from email text and attached PDFs where practical.",
        "4. Create a tracking record in Google Sheets/Airtable/Postgres or the client's CRM.",
        "5. Draft an acknowledgement or missing-information reply for human approval.",
        "6. Send daily/weekly operational summaries.",
        "",
        "Simple architecture: Python scheduled job or FastAPI service, Gmail/Google Workspace "
        "API, lightweight database, OCR only if documents require it, LLM extraction only for "
        "messy unstructured text, and human approval before any external reply.",
        "",
        "## Initial Scope",
        "",
        "One workflow, one inbox/form source, 3-5 request categories, one output tracker, one "
        "approval path, and one weekly report. Delivery target: days to a few weeks.",
        "",
        "## Pricing Hypothesis",
        "",
        "- Conservative low implementation: **€1,500-€2,500**.",
        "- Recommended first offer: **€3,000-€4,500**.",
        "- Upper initial range: **€5,000-€7,500** if OCR, CRM integration or multiple flows are included.",
        "",
        "## Monthly Recurring Service",
        "",
        "Ongoing value: hosting, monitoring, small workflow adjustments, prompt/rule tuning, "
        "usage review, error handling, support, API maintenance, and a monthly operations report.",
        "",
        "Suggested monthly price: **€300-€600/month**. For the first customer, a practical anchor "
        "is **€450/month** after implementation.",
        "",
        "## Path to €900/month",
        "",
        "1. Two clients at €450/month after two implementation projects.",
        "2. Three clients at €300/month with a narrow, low-support workflow.",
        "3. One larger client at €900/month only if there are several workflows or critical integrations.",
        "",
        "Recommended path: **two clients at €450/month**. It keeps the offer realistic for Spanish "
        "SMB advisory firms while reaching €900/month without needing an enterprise sale.",
        "",
        "## Positioning",
        "",
        "One-sentence: Sergio helps advisory firms automate the messy operational workflows between "
        "client email, documents and internal systems, so teams spend less time triaging and copying.",
        "",
        "30-second explanation: I look for one repetitive workflow where client requests or documents "
        "arrive in an unstructured way, then build a small integration that classifies the request, "
        "extracts the useful fields, routes it to the right place, and gives the team a clear control "
        "view. AI can help with messy text or PDFs, but the value is operational: fewer manual steps, "
        "faster response, and cleaner handoffs.",
        "",
        "Problem-oriented positioning: operational automation for advisory workflows, not AI transformation.",
    ]
    OUTPUTS["offer"].write_text("\n".join(lines))


def company_selection_text(name: str, row: dict) -> list[str]:
    reasons = {
        "CE Consulting": "Best classic asesoría-network fit: many offices/service surfaces and enough evidence density to open with intake and routing.",
        "TaxDown": "Strong fiscal workflow and tooling signals; useful for validating higher-volume support/demo/intake automation even if it is more tech-enabled than a classic asesoría.",
        "Ayuda T Pymes": "Clear SMB advisory positioning, support channels and broad service situations create a credible intake/follow-up angle.",
        "Aselec Consultores": "Smaller advisory firm with public contact form and attention hours; likely simpler buyer path than enterprise firms.",
        "Billin": "Accounting-adjacent workflow evidence, Zendesk/HubSpot/GTM and gestoría directory make it useful for validating document/support automation.",
        "Anfix": "Accounting software for asesorías with help/onboarding resources and HubSpot/GTM; useful adjacent validation for support/onboarding flows.",
        "Grant Thornton Espana": "High evidence density and outsourcing/tax/advisory surface; selected as a larger benchmark, not first outreach priority.",
        "BDO Espana": "Multi-office audit/advisory/tax/outsourcing evidence; good for learning enterprise pain patterns, slower for first sale.",
        "Ayming Espana": "Fiscal/compliance advisory with partner and multi-country signals; useful for lead routing and content/reporting workflows.",
        "AFI": "Financial consulting group with multi-service, multi-location and event/application signals; strong for inquiry routing hypotheses.",
    }
    automation = {
        "CE Consulting": "Automate classification and routing of client requests across advisory areas and offices.",
        "TaxDown": "Automate support/demo intake, tax-case categorization and missing-information follow-up.",
        "Ayuda T Pymes": "Automate service-request intake, status tracking and follow-up for autónomo/company cases.",
        "Aselec Consultores": "Automate contact-form triage, acknowledgement and advisor assignment.",
        "Billin": "Automate support/request classification and handoff between helpdesk, product and gestoría workflows.",
        "Anfix": "Automate onboarding/support triage around first steps and accounting/invoicing workflows.",
        "Grant Thornton Espana": "Automate contact/RFP/career inquiry routing by office and service line.",
        "BDO Espana": "Automate multi-office contact intake and service-line routing.",
        "Ayming Espana": "Automate partner/contact lead routing and marketing attribution around advisory services.",
        "AFI": "Automate inquiry classification for services, education/events and multi-location contact flows.",
    }
    value = (
        "The value would come from reducing repetitive triage, manual copying, missed follow-ups "
        "and response delays, not from an invented revenue uplift."
    )
    return [
        f"## {name}",
        "",
        f"- Domain: {row['domain']}",
        f"- Sub-vertical: {row['subtype']}",
        f"- Total score: {row['total_score']}",
        f"- Why selected: {reasons[name]}",
        "- Strongest observed evidence:",
        *[f"  - {bullet}" for bullet in evidence_bullets(row, 4)],
        "- Pain hypothesis: Hypothesis, not confirmed. Client requests/documents likely need "
        "manual review, routing, follow-up or data entry.",
        f"- Initial automation hypothesis: {automation[name]}",
        f"- Economic value hypothesis: {value}",
        f"- Recommended buyer role: {buyer_role(name, row)}",
        f"- Why now: {why_now(row)}",
        f"- Outreach angle: {outreach_angle(name, row)}",
        "",
    ]


def buyer_role(name: str, row: dict) -> str:
    overrides = {
        "CE Consulting": "Managing Director / Operations Director",
        "TaxDown": "Head of Operations / Head of Customer Support",
        "Ayuda T Pymes": "CEO / Operations Director",
        "Aselec Consultores": "Managing Partner / Office Director",
        "Billin": "Head of Operations / Head of Support",
        "Anfix": "Head of Customer Support / Product Operations",
    }
    return overrides.get(name) or (row.get("recommended_buyer_roles") or ["Operations Director"])[0]


def why_now(row: dict) -> str:
    if row.get("why_now") or any(signal.startswith("HIRING") for signal in row.get("matched_signals", [])):
        return "Existing evidence includes hiring/growth/why-now style signals."
    return "No strong why-now signal detected."


def outreach_angle(name: str, row: dict) -> str:
    if name == "CE Consulting":
        return "I noticed the advisory-network/offices footprint and would like to understand how inbound client requests get routed today."
    if name == "Ayuda T Pymes":
        return "Your site shows many client situations and support paths; I am testing whether intake/status workflows can be simplified for advisory teams."
    if name == "Aselec Consultores":
        return "Your contact flow and client-attention hours suggest a concrete workflow to understand before proposing any automation."
    if name == "TaxDown":
        return "Your consumer, autónomo and enterprise flows suggest intake/support routing complexity worth understanding."
    if name == "Billin":
        return "The accounting/support stack signals suggest a useful conversation around request classification and support handoffs."
    return "The public signals suggest multi-service inbound and operational handoff complexity worth validating in a short conversation."


def write_top10(rows: dict[str, dict]) -> None:
    lines = [
        "# Professional Services Top 10 Prospects",
        "",
        "Selection prioritizes fit with the winning accounting/tax/gestoría workflow hypothesis, "
        "evidence strength, buyer reachability and credible conversation angle. It is not sorted solely by score.",
        "",
    ]
    for name in TOP10:
        lines.extend(company_selection_text(name, rows[name]))
    OUTPUTS["top10"].write_text("\n".join(lines))


def write_first5(rows: dict[str, dict]) -> None:
    invalidators = {
        "CE Consulting": "Invalidated if office/service routing is already fully automated and no team manually reviews inbound requests.",
        "Ayuda T Pymes": "Invalidated if requests are already cleanly categorized, tracked and routed without manual follow-up.",
        "Aselec Consultores": "Invalidated if contact-form volume is too low or every inquiry is handled ad hoc by the same person without operational pain.",
        "TaxDown": "Invalidated if support/demo/tax-case flows are already fully handled by existing Intercom/HubSpot automation.",
        "Billin": "Invalidated if Zendesk/HubSpot already classifies and routes requests with no manual copying or backlog.",
    }
    lines = [
        "# First 5 Companies Sergio Should Approach",
        "",
        "These are manual commercial-review targets. Do not contact until Sergio reviews the evidence "
        "and identifies real decision makers.",
        "",
    ]
    for name in FIRST5:
        row = rows[name]
        lines.extend(
            [
                f"## {name}",
                "",
                f"- Domain: {row['domain']}",
                f"- Why this company first: {outreach_angle(name, row)}",
                "- Business hypothesis tested: Advisory/client support teams have at least one "
                "repetitive intake, routing, document or follow-up workflow worth automating.",
                f"- What would invalidate it: {invalidators[name]}",
                "- Three discovery questions:",
                "  1. What happens from the moment a client request or document arrives until it is assigned?",
                "  2. Where does someone manually copy, review or reformat information today?",
                "  3. Which request type creates the most follow-up or missing-information work?",
                "- What Sergio should NOT pitch yet: a broad AI transformation project, a chatbot, "
                "a generic CRM replacement, or a multi-month platform build.",
                "",
            ]
        )
    OUTPUTS["first5"].write_text("\n".join(lines))


def write_playbook() -> None:
    lines = [
        "# Professional Services Discovery Playbook",
        "",
        "## Buyer-role Strategy",
        "",
        "| Company size | Likely buyer | Likely champion | Likely blocker |",
        "|---|---|---|---|",
        "| 1-10 employees | Founder / Managing Partner | Senior administrator or lead advisor | External IT/provider or owner skepticism |",
        "| 10-50 employees | Managing Partner / Operations Manager | Office manager / client services lead | Partner worried about disruption or compliance |",
        "| 50-150 employees | COO / Head of Operations | Department ops lead / transformation owner | IT, compliance, data-protection owner |",
        "",
        "## Positioning",
        "",
        "One sentence: Sergio helps advisory firms automate the operational workflow between client "
        "email, documents and internal systems so teams spend less time triaging and copying.",
        "",
        "30-second explanation: I look for one repetitive client-intake or document workflow, then "
        "build a small integration that classifies requests, extracts the useful fields, routes "
        "work to the right place and gives the team a simple control view. AI is only used where "
        "messy text or PDFs make deterministic rules insufficient.",
        "",
        "Problem-oriented positioning: automation and integrations for advisory operations, with "
        "measurable improvement in response time, manual processing and handoff quality.",
        "",
        "## 20-minute Discovery Structure",
        "",
        "- 0-3 min: context. Confirm Sergio is diagnosing one workflow, not pitching a platform.",
        "- 3-12 min: understand workflow. Map one request/document path end to end.",
        "- 12-17 min: quantify pain. Volume, time, rework, missed follow-ups, error risk.",
        "- 17-20 min: agree next step. If pain is real, ask for one sample workflow and propose a small diagnostic.",
        "",
        "## Reusable Questions",
        "",
        "1. What are the most common client requests or documents your team receives every week?",
        "2. What happens from arrival until the request is assigned or completed?",
        "3. Where does someone need to manually copy information between systems?",
        "4. Which request type most often arrives incomplete?",
        "5. How do you track whether a client has replied with missing information?",
        "6. Which inbox, form or channel creates the most operational noise?",
        "7. What reporting do you wish you had without manually compiling it?",
        "8. What part of this workflow would you remove first if you could?",
        "9. What tools already handle this well?",
        "10. If this were improved, what would be visibly different for the team after one month?",
        "",
        "## Commercial Validation Criteria",
        "",
        "Strong validation: at least one of the first five confirms a recurring intake/document "
        "workflow, quantifies pain, and asks for a follow-up/demo/proposal.",
        "",
        "Partial validation: at least three confirm the workflow/pain exists, but no one shows buying "
        "intent or urgency yet.",
        "",
        "Invalidated: most report that the process is already solved, low volume, not economically "
        "important, or owned by an incumbent provider with no appetite for change.",
        "",
        "## Decision Gate",
        "",
        "- A. Is there one Professional Services sub-vertical with a repeatable problem worth validating? **YES**",
        "- B. Can Sergio explain one simple service offer without vague AI transformation language? **YES**",
        "- C. Are there five existing companies with credible evidence-backed conversation reasons? **YES**",
        "- D. Is there a realistic path to the first €900/month? **YES**",
        "",
        "**COMMERCIAL_OUTREACH_READY**",
        "",
        "Next action is human: Sergio reviews the Top 5 evidence, identifies real decision makers, "
        "prepares individual messages, does manual outreach, runs discovery conversations, and records outcomes.",
    ]
    OUTPUTS["playbook"].write_text("\n".join(lines))


def write_json(rows: dict[str, dict], segments: dict[str, dict]) -> None:
    report = {
        "generated_at": datetime.now(UTC).isoformat(),
        "source": "existing Professional Services cohort; no rerun research",
        "winning_subvertical": "Accounting / tax / gestoría advisory",
        "secondary_subvertical": "Legal services",
        "decision_gate": "COMMERCIAL_OUTREACH_READY",
        "segments": segments,
        "top10": [rows[name] for name in TOP10],
        "first5": [rows[name] for name in FIRST5],
    }
    OUTPUTS["json"].write_text(json.dumps(report, indent=2, ensure_ascii=True))


def main() -> None:
    rows = load_rows()
    segments = aggregate(rows)
    write_segmentation(rows, segments)
    write_offer()
    write_top10(rows)
    write_first5(rows)
    write_playbook()
    write_json(rows, segments)
    for path in OUTPUTS.values():
        print(path)


if __name__ == "__main__":
    main()
