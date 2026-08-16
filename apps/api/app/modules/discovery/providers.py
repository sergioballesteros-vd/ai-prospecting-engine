import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

import httpx

from app.infrastructure.settings import Settings
from app.modules.research.website import normalize_domain


@dataclass(frozen=True)
class DiscoveryCriteria:
    country: str
    city_or_region: str
    industries: list[str]
    employee_min: int | None
    employee_max: int | None
    target_company_count: int


@dataclass(frozen=True)
class CompanyCandidate:
    name: str
    domain: str | None
    website_url: str | None
    industry: str | None
    country: str | None
    city: str | None
    source: str
    source_url: str
    metadata: dict


class CompanyDiscoveryProvider(Protocol):
    provider_name: str

    async def discover(self, criteria: DiscoveryCriteria) -> list[CompanyCandidate]: ...


class CsvCompanyDiscoveryProvider:
    provider_name = "csv"

    def __init__(self, path: str | None = None) -> None:
        self.path = Path(path) if path else None

    async def discover(self, criteria: DiscoveryCriteria) -> list[CompanyCandidate]:
        rows = _fallback_rows() if self.path is None else _read_csv(self.path)
        candidates: list[CompanyCandidate] = []
        for row in rows:
            if not _matches(row, criteria):
                continue
            domain = _safe_domain(row.get("domain") or row.get("website_url") or "")
            candidates.append(
                CompanyCandidate(
                    name=row.get("name", "").strip(),
                    domain=domain,
                    website_url=row.get("website_url") or (f"https://{domain}" if domain else None),
                    industry=row.get("industry") or criteria.industries[0],
                    country=row.get("country") or criteria.country,
                    city=row.get("city") or criteria.city_or_region,
                    source="csv",
                    source_url=str(self.path or "built-in-sample"),
                    metadata={"row": row},
                )
            )
            if len(candidates) >= criteria.target_company_count:
                break
        return [candidate for candidate in candidates if candidate.name and candidate.domain]


class OverpassCompanyDiscoveryProvider:
    provider_name = "overpass"

    def __init__(self, endpoint: str) -> None:
        self.endpoint = endpoint

    async def discover(self, criteria: DiscoveryCriteria) -> list[CompanyCandidate]:
        query = _overpass_query(criteria)
        async with httpx.AsyncClient(
            timeout=25, headers={"User-Agent": "AIProspectingEngine/0.1"}
        ) as client:
            response = await client.post(self.endpoint, data={"data": query})
            response.raise_for_status()
        payload = response.json()
        candidates: list[CompanyCandidate] = []
        for element in payload.get("elements", []):
            tags = element.get("tags", {})
            name = tags.get("name")
            website = tags.get("website") or tags.get("contact:website")
            domain = _safe_domain(website or "")
            if not name or not domain:
                continue
            candidates.append(
                CompanyCandidate(
                    name=name,
                    domain=domain,
                    website_url=website if str(website).startswith("http") else f"https://{domain}",
                    industry=criteria.industries[0] if criteria.industries else None,
                    country=criteria.country,
                    city=criteria.city_or_region,
                    source="overpass",
                    source_url=self.endpoint,
                    metadata={
                        "osm_id": element.get("id"),
                        "osm_type": element.get("type"),
                        "tags": tags,
                    },
                )
            )
            if len(candidates) >= criteria.target_company_count:
                break
        return candidates


def provider_from_settings(settings: Settings) -> CompanyDiscoveryProvider:
    if settings.discovery_provider == "overpass":
        return OverpassCompanyDiscoveryProvider(settings.overpass_endpoint)
    return CsvCompanyDiscoveryProvider(settings.discovery_csv_path)


def _read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _matches(row: dict[str, str], criteria: DiscoveryCriteria) -> bool:
    industry = (row.get("industry") or "").lower()
    city = (row.get("city") or row.get("city_or_region") or "").lower()
    country = (row.get("country") or "").lower()
    if criteria.country and country and criteria.country.lower() not in country:
        return False
    if criteria.city_or_region and city and criteria.city_or_region.lower() not in city:
        return False
    if criteria.industries and industry:
        requested = [item.lower().strip() for item in criteria.industries]
        if not any(item in industry or industry in item for item in requested):
            return False
    return True


def _safe_domain(value: str) -> str | None:
    try:
        return normalize_domain(value)
    except ValueError:
        return None


def _overpass_query(criteria: DiscoveryCriteria) -> str:
    category_regex = "|".join(_industry_terms(criteria.industries))
    area = f"{criteria.city_or_region}, {criteria.country}"
    return f"""
    [out:json][timeout:25];
    area["name"="{area}"]->.searchArea;
    (
      node["name"]["website"]["amenity"~"{category_regex}",i](area.searchArea);
      way["name"]["website"]["amenity"~"{category_regex}",i](area.searchArea);
      relation["name"]["website"]["amenity"~"{category_regex}",i](area.searchArea);
      node["name"]["contact:website"]["amenity"~"{category_regex}",i](area.searchArea);
      way["name"]["contact:website"]["amenity"~"{category_regex}",i](area.searchArea);
      relation["name"]["contact:website"]["amenity"~"{category_regex}",i](area.searchArea);
    );
    out tags {criteria.target_company_count};
    """


def _industry_terms(industries: list[str]) -> list[str]:
    text = " ".join(industries).lower()
    if "training" in text or "education" in text or "formacion" in text or "formación" in text:
        return ["school", "college", "training", "language_school", "music_school"]
    if "clinic" in text or "health" in text:
        return ["clinic", "doctors", "dentist"]
    if "real" in text:
        return ["estate_agent"]
    return ["office", "coworking_space", "school", "clinic"]


def _fallback_rows() -> list[dict[str, str]]:
    return [
        {
            "name": "Ironhack Madrid",
            "domain": "ironhack.com",
            "website_url": "https://www.ironhack.com",
            "industry": "training companies",
            "country": "Spain",
            "city": "Madrid",
        },
        {
            "name": "ThePower Business School",
            "domain": "thepowermba.com",
            "website_url": "https://www.thepowermba.com",
            "industry": "training companies",
            "country": "Spain",
            "city": "Madrid",
        },
        {
            "name": "Codenotch",
            "domain": "codenotch.com",
            "website_url": "https://www.codenotch.com",
            "industry": "training companies",
            "country": "Spain",
            "city": "Madrid",
        },
    ]
