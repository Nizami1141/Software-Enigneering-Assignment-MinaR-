from fastapi import APIRouter, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException
from starlette.routing import Match

from api.mock_auth import bearer_scheme, require_user


HTTP_ERRORS = {
    400: ("VALIDATION_ERROR", "The request contains invalid or missing fields."),
    401: ("UNAUTHORIZED", "Provide a valid token in the Authorization header."),
    403: ("FORBIDDEN", "You do not have access to this report."),
    404: ("NOT_FOUND", "The requested endpoint or report was not found."),
    405: ("METHOD_NOT_ALLOWED", "This endpoint does not support that HTTP method."),
    500: ("INTERNAL_ERROR", "The API could not complete the request."),
}


def error_response(status: int, message: str | None = None, *, details=None, headers=None):
    code, default_message = HTTP_ERRORS[status]
    error = {"code": code, "message": message or default_message}
    if status == 400:
        error["details"] = details or [{"field": "request", "message": error["message"]}]
    return JSONResponse({"success": False, "error": error}, status_code=status, headers=headers)


def register_error_handlers(app: FastAPI, reports_router: APIRouter):
    @app.exception_handler(HTTPException)
    async def handle_http_error(request: Request, exc: HTTPException):
        headers = dict(exc.headers or {})
        if exc.status_code == 405:
            # The default Allow header can omit methods declared on other routes at this path.
            methods = set()
            for route in [*reports_router.routes, *app.routes]:
                route_methods = getattr(route, "methods", None)
                if route_methods and route.matches(request.scope)[0] == Match.PARTIAL:
                    methods.update(route_methods)
            if methods:
                headers["Allow"] = ", ".join(sorted(methods))
        status = exc.status_code if exc.status_code in HTTP_ERRORS else 500
        message = exc.detail if status in (400, 403) else None
        if status == 404 and exc.detail == "Clearance report was not found.":
            message = exc.detail
        return error_response(status, message, headers=headers)

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: RequestValidationError):
        errors = exc.errors()
        if any(error["type"] == "json_invalid" for error in errors):
            # FastAPI can reject malformed JSON before running the bearer dependency.
            try:
                require_user(await bearer_scheme(request))
            except HTTPException as auth_error:
                return await handle_http_error(request, auth_error)
            return error_response(400, details=[{"field": "body", "message": "Send valid JSON."}])

        details = [
            {
                "field": ".".join(str(part) for part in error["loc"][1:]) or error["loc"][0],
                "message": error["msg"],
            }
            for error in errors
        ]
        return error_response(400, details=details)

    @app.exception_handler(Exception)
    async def handle_server_error(_request: Request, _exc: Exception):
        return error_response(500)
