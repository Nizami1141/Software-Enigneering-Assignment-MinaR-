from fastapi import FastAPI

from api.clearance_reports import initial_reports, router as reports_router
from api.prototype_errors import register_error_handlers


def create_prototype_api() -> FastAPI:
    api = FastAPI(title="MinaR Clearance Reports", version="1.0.0", redirect_slashes=False)
    api.state.reports = initial_reports()
    register_error_handlers(api, reports_router)
    api.include_router(reports_router)
    return api


# The assignment can run by itself without loading the satellite and AI integrations.
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None, redirect_slashes=False)
app.mount("/api/v1", create_prototype_api())
