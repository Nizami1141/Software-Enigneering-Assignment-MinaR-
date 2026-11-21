from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from api.mock_auth import CurrentUser, User
from api.report_models import Report, ReportInput


def initial_reports() -> dict[str, Report]:
    entries = [
        ("cr-101", "user-a", "Demo Sector A1", "Prepared the first progress report.", "draft"),
        ("cr-102", "user-a", "Demo Sector A2", "Submitted the weekly progress summary.", "submitted"),
        ("cr-201", "user-b", "Demo Sector B1", "Recorded notes for the weekly summary.", "draft"),
        ("cr-202", "user-b", "Demo Sector B2", "Reviewed the previous progress report.", "reviewed"),
    ]
    return {
        report_id: Report(
            id=report_id, ownerId=owner_id, sectorName=sector, summary=summary, status=status
        )
        for report_id, owner_id, sector, summary, status in entries
    }


def get_reports(request: Request) -> dict[str, Report]:
    return request.app.state.reports


def find_report(reports: dict[str, Report], report_id: str, user: User) -> Report:
    report = reports.get(report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Clearance report was not found.")
    if not user.can_access(report.owner_id):
        raise HTTPException(status_code=403, detail="You do not have access to this report.")
    return report


router = APIRouter(
    prefix="/clearance-reports",
    tags=["Clearance reports"],
    responses={
        401: {"description": "Missing or invalid bearer token"},
        "4XX": {"description": "See the API documentation for client error responses"},
    },
)
Reports = Annotated[dict[str, Report], Depends(get_reports)]


@router.get("", responses={400: {"description": "Invalid pagination parameters"}})
async def list_reports(
    user: CurrentUser,
    reports: Reports,
    page: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(alias="perPage", ge=1, le=50)] = 10,
):
    visible = [report for report in reports.values() if user.can_access(report.owner_id)]
    start = (page - 1) * per_page
    return {
        "success": True,
        "message": "Clearance reports retrieved.",
        "data": [report.model_dump(by_alias=True) for report in visible[start : start + per_page]],
        "meta": {"total": len(visible), "page": page, "perPage": per_page},
    }


report_errors = {
    403: {"description": "Report belongs to another user"},
    404: {"description": "Report was not found"},
}
body_errors = {400: {"description": "Missing or invalid report fields"}}


@router.get("/{report_id}", responses=report_errors)
async def read_report(report_id: str, user: CurrentUser, reports: Reports):
    report = find_report(reports, report_id, user)
    return {
        "success": True,
        "message": "Clearance report retrieved.",
        "data": report.model_dump(by_alias=True),
    }


@router.post("", status_code=201, responses=body_errors)
async def create_report(body: ReportInput, user: CurrentUser, reports: Reports):
    report = Report(
        id=f"cr-{uuid4().hex}", ownerId=user.id, **body.model_dump(by_alias=True)
    )
    reports[report.id] = report
    return {
        "success": True,
        "message": "Clearance report created.",
        "data": report.model_dump(by_alias=True),
    }


@router.put("/{report_id}", responses={**report_errors, **body_errors})
async def update_report(report_id: str, body: ReportInput, user: CurrentUser, reports: Reports):
    existing = find_report(reports, report_id, user)
    updated = Report(id=existing.id, ownerId=existing.owner_id, **body.model_dump(by_alias=True))
    reports[report_id] = updated
    return {
        "success": True,
        "message": "Clearance report updated.",
        "data": updated.model_dump(by_alias=True),
    }


@router.delete("/{report_id}", responses=report_errors)
async def delete_report(report_id: str, user: CurrentUser, reports: Reports):
    find_report(reports, report_id, user)
    del reports[report_id]
    return {"success": True, "message": "Clearance report deleted.", "data": None}
