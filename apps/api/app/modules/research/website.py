import asyncio
import hashlib
import re
from dataclasses import dataclass
from urllib.parse import parse_qsl, urlencode, urljoin, urlparse, urlunparse

import httpx
from bs4 import BeautifulSoup

DEFAULT_MAX_PAGES = 12
DEFAULT_MAX_CONTENT_BYTES = 180_000
DEFAULT_RETRIES = 1
DEFAULT_RATE_LIMIT_SECONDS = 0.25
RELEVANT_LINK_KEYWORDS = {
    "about",
    "company",
    "services",
    "solutions",
    "products",
    "pricing",
    "contact",
    "demo",
    "book",
    "sales",
    "locations",
    "offices",
    "campuses",
    "admissions",
    "apply",
    "partners",
    "customers",
    "case",
    "careers",
    "jobs",
    "support",
    "help",
    "integrations",
}
RELEVANT_SEED_PATHS = [
    "about",
    "company",
    "services",
    "solutions",
    "products",
    "pricing",
    "contact",
    "demo",
    "locations",
    "campuses",
    "admissions",
    "apply",
    "partners",
    "customers",
    "case-studies",
    "careers",
    "jobs",
    "support",
    "help",
    "integrations",
]
SKIP_PATH_KEYWORDS = {
    "login",
    "account",
    "signin",
    "signup",
    "privacy",
    "legal",
    "cookies",
    "terms",
    "blog/page",
    "tag/",
    "author/",
}
BINARY_EXTENSIONS = (
    ".pdf",
    ".zip",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".svg",
    ".mp4",
    ".mp3",
    ".doc",
    ".docx",
    ".xls",
    ".xlsx",
)


@dataclass(frozen=True)
class ExtractedPage:
    url: str
    title: str
    text: str
    status_code: int
    selected_reason: str = "seed"
    priority_score: int = 0
    content_bytes: int = 0
    technical_text: str = ""


@dataclass(frozen=True)
class DetectedEvidence:
    signal_type: str
    source_url: str
    content_excerpt: str
    confidence: float
    metadata: dict
    fingerprint: str


@dataclass(frozen=True)
class CrawlSkippedPage:
    url: str
    reason: str


@dataclass(frozen=True)
class CrawlFailure:
    url: str
    error: str


@dataclass(frozen=True)
class CrawlResult:
    pages: list[ExtractedPage]
    discovered_urls: list[str]
    skipped: list[CrawlSkippedPage]
    failures: list[CrawlFailure]
    content_bytes: int


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


async def extract_relevant_pages(
    domain: str,
    timeout_seconds: float = 10.0,
    max_pages: int = DEFAULT_MAX_PAGES,
    max_content_bytes: int = DEFAULT_MAX_CONTENT_BYTES,
    retries: int = DEFAULT_RETRIES,
    rate_limit_seconds: float = DEFAULT_RATE_LIMIT_SECONDS,
) -> CrawlResult:
    base_url = website_url_for_domain(domain)
    normalized_domain = normalize_domain(domain)
    pages: list[ExtractedPage] = []
    discovered: dict[str, tuple[int, str]] = {_normalize_url(base_url): (100, "homepage")}
    skipped: list[CrawlSkippedPage] = []
    failures: list[CrawlFailure] = []
    visited: set[str] = set()
    total_bytes = 0
    for path in RELEVANT_SEED_PATHS:
        discovered[_normalize_url(urljoin(base_url + "/", path))] = (25, f"seed:{path}")
    async with httpx.AsyncClient(
        timeout=timeout_seconds,
        follow_redirects=True,
        headers={"User-Agent": "AIProspectingEngine/0.1 research bot"},
    ) as client:
        while len(pages) < max_pages and discovered:
            url, (score, reason) = _pop_next_url(discovered)
            if url in visited:
                continue
            visited.add(url)
            response = await _fetch(client, url, retries)
            if isinstance(response, CrawlFailure):
                failures.append(response)
                continue
            content_type = response.headers.get("content-type", "")
            final_url = _normalize_url(str(response.url))
            if final_url in visited and final_url != url:
                skipped.append(CrawlSkippedPage(final_url, "duplicate_redirect"))
                continue
            visited.add(final_url)
            if not _same_domain(final_url, normalized_domain):
                skipped.append(CrawlSkippedPage(final_url, "redirected_off_domain"))
                continue
            if response.status_code >= 400:
                skipped.append(CrawlSkippedPage(final_url, f"status_{response.status_code}"))
                continue
            if "text/html" not in content_type:
                skipped.append(CrawlSkippedPage(final_url, "non_html"))
                continue
            page = _extract_page(
                url=final_url,
                html=response.text,
                status=response.status_code,
                selected_reason=reason,
                priority_score=score,
            )
            page_bytes = page.content_bytes
            if total_bytes + page_bytes > max_content_bytes and pages:
                skipped.append(CrawlSkippedPage(final_url, "content_budget_exceeded"))
                continue
            pages.append(
                page
            )
            total_bytes += page_bytes
            for link_url, link_score, link_reason in _discover_links(
                final_url, response.text, normalized_domain
            ):
                if link_url in visited:
                    continue
                if _should_skip_url(link_url):
                    skipped.append(CrawlSkippedPage(link_url, "low_relevance_or_excluded"))
                    continue
                if link_url in discovered and discovered[link_url][0] >= link_score:
                    continue
                discovered[link_url] = (link_score, link_reason)
            if rate_limit_seconds > 0:
                await asyncio.sleep(rate_limit_seconds)
    return CrawlResult(
        pages=pages,
        discovered_urls=sorted(visited | set(discovered)),
        skipped=skipped,
        failures=failures,
        content_bytes=total_bytes,
    )


