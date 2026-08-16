import re
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

RELEVANT_PATHS = ["", "about", "services", "contact", "locations", "careers", "jobs"]


@dataclass(frozen=True)
class ExtractedPage:
    url: str
    title: str
    text: str
    status_code: int


@dataclass(frozen=True)
class DetectedEvidence:
    signal_type: str
    source_url: str
    content_excerpt: str
    confidence: float
    metadata: dict


def normalize_domain(value: str) -> str:
    candidate = value.strip().lower()
    if "://" not in candidate:
        candidate = f"https://{candidate}"
    parsed = urlparse(candidate)
    domain = parsed.netloc or parsed.path
    domain = domain.removeprefix("www.").strip("/")
    if not domain or "." not in domain:
        raise ValueError("Enter a valid company domain")
    return domain


def website_url_for_domain(domain: str) -> str:
    return f"https://{domain}"


async def extract_relevant_pages(domain: str, timeout_seconds: float = 10.0) -> list[ExtractedPage]:
    base_url = website_url_for_domain(domain)
    pages: list[ExtractedPage] = []
    async with httpx.AsyncClient(
        timeout=timeout_seconds,
        follow_redirects=True,
        headers={"User-Agent": "AIProspectingEngine/0.1 research bot"},
    ) as client:
        for path in RELEVANT_PATHS:
            url = urljoin(base_url + "/", path)
            try:
                response = await client.get(url)
            except httpx.HTTPError:
                continue
            content_type = response.headers.get("content-type", "")
            if response.status_code >= 400 or "text/html" not in content_type:
                continue
            pages.append(
                _extract_page(
                    url=str(response.url), html=response.text, status=response.status_code
                )
            )
    return pages


def detect_evidence(pages: list[ExtractedPage]) -> list[DetectedEvidence]:
    evidence: list[DetectedEvidence] = []
    seen: set[tuple[str, str]] = set()
    rules = [
        ("USES_HUBSPOT", r"\bhubspot\b", 0.86),
        ("USES_SALESFORCE", r"\bsalesforce\b", 0.86),
        ("USES_PIPEDRIVE", r"\bpipedrive\b", 0.86),
        ("USES_CALENDLY", r"\bcalendly\b", 0.82),
        ("HAS_CRM", r"\bcrm\b|customer relationship", 0.68),
        ("HAS_SALES_TEAM", r"\bsales team\b|\bsales manager\b|\bcomercial\b|\bventas\b", 0.64),
        ("HIRING_SALES", r"\bhiring\b|\bcareers\b|\bjobs\b|\btrabaja con nosotros\b", 0.58),
        ("MULTIPLE_LOCATIONS", r"\blocations\b|\boffices\b|\bsedes\b|\bdelegaciones\b", 0.62),
        ("MULTIPLE_CONTACT_FORMS", r"\bcontact form\b|\bformulario\b|\bquote request\b", 0.58),
        ("HAS_API", r"\bapi\b|\bintegration\b|\bintegraci[oó]n", 0.56),
    ]
    for page in pages:
        for signal_type, pattern, confidence in rules:
            match = re.search(pattern, page.text, flags=re.IGNORECASE)
            if not match:
                continue
            key = (signal_type, page.url)
            if key in seen:
                continue
            seen.add(key)
            evidence.append(
                DetectedEvidence(
                    signal_type=signal_type,
                    source_url=page.url,
                    content_excerpt=_excerpt(page.text, match.start()),
                    confidence=confidence,
                    metadata={"detector": "regex", "pattern": pattern, "page_title": page.title},
                )
            )
    if pages and not evidence:
        first_page = pages[0]
        evidence.append(
            DetectedEvidence(
                signal_type="PUBLIC_WEBSITE_AVAILABLE",
                source_url=first_page.url,
                content_excerpt=_excerpt(first_page.text, 0),
                confidence=0.5,
                metadata={"detector": "fallback", "page_title": first_page.title},
            )
        )
    return evidence


def _extract_page(url: str, html: str, status: int) -> ExtractedPage:
    soup = BeautifulSoup(html, "html.parser")
    for node in soup(["script", "style", "noscript", "svg"]):
        node.decompose()
    title = soup.title.string.strip() if soup.title and soup.title.string else url
    text = " ".join(soup.get_text(" ").split())
    return ExtractedPage(url=url, title=title[:255], text=text[:6000], status_code=status)


def _excerpt(text: str, start: int, radius: int = 220) -> str:
    begin = max(0, start - radius)
    end = min(len(text), start + radius)
    return text[begin:end].strip()
