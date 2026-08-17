from secrets import compare_digest

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.api.routes import router
from app.infrastructure.settings import get_settings

settings = get_settings()

app = FastAPI(title="AI Prospecting Engine API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in settings.cors_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def is_authorized_request(configured_token: str | None, authorization_header: str | None) -> bool:
    if not configured_token:
        return True
    scheme, _, token = (authorization_header or "").partition(" ")
    return scheme.lower() == "bearer" and compare_digest(token, configured_token)


@app.middleware("http")
async def require_api_token(request: Request, call_next):
    if (
        request.method != "OPTIONS"
        and request.url.path != "/api/health"
        and not is_authorized_request(settings.app_api_token, request.headers.get("authorization"))
    ):
        return JSONResponse({"detail": "Unauthorized"}, status_code=401)
    return await call_next(request)


app.include_router(router, prefix="/api")
