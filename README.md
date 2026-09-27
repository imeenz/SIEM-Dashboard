# SIEM Dashboard

A full-stack Security Information and Event Management platform for collecting, normalizing, detecting, and investigating security events through a centralized security operations interface.

![SIEM Dashboard](docs/screenshots/dashboard-overview.png)

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React, TypeScript, Vite, Tailwind CSS |
| Backend | Python, FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Migrations | Alembic |
| Authentication | JWT |
| API Documentation | OpenAPI / Swagger |
| Testing | Pytest |
| Code Quality | Ruff, Black |

## Table of Contents

- [Architecture](#architecture)
- [How It Works](#how-it-works)
  - [Core Workflow](#core-workflow)
  - [Security Event Pipeline](#security-event-pipeline)
  - [Detection and Correlation](#detection-and-correlation)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#clone-the-repository)
  - [Backend Setup](#backend-setup)
  - [Database Setup](#database-setup)
  - [Frontend Setup](#frontend-setup)
- [Configuration](#configuration)
- [How to Run](#how-to-run)
  - [Start the Backend](#start-the-backend)
  - [Start the Frontend](#start-the-frontend)
  - [Create an Account](#create-an-account)
  - [Sign In](#sign-in)
- [API Documentation](#api-documentation)
- [Testing](#testing)

---

## Architecture

```text
siem-dashboard/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── dependencies/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── utils/
│   │   └── main.py
│   │
│   ├── alembic/
│   ├── tests/
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.*
│
├── docs/
│   └── screenshots/
│       ├── login.png
│       ├── dashboard-overview.png
│       ├── dashboard-alerts.png
│       ├── alerts.png
│       ├── events.png
│       ├── detections.png
│       └── api-docs.png
│
└── README.md
```

The application follows a layered full-stack architecture.

```text
┌───────────────────────────────────────────────┐
│                 React Frontend                │
│              TypeScript + Vite                │
│                                               │
│  Dashboard │ Events │ Alerts │ Detections    │
└───────────────────────┬───────────────────────┘
                        │
                        │ REST API / JWT
                        ▼
┌───────────────────────────────────────────────┐
│                 FastAPI Backend               │
│                                               │
│  API Routes                                   │
│      │                                        │
│  Services                                     │
│      │                                        │
│  Repositories                                 │
│      │                                        │
│  SQLAlchemy ORM                               │
└───────────────────────┬───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────┐
│                  PostgreSQL                   │
│                                               │
│  Users │ Events │ Detections │ Alerts        │
└───────────────────────────────────────────────┘
```

---

## How It Works

### Core Workflow

The SIEM processes security activity through a series of stages, from event ingestion to analyst investigation.

```text
Security Event
      ↓
   Ingestion
      ↓
Parsing & Normalization
      ↓
 PostgreSQL
      ↓
Detection & Correlation
      ↓
    Alerts
      ↓
Investigation
```

### Security Event Pipeline

Security events are processed through the following pipeline:

```text
Event Source
     │
     ▼
Ingestion
     │
     ▼
Parser
     │
     ▼
Normalization
     │
     ▼
Database Storage
     │
     ▼
Detection Engine
     │
     ▼
Alert Generation
     │
     ▼
Dashboard
```

The normalized event model provides a consistent representation of security activity regardless of the original event source.

Examples of events represented in the system include:

- Failed authentication attempts
- Firewall blocks
- Firewall allows
- IDS alerts
- Database service events
- Scheduled task events
- Web server events

### Detection and Correlation

The detection layer evaluates normalized events against security rules.

```text
Security Event
      │
      ▼
Detection Rule
      │
      ▼
Detection
      │
      ▼
Alert
      │
      ▼
Analyst Investigation
```

Current detection rules include:

| Detection Rule | Description | Severity |
|---|---|---|
| `ssh_brute_force` | Possible SSH brute-force activity | High |
| `suspicious_firewall_activity` | Repeated firewall blocks from the same source | High |
| `critical_ids_alert` | Critical IDS activity | Critical |

Detections maintain a relationship with the event that triggered them, providing traceability between security activity and the resulting alert.

---

## Installation

The application can be run locally with PostgreSQL, Python, and Node.js.

### Prerequisites

Make sure the following are installed:

- Python 3.11 or newer
- Node.js 20 or newer
- PostgreSQL 16 or newer
- Git
- npm

Verify the installations:

```bash
python --version
node --version
npm --version
psql --version
git --version
```

### Clone the Repository

```bash
git clone https://github.com/imeenz/SIEM-Dashboard.git
cd SIEM-Dashboard
```

### Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a Python virtual environment.

#### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the backend dependencies:

```bash
pip install -r requirements.txt
```

### Database Setup

Create a PostgreSQL database for the application.

For example:

```sql
CREATE DATABASE siem_dashboard;
```

Configure the database connection in the backend environment file.

Run the database migrations:

```bash
alembic upgrade head
```

This creates the required database schema.

### Frontend Setup

Open a second terminal and navigate to the frontend directory:

```bash
cd frontend
```

Install the frontend dependencies:

```bash
npm install
```

---

## Configuration

The backend uses environment variables for application configuration.

Create:

```text
backend/.env
```

Configure the database connection and application secret according to your local environment.

Example:

```env
DATABASE_URL=postgresql://USERNAME:PASSWORD@localhost:5432/siem_dashboard
SECRET_KEY=your-secret-key
```

Use a strong secret key for environments outside local development.

Do not commit `.env` files containing real credentials or secrets to version control.

---

## How to Run

After completing the installation and configuration steps, start the backend and frontend separately.

### Start the Backend

From the `backend` directory:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

### Start the Frontend

From the `frontend` directory:

```bash
npm run dev
```

The frontend will normally be available at:

```text
http://localhost:5173
```

Open the frontend URL in your browser.

### Create an Account

On the first launch, create an analyst account through the registration page.

Enter:

- Full name
- Email address
- Password

The account is stored in PostgreSQL and can then be used to authenticate with the application.

### Sign In

After creating an account, use the registered email address and password to access the security operations dashboard.

![Login](docs/screenshots/login.png)

After authentication, the dashboard provides access to:

- Security Overview
- Alerts
- Events
- Detections

![Dashboard](docs/screenshots/dashboard-overview.png)

---

## API Documentation

FastAPI automatically generates interactive API documentation.

Once the backend is running, open:

```text
http://localhost:8000/docs
```

The Swagger interface provides:

- Available API endpoints
- Request parameters
- Request schemas
- Response schemas
- Authentication requirements
- Interactive endpoint testing

The OpenAPI specification is also available through FastAPI's generated OpenAPI endpoint.

![API Documentation](docs/screenshots/api-docs.png)

---

## Testing

The backend includes an automated test suite covering the main application functionality.

Run the backend tests from the `backend` directory:

```bash
pytest
```

The project has been validated with the complete backend test suite.

Current validation:

```text
107 tests passed
```

Run the Python linting checks:

```bash
ruff check .
```

Check Python formatting:

```bash
black --check .
```

From the frontend directory, run the frontend linting checks:

```bash
npm run lint
```

Create a production frontend build:

```bash
npm run build
```

---