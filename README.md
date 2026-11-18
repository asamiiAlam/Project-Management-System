# Project Management System (PMS) — REST API

A Django REST Framework backend for managing departments, projects, tasks, collaborative project chat, employee submissions, and notifications. Authentication uses JWT (SimpleJWT), with a Google Sign-In integration discussed and tested separately.

> **Documentation status (17 November 2026):** This README is based on the shared Django URL/view source, deployment logs, and development conversations—not a fresh checkout of the entire latest repository. **Implemented / previously observed** means present in shared source or earlier observed usage; it does not guarantee that the latest Render deployment includes it. **Confirm** means check the current `PMS/urls.py`, `accounts/urls.py`, and `Project/urls.py`. **Proposed** endpoints are explicitly not claimed as deployed.

## Live environments

| Environment | Base URL |
| --- | --- |
| **Hosted backend (Render)** | **https://project-management-system-ekr7.onrender.com** |
| Frontend (Netlify) | https://management-system-practice.netlify.app |
| Local backend | http://127.0.0.1:8000 |

**API base URL:**

```text
https://project-management-system-ekr7.onrender.com
```

All URL paths below have a trailing slash. Replace `{id}`, `{project_id}`, `{task_id}`, `{user_id}` etc. with numeric IDs.

## Tech stack

- **Backend:** Django + Django REST Framework
- **Authentication:** SimpleJWT access/refresh tokens; Google ID-token exchange (where deployed)
- **Databases:** SQLite (local); PostgreSQL (Render, when `DATABASE_URL` configured)
- **File storage:** Cloudinary where configured
- **Deployment:** Render; WhiteNoise for static files
- **Frontend:** React app deployed on Netlify

## Getting started with the hosted API

### 1. Obtain access and refresh tokens

```bash
curl -X POST "https://project-management-system-ekr7.onrender.com/api/login/" \
  -H "Content-Type: application/json" \
  -d '{"username":"YOUR_USERNAME","password":"YOUR_PASSWORD"}'
```

Typical successful SimpleJWT response:

```json
{"refresh":"<refresh-token>","access":"<access-token>"}
```

### 2. Access a protected endpoint

```bash
curl "https://project-management-system-ekr7.onrender.com/api/profile/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 3. Refresh an expired access token

```bash
curl -X POST "https://project-management-system-ekr7.onrender.com/api/token/refresh/" \
  -H "Content-Type: application/json" \
  -d '{"refresh":"YOUR_REFRESH_TOKEN"}'
