# Bidii Quality Builders - Construction Management System

A comprehensive Django REST Framework application for managing construction projects, developed for SWE-II final year project.

## Project Overview

Bidii Quality Builders is a construction management system that handles the complete workflow of a building company, from initial customer contact to final payment. The system manages estimates, job scheduling, worker allocation, material ordering, and invoice processing.

## Features

### Core Functionality
- **Customer Management**: Track customer contact details and project history
- **Estimate Processing**: Create estimates from initial contact through property visit to detailed costing
- **Job Scheduling**: Schedule and manage construction jobs with worker assignments
- **Worker Management**: Manage skilled workers (bricklayers, carpenters, plumbers, etc.)
- **Material Ordering**: Track materials, suppliers, and deliveries
- **Invoice & Payment Processing**: Generate invoices and track payments with 30-day payment terms
- **Dashboard Analytics**: Visualize business metrics using Matplotlib charts

### Security Features
- JWT (JSON Web Token) authentication
- Role-based access control
- Secure password hashing
- CSRF protection
- XSS protection
- CORS configuration
- SSL/HTTPS ready

### API Documentation
- Swagger/OpenAPI documentation
- Interactive API testing interface
- ReDoc documentation

## Technology Stack

- **Backend Framework**: Django 4.2.7
- **API Framework**: Django REST Framework 3.14.0
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Data Visualization**: Matplotlib 3.8.2
- **API Documentation**: drf-yasg
- **Task Queue**: Celery with Redis (for background tasks)
- **Security**: django-cors-headers, python-decouple

## Project Structure

