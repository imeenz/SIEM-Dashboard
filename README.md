# SIEM Dashboard

A full-stack Security Information and Event Management platform for collecting, normalizing, detecting, and investigating security events through a centralized security operations interface.

![SIEM Dashboard](docs/screenshots/dashboard-overview.png)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Security Event Pipeline](#security-event-pipeline)
- [Detection and Correlation](#detection-and-correlation)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Screenshots](#screenshots)
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Clone the Repository](#clone-the-repository)
  - [Backend Setup](#backend-setup)
  - [Database Setup](#database-setup)
  - [Frontend Setup](#frontend-setup)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Project Status](#project-status)
- [Future Improvements](#future-improvements)
- [License](#license)

---

## Overview

SIEM Dashboard is a full-stack security monitoring platform designed to centralize security events and provide a unified interface for monitoring, detection, alerting, and investigation.

The system receives security events, parses and normalizes them into a consistent structure, stores them in PostgreSQL, and applies detection and correlation logic to identify suspicious activity.

Detected activity is presented through a React-based security operations dashboard backed by a FastAPI REST API.

### Core workflow

```text
Raw Security Event
        │
        ▼
    Ingestion
        │
        ▼
Parsing & Normalization
        │
        ▼
   PostgreSQL
        │
        ▼
Detection & Correlation
        │
        ▼
      Alerts
        │
        ▼
Investigation Dashboard
```

The project focuses on building the core components of a SIEM platform while maintaining a modular architecture that can be extended with additional data sources, detection rules, integrations, and security capabilities.

---

## Features

### Security Event Management

- Centralized security event storage
- Event normalization
- Event search
- Source and destination IP tracking
- Event severity classification
- Security event categorization
- Timestamp-based event tracking

### Detection

- Rule-based security detection
- SSH brute-force detection
- Suspicious firewall activity detection
- Critical IDS alert detection
- Detection-to-event correlation
- Severity classification

### Alert Management

- Centralized alert management
- Critical, High, Medium, and Low severity levels
- Alert status management
- Alert filtering
- Alert search
- Recent alert overview

### Security Operations Dashboard

- Security overview
- Severity KPI cards
- Event activity visualization
- Severity distribution
- Recent alerts
- Real-time-style dashboard updates
- Security operations status indicator

### Authentication

- User registration
- Secure login
- JWT-based authentication
- Protected API endpoints
- Session handling
- Logout functionality
- Protected frontend routes

### API

- RESTful backend API
- FastAPI
- OpenAPI specification
- Swagger UI
- Automatic API documentation

---

## Architecture

The application follows a layered full-stack architecture.

```text
┌───────────────────────────────────────────────┐
│                 React Frontend                │
│             TypeScript + Vite                 │
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
│ Users │ Events │ Detections │ Alerts         │
└───────────────────────────────────────────────┘
```

### Backend layers

The backend is separated into dedicated layers for API handling, business logic, persistence, validation, and infrastructure concerns.

```text
backend/
└── app/
    ├── api/
    ├── core/
    ├── dependencies/
    ├── models/
    ├── repositories/
    ├── schemas/
    ├── services/
    ├── utils/
    └── main.py
```

This separation allows individual components to be extended without tightly coupling the API layer to database implementation details.

---

## Security Event Pipeline

A central part of the platform is the event processing pipeline.

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
     ├───────────────┐
     ▼               ▼
Detection         No Detection
     │
     ▼
Alert Generation
     │
     ▼
Dashboard
```

The normalized event model provides a consistent representation regardless of the original event source.

Examples of events represented in the system include:

- Failed authentication attempts
- Firewall blocks
- Firewall allows
- IDS alerts
- Database service events
- Scheduled task events
- Web server events

---

## Detection and Correlation

The detection layer evaluates normalized events against security rules.

Current detection examples include:

| Detection Rule | Description | Severity |
|---|---|---|
| `ssh_brute_force` | Detects possible SSH brute-force activity | High |
| `suspicious_firewall_activity` | Detects repeated firewall blocks from the same source | High |
| `critical_ids_alert` | Detects critical IDS activity | Critical |

Detections maintain a relationship with the event that triggered them, allowing analysts to move from a detection back to the underlying security event.

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

This relationship provides traceability between raw security activity and the resulting security alert.

---

## Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React |
| Language | TypeScript |
| Frontend Build Tool | Vite |
| Styling | Tailwind CSS |
| Backend | Python |
| API Framework | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Database Migrations | Alembic |
| Authentication | JWT |
| API Specification | OpenAPI |
| API Documentation | Swagger UI |
| Testing | Pytest |
| Python Linting | Ruff |
| Python Formatting | Black |

---

## Project Structure

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

---

## Screenshots

### Authentication

The application provides a dedicated analyst authentication interface using JWT-based authentication.

![Login](docs/screenshots/login.png)

### Security Dashboard

The main dashboard provides a centralized overview of security activity, including severity metrics, event activity, alert distribution, and recent alerts.

![Dashboard Overview](docs/screenshots/dashboard-overview.png)

![Dashboard Alerts](docs/screenshots/dashboard-alerts.png)

### Alerts

The alert management interface allows analysts to search and filter security alerts and update their status.

![Alerts](docs/screenshots/alerts.png)

### Security Events

The events interface exposes normalized security events with severity, source and destination information, event types, messages, and timestamps.

![Security Events](docs/screenshots/events.png)

### Detections

The detection interface provides visibility into security rules and the events that triggered them.

![Detections](docs/screenshots/detections.png)

### API Documentation

The backend exposes an automatically generated OpenAPI specification through FastAPI's Swagger interface.

![API Documentation](docs/screenshots/api-docs.png)

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

---

### Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/siem-dashboard.git
cd siem-dashboard
```

Replace `YOUR_USERNAME` with the GitHub account that hosts the repository.

---

## Backend Setup

Navigate to the backend directory:

```bash
cd backend
```

Create a Python virtual environment:

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the backend dependencies:

```bash
pip install -r requirements.txt
```

---

## Database Setup

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

---

## Frontend Setup

Open a second terminal and navigate to the frontend:

```bash
cd frontend
```

Install the dependencies:

```bash
npm install
```

---

## Configuration

The backend uses environment variables for configuration.

Create the environment file:

```text
backend/.env
```

Configure the database connection and application secret according to the environment configuration used by the backend.

A typical configuration includes:

```env
DATABASE_URL=postgresql://USERNAME:PASSWORD@localhost:5432/siem_dashboard
SECRET_KEY=your-secret-key
```

Use a strong secret key for environments outside local development.

Do not commit `.env` files containing real credentials or secrets to version control.

---

## Running the Application

The backend and frontend are started separately during local development.

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

Open the frontend URL in a browser and sign in using a registered account.

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

---

## Testing

The backend includes an automated test suite covering the main application functionality.

Run the backend tests from the `backend` directory:

```bash
pytest
```

The project has been validated with the complete backend test suite.

Current validation includes:

```text
107 tests passed
```

Code quality checks can also be run with:

```bash
ruff check .
black --check .
```

The frontend can be validated with:

```bash
npm run lint
```

A production frontend build can be generated with:

```bash
npm run build
```

---

## Project Status

The core SIEM platform is complete and functional.

Implemented components include:

- Authentication
- JWT authorization
- Security event management
- Event normalization
- PostgreSQL persistence
- Detection rules
- Detection-to-event relationships
- Alert generation
- Alert management
- Security dashboard
- React frontend
- FastAPI backend
- PostgreSQL database
- Alembic migrations
- REST API
- Swagger/OpenAPI documentation
- Automated backend tests
- Frontend linting
- Production frontend build

The project is currently focused on the core SIEM workflow and is structured to support additional integrations and security capabilities in future iterations.

---

## Future Improvements

Potential extensions include:

- Syslog listener integration
- Additional log source integrations
- Network IDS integration
- Threat intelligence enrichment
- Advanced correlation rules
- MITRE ATT&CK mapping
- IP reputation analysis
- Email and messaging notifications
- Role-based access control
- Advanced incident investigation workflows
- Long-term event analytics
- Additional dashboard visualizations
- Automated response actions

These capabilities are intentionally kept separate from the current core implementation so the existing architecture can evolve without introducing unnecessary infrastructure dependencies.

---

## License

No license has currently been specified for this repository.

If this project is intended to be distributed as open-source software, add an appropriate license file such as MIT, Apache-2.0, or another license that matches the intended usage terms.