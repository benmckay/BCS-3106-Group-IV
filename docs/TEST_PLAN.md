# Test Plan
## Bidii Quality Builders Construction Management System

**Version:** 1.0  
**Date:** November 12, 2025  
**Project:** SWE-II Final Year Project

---

## Table of Contents
1. [Introduction](#1-introduction)
2. [Test Strategy](#2-test-strategy)
3. [Test Scope](#3-test-scope)
4. [Test Approach](#4-test-approach)
5. [Test Cases](#5-test-cases)
6. [Test Environment](#6-test-environment)
7. [Test Schedule](#7-test-schedule)

---

## 1. Introduction

### 1.1 Purpose
This document describes the test plan for the Bidii Quality Builders Construction Management System, detailing the testing strategy, test cases, and procedures to ensure the system meets all specified requirements.

### 1.2 Scope
This test plan covers:
- Unit testing of individual components
- Integration testing of system modules
- API endpoint testing
- Security testing
- Performance testing
- User acceptance testing

### 1.3 Test Objectives
- Verify all functional requirements are implemented correctly
- Ensure system security and data integrity
- Validate API endpoints and responses
- Confirm system performance meets requirements
- Identify and document defects

---

## 2. Test Strategy

### 2.1 Testing Levels

#### 2.1.1 Unit Testing
- Test individual functions and methods
- Test model validations and properties
- Test serializer validations
- Coverage target: 80%

#### 2.1.2 Integration Testing
- Test API endpoints
- Test database operations
- Test authentication and authorization
- Test business logic workflows

#### 2.1.3 System Testing
- Test complete workflows end-to-end
- Test inter-module dependencies
- Test error handling

#### 2.1.4 Security Testing
- Test authentication mechanisms
- Test authorization controls
- Test input validation
- Test for common vulnerabilities (SQL injection, XSS, CSRF)

#### 2.1.5 Performance Testing
- Test API response times
- Test concurrent user handling
- Test database query performance
- Test chart generation performance

### 2.2 Testing Types

- **Functional Testing**: Verify features work as specified
- **Regression Testing**: Ensure changes don't break existing functionality
- **Security Testing**: Validate security measures
- **Performance Testing**: Verify system performance
- **Usability Testing**: Ensure API is intuitive and well-documented

---

## 3. Test Scope

### 3.1 In Scope
- All API endpoints
- Authentication and authorization
- Database models and validations
- Business logic and calculations
- Dashboard and reporting features
- Security features
- Error handling

### 3.2 Out of Scope
- Third-party library internals
- Database engine internals
- Operating system functionality
- Network infrastructure

---

## 4. Test Approach

### 4.1 Test Automation
- Django's built-in test framework
- REST Framework test utilities
- Automated test execution in CI/CD pipeline

### 4.2 Test Data Management
- Use Django fixtures for test data
- Create test factories for model instances
- Reset database between tests

### 4.3 Defect Management
- Track defects in issue tracking system
- Classify by severity (Critical, High, Medium, Low)
- Retest fixed defects

---

## 5. Test Cases

### 5.1 Authentication Test Cases

#### TC-AUTH-001: User Registration
**Objective**: Verify new user can register  
**Preconditions**: None  
**Test Steps**:
1. Send POST request to `/api/auth/register/`
2. Provide valid username, email, password, password2
3. Verify response status is 201
4. Verify user is created in database

**Expected Result**: User created successfully with hashed password  
**Priority**: High  
**Test Data**:
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "first_name": "Test",
  "last_name": "User",
  "password": "SecurePass123!",
  "password2": "SecurePass123!"
}
```

#### TC-AUTH-002: User Login
**Objective**: Verify user can login with valid credentials  
**Preconditions**: User account exists  
**Test Steps**:
1. Send POST request to `/api/auth/login/`
2. Provide valid username and password
3. Verify response status is 200
4. Verify JWT tokens are returned

**Expected Result**: Access and refresh tokens returned  
**Priority**: High  

#### TC-AUTH-003: Invalid Login
**Objective**: Verify system rejects invalid credentials  
**Preconditions**: None  
**Test Steps**:
1. Send POST request to `/api/auth/login/`
2. Provide invalid credentials
3. Verify response status is 401

**Expected Result**: Authentication error returned  
**Priority**: High  

#### TC-AUTH-004: Token Refresh
**Objective**: Verify token refresh mechanism  
**Preconditions**: Valid refresh token  
**Test Steps**:
1. Send POST request to `/api/auth/token/refresh/`
2. Provide valid refresh token
3. Verify new access token is returned

**Expected Result**: New access token returned  
**Priority**: High  

#### TC-AUTH-005: Protected Endpoint Access
**Objective**: Verify authentication is required for protected endpoints  
**Preconditions**: None  
**Test Steps**:
1. Send GET request to `/api/customers/` without token
2. Verify response status is 401

**Expected Result**: Unauthorized error  
**Priority**: High  

---

### 5.2 Customer Management Test Cases

#### TC-CUST-001: Create Customer
**Objective**: Verify customer can be created  
**Preconditions**: Authenticated user  
**Test Steps**:
1. Send POST request to `/api/customers/`
2. Provide valid customer data
3. Verify response status is 201
4. Verify customer data is returned

**Expected Result**: Customer created successfully  
**Priority**: High  
**Test Data**:
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "+254712345678",
  "address": "123 Main St",
  "city": "Nairobi",
  "postal_code": "00100"
}
```

#### TC-CUST-002: Duplicate Email Validation
**Objective**: Verify system prevents duplicate customer emails  
**Preconditions**: Customer with email exists  
**Test Steps**:
1. Send POST request to `/api/customers/`
2. Provide email that already exists
3. Verify response status is 400
4. Verify validation error message

**Expected Result**: Duplicate email error returned  
**Priority**: High  

#### TC-CUST-003: List Customers
**Objective**: Verify customers can be listed  
**Preconditions**: Customers exist in database  
**Test Steps**:
1. Send GET request to `/api/customers/`
2. Verify response status is 200
3. Verify list of customers is returned

**Expected Result**: Paginated list of customers  
**Priority**: Medium  

#### TC-CUST-004: Search Customers
**Objective**: Verify customer search functionality  
**Preconditions**: Customers exist  
**Test Steps**:
1. Send GET request to `/api/customers/?search=John`
2. Verify response status is 200
3. Verify only matching customers returned

**Expected Result**: Filtered customer list  
**Priority**: Medium  

#### TC-CUST-005: Update Customer
**Objective**: Verify customer can be updated  
**Preconditions**: Customer exists  
**Test Steps**:
1. Send PUT request to `/api/customers/{id}/`
2. Provide updated data
3. Verify response status is 200
4. Verify changes are saved

**Expected Result**: Customer updated successfully  
**Priority**: High  

#### TC-CUST-006: Delete Customer
**Objective**: Verify customer can be deleted  
**Preconditions**: Customer exists with no dependent records  
**Test Steps**:
1. Send DELETE request to `/api/customers/{id}/`
2. Verify response status is 204
3. Verify customer is deleted from database

**Expected Result**: Customer deleted successfully  
**Priority**: Medium  

---

### 5.3 Estimate Management Test Cases

#### TC-EST-001: Create Estimate
**Objective**: Verify estimate can be created  
**Preconditions**: Customer exists, authenticated user  
**Test Steps**:
1. Send POST request to `/api/estimates/`
2. Provide estimate data
3. Verify response status is 201
4. Verify created_by is set to current user

**Expected Result**: Estimate created with PENDING status  
**Priority**: High  

#### TC-EST-002: Property Visit Workflow
**Objective**: Verify estimate workflow from PENDING to VISITED  
**Preconditions**: Estimate with PENDING status exists  
**Test Steps**:
1. Send PUT request to update estimate
2. Set property_visit_date
3. Add detailed_work_description
4. Update status to VISITED
5. Verify changes are saved

**Expected Result**: Estimate status updated to VISITED  
**Priority**: High  

#### TC-EST-003: Send Estimate Workflow
**Objective**: Verify estimate can be marked as SENT  
**Preconditions**: Estimate with VISITED status exists  
**Test Steps**:
1. Send PUT request to update estimate
2. Set estimated_cost and duration
3. Update status to SENT
4. Verify estimate_sent_date is set

**Expected Result**: Estimate marked as SENT with date  
**Priority**: High  

#### TC-EST-004: Three-Day Rule Validation
**Objective**: Verify 3-day sending rule is tracked  
**Preconditions**: Estimate with property_visit_date 4+ days ago  
**Test Steps**:
1. Retrieve estimate
2. Check is_within_3_days_of_visit property
3. Verify it returns False

**Expected Result**: Property correctly identifies late estimates  
**Priority**: Medium  

#### TC-EST-005: Accept Estimate
**Objective**: Verify estimate can be accepted  
**Preconditions**: Estimate with SENT status exists  
**Test Steps**:
1. Send PUT request to update estimate
2. Update status to ACCEPTED
3. Verify response_date is set

**Expected Result**: Estimate marked as ACCEPTED  
**Priority**: High  

---

### 5.4 Job Management Test Cases

#### TC-JOB-001: Create Job from Estimate
**Objective**: Verify job can be created from accepted estimate  
**Preconditions**: Accepted estimate exists  
**Test Steps**:
1. Send POST request to `/api/jobs/`
2. Link to accepted estimate
3. Provide job details
4. Verify response status is 201

**Expected Result**: Job created with SCHEDULED status  
**Priority**: High  

#### TC-JOB-002: Assign Workers to Job
**Objective**: Verify workers can be assigned to job  
**Preconditions**: Job and workers exist  
**Test Steps**:
1. Send PUT request to update job
2. Provide worker_ids array
3. Verify workers are assigned

**Expected Result**: Workers successfully assigned to job  
**Priority**: High  

#### TC-JOB-003: Job Confirmation
**Objective**: Verify job can be confirmed  
**Preconditions**: Job with SCHEDULED status exists  
**Test Steps**:
1. Send POST request to `/api/jobs/{id}/confirm/`
2. Verify status changes to CONFIRMED
3. Verify confirmation_date is set

**Expected Result**: Job confirmed with date recorded  
**Priority**: High  

#### TC-JOB-004: Start Job
**Objective**: Verify job can be started  
**Preconditions**: Job with CONFIRMED status exists  
**Test Steps**:
1. Send POST request to `/api/jobs/{id}/start/`
2. Verify status changes to IN_PROGRESS
3. Verify actual_start_date is set

**Expected Result**: Job started with actual date recorded  
**Priority**: High  

#### TC-JOB-005: Complete Job
**Objective**: Verify job can be completed  
**Preconditions**: Job with IN_PROGRESS status exists  
**Test Steps**:
1. Send POST request to `/api/jobs/{id}/complete/`
2. Verify status changes to COMPLETED
3. Verify actual_end_date is set

**Expected Result**: Job completed with end date recorded  
**Priority**: High  

#### TC-JOB-006: Upcoming Jobs List
**Objective**: Verify upcoming jobs can be retrieved  
**Preconditions**: Future scheduled jobs exist  
**Test Steps**:
1. Send GET request to `/api/jobs/upcoming/`
2. Verify only future jobs are returned
3. Verify jobs are in SCHEDULED or CONFIRMED status

**Expected Result**: List of upcoming jobs  
**Priority**: Medium  

#### TC-JOB-007: Date Validation
**Objective**: Verify end date cannot be before start date  
**Preconditions**: Authenticated user  
**Test Steps**:
1. Send POST request to create job
2. Set end_date before start_date
3. Verify validation error is returned

**Expected Result**: Validation error for invalid dates  
**Priority**: High  

---

### 5.5 Material Management Test Cases

#### TC-MAT-001: Add Material to Job
**Objective**: Verify material can be added to job  
**Preconditions**: Job and supplier exist  
**Test Steps**:
1. Send POST request to `/api/materials/`
2. Provide material details
3. Link to job and supplier
4. Verify material is created

**Expected Result**: Material added successfully  
**Priority**: High  

#### TC-MAT-002: Calculate Material Total Cost
**Objective**: Verify total cost calculation  
**Preconditions**: Material exists  
**Test Steps**:
1. Create material with quantity=10, unit_cost=50
2. Retrieve material
3. Verify total_cost = 500

**Expected Result**: Total cost correctly calculated  
**Priority**: High  

#### TC-MAT-003: Mark Material as Delivered
**Objective**: Verify material delivery tracking  
**Preconditions**: Material with order exists  
**Test Steps**:
1. Send PUT request to update material
2. Set is_delivered=True
3. Set actual_delivery_date
4. Verify changes are saved

**Expected Result**: Material marked as delivered  
**Priority**: Medium  

---

### 5.6 Invoice and Payment Test Cases

#### TC-INV-001: Generate Invoice
**Objective**: Verify invoice can be generated  
**Preconditions**: Completed job exists  
**Test Steps**:
1. Send POST request to `/api/invoices/`
2. Link to completed job
3. Provide costs
4. Verify invoice_number is auto-generated
5. Verify due_date is 30 days from now

**Expected Result**: Invoice created with auto-generated number  
**Priority**: High  

#### TC-INV-002: Invoice Number Auto-Generation
**Objective**: Verify unique invoice numbers are generated  
**Preconditions**: None  
**Test Steps**:
1. Create first invoice
2. Verify invoice_number is "INV-00001"
3. Create second invoice
4. Verify invoice_number is "INV-00002"

**Expected Result**: Sequential invoice numbers  
**Priority**: High  

#### TC-INV-003: Calculate Invoice Total
**Objective**: Verify total amount calculation  
**Preconditions**: None  
**Test Steps**:
1. Create invoice with:
   - labor_cost = 1000
   - material_cost = 500
   - additional_costs = 100
   - tax_rate = 10
2. Verify subtotal = 1600
3. Verify tax_amount = 160
4. Verify total_amount = 1760

**Expected Result**: Correct calculation of all amounts  
**Priority**: High  

#### TC-INV-004: Record Payment
**Objective**: Verify payment can be recorded  
**Preconditions**: Invoice exists  
**Test Steps**:
1. Send POST request to `/api/payments/`
2. Provide payment details
3. Link to invoice
4. Verify payment is recorded
5. Verify invoice.amount_paid is updated

**Expected Result**: Payment recorded and invoice updated  
**Priority**: High  

#### TC-INV-005: Invoice Status Update on Full Payment
**Objective**: Verify invoice status changes to PAID  
**Preconditions**: Invoice with total_amount=1000 exists  
**Test Steps**:
1. Create payment of 1000
2. Verify invoice status changes to PAID
3. Verify balance_due = 0

**Expected Result**: Invoice marked as PAID  
**Priority**: High  

#### TC-INV-006: Partial Payments
**Objective**: Verify multiple partial payments are supported  
**Preconditions**: Invoice with total_amount=1000 exists  
**Test Steps**:
1. Create payment of 400
2. Verify balance_due = 600
3. Create payment of 300
4. Verify balance_due = 300
5. Create payment of 300
6. Verify status = PAID

**Expected Result**: Multiple payments correctly tracked  
**Priority**: High  

#### TC-INV-007: Overdue Invoice Detection
**Objective**: Verify overdue invoices are identified  
**Preconditions**: Invoice with past due_date exists  
**Test Steps**:
1. Send GET request to `/api/invoices/overdue/`
2. Verify overdue invoice is in list
3. Verify status is updated to OVERDUE

**Expected Result**: Overdue invoices correctly identified  
**Priority**: High  

---

### 5.7 Dashboard and Reporting Test Cases

#### TC-DASH-001: Get Dashboard Statistics
**Objective**: Verify dashboard stats are calculated correctly  
**Preconditions**: Test data exists  
**Test Steps**:
1. Send GET request to `/api/dashboard/stats/`
2. Verify response contains all required metrics
3. Verify counts are accurate

**Expected Result**: Accurate statistics returned  
**Priority**: Medium  

#### TC-DASH-002: Generate Job Status Chart
**Objective**: Verify job status chart is generated  
**Preconditions**: Jobs with various statuses exist  
**Test Steps**:
1. Send GET request to `/api/dashboard/charts/`
2. Verify response contains job_status chart
3. Verify it's a valid base64 encoded image

**Expected Result**: Chart image generated successfully  
**Priority**: Medium  

#### TC-DASH-003: Generate Revenue Chart
**Objective**: Verify revenue chart is generated  
**Preconditions**: Invoices exist  
**Test Steps**:
1. Send GET request to `/api/dashboard/charts/`
2. Verify response contains revenue_trend chart
3. Verify chart data reflects actual invoices

**Expected Result**: Revenue chart generated successfully  
**Priority**: Medium  

---

### 5.8 Security Test Cases

#### TC-SEC-001: SQL Injection Prevention
**Objective**: Verify system is protected against SQL injection  
**Preconditions**: None  
**Test Steps**:
1. Send request with SQL injection in search parameter
2. Example: `?search='; DROP TABLE customers; --`
3. Verify no SQL injection occurs
4. Verify appropriate error or empty result

**Expected Result**: SQL injection blocked  
**Priority**: Critical  

#### TC-SEC-002: XSS Prevention
**Objective**: Verify system sanitizes inputs  
**Preconditions**: None  
**Test Steps**:
1. Send POST request with XSS payload in field
2. Example: `<script>alert('XSS')</script>`
3. Verify script is not executed
4. Verify data is sanitized

**Expected Result**: XSS attack prevented  
**Priority**: Critical  

#### TC-SEC-003: CSRF Protection
**Objective**: Verify CSRF protection is active  
**Preconditions**: None  
**Test Steps**:
1. Send POST request without CSRF token
2. Verify request is rejected

**Expected Result**: CSRF protection working  
**Priority**: High  

#### TC-SEC-004: Password Strength Validation
**Objective**: Verify weak passwords are rejected  
**Preconditions**: None  
**Test Steps**:
1. Attempt to register with password "123"
2. Verify validation error is returned
3. Verify password requirements are communicated

**Expected Result**: Weak password rejected  
**Priority**: High  

#### TC-SEC-005: Unauthorized Access Prevention
**Objective**: Verify users can only access authorized resources  
**Preconditions**: Two user accounts exist  
**Test Steps**:
1. Login as User A
2. Attempt to access/modify User B's private data
3. Verify access is denied

**Expected Result**: Unauthorized access prevented  
**Priority**: High  

---

### 5.9 Performance Test Cases

#### TC-PERF-001: API Response Time
**Objective**: Verify API responds within acceptable time  
**Preconditions**: System under normal load  
**Test Steps**:
1. Send GET request to `/api/customers/`
2. Measure response time
3. Verify response time < 2 seconds

**Expected Result**: Fast response time  
**Priority**: Medium  

#### TC-PERF-002: Concurrent Users
**Objective**: Verify system handles multiple concurrent users  
**Preconditions**: Performance test environment  
**Test Steps**:
1. Simulate 100 concurrent users
2. Execute various API operations
3. Verify all requests complete successfully
4. Verify response times remain acceptable

**Expected Result**: System handles concurrent load  
**Priority**: Medium  

#### TC-PERF-003: Database Query Optimization
**Objective**: Verify queries are optimized  
**Preconditions**: Large dataset exists  
**Test Steps**:
1. Enable SQL query logging
2. Execute list endpoints
3. Verify N+1 queries are avoided
4. Verify appropriate use of select_related/prefetch_related

**Expected Result**: Optimized database queries  
**Priority**: Medium  

---

## 6. Test Environment

### 6.1 Hardware Requirements
- Development machine with 8GB RAM minimum
- Processor: Dual-core or better
- Storage: 10GB available space

### 6.2 Software Requirements
- Python 3.8+
- Django 4.2.7
- PostgreSQL or SQLite
- Modern web browser for Swagger UI

### 6.3 Test Tools
- Django Test Framework
- DRF Test utilities
- Coverage.py for code coverage
- Postman/curl for manual API testing
- Locust or Apache JMeter for load testing

---

## 7. Test Schedule

| Phase | Duration | Responsible |
|-------|----------|-------------|
| Unit Testing | 1 week | Developers |
| Integration Testing | 1 week | QA Team |
| System Testing | 3 days | QA Team |
| Security Testing | 2 days | Security Team |
| Performance Testing | 2 days | QA Team |
| UAT | 1 week | Client/Stakeholders |
| Bug Fixes | 1 week | Developers |
| Regression Testing | 2 days | QA Team |

---

## 8. Test Deliverables

- Test plan document (this document)
- Test case specifications
- Test execution reports
- Defect reports
- Test coverage reports
- Test summary report

---

## 9. Exit Criteria

Testing is complete when:
- All critical and high priority test cases pass
- Code coverage ≥ 80%
- No critical or high severity defects open
- All security test cases pass
- Performance requirements met
- UAT sign-off received

---

## 10. Sample Test Implementation

### Example Unit Test (Python/Django)

```python
from django.test import TestCase
from django.contrib.auth.models import User
from construction.models import Customer, Estimate
from datetime import date, timedelta

class EstimateModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='+254712345678',
            address='123 Main St',
            city='Nairobi',
            postal_code='00100'
        )
    
    def test_create_estimate(self):
        """Test creating an estimate"""
        estimate = Estimate.objects.create(
            customer=self.customer,
            created_by=self.user,
            work_description='Build new garage',
            estimated_cost=50000,
            status='PENDING'
        )
        self.assertEqual(estimate.status, 'PENDING')
        self.assertEqual(estimate.customer, self.customer)
    
    def test_estimate_3_day_rule(self):
        """Test 3-day rule for estimate sending"""
        estimate = Estimate.objects.create(
            customer=self.customer,
            created_by=self.user,
            work_description='Build new garage',
            property_visit_date=date.today() - timedelta(days=2)
        )
        self.assertTrue(estimate.is_within_3_days_of_visit)
        
        estimate.property_visit_date = date.today() - timedelta(days=4)
        estimate.save()
        self.assertFalse(estimate.is_within_3_days_of_visit)

class EstimateAPITest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)
        
        self.customer = Customer.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            phone='+254712345678',
            address='123 Main St',
            city='Nairobi',
            postal_code='00100'
        )
    
    def test_create_estimate_api(self):
        """Test creating estimate via API"""
        data = {
            'customer_id': self.customer.id,
            'work_description': 'Build new garage',
            'estimated_cost': 50000,
            'estimated_duration_days': 30
        }
        response = self.client.post('/api/estimates/', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['status'], 'PENDING')
```

---

**Document Approval:**

| Role | Name | Signature | Date |
|------|------|-----------|------|
| QA Lead | Morgan Otieno | BSCNRB547823 | 10/11/2025 |
| Project Manager | Benjamin Karanja | BSCNRB185323 | 10/11/2025 |
| Development Lead | Cyrus Ndirangu | BSCNRB279820 | 10/11/2025 |
| System Architect | Gladys Maseki | BSCNRB116424 | 10/11/2025 |