```
SWE-II-proj/
├── bidii_project/          # Main project configuration
│   ├── settings.py         # Project settings
│   ├── urls.py            # Main URL configuration
│   └── wsgi.py            # WSGI configuration
├── construction/           # Main application
│   ├── models.py          # Database models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views and viewsets
│   ├── urls.py            # App URL configuration
│   └── admin.py           # Admin interface configuration
├── docs/                  # Project documentation
│   ├── SRS.md            # Software Requirements Specification
│   ├── TEST_PLAN.md      # Test Plan and Test Cases
│   ├── RTM.md            # Requirements Traceability Matrix
│   └── ARCHITECTURE.md   # Software Architecture and Design
├── requirements.txt       # Python dependencies
├── manage.py             # Django management script
└── README.md             # This file
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository
```bash
cd Users\benjamin.karanja\Projects\BCS-3106-Group-IV 
```

### Step 2: Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration
Create a `.env` file in the project root (optional, defaults are provided):
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Step 5: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 7: Run Development Server
```bash
python manage.py runserver
```

The application will be available at:
- API Root: http://127.0.0.1:8000/
- Swagger UI: http://127.0.0.1:8000/swagger/
- ReDoc: http://127.0.0.1:8000/redoc/
- Admin Panel: http://127.0.0.1:8000/admin/

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login (get JWT token)
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `GET /api/auth/user/` - Get current user details

### Customers
- `GET /api/customers/` - List all customers
- `POST /api/customers/` - Create new customer
- `GET /api/customers/{id}/` - Get customer details
- `PUT /api/customers/{id}/` - Update customer
- `DELETE /api/customers/{id}/` - Delete customer
- `GET /api/customers/{id}/estimates/` - Get customer estimates
- `GET /api/customers/{id}/jobs/` - Get customer jobs

### Workers
- `GET /api/workers/` - List all workers
- `POST /api/workers/` - Create new worker
- `GET /api/workers/{id}/` - Get worker details
- `PUT /api/workers/{id}/` - Update worker
- `DELETE /api/workers/{id}/` - Delete worker
- `GET /api/workers/available/` - Get available workers

### Estimates
- `GET /api/estimates/` - List all estimates
- `POST /api/estimates/` - Create new estimate
- `GET /api/estimates/{id}/` - Get estimate details
- `PUT /api/estimates/{id}/` - Update estimate
- `DELETE /api/estimates/{id}/` - Delete estimate
- `GET /api/estimates/pending_visits/` - Get estimates pending visit
- `GET /api/estimates/accepted/` - Get accepted estimates

### Jobs
- `GET /api/jobs/` - List all jobs
- `POST /api/jobs/` - Create new job
- `GET /api/jobs/{id}/` - Get job details
- `PUT /api/jobs/{id}/` - Update job
- `DELETE /api/jobs/{id}/` - Delete job
- `GET /api/jobs/upcoming/` - Get upcoming jobs
- `GET /api/jobs/in_progress/` - Get jobs in progress
- `GET /api/jobs/needs_confirmation/` - Get jobs needing confirmation
- `POST /api/jobs/{id}/confirm/` - Confirm job start date
- `POST /api/jobs/{id}/start/` - Start a job
- `POST /api/jobs/{id}/complete/` - Complete a job

### Suppliers
- `GET /api/suppliers/` - List all suppliers
- `POST /api/suppliers/` - Create new supplier
- `GET /api/suppliers/{id}/` - Get supplier details
- `PUT /api/suppliers/{id}/` - Update supplier
- `DELETE /api/suppliers/{id}/` - Delete supplier

### Materials
- `GET /api/materials/` - List all materials
- `POST /api/materials/` - Create new material
- `GET /api/materials/{id}/` - Get material details
- `PUT /api/materials/{id}/` - Update material
- `DELETE /api/materials/{id}/` - Delete material
- `GET /api/materials/pending_delivery/` - Get materials pending delivery

### Invoices
- `GET /api/invoices/` - List all invoices
- `POST /api/invoices/` - Create new invoice
- `GET /api/invoices/{id}/` - Get invoice details
- `PUT /api/invoices/{id}/` - Update invoice
- `DELETE /api/invoices/{id}/` - Delete invoice
- `GET /api/invoices/overdue/` - Get overdue invoices
- `GET /api/invoices/unpaid/` - Get unpaid invoices

### Payments
- `GET /api/payments/` - List all payments
- `POST /api/payments/` - Create new payment
- `GET /api/payments/{id}/` - Get payment details
- `PUT /api/payments/{id}/` - Update payment
- `DELETE /api/payments/{id}/` - Delete payment

### Dashboard & Reports
- `GET /api/dashboard/stats/` - Get dashboard statistics
- `GET /api/dashboard/charts/` - Get dashboard charts (Matplotlib images)
- `GET /api/reports/?type=summary` - Get summary report
- `GET /api/reports/?type=customer` - Get customer report
- `GET /api/reports/?type=financial` - Get financial report

## Database Models

### Customer
Stores customer information including contact details and address.

### Worker
Represents skilled workers with their specializations, rates, and availability.

### Estimate
Manages estimate workflow from initial contact to acceptance/rejection.

### Job
Handles job scheduling, worker assignments, and project tracking.

### Supplier
Maintains supplier information for material ordering.

### Material
Tracks materials required for jobs, including ordering and delivery.

### Invoice
Manages invoice generation with automatic numbering and payment tracking.

### Payment
Records payments made against invoices with multiple payment methods.

## Business Rules Implemented

1. **Estimate Workflow**
   - Initial contact recorded with basic work description
   - Property visit scheduled
   - Detailed estimate sent within 3 days of property visit
   - Customer accepts/rejects estimate

2. **Job Scheduling**
   - Jobs scheduled based on accepted estimates
   - Start date confirmed few days before job begins
   - Materials ordered for delivery on start date
   - Workers assigned to jobs

3. **Invoice & Payment**
   - Invoice generated at job completion
   - 30-day payment term automatically applied
   - Multiple payments supported per invoice
   - Automatic status updates (paid/overdue)

## Testing

Run tests with:
```bash
python manage.py test construction
```

See `docs/TEST_PLAN.md` for detailed test cases and testing strategy.

## Security Best Practices

1. **Authentication**: JWT-based authentication for API access
2. **Password Security**: Strong password validators enabled
3. **HTTPS**: Configure for production deployment
4. **Environment Variables**: Sensitive data stored in .env file
5. **CORS**: Configured for specific origins
6. **SQL Injection**: Protected by Django ORM
7. **XSS**: Protected by Django's built-in security
8. **CSRF**: CSRF protection enabled

## Production Deployment

### PostgreSQL Setup
Update `.env`:
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=bidii_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### Static Files
```bash
python manage.py collectstatic
```

### Environment Variables
Set `DEBUG=False` and configure proper `SECRET_KEY` and `ALLOWED_HOSTS`.

## Documentation

Comprehensive project documentation is available in the `docs/` directory:

- **SRS.md**: Software Requirements Specification with UML diagrams
- **ARCHITECTURE.md**: System architecture and design decisions
- **TEST_PLAN.md**: Testing strategy and test cases
- **RTM.md**: Requirements Traceability Matrix

## Contributing

This project is developed as a final year Software Engineering II project.

## License

This project is developed for educational purposes.

## Contact

For questions or support, contact the development team.

## Acknowledgments

- Django and Django REST Framework communities
- Bidii Quality Builders (case study provider)
- Software Engineering II course instructors

