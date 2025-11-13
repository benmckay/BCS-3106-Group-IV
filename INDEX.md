# Project Index and Navigation Guide
## Bidii Quality Builders Construction Management System

**Complete Guide to All Project Files and Documentation**

## Table of Contents

1. [Quick Navigation](#quick-navigation)
2. [Getting Started](#getting-started)
3. [Documentation](#documentation)
4. [Source Code](#source-code)
5. [Testing](#testing)
6. [Configuration](#configuration)



## Quick Navigation

### Start Here!
1. **First Time?** → Read [`QUICKSTART.md`](QUICKSTART.md)
2. **Project Overview?** → Read [`PROJECT_SUMMARY.md`](PROJECT_SUMMARY.md)
3. **Detailed Docs?** → Read [`README.md`](README.md)
4. **Run the App** → See [Quick Start Guide](#getting-started)



## Getting Started

### Essential Files for Setup

| File | Purpose | Action |
|||--|
| [`QUICKSTART.md`](QUICKSTART.md) | 5-minute setup guide | START HERE |
| [`requirements.txt`](requirements.txt) | Python dependencies | `pip install -r requirements.txt` |
| [`README.md`](README.md) | Complete documentation | Read for full details |

### Quick Setup Commands
```bash
# 1. Activate environment
source venv/bin/activate

# 2. Install requirements
pip install -r requirements.txt

# 3. Run migrations
python manage.py migrate

# 4. Create sample data
python manage.py create_sample_data

# 5. Start server
python manage.py runserver

# 5. Open browser: http://127.0.0.1:8000/
```



## Documentation

### Project Documentation (Similar to Project Documentation)

| Document | Location | Pages | Description |
|-|-|-|-|
| **Software Requirements Specification** | [`docs/SRS.md`](docs/SRS.md) | 15+ | Complete functional and non-functional requirements with UML diagrams |
| **Software Architecture & Design** | [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | 20+ | System architecture, design patterns, database schema |
| **Test Plan & Test Cases** | [`docs/TEST_PLAN.md`](docs/TEST_PLAN.md) | 15+ | Testing strategy with 50+ test cases |
| **Requirements Traceability Matrix** | [`docs/RTM.md`](docs/RTM.md) | 12+ | Traceability of all 69 requirements |
| **Project Plan & GANTT Chart** | [`docs/PROJECT_PLAN.md`](docs/PROJECT_PLAN.md) | 10+ | 15-week project timeline and planning |

### Supporting Documentation

| Document | Location | Description |
|-|-|-|
| **Project Summary** | [`PROJECT_SUMMARY.md`](PROJECT_SUMMARY.md) | High-level project overview and achievements |
| **README** | [`README.md`](README.md) | Complete system documentation and user guide |
| **Quick Start Guide** | [`QUICKSTART.md`](QUICKSTART.md) | Fast setup and getting started |
| **This Index** | [`INDEX.md`](INDEX.md) | Navigation guide (you are here!) |



## Source Code

### Main Application Structure

```
construction/
├── models.py              # 8 database models (Customer, Worker, Estimate, etc.)
├── serializers.py         # 15+ DRF serializers for API
├── views.py              # 8 viewsets + dashboard views (40+ endpoints)
├── urls.py               # URL routing for all API endpoints
├── admin.py              # Django admin configuration
├── tests/                # Test suite
│   ├── test_models.py    # 21 model tests (all passing)
│   └── test_api.py       # 15+ API tests
├── management/           # Custom management commands
│   └── commands/
│       └── create_sample_data.py  # Sample data generator
└── migrations/           # Database migrations
```

### Project Configuration

```
bidii_project/
├── settings.py          # Django settings with security config
├── urls.py              # Main URL configuration with Swagger
└── wsgi.py              # WSGI configuration for deployment
```

### Key Files by Purpose

#### Database Models (`construction/models.py`)
- **Customer**: Customer information management
- **Worker**: Skilled worker management
- **Estimate**: Estimate workflow
- **Job**: Job scheduling and tracking
- **Supplier**: Supplier management
- **Material**: Material tracking
- **Invoice**: Invoice generation
- **Payment**: Payment processing

#### API Endpoints (`construction/views.py`)
- **CustomerViewSet**: Customer CRUD + custom actions
- **WorkerViewSet**: Worker management
- **EstimateViewSet**: Estimate workflow management
- **JobViewSet**: Job scheduling with confirm/start/complete
- **MaterialViewSet**: Material tracking
- **InvoiceViewSet**: Invoice management with overdue detection
- **PaymentViewSet**: Payment processing
- **Dashboard Views**: Stats and charts with Matplotlib

#### API Serializers (`construction/serializers.py`)
All models have corresponding serializers with validation:
- CustomerSerializer
- WorkerSerializer
- EstimateSerializer
- JobSerializer
- MaterialSerializer
- InvoiceSerializer
- PaymentSerializer
- Plus detailed and nested variants


## Testing

### Test Files

| File | Tests | Status | Description |
||-|--|-|
| [`construction/tests/test_models.py`](construction/tests/test_models.py) | 21 | All Pass | Model and business logic tests |
| [`construction/tests/test_api.py`](construction/tests/test_api.py) | 15+ | Ready | API endpoint tests |

### Running Tests

```bash
# Run all tests
python manage.py test construction.tests

# Run specific test file
python manage.py test construction.tests.test_models

# Run with verbose output
python manage.py test construction.tests -v 2

# Run with coverage (if installed)
coverage run --source='construction' manage.py test
coverage report
```


## Configuration

### Settings File (`bidii_project/settings.py`)

Key configurations:
- **Security**: JWT, CORS, CSRF protection
- **REST Framework**: Authentication, permissions, pagination
- **Database**: SQLite (dev) / PostgreSQL (prod) ready
- **Static/Media**: File upload configuration
- **Swagger**: API documentation settings

### Environment Variables (`.env` - optional)

Create `.env` file for custom configuration:
```env
SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Dependencies (`requirements.txt`)

Main packages:
- Django 4.2.7
- djangorestframework 3.14.0
- djangorestframework-simplejwt 5.3.1
- matplotlib 3.8.2
- drf-yasg 1.21.7
- And more...



## Project Statistics

### Code Metrics
- **Python Files**: 10+
- **Lines of Code**: 3000+
- **Database Models**: 8
- **API Endpoints**: 40+
- **Test Cases**: 36+
- **Database Fields**: 100+

### Documentation Metrics
- **Total Documents**: 11
- **Documentation Pages**: 90+
- **Requirements**: 69 (all implemented)
- **Test Cases**: 50+ documented
- **UML Diagrams**: 5+


## API Endpoints Quick Reference

### Default Credentials

After running `create_sample_data`:

**Admin User:**
```
Username: admin
Password: admin123
```

**Sample Workers:**
```
john_mason / password123
mary_carpenter / password123
peter_plumber / password123
```



## Project Architecture

### 3-Tier Architecture (Simple MVC)
```
┌─────────────────────────┐
│   Presentation Layer    │  ← API Endpoints (RESTful)
├─────────────────────────┤
│   Business Logic Layer  │  ← Models, Serializers, Views
├─────────────────────────┤
│   Data Access Layer     │  ← Django ORM, Database
└─────────────────────────┘
```

### Technology Stack
- **Backend**: Django 4.2.7
- **API**: Django REST Framework 3.14.0
- **Auth**: JWT (Simple JWT)
- **Database**: SQLite/PostgreSQL
- **Visualization**: Matplotlib
- **Documentation**: Swagger/OpenAPI
- **Testing**: Django Test Framework


### External Resources
- Django Docs: https://docs.djangoproject.com/
- DRF Docs: https://www.django-rest-framework.org/
- Case Study: Bidii Quality Builders Requirements

## Checklist

- [x] All tests pass: `python manage.py test`
- [x] Server runs: `python manage.py runserver`
- [x] Swagger UI accessible: http://127.0.0.1:8000/swagger/
- [x] Sample data loads: `python manage.py create_sample_data`
- [x] All 5 main documents in `docs/` folder
- [x] README.md complete
- [x] Code follows PEP 8
- [x] All requirements implemented (check RTM)