```

**Client guidance:** Call `/api/profile/` after login. To determine `Employee` versus `Manager`, the earlier profile-picture serializer exposes a `role` property via `/api/profile-picture/`. The main `/api/profile/` response may not contain `role` or `is_superuser`; these cannot safely be inferred from `is_staff`.

---

## API directory

### Authentication and accounts (`/api/`)

The core account routes below are present in the shared `accounts/urls.py` (assuming the `/api/` mount in the root URLconf).

| Method | Endpoint | Description | Authentication |
| --- | --- | --- | --- |
| `POST` | [`/api/register/`](https://project-management-system-ekr7.onrender.com/api/register/) | Register a user | Public |
| `POST` | [`/api/login/`](https://project-management-system-ekr7.onrender.com/api/login/) | Obtain JWT tokens | Public |
| `POST` | [`/api/token/`](https://project-management-system-ekr7.onrender.com/api/token/) | Alternate JWT login | Public |
| `POST` | [`/api/token/refresh/`](https://project-management-system-ekr7.onrender.com/api/token/refresh/) | Refresh access token | Refresh token |
| `GET` | [`/api/profile/`](https://project-management-system-ekr7.onrender.com/api/profile/) | Get current user | Bearer JWT |
| `PATCH`, `PUT` | [`/api/profile/`](https://project-management-system-ekr7.onrender.com/api/profile/) | Update current user | Bearer JWT |
| `DELETE` | [`/api/profile/`](https://project-management-system-ekr7.onrender.com/api/profile/) | Delete current user (existing generic view; use caution) | Bearer JWT |
| `POST` | [`/api/change-password/`](https://project-management-system-ekr7.onrender.com/api/change-password/) | Change password | Bearer JWT |
| `POST` | [`/api/logout/`](https://project-management-system-ekr7.onrender.com/api/logout/) | Invalidate/blacklist refresh token | Bearer JWT + refresh |
| `POST` | [`/api/forgot-password/`](https://project-management-system-ekr7.onrender.com/api/forgot-password/) | Request password-reset OTP | Public |
| `POST` | [`/api/reset-password/`](https://project-management-system-ekr7.onrender.com/api/reset-password/) | Reset password using OTP | Public |

**Additional account routes observed in later deployment/integration work** (confirm against latest `accounts/urls.py`):

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET`, `PUT`/`PATCH`* | [`/api/profile-picture/`](https://project-management-system-ekr7.onrender.com/api/profile-picture/) | View/update avatar and read profile role |
| `GET` | [`/api/all_employees/`](https://project-management-system-ekr7.onrender.com/api/all_employees/) | List employees for assignment (paginated) |
| `POST` | [`/api/google-login/`](https://project-management-system-ekr7.onrender.com/api/google-login/) | Exchange a Google ID token for Django JWT tokens |

\* Confirm supported upload verb and multipart handling in current view. Successful Google JWT exchange was previously tested; it does not verify the latest route state.

### Departments (`/project/`)

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | [`/project/departments/`](https://project-management-system-ekr7.onrender.com/project/departments/) | List departments |
| `POST` | [`/project/departments/`](https://project-management-system-ekr7.onrender.com/project/departments/) | Create department (authorized staff) |
| `GET` | `/project/departments/{id}/` | Get department |
| `PUT`, `PATCH` | `/project/departments/{id}/` | Update department |
| `DELETE` | `/project/departments/{id}/` | Delete department |
| `GET` | `/project/departments/{department_id}/projects/` | List projects by department |

### Projects

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | [`/project/projects/`](https://project-management-system-ekr7.onrender.com/project/projects/) | List projects (paginated) |
| `POST` | [`/project/projects/`](https://project-management-system-ekr7.onrender.com/project/projects/) | Create project; backend assigns logged-in creator as `manager` in shared view |
| `GET` | `/project/projects/{id}/` | Retrieve project |
| `PUT`, `PATCH` | `/project/projects/{id}/` | Update project |
| `DELETE` | `/project/projects/{id}/` | Delete project |

**Project priority:** Newer code adds `priority` (e.g., `Low`, `Medium`, `High`, `Urgent`, default `Medium`). Confirm database migration and serializer are deployed before relying on it.

### Tasks

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | [`/project/tasks/`](https://project-management-system-ekr7.onrender.com/project/tasks/) | List tasks (paginated) |
| `POST` | [`/project/tasks/`](https://project-management-system-ekr7.onrender.com/project/tasks/) | Create task |
| `GET` | `/project/tasks/{id}/` | Retrieve task |
| `PUT`, `PATCH` | `/project/tasks/{id}/` | Edit task (authorization required) |
| `DELETE` | `/project/tasks/{id}/` | Delete task (authorization required) |
| `GET` | `/project/tasks/user/{user_id}/` | Tasks for a given user (backend must enforce access) |

### Chatboxes and messages

These routes were documented during the project chat implementation. Confirm request payloads and access rules against the latest serializers and permissions.

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/project/chatboxes/{project_id}/` | Read a project's chatbox |
| `GET` | [`/project/chatboxes/admins/`](https://project-management-system-ekr7.onrender.com/project/chatboxes/admins/) | Chatbox admin list |
| `GET` | `/project/chatboxes/admins/{id}/` | Chatbox admin detail |
| `GET`, `POST` | [`/project/messages/`](https://project-management-system-ekr7.onrender.com/project/messages/) | List/send chat messages |
| `GET`, `PUT`, `PATCH`, `DELETE`* | `/project/messages/{id}/` | Message detail and allowed modifications |

\* Exact verbs depend on the currently configured view class. Do not assume project membership is enforced merely because the chatbox can be retrieved.

### Notifications

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | [`/project/notifications/`](https://project-management-system-ekr7.onrender.com/project/notifications/) | Get logged-in user's notifications |
| `POST`* | `/project/notifications/{id}/read/` | Acknowledge/dismiss notification |

\* Earlier implementation reportedly **deletes** the notification rather than setting a persisted `is_read` flag; confirm method and behavior before integrating dismissal.

### Task submissions

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | [`/project/tasks/submissions/`](https://project-management-system-ekr7.onrender.com/project/tasks/submissions/) | List task submissions (scope depends on backend queryset) |
| `POST` | [`/project/tasks/submissions/`](https://project-management-system-ekr7.onrender.com/project/tasks/submissions/) | Submit task result with message, URL, optional file |

**Submission example** (verify serializer field requirements):

```json
{"task":8,"message":"Implementation completed","url":"https://github.com/example/repo"}
```

For file attachment, use `multipart/form-data` and the `file` field, if enabled by the current parser configuration.

---

## Planned / discussed endpoints — NOT VERIFIED AS DEPLOYED

The following were designed during later discussions. **Do not call these from production React until backend URLs, serializers, and permission checks are implemented and tested.**

| Method | Proposed path | Purpose | Access rule |
| --- | --- | --- | --- |
| `GET` | `/project/projects/{project_id}/submissions/` | List submissions across tasks of one project | Project manager or superuser only |
| `PATCH` | `/project/tasks/{task_id}/status/` | Update task status following submission review | Owning project manager or superuser only |
| `GET` | `/project/projects/{project_id}/members/` | List assigned project members | Authorized project participants |
| `POST` | `/project/projects/{project_id}/members/` | Assign project member | Manager or superuser |
| `DELETE` | `/project/projects/{project_id}/members/{user_id}/` | Remove project member | Manager or superuser |

**Important:** Restricting `PATCH /project/tasks/{task_id}/status/` is not sufficient by itself. Existing generic task update routes must also reject unauthorized status updates, otherwise the new manager-only rule can be bypassed. Checking that a task has at least one submission does not prove it was read/reviewed.

---

## Authentication request examples

### Google Sign-In (when installed)

The frontend obtains a Google Identity Services credential and submits the **Google ID token**, not the Google access token:

```http
POST /api/google-login/
Content-Type: application/json

{"id_token":"<google-id-token>"}
```

On success the Django API returns `access` and `refresh` JWTs. Use the same authentication flow as password login, then fetch `/api/profile/` and, where necessary, `/api/profile-picture/`.

### Log out

```http
POST /api/logout/
Authorization: Bearer <access-token>
Content-Type: application/json

{"refresh":"<refresh-token>"}
```

### Update task status (planned route only)

```http
PATCH /project/tasks/8/status/
Authorization: Bearer <manager-or-superuser-access-token>
Content-Type: application/json

{"status":"Completed"}
```

---

## Response conventions

- **`200 OK`:** Successful retrieval or update.
- **`201 Created`:** Successful creation.
- **`204 No Content`:** Successful deletion or dismiss action (where implemented).
- **`400 Bad Request`:** Invalid body/field validation.
- **`401 Unauthorized`:** Missing/expired/invalid bearer token.
- **`403 Forbidden`:** Authenticated but lacks permission.
- **`404 Not Found`:** Resource does not exist or is intentionally concealed.
- **`405 Method Not Allowed`:** Valid URL with unsupported HTTP method.
- **`500 Internal Server Error`:** Unexpected backend failure; inspect server logs.

The shared DRF settings use page-number pagination (`PAGE_SIZE = 3`). A paginated list commonly looks like:

```json
{"count":4,"next":"https://project-management-system-ekr7.onrender.com/project/projects/?page=2","previous":null,"results":[{"id":1}]}
```

This is an **illustration**, not a real response. Clients must follow `next` (or query `?page=N`) to retrieve subsequent pages.

## Authorization overview

| Role | Expected access |
| --- | --- |
| Employee | Own tasks, permitted projects and chat, own submissions/notifications |
| Project Manager | Create/manage owned projects, assign tasks, access project submissions (once review API is installed) |
| Superuser | Administrative access consistent with backend permission checks |

**Security reminder:** Frontend role checks only control visible UI. Object ownership, project membership, task access, and chat permissions **must** be enforced by the Django backend. Shared historical code used broad `queryset = Model.objects.all()` in some list views: review data filtering before release.

## Local development

```bash
# 1. Create and activate a virtual environment
python -m venv venv
# Windows Git Bash:
source venv/Scripts/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure required environment variables in .env
# e.g. SECRET_KEY, DEBUG, DATABASE_URL (if using PostgreSQL),
# GOOGLE_CLIENT_ID, CLOUDINARY_URL, relevant email settings

# 4. Apply migrations
python manage.py migrate

# 5. Run backend
python manage.py runserver
```

- If local `DATABASE_URL` is not set, the earlier settings fall back to SQLite (`db.sqlite3`).
- On Render, confirm PostgreSQL connection and ensure `python manage.py migrate --noinput` runs against the correct database.
- Never commit `.env`, secrets, API tokens, or local database files.
- Set `DEBUG=False` in production and configure trusted hosts/CORS appropriately.

## Maintaining this API reference

Before calling this document complete, compare it with the latest:

1. `PMS/urls.py` — authoritative `/api/` and `/project/` mount points.
2. `accounts/urls.py` — account, token, Google, and profile URLs.
3. `Project/urls.py` — all project, task, chat, notification, and submission URLs.
4. `views.py`, serializers and permission classes — permitted methods, input/output fields, and role restrictions.
5. Production deployment logs and authenticated integration tests — verify the published behavior.

**License:** Add the actual repository license only if the project owner has chosen one.