async def _fetch(
    client: httpx.AsyncClient, url: str, retries: int
) -> httpx.Response | CrawlFailure:
    last_error = "request_failed"
    for attempt in range(retries + 1):
        try:
            return await client.get(url)
        except httpx.HTTPError as exc:
            last_error = exc.__class__.__name__
            if attempt < retries:
                await asyncio.sleep(0.2 * (attempt + 1))
    return CrawlFailure(url, last_error)


def _discover_links(
    page_url: str, html: str, domain: str
) -> list[tuple[str, int, str]]:
    soup = BeautifulSoup(html, "html.parser")
    links: list[tuple[str, int, str]] = []
    for anchor in soup.find_all("a", href=True):
        url = _normalize_url(urljoin(page_url, str(anchor["href"])))
        if not _same_domain(url, domain):
            continue
        anchor_text = " ".join(anchor.get_text(" ").split()).lower()
        parsed_path = urlparse(url).path.lower()
        haystack = f"{anchor_text} {parsed_path}"
        matched = sorted(keyword for keyword in RELEVANT_LINK_KEYWORDS if keyword in haystack)
        if not matched:
            continue
        score = min(99, 40 + len(matched) * 12)
        links.append((url, score, f"matched:{','.join(matched[:4])}"))
    links.sort(key=lambda item: (-item[1], item[0]))
    return links


def _pop_next_url(discovered: dict[str, tuple[int, str]]) -> tuple[str, tuple[int, str]]:
    url, priority = max(discovered.items(), key=lambda item: (item[1][0], -len(item[0])))
    del discovered[url]
    return url, priority


def _same_domain(url: str, domain: str) -> bool:
    try:
        candidate = normalize_domain(url)
    except ValueError:
        return False
    return candidate == domain


def _normalize_url(url: str) -> str:
    parsed = urlparse(url)
    scheme = parsed.scheme.lower() or "https"
    netloc = parsed.netloc.lower().removeprefix("www.")
    path = re.sub(r"/+", "/", parsed.path or "/")
    if path != "/":
        path = path.rstrip("/")
    allowed_query = [
        (key, value)
        for key, value in parse_qsl(parsed.query, keep_blank_values=False)
        if key.lower() in {"page", "p"}
    ][:1]
    return urlunparse(
        (scheme, netloc, path, "", urlencode(allowed_query), "")
    )


def _should_skip_url(url: str) -> bool:
    parsed = urlparse(url)
    path = parsed.path.lower()
    if path.endswith(BINARY_EXTENSIONS):
        return True
    if any(keyword in path for keyword in SKIP_PATH_KEYWORDS):
        return True
    if parsed.query and not any(key in {"page", "p"} for key, _ in parse_qsl(parsed.query)):
        return True
    return False


