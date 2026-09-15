# LeafGuard

LeafGuard is a full-stack Django web platform that instantly diagnoses plant leaf diseases from a photo using a PyTorch ResNet-18 model trained on the PlantVillage dataset. It pairs AI-driven diagnosis with symptom and treatment guidance, scan history tracking, a staff-authored disease-alert blog, and a freemium subscription tier.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Repository Structure](#repository-structure)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Clone the Repository](#1-clone-the-repository)
  - [Create a Virtual Environment](#2-create-a-virtual-environment)
  - [Install Dependencies](#3-install-dependencies)
  - [Configure Environment Variables](#4-configure-environment-variables)
  - [Run Database Migrations](#5-run-database-migrations)
  - [Start the Development Server](#6-start-the-development-server)
- [Environment Variables](#environment-variables)
- [Architecture and Design Notes](#architecture-and-design-notes)
- [Testing](#testing)
- [Disclaimer](#disclaimer)

## Features

**AI-Powered Disease Scanning**
- Upload a leaf photo through a drag-and-drop interface
- Real-time inference via a ResNet-18 model covering 38 plant/disease classes from the PlantVillage dataset
- Returns disease name, confidence score, symptoms, and treatment guidance
- Scan results are snapshotted at scan time, so historical results remain accurate even if the knowledge base is later updated

**Scan History**
- Every scan is logged per user for later review
- Indexed for fast retrieval of a user's most recent scans

**Accounts and Subscription Tiers**
- Custom user model with email-based authentication
- Free tier limited to a configurable number of scans per day
- Premium tier bypasses the daily scan limit
- Profile management with avatar and bio support

**Blog and Disease Alerts**
- Staff-authored articles on plant health, prevention tips, and disease outbreaks
- Rich-text authoring via CKEditor
- Category and tag-based organization

**Platform Foundations**
- Role-based access (guest, registered user, admin/staff)
- Rate limiting on scan submissions
- Media files organized by date to keep storage manageable at scale

## Tech Stack

- **Backend:** Django 6, Django REST Framework
- **Machine Learning:** PyTorch, Torchvision (ResNet-18)
- **Frontend:** Django Templates, Tailwind CSS, Crispy Forms
- **Authentication:** Custom user model with email login, JWT support via `djangorestframework-simplejwt`
- **Rich Text:** django-ckeditor
- **Task Queue:** Celery with Redis (for asynchronous/background work)
- **Database:** SQLite (development), configurable for production
- **Static Files:** WhiteNoise

## Repository Structure

```
LeafGuard/
├── apps/
│   ├── accounts/          Custom user model, authentication, subscription tiers
│   ├── blog/               Disease-alert articles, categories, and tags
│   ├── core/                Home page and shared context processors
│   └── scanner/            Upload form, ML inference service, scan history
├── config/
│   ├── settings/           Base, development, and production settings
│   ├── urls.py              Root URL configuration
│   ├── asgi.py
│   └── wsgi.py
├── ml_models/               Trained model weights and class index mapping
├── media/                   User-uploaded scan images and blog covers
├── static/                  Compiled CSS and JavaScript
├── static_src/               Tailwind CSS source
├── templates/                 HTML templates for all apps
├── manage.py
├── requirements.txt
├── tailwind.config.js
└── postcss.config.js
```

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.12 or higher
- pip (Python package manager)
- Redis (for Celery task queue, optional for basic local development)
- Node.js and npm (only required if rebuilding Tailwind CSS from source)

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/ayush-yogi11/LeafGuard
cd LeafGuard
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root (see [Environment Variables](#environment-variables) below for the full list).

### 5. Run Database Migrations

```bash
python manage.py migrate
```

### 6. Start the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`.

## Environment Variables

The following variables are read via `python-decouple` and should be set in a `.env` file:

| Variable | Description | Default |
|---|---|---|
| `SECRET_KEY` | Django secret key | Required |
| `DEBUG` | Enable debug mode | `False` |
| `ALLOWED_HOSTS` | Comma-separated list of allowed hosts | Empty |
| `FREE_DAILY_SCAN_LIMIT` | Number of scans free-tier users get per day | `3` |

## Architecture and Design Notes

- **Custom User Model:** Role and subscription-tier fields live directly on the user model rather than a separate profile, avoiding an extra join on every request that touches scanning.
- **Singleton ML Service:** The trained model is loaded once into memory using a thread-safe singleton, rather than reloading it on every inference request.
- **Snapshotted Results:** Symptom and treatment text is copied into each scan record at the time of scanning, so edits to the knowledge base never retroactively change a user's historical results.
- **Settings Split:** Base settings are shared, with separate `dev.py` and `prod.py` overrides for environment-specific configuration (e.g., database engine, logging).

## Testing

Each app includes its own `tests.py`. Run the full test suite with:

```bash
python manage.py test
```

## Disclaimer

The disease information provided by LeafGuard is general-purpose reference content generated for educational use and is not a substitute for professional agronomic diagnosis. Growers making real treatment decisions should consult a qualified plant pathologist or agricultural extension service.
