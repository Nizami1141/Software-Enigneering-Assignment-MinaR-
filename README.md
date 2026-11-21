# Software-Engineering-Assignment-MinaR-

MinaR helps coordinators and analysts track demining progress. This Assignment 2 prototype provides a REST API for fictional clearance reports and a browser greeting page. [GitHub repository](https://github.com/Nizami1141/Software-Engineering-Assignment-MinaR-)

**[Watch the MinaR team demo on YouTube](https://youtu.be/-CQfO0zoP7A)**

FastAPI handles routing, Pydantic validates report data, and Uvicorn serves the application.

## How the prototype works

1. **Load sample data.** The API starts with two reports for user A and two for user B. Changes are stored in memory and reset on server restart.
2. **Check access.** Each report request uses a mock bearer token. Regular users can manage their own reports. The administrator can view, update and delete any report.
3. **Manage reports.** Use the API to list, read, create, update and delete reports. Lists support pagination. The server validates the sector name, summary and status on create and update.
4. **Return the result.** JSON responses include a success message or an error code. Validation errors identify the fields that need fixing. The public greeting endpoint returns HTML with the project description, team and available routes.

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

To use Postman, start the backend and import the [collection JSON](docs/minar-assignment2.postman_collection.json). Run the collection in order, or send individual requests. For the CRUD demo, send **Create a report as A** first so Postman can save the report ID for the read, update and delete requests.

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

## Demo recording guide

Record one video with all three speakers. Use the same order if you record separate clips and join them afterward. Aim for **4 minutes 20 seconds** and keep the final video under **5 minutes**.

Start the backend with fresh mock data before recording. Keep the request and response, including the HTTP status, visible on screen. Use the [Postman collection](docs/minar-assignment2.postman_collection.json), the [HTTP request file](docs/assignment2-requests.http) or [Swagger](http://127.0.0.1:8000/api/v1/docs). In Swagger, enter the token itself in the **Authorize** dialog.

If Nizami is sharing the screen for all three speakers, start with Swagger open. Keep the greeting page in a second browser tab and the README ready to show at the end. Let the speaker finish each cue before sending the request. Pause briefly on the result so viewers can read it.

### 0:00–1:40 · Elvin Azizli · Report CRUD

**What was built.** Five report endpoints, four sample records and pagination. [CRUD source](backend/api/clearance_reports.py)

Before Elvin starts, Nizami authorizes Swagger with `user-a-token`. For each request, expand the matching operation, click **Try it out**, fill in the fields from the table, then click **Execute**. Read the status from **Server response**.

| Elvin says | Nizami does on screen |
| --- | --- |
| “MinaR tracks clearance progress. I’ll start by listing the reports available to user A.” | Run **GET `/clearance-reports`** with `page=1` and `perPage=1`. Show `200 OK`, one report in `data` and `meta.total: 2` on a fresh server. |
| “Next I’ll create a new draft report.” | Run **POST `/clearance-reports`** with the draft body below. Show `201 Created` and copy the full ID from `data.id`. |
| “I’ll use that ID to read the report back.” | Run **GET `/clearance-reports/{report_id}`** with the copied ID in `report_id`. Show `200 OK` and the matching ID. |
| “Now I’ll update the report to submitted.” | Run **PUT `/clearance-reports/{report_id}`** with the same ID and the submitted body below. Show `200 OK` and `"status": "submitted"`. |
| “Finally I’ll delete the report we just created.” | Run **DELETE `/clearance-reports/{report_id}`** with the same ID. Show `200 OK` and `"data": null`. |
| “A second read confirms that the report is gone.” | Return to **GET `/clearance-reports/{report_id}`** and execute it again with the same ID. Show `404 Not Found`. |
| “Nizami will now explain how access and validation work.” | Leave Swagger visible. Clear the token with **Authorize → Logout → Close** to prepare Nizami’s first request. |

**Draft body for POST**

```json
{
  "sectorName": "Demo Sector A3",
  "summary": "Drafted an end-of-week report.",
  "status": "draft"
}
```

**Submitted body for PUT**

```json
{
  "sectorName": "Demo Sector A3",
  "summary": "Submitted the end-of-week report.",
  "status": "submitted"
}
```

### 1:40–3:20 · Nizami Guliyev · Access and validation

**What was built.** Three mock tokens, ownership checks and a consistent JSON error format. [Auth](backend/api/mock_auth.py) · [Report validation](backend/api/report_models.py) · [Error handlers](backend/api/prototype_errors.py)

**Say**

> Regular users can manage their own reports. The administrator can access all reports. The API returns a different status for a missing token, insufficient permissions or invalid report data.

**Show**

1. Clear authorization and list the reports. Show `401 Unauthorized` and the `UNAUTHORIZED` error code.
2. Authorize as `user-a-token` and request `GET /api/v1/clearance-reports/cr-201`. Show `403 Forbidden` because the report belongs to user B.
3. Switch to `admin-token` and repeat the same request. Show `200 OK` and `ownerId: "user-b"`.
4. Switch back to `user-a-token` and run the **Missing summary** example. Show `400 Bad Request`, `VALIDATION_ERROR` and `summary` in `error.details`.

### 3:20–4:20 · Ramil Khaspoladov · Greeting and documentation

**What was built.** A responsive public greeting page, an API reference and example requests. [Greeting source](backend/greeting.html) · [API reference](docs/assignment2-api.md)

When Nizami finishes showing the validation error, give Ramil the floor. Have the [greeting page](http://127.0.0.1:8000/api/v1/greeting) ready in its own tab. Enter the student IDs before recording this section.

| Ramil says | Nizami does on screen |
| --- | --- |
| “This is MinaR’s public greeting page. It explains what the prototype does and shows that version one is running.” | Switch to the greeting tab. Show the title, project description and `API running · v1` at the top. |
| “The page lists the operations available in the API.” | Scroll to **Available endpoints**. Pause on the list so viewers can see the HTTP methods and paths. |
| “Below that, you can see our team and project roles.” | Scroll to **Project team**. Keep all three names and their student IDs visible while Ramil speaks. |
| “The interactive documentation lets you try each request.” | Click **Open interactive API docs** and show the Swagger operation list. |
| “The README explains how to run the prototype and links to the Postman collection.” | Switch to the README you opened before recording. Show **Run the prototype** and the link to the collection. |
| “Thank you for watching.” | Hold the README on screen until Ramil finishes, then stop recording. |

[Watch the finished team demo](https://youtu.be/-CQfO0zoP7A).

## Three-hour Git work session

Use the public [Nizami1141/Software-Engineering-Assignment-MinaR- repository](https://github.com/Nizami1141/Software-Engineering-Assignment-MinaR-). If it is empty, the owner can add a starter README in GitHub to initialize `main`. The owner invites the other team members as collaborators, and each accepts from their own account.

Make a fresh clone in a new directory. Copy the files for your Assignment 2 feature into that clone. Keep the original project history and credentials in the original checkout.

```sh
git clone https://github.com/Nizami1141/Software-Engineering-Assignment-MinaR-.git
cd Software-Engineering-Assignment-MinaR-
git remote get-url origin
git config user.name "Your Name"
git config user.email "YOUR_GITHUB_EMAIL"
```

Use your verified GitHub email or the `noreply` address listed in your GitHub settings. If you cloned the repository before the owner initialized `main`, run `git fetch origin` and then `git switch --track origin/main` once the branch is available.

Share the push script before the first 30-minute block. It can land as a small tooling PR on `feature/git-work-session` with the message `Add timed pushes for feature branches`.

### Branches and handoffs

| Owner | Feature branch | Files and changes |
| --- | --- | --- |
| Nizami Guliyev | `feature/mock-auth-validation` | Mock tokens, ownership rules, report models and API error handlers |
| Elvin Azizli | `feature/clearance-report-crud` | Report routes, sample data, pagination, prototype startup and FastAPI integration |
| Ramil Khaspoladov | `feature/greeting-and-docs` | HTML greeting and its router, API docs, Postman collection, contributor list and README |

Open each PR into `main`. Merge Nizami's PR first so Elvin's CRUD can import the auth and validation modules. Merge Elvin's PR second so Ramil can add the `greeting_router` import and registration in `backend/prototype.py`. To bring a merged dependency into a feature branch you already pushed, run `git fetch origin` and `git merge origin/main` from that branch.

| Session time | Nizami | Elvin | Ramil |
| --- | --- | --- | --- |
| 0–30 min | Review and commit mock bearer authentication | Verify startup dependencies and commit the prototype requirements | Review and commit the greeting HTML |
| 30–60 min | Commit validation and error handling. Review and merge the first PR. | Review the route contract and prepare CRUD with sample data | Commit the API examples and Postman collection |
| 60–90 min | Review Elvin's changes and test authorization cases | Bring in `main`, then commit CRUD and pagination | Review API docs and update contributor details |
| 90–120 min | Verify error responses in Elvin's PR | Commit FastAPI startup and integration. Review and merge the second PR. | Rehearse the greeting and documentation demo |
| 120–150 min | Review the greeting and access examples | Run the full collection with the greeting integrated | Bring in `main`, commit the greeting router and its registration, and open the final PR |
| 150–180 min | Review the final PR | Verify a fresh start from the final branch | Update the README and contributor summary, then finish the final PR |

Commit each change when it is ready, using a clear message such as `Add mock bearer authentication`, `Add report pagination` or `Add the public greeting route`. Stage specific files with `git add <file>` and review them with `git diff --cached` before committing. Preserve the individual commits when merging the PRs.

### Push your branch every 30 minutes

Run the [feature-branch push script](scripts/push-feature-branch.py) from the repository root in a second terminal after switching to your assigned `feature/` branch.

```sh
python scripts/push-feature-branch.py
```

Use `python3` on systems where that is the Python command. On Windows, you can use `.\.venv\Scripts\python.exe scripts/push-feature-branch.py` after setting up the virtual environment above. The script checks at 30, 60, 90, 120, 150 and 180 minutes and pushes local commits to the same branch name on `origin`. Create commits yourself as you finish each change. Leave the terminal open during the session. Press **Ctrl+C** to stop. A failed push is retried at the next scheduled check. To send a ready change before the next check, run `git push -u origin HEAD` from your feature branch.

### Before submission

- Copy the [.gitignore](.gitignore) to the clean clone and review each staged change for secrets and generated files before committing. Keep local environment files, `node_modules` and build output in your local workspace.
- Fill in the student IDs and each member's actual responsibilities in [CONTRIBUTORS.md](CONTRIBUTORS.md). Update the IDs shown on the greeting page.
- After merging the feature PRs, update your local `main`, run `git shortlog -sn --all`, and replace the snapshot below. Update the README with the team's actual contributions and check that the instructor can open the demo link.

## Contributors

See [CONTRIBUTORS.md](CONTRIBUTORS.md) for team roles and the prototype review split.

Output of `git shortlog -sn --all` from the original local project checkout:

```text
     2	Elvin Azizli
```

Replace this snapshot with the output from the GitHub submission clone after merging the team's pull requests.
