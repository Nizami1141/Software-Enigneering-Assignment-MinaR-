# Software-Engineering-Assignment-MinaR-

MinaR helps coordinators and analysts track demining progress. This Assignment 2 prototype provides a REST API for fictional clearance reports and a browser greeting page. [GitHub repository](https://github.com/Nizami1141/Software-Engineering-Assignment-MinaR-)

**[Watch the MinaR team demo on YouTube](https://youtu.be/-CQfO0zoP7A)**

FastAPI handles routing, Pydantic validates report data, and Uvicorn serves the application.

## Features

- Create, read, update and delete clearance reports. Report lists support pagination.
- Authenticate with mock bearer tokens. Regular users can manage their own reports, and the administrator can access reports from both users.
- Validate report fields and return structured errors that identify invalid or missing fields.
- Open a public greeting page with the project description, available routes and team details.

The API starts with four sample reports, two for each regular user. Changes are stored in memory and reset when the server restarts.

## Run the prototype

Use Python 3.10 or later. On Windows, run these commands from the repository root.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r backend/requirements-prototype.txt
cd backend
..\.venv\Scripts\python.exe -m uvicorn prototype:app --port 8000
```

On macOS or Linux, run these commands from the repository root.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r backend/requirements-prototype.txt
cd backend
../.venv/bin/python -m uvicorn prototype:app --port 8000
```

- [Greeting page](http://127.0.0.1:8000/api/v1/greeting)
- [Interactive API documentation](http://127.0.0.1:8000/api/v1/docs)
- [API contract with request and response examples](docs/assignment2-api.md)
- [Postman collection](docs/minar-assignment2.postman_collection.json)
- [Runnable HTTP requests](docs/assignment2-requests.http)

Run the prototype with a single worker so every request uses the same in-memory data.

## API overview

| Method | Path | Operation | Success |
| --- | --- | --- | --- |
| `GET` | `/api/v1/clearance-reports` | List reports with pagination | `200` |
| `GET` | `/api/v1/clearance-reports/{id}` | Read a report | `200` |
| `POST` | `/api/v1/clearance-reports` | Create a report | `201` |
| `PUT` | `/api/v1/clearance-reports/{id}` | Update a report | `200` |
| `DELETE` | `/api/v1/clearance-reports/{id}` | Delete a report | `200` |
| `GET` | `/api/v1/greeting` | Open the public project and team page | `200` (HTML) |

Report endpoints use mock bearer tokens. See the [API reference](docs/assignment2-api.md) for required fields, permissions, and response examples.

## Try a request

```sh
curl -i -H "Authorization: Bearer user-a-token" http://127.0.0.1:8000/api/v1/clearance-reports
```

Use `curl.exe` on Windows PowerShell if `curl` is an alias. On a fresh server, the request returns `200 OK` and the two reports owned by user A. To see the access check, append `/cr-201` to the URL. The same token gets `403 Forbidden` because user B owns that report. Replace it with `admin-token` to get `200 OK`.

The three fixed classroom tokens are `user-a-token`, `user-b-token` and `admin-token`.

To use Postman, start the backend and import the [collection JSON](docs/minar-assignment2.postman_collection.json). Run the collection in order. For individual CRUD requests, **Create a report as A** saves the generated ID for the read, update and delete requests.

In the full MinaR project checkout, start the original Next.js interface from the repository root with `npm install` and `npm run dev`. The original FastAPI application in that checkout mounts the prototype under `/api/v1`.

## Project structure

| File or directory | Purpose |
| --- | --- |
| [backend/prototype.py](backend/prototype.py) | Standalone FastAPI entry point |
| [backend/api/clearance_reports.py](backend/api/clearance_reports.py) | Report routes, sample data, and pagination |
| [backend/api/mock_auth.py](backend/api/mock_auth.py) | Mock tokens and ownership checks |
| [backend/api/report_models.py](backend/api/report_models.py) and [backend/api/prototype_errors.py](backend/api/prototype_errors.py) | Input validation and structured JSON errors |
| [backend/greeting.html](backend/greeting.html) | Public greeting page |
| [docs/](docs/) | API reference, HTTP examples, and Postman collection |

## Contributors

| Team member | Assignment 2 responsibilities |
| --- | --- |
| Elvin Azizli | Report CRUD, sample data and pagination |
| Nizami Guliyev | Mock authentication, role checks and validation |
| Ramil Khaspoladov | Greeting page, API examples and demo |

See [CONTRIBUTORS.md](CONTRIBUTORS.md) for the team roster and original project roles.

Output of `git shortlog -sn --all` from the original local project checkout:

```text
     2	Elvin Azizli
```

Replace this snapshot with the output from the GitHub submission clone after merging the team's pull requests.
