# MinaR Clearance Reports API

Base URL: `http://127.0.0.1:8000/api/v1`.

The resource represents a fictional progress report for a demo sector. The server assigns the report ID and takes its owner from the authenticated user. A create or update takes the same three editable fields.

| JSON field | Validation |
| --- | --- |
| `sectorName` | Required string, 3–80 characters after trimming |
| `summary` | Required string, 10–500 characters after trimming |
| `status` | Required string, one of `draft`, `submitted` or `reviewed` |

Send a JSON object. Unknown body fields, including `id` and `ownerId`, are rejected. `PUT` replaces all three editable fields and preserves the ID and owner.

## Authentication

Send `Authorization: Bearer <token>` on every clearance report request. Send `Content-Type: application/json` with `POST` and `PUT`.

| Token | Role | Seed report IDs |
| --- | --- | --- |
| `user-a-token` | Regular user A, owns reports with `ownerId: "user-a"` | `cr-101`, `cr-102` |
| `user-b-token` | Regular user B, owns reports with `ownerId: "user-b"` | `cr-201`, `cr-202` |
| `admin-token` | Administrator, can read, update and delete every report. Owns reports it creates. | Can access all four |

Regular users see only their own reports in the list. An authenticated request for a report owned by another user returns `403`. This prototype makes the distinction between an ownership restriction and a missing report explicit for the classroom demo. Use `cr-missing` to demonstrate `404`.

## Endpoints

| Method and path | Parameters | Success | Errors |
| --- | --- | --- | --- |
| `GET /clearance-reports` | Optional query `page` (integer ≥ 1, default 1) and `perPage` (integer 1–50, default 10) | `200`, array with paging metadata | `400`, `401`, `405`, `500` |
| `GET /clearance-reports/{id}` | Path `id`, an existing report ID | `200`, one report | `401`, `403`, `404`, `405`, `500` |
| `POST /clearance-reports` | JSON body with all three editable fields | `201`, the created report | `400`, `401`, `405`, `500` |
| `PUT /clearance-reports/{id}` | Path `id` and JSON body with all three editable fields | `200`, the updated report | `400`, `401`, `403`, `404`, `405`, `500` |
| `DELETE /clearance-reports/{id}` | Path `id` | `200`, with `data: null` | `401`, `403`, `404`, `405`, `500` |
| `GET /greeting` | Public. No headers or parameters required. | `200`, HTML | `405`, `500` |

List paging is applied after ownership filtering. `total` counts all visible entries before paging. A page beyond the end returns an empty array with the same total.

## Example requests and responses

Each example assumes the four seed reports are still present. See [the HTTP request file](assignment2-requests.http) for more cases.

### List reports

```http
GET /api/v1/clearance-reports?page=1&perPage=1
Authorization: Bearer user-a-token
```

`200 OK`

```json
{
  "success": true,
  "message": "Clearance reports retrieved.",
  "data": [
    {"id": "cr-101", "ownerId": "user-a", "sectorName": "Demo Sector A1", "summary": "Prepared the first progress report.", "status": "draft"}
  ],
  "meta": {"total": 2, "page": 1, "perPage": 1}
}
```

### Read a report

```http
GET /api/v1/clearance-reports/cr-101
Authorization: Bearer user-a-token
```

`200 OK`

```json
{
  "success": true,
  "message": "Clearance report retrieved.",
  "data": {"id": "cr-101", "ownerId": "user-a", "sectorName": "Demo Sector A1", "summary": "Prepared the first progress report.", "status": "draft"}
}
```

### Create a report

```http
POST /api/v1/clearance-reports
Authorization: Bearer user-a-token
Content-Type: application/json

{"sectorName": "Demo Sector A3", "summary": "Drafted an end-of-week report.", "status": "draft"}
```

`201 Created`. Copy the ID from the returned report for later requests.

```json
{
  "success": true,
  "message": "Clearance report created.",
  "data": {
    "id": "cr-98e1d3cb095b4e95a08427d122111930",
    "ownerId": "user-a",
    "sectorName": "Demo Sector A3",
    "summary": "Drafted an end-of-week report.",
    "status": "draft"
  }
}
```

### Update a report

```http
PUT /api/v1/clearance-reports/cr-101
Authorization: Bearer user-a-token
Content-Type: application/json

{"sectorName": "Demo Sector A1", "summary": "Finalized the first progress report.", "status": "submitted"}
```

`200 OK`

```json
{
  "success": true,
  "message": "Clearance report updated.",
  "data": {"id": "cr-101", "ownerId": "user-a", "sectorName": "Demo Sector A1", "summary": "Finalized the first progress report.", "status": "submitted"}
}
```

### Delete a report

```http
DELETE /api/v1/clearance-reports/cr-101
Authorization: Bearer user-a-token
```

`200 OK`

```json
{"success": true, "message": "Clearance report deleted.", "data": null}
```

### Open the greeting page

```http
GET /api/v1/greeting
```

`200 OK` with `Content-Type: text/html; charset=utf-8`. The HTML document starts with `<!doctype html>` and includes the heading `MinaR Clearance Reports`.

## Error responses

| Status | Code | When |
| --- | --- | --- |
| `400` | `VALIDATION_ERROR` | Invalid or missing JSON fields, malformed JSON or invalid pagination |
| `401` | `UNAUTHORIZED` | Missing or invalid bearer token. The response includes `WWW-Authenticate: Bearer`. |
| `403` | `FORBIDDEN` | A regular user tries to read, update or delete another user's report |
| `404` | `NOT_FOUND` | Report ID or API path does not exist |
| `405` | `METHOD_NOT_ALLOWED` | Path exists but the HTTP method is unsupported. The response includes `Allow`. |
| `500` | `INTERNAL_ERROR` | Unexpected server failure |

Validation errors include `details`. For example, a request body with no `summary`:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request contains invalid or missing fields.",
    "details": [{"field": "summary", "message": "Field required"}]
  }
}
```

Other errors have a code and message. For example, user A reading `cr-201` gets `403`:

```json
{
  "success": false,
  "error": {"code": "FORBIDDEN", "message": "You do not have access to this report."}
}
```

## Demo walkthrough

1. List as user A and as admin to show that paging totals count only visible reports.
2. Create a report as user A. Copy its returned ID, read it, update it and delete it. Read it again to show `404`.
3. Show `401` without a bearer token, then show user A getting `403` for `cr-201`. Repeat the same read as admin to show `200`.
4. Submit a body missing `summary` to show `400` and the field-level error.
5. Open [the greeting page](http://127.0.0.1:8000/api/v1/greeting) in a browser and show the project, team and endpoint list.
