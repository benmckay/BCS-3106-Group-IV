# Quick Start Guide
## Bidii Quality Builders Construction Management System

Get up and running in 5 minutes!

---

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (included in Python 3)

---

## Step-by-Step Setup

### 1. Navigate to Project Directory
```bash
cd /SWE-II-proj
```

### 2. Activate Virtual Environment
```bash
source venv/bin/activate
```
*(Virtual environment is already created with all dependencies installed)*

### 3. Run Database Migrations
```bash
python manage.py migrate
```

### 4. Create Sample Data (Optional but Recommended)
```bash
python manage.py create_sample_data
```

This creates:
- Admin user (username: `admin`, password: `admin123`)
- 4 sample customers
- 3 workers with different specializations
- 2 suppliers
- Multiple estimates (pending, sent, accepted)
- Sample jobs with workers assigned
- Materials for jobs
- A completed job with invoice and payment

### 5. Start the Development Server
```bash
python manage.py runserver
```

### 6. Access the Application

The server will start at `http://127.0.0.1:8000/`

#### Available Interfaces:

1. **Swagger UI (Interactive API Documentation)**
   - URL: http://127.0.0.1:8000/swagger/
   - Best place to start!
   - Explore all endpoints
   - Test API calls directly

2. **ReDoc (Alternative API Documentation)**
   - URL: http://127.0.0.1:8000/redoc/
   - Cleaner documentation view

3. **Django Admin Panel**
   - URL: http://127.0.0.1:8000/admin/
   - Login: `admin` / `admin123`
   - Manage all data through web interface

4. **API Root**
   - URL: http://127.0.0.1:8000/api/
   - Browse API endpoints

---

## Quick API Testing

### 1. Get JWT Token

**Request:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

Save the `access` token for subsequent requests.

### 2. List Customers

**Request:**
```bash
curl -X GET http://127.0.0.1:8000/api/customers/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 3. Using Swagger UI (Easier!)

1. Go to http://127.0.0.1:8000/swagger/
2. Click "Authorize" button at the top right
3. Enter: `Bearer YOUR_ACCESS_TOKEN`
4. Click "Authorize"
5. Now you can test any endpoint by clicking "Try it out"

---

## Common Tasks

### View Dashboard Statistics
```bash
curl -X GET http://127.0.0.1:8000/api/dashboard/stats/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Create a New Customer
```bash
curl -X POST http://127.0.0.1:8000/api/customers/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "+254712345678",
    "address": "123 Main St",
    "city": "Nairobi",
    "postal_code": "00100"
  }'
```

### List All Jobs
```bash
curl -X GET http://127.0.0.1:8000/api/jobs/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Get Dashboard Charts
```bash
curl -X GET http://127.0.0.1:8000/api/dashboard/charts/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Run Tests

```bash
# Run all tests
python manage.py test construction.tests

# Run specific test file
python manage.py test construction.tests.test_models

# Run with verbose output
python manage.py test construction.tests -v 2
```

---

## Project Structure Overview

```
project/
├── bidii_project/          # Django project settings
├── construction/           # Main application
│   ├── models.py          # Database models
│   ├── views.py           # API views
│   ├── serializers.py     # Data serializers
│   ├── urls.py            # URL routing
│   └── tests/             # Test suite
├── docs/                  # Documentation
├── requirements.txt       # Dependencies
└── manage.py             # Django management
```

---

## API Endpoints Summary

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Get JWT token
- `POST /api/auth/token/refresh/` - Refresh token
- `GET /api/auth/user/` - Get current user

### Core Resources
- `/api/customers/` - Customer management
- `/api/workers/` - Worker management
- `/api/estimates/` - Estimate processing
- `/api/jobs/` - Job scheduling
- `/api/materials/` - Material tracking
- `/api/suppliers/` - Supplier management
- `/api/invoices/` - Invoice generation
- `/api/payments/` - Payment processing

### Analytics
- `/api/dashboard/stats/` - Business statistics
- `/api/dashboard/charts/` - Matplotlib visualizations
- `/api/reports/` - Various reports

---

## Troubleshooting

### Port Already in Use
If port 8000 is busy:
```bash
python manage.py runserver 8001
```

### Database Issues
Reset database:
```bash
rm db.sqlite3
python manage.py migrate
python manage.py create_sample_data
```

### Module Not Found
Ensure virtual environment is activated:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## Next Steps

1. ✅ Explore API using Swagger UI
2. ✅ Review documentation in `docs/` folder
3. ✅ Read `README.md` for detailed information
4. ✅ Check `PROJECT_SUMMARY.md` for project overview
5. ✅ Review test cases in `construction/tests/`

---

## Support

For detailed documentation, see:
- `README.md` - Complete system documentation
- `docs/SRS.md` - Requirements specification
- `docs/ARCHITECTURE.md` - System architecture
- `docs/TEST_PLAN.md` - Testing documentation
- `PROJECT_SUMMARY.md` - Project overview

---

## Default Credentials

**Admin User:**
- Username: `admin`
- Password: `admin123`

**Sample Worker Users:**
- Username: `john_mason` / Password: `password123`
- Username: `mary_carpenter` / Password: `password123`
- Username: `peter_plumber` / Password: `password123`

---

**Happy Coding! 🚀**

*Built with Django REST Framework for SWE-II Final Year Project*