def detect_evidence(pages: list[ExtractedPage]) -> list[DetectedEvidence]:
    evidence: list[DetectedEvidence] = []
    rules = [
        ("USES_HUBSPOT", r"\bhubspot\b", 0.86),
        ("USES_SALESFORCE", r"\bsalesforce\b", 0.86),
        ("USES_INTERCOM", r"\bintercom\b|intercomcdn|intercom.io", 0.84),
        ("USES_ZENDESK", r"\bzendesk\b|zdassets", 0.84),
        ("USES_TYPEFORM", r"\btypeform\b|typeform.com", 0.82),
        ("USES_CALENDLY", r"\bcalendly\b", 0.82),
        ("USES_GOOGLE_TAG_MANAGER", r"googletagmanager|gtm-[a-z0-9]+", 0.84),
        ("USES_META_PIXEL", r"\bmeta pixel\b|connect.facebook.net|fbq\(", 0.82),
        (
            "HAS_CRM_INDICATORS",
            r"\bcrm\b|customer relationship|gesti[oó]n de clientes",
            0.68,
        ),
        (
            "HAS_MARKETING_AUTOMATION_INDICATORS",
            r"marketing automation|automatizaci[oó]n de marketing|lead nurturing",
            0.66,
        ),
        (
            "HAS_SALES_TEAM",
            r"\bsales team\b|\bsales manager\b|\bcomercial\b|\bventas\b|equipo comercial",
            0.64,
        ),
        (
            "HAS_OPERATIONS_TEAM",
            r"\boperations team\b|\bcoo\b|operaciones|equipo de operaciones",
            0.62,
        ),
        (
            "HAS_CUSTOMER_SUCCESS_TEAM",
            r"customer success|customer care|atenci[oó]n al cliente|soporte al cliente",
            0.62,
        ),
        (
            "MULTIPLE_LOCATIONS",
            r"\blocations\b|\boffices\b|\bsedes\b|\bdelegaciones\b|\bcampus\b",
            0.62,
        ),
        (
            "MULTIPLE_COUNTRIES",
            r"\binternational\b|\bglobal\b|\bpa[ií]ses\b|\bcountries\b|"
            r"\bespa[ñn]a\b.*\b(m[eé]xico|colombia|per[uú]|chile|portugal)\b",
            0.6,
        ),
        (
            "MULTIPLE_LANGUAGES",
            r"\blanguages\b|\bidiomas\b|\bespa[ñn]ol\b.*\benglish\b|\bingl[eé]s\b",
            0.58,
        ),
        (
            "MULTIPLE_PRODUCTS_OR_SERVICES",
            r"\bprogramas\b|\bmasters?\b|\bcursos\b|\bbootcamps?\b|\bservices\b|"
            r"\bsolutions\b|\bproductos\b",
            0.62,
        ),
        (
            "HAS_CONTACT_FORM",
            r"contact form|formulario de contacto|solicita informaci[oó]n|request information",
            0.62,
        ),
        (
            "HAS_DEMO_CTA",
            r"\bbook a demo\b|\brequest a demo\b|\bsolicita una demo\b|\bpide una demo\b",
            0.66,
        ),
        (
            "HAS_BOOKING_FLOW",
            r"\bbook now\b|\bbook a call\b|\breserva\b|\bagenda una llamada\b|\bcalendly\b",
            0.64,
        ),
        (
            "HAS_ADMISSIONS_FLOW",
            r"\badmissions?\b|\badmisiones\b|\bproceso de admisi[oó]n\b",
            0.68,
        ),
        (
            "HAS_APPLICATION_FLOW",
            r"\bapply now\b|\baplica ahora\b|\binscr[ií]bete\b|"
            r"\bsolicitud de admisi[oó]n\b",
            0.66,
        ),
        (
            "HAS_SUPPORT_FLOW",
            r"\bsupport\b|\bhelp center\b|\bcentro de ayuda\b|\bsoporte\b",
            0.62,
        ),
        (
            "HAS_PARTNER_PROGRAM",
            r"\bpartners?\b|\bpartner program\b|\bprograma de partners?\b|colaboradores",
            0.62,
        ),
        (
            "HAS_CUSTOMER_CASE_STUDIES",
            r"case stud(?:y|ies)|casos de [eé]xito|clientes|customer stories",
            0.64,
        ),
        (
            "HAS_INTEGRATIONS",
            r"\bintegrations?\b|\bintegraciones\b|\bconnectors?\b|\bwebhooks?\b",
            0.64,
        ),
        ("HAS_API", r"\bapi\b|\bdeveloper\b|\bdevelopers\b|\bwebhooks?\b", 0.62),
        (
            "HIRING",
            r"\bhiring\b|\bcareers\b|\bjobs\b|\btrabaja con nosotros\b|\bofertas de empleo\b",
            0.6,
        ),
        ("HIRING_SALES", r"\bsales\b|\bventas\b|\bcomercial\b", 0.58),
        ("HIRING_OPERATIONS", r"\boperations?\b|\boperaciones\b", 0.58),
        (
            "HIRING_CUSTOMER_SUCCESS",
            r"customer success|customer support|atenci[oó]n al cliente",
            0.58,
        ),
        (
            "HIRING_ENGINEERING",
            r"\bengineering\b|\bdeveloper\b|\bsoftware\b|\bingenier[ií]a\b|\bdesarrollador",
            0.58,
        ),
        (
            "WHY_NOW",
            r"current openings|open positions|ofertas abiertas|estamos contratando|"
            r"recently launched|nuevo campus|nueva sede|expansi[oó]n",
            0.58,
        ),
    ]
    seen: set[str] = set()
    for page in pages:
        searchable_text = f"{page.text} {page.technical_text}".strip()
        for signal_type, pattern, confidence in rules:
            match = re.search(pattern, searchable_text, flags=re.IGNORECASE)
            if not match:
                continue
            if signal_type.startswith("HIRING") and not _is_hiring_context(page):
                continue
            excerpt = _excerpt(searchable_text, match.start())
            fingerprint = evidence_fingerprint(signal_type, page.url, excerpt)
            if fingerprint in seen:
                continue
            seen.add(fingerprint)
            evidence.append(
                DetectedEvidence(
                    signal_type=signal_type,
                    source_url=page.url,
                    content_excerpt=excerpt,
                    confidence=confidence,
                    metadata={
                        "detector": "regex",
                        "pattern": pattern,
                        "page_title": page.title,
                        "quality": _quality_metadata(page, excerpt, confidence),
                    },
                    fingerprint=fingerprint,
                )
            )
    if pages and not evidence:
        first_page = pages[0]
        excerpt = _excerpt(first_page.text, 0)
        evidence.append(
            DetectedEvidence(
                signal_type="PUBLIC_WEBSITE_AVAILABLE",
                source_url=first_page.url,
                content_excerpt=excerpt,
                confidence=0.5,
                metadata={
                    "detector": "fallback",
                    "page_title": first_page.title,
                    "quality": _quality_metadata(first_page, excerpt, 0.5),
                },
                fingerprint=evidence_fingerprint(
                    "PUBLIC_WEBSITE_AVAILABLE", first_page.url, excerpt
                ),
            )
        )
    return evidence


def evidence_fingerprint(signal_type: str, source_url: str, content: str) -> str:
    normalized = " ".join(content.lower().split())
    payload = f"{signal_type}|{_normalize_url(source_url)}|{normalized[:500]}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _extract_page(
    url: str,
    html: str,
    status: int,
    selected_reason: str = "seed",
    priority_score: int = 0,
    content_bytes: int = 0,
) -> ExtractedPage:
    soup = BeautifulSoup(html, "html.parser")
    technical_text = _technical_markers(html)
    for node in soup(["script", "style", "noscript", "svg"]):
        node.decompose()
    title = soup.title.string.strip() if soup.title and soup.title.string else url
    text = " ".join(soup.get_text(" ").split())
    return ExtractedPage(
        url=url,
        title=title[:255],
        text=text[:12000],
        status_code=status,
        selected_reason=selected_reason,
        priority_score=priority_score,
        content_bytes=content_bytes or len(f"{text} {technical_text}".encode()),
        technical_text=technical_text,
    )


def _excerpt(text: str, start: int, radius: int = 220) -> str:
    begin = max(0, start - radius)
    end = min(len(text), start + radius)
    return text[begin:end].strip()


def _is_hiring_context(page: ExtractedPage) -> bool:
    url_path = urlparse(page.url).path.lower()
    text = page.text.lower()
    return any(term in url_path for term in ("career", "jobs", "trabaja", "empleo")) or any(
        term in text for term in ("open positions", "job openings", "ofertas de empleo")
    )


def _quality_metadata(page: ExtractedPage, excerpt: str, confidence: float) -> dict[str, object]:
    relevance = min(1.0, 0.45 + (page.priority_score / 100) * 0.4 + confidence * 0.15)
    specificity = min(1.0, 0.35 + min(len(excerpt), 260) / 400)
    return {
        "source_relevance": round(relevance, 2),
        "extraction_confidence": confidence,
        "specificity": round(specificity, 2),
    }


def _technical_markers(html: str) -> str:
    markers = re.findall(
        r"hubspot|salesforce|intercom|zendesk|zdassets|typeform|calendly|"
        r"googletagmanager|gtm-[a-z0-9]+|connect\.facebook\.net|fbq\(",
        html,
        flags=re.IGNORECASE,
    )
    return " ".join(markers[:50])
