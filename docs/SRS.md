# Software Requirements Specification (SRS)
## Bidii Quality Builders Construction Management System

**Version:** 1.0  
**Date:** November 12, 2025  
**Project:** SWE-II Final Year Project

---

## Table of Contents
1. [Introduction](#1-introduction)
2. [Overall Description](#2-overall-description)
3. [System Features and Requirements](#3-system-features-and-requirements)
4. [System Modeling](#4-system-modeling)
5. [Non-Functional Requirements](#5-non-functional-requirements)
6. [External Interface Requirements](#6-external-interface-requirements)

---

## 1. Introduction

### 1.1 Purpose
This Software Requirements Specification (SRS) document provides a complete description of the Construction Management System for Bidii Quality Builders. It describes the functional and non-functional requirements, system constraints, and design considerations.

### 1.2 Scope
The Bidii Quality Builders Construction Management System is a web-based application that will:
- Manage customer information and contact details
- Process estimates from initial contact to acceptance
- Schedule and manage construction jobs
- Track skilled workers and their assignments
- Manage material ordering and supplier relationships
- Generate invoices and track payments
- Provide dashboard analytics and reporting

### 1.3 Definitions, Acronyms, and Abbreviations
- **API**: Application Programming Interface
- **DRF**: Django REST Framework
- **JWT**: JSON Web Token
- **CRUD**: Create, Read, Update, Delete
- **SRS**: Software Requirements Specification
- **UI**: User Interface
- **RTM**: Requirements Traceability Matrix

### 1.4 References
- Django Documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- Case Study: Bidii Quality Builders Business Requirements

### 1.5 Overview
The remainder of this document contains detailed descriptions of system functionality, constraints, and requirements organized by feature area.

---

## 2. Overall Description

### 2.1 Product Perspective
The system is a standalone web application that provides a complete construction management solution. It uses:
- Django backend with RESTful API architecture
- JWT-based authentication
- SQLite/PostgreSQL database
- Matplotlib for data visualization

### 2.2 Product Functions
The major functions include:
1. Customer relationship management
2. Estimate creation and tracking
3. Job scheduling and management
4. Worker assignment and tracking
5. Material ordering and delivery tracking
6. Invoice generation and payment processing
7. Dashboard analytics and reporting

### 2.3 User Characteristics
**Primary Users:**
- **Proprietor/Manager**: Full system access, creates estimates, schedules jobs, manages workers
- **Office Staff**: Customer management, estimate tracking, invoice processing
- **Workers**: View assigned jobs and schedules

**User Skill Levels:**
- Basic computer literacy required
- Familiarity with web applications
- No programming knowledge required

### 2.4 Constraints
- Must use Python and Django Framework
- Must implement RESTful API architecture
- Must include secure coding practices
- Must use Matplotlib for visualizations
- Internet connection required for cloud deployment

### 2.5 Assumptions and Dependencies
- Users have modern web browsers
- System has reliable internet connectivity
- Database backup procedures are in place
- SSL certificates configured for production

---

## 3. System Features and Requirements

### 3.1 Customer Management

#### 3.1.1 Description
System shall manage customer information including contact details, addresses, and project history.

#### 3.1.2 Functional Requirements
- **REQ-CM-001**: System shall store customer first name, last name, email, phone, address
- **REQ-CM-002**: System shall validate email uniqueness
- **REQ-CM-003**: System shall provide search functionality by name, email, or phone
- **REQ-CM-004**: System shall display customer's estimate and job history
- **REQ-CM-005**: System shall allow CRUD operations on customer records

#### 3.1.3 Priority
High

---

### 3.2 Estimate Processing

#### 3.2.1 Description
System shall manage the complete estimate workflow from initial contact through property visit to estimate acceptance/rejection.

#### 3.2.2 Functional Requirements
- **REQ-EP-001**: System shall record initial customer contact date and work outline
- **REQ-EP-002**: System shall schedule property visit dates
- **REQ-EP-003**: System shall allow adding detailed work description after property visit
- **REQ-EP-004**: System shall generate detailed cost estimates
- **REQ-EP-005**: System shall track estimate status (Pending, Visited, Sent, Accepted, Rejected)
- **REQ-EP-006**: System shall alert if estimate not sent within 3 days of property visit
- **REQ-EP-007**: System shall record customer response date
- **REQ-EP-008**: System shall link accepted estimates to jobs

#### 3.2.3 Business Rules
- BR-EP-001: Estimate must be sent within 3 days of property visit
- BR-EP-002: Only accepted estimates can be converted to jobs
- BR-EP-003: Estimate must include estimated cost and duration

#### 3.2.4 Priority
High

---

### 3.3 Job Scheduling and Management

#### 3.3.1 Description
System shall manage job scheduling, worker assignments, and project tracking.

#### 3.3.2 Functional Requirements
- **REQ-JM-001**: System shall create jobs from accepted estimates
- **REQ-JM-002**: System shall schedule job start and end dates
- **REQ-JM-003**: System shall assign workers to jobs
- **REQ-JM-004**: System shall track job status (Scheduled, Confirmed, In Progress, Completed, Cancelled)
- **REQ-JM-005**: System shall send confirmation reminders 1-5 days before start
- **REQ-JM-006**: System shall record actual start and end dates
- **REQ-JM-007**: System shall display upcoming jobs
- **REQ-JM-008**: System shall display jobs in progress
- **REQ-JM-009**: System shall link jobs to materials and invoices

#### 3.3.3 Business Rules
- BR-JM-001: Jobs must be based on accepted estimates
- BR-JM-002: Customer confirmation required before job starts
- BR-JM-003: Materials ordered for delivery on job start date
- BR-JM-004: Job can be assigned multiple workers

#### 3.3.4 Priority
High

---

### 3.4 Worker Management

#### 3.4.1 Description
System shall manage skilled workers, their specializations, and availability.

#### 3.4.2 Functional Requirements
- **REQ-WM-001**: System shall store worker details (name, type, contact, rate, experience)
- **REQ-WM-002**: System shall categorize workers (Bricklayer, Carpenter, Plumber, Electrician, Painter, General)
- **REQ-WM-003**: System shall track worker availability status
- **REQ-WM-004**: System shall display available workers for job assignment
- **REQ-WM-005**: System shall track hourly rates
- **REQ-WM-006**: System shall link workers to user accounts

#### 3.4.3 Priority
High

---

### 3.5 Supplier and Material Management

#### 3.5.1 Description
System shall manage suppliers and track materials for jobs.

#### 3.5.2 Functional Requirements
- **REQ-SM-001**: System shall store supplier information
- **REQ-SM-002**: System shall track materials per job
- **REQ-SM-003**: System shall record material quantities, units, and costs
- **REQ-SM-004**: System shall track order dates and delivery dates
- **REQ-SM-005**: System shall mark materials as delivered
- **REQ-SM-006**: System shall calculate total material cost per job

#### 3.5.3 Business Rules
- BR-SM-001: Materials ordered to arrive on job start date
- BR-SM-002: Material cost contributes to invoice total

#### 3.5.4 Priority
Medium

---

### 3.6 Invoice and Payment Processing

#### 3.6.1 Description
System shall generate invoices and track payments with 30-day payment terms.

#### 3.6.2 Functional Requirements
- **REQ-IP-001**: System shall generate invoices at job completion
- **REQ-IP-002**: System shall auto-generate unique invoice numbers
- **REQ-IP-003**: System shall calculate labor, material, and additional costs
- **REQ-IP-004**: System shall apply tax rates
- **REQ-IP-005**: System shall set due date to 30 days from invoice date
- **REQ-IP-006**: System shall track invoice status (Draft, Sent, Paid, Overdue, Cancelled)
- **REQ-IP-007**: System shall record payments against invoices
- **REQ-IP-008**: System shall support multiple payment methods
- **REQ-IP-009**: System shall calculate balance due
- **REQ-IP-010**: System shall identify overdue invoices
- **REQ-IP-011**: System shall auto-update invoice status based on payments

#### 3.6.3 Business Rules
- BR-IP-001: Invoice due date is 30 days from invoice date
- BR-IP-002: Invoice status changes to "Paid" when full amount received
- BR-IP-003: Invoice marked "Overdue" if unpaid past due date
- BR-IP-004: Multiple partial payments allowed per invoice

#### 3.6.4 Priority
High

---

### 3.7 Dashboard and Reporting

#### 3.7.1 Description
System shall provide analytics dashboards with visualizations and reports.

#### 3.7.2 Functional Requirements
- **REQ-DR-001**: System shall display key business statistics
- **REQ-DR-002**: System shall generate charts using Matplotlib:
  - Job status distribution (pie chart)
  - Revenue over time (line chart)
  - Worker type distribution (bar chart)
  - Invoice status distribution (bar chart)
  - Monthly job completion rate (line chart)
- **REQ-DR-003**: System shall provide summary reports
- **REQ-DR-004**: System shall provide customer reports
- **REQ-DR-005**: System shall provide financial reports
- **REQ-DR-006**: Dashboard shall show counts for:
  - Total customers
  - Active/scheduled/completed jobs
  - Pending/accepted estimates
  - Paid/overdue invoices
  - Total/pending revenue
  - Available workers

#### 3.7.3 Priority
Medium

---

### 3.8 Authentication and Security

#### 3.8.1 Description
System shall implement secure authentication and authorization.

#### 3.8.2 Functional Requirements
- **REQ-AS-001**: System shall use JWT for authentication
- **REQ-AS-002**: System shall provide user registration
- **REQ-AS-003**: System shall provide user login/logout
- **REQ-AS-004**: System shall implement role-based access control
- **REQ-AS-005**: System shall enforce strong password requirements
- **REQ-AS-006**: System shall protect against common security vulnerabilities
- **REQ-AS-007**: System shall provide token refresh mechanism

#### 3.8.3 Priority
High

---

## 4. System Modeling

### 4.1 Use Case Diagram

```
                        Bidii Quality Builders System
                        
    +-------------------+
    |   Proprietor      |
    +-------------------+
            |
            |--- Create Estimate
            |--- Schedule Property Visit
            |--- Send Estimate
            |--- Schedule Job
            |--- Assign Workers
            |--- Order Materials
            |--- Generate Invoice
            |--- View Dashboard
            |--- View Reports
            
    +-------------------+
    |   Office Staff    |
    +-------------------+
            |
            |--- Manage Customers
            |--- Track Estimates
            |--- Process Payments
            |--- View Jobs
            
    +-------------------+
    |     Worker        |
    +-------------------+
            |
            |--- View Assigned Jobs
            |--- Update Availability
```

### 4.2 Class Diagram (Simplified)

```
┌─────────────────────┐
│     Customer        │
├─────────────────────┤
│ - first_name        │
│ - last_name         │
│ - email             │
│ - phone             │
│ - address           │
└─────────────────────┘
         │ 1
         │
         │ *
┌─────────────────────┐
│     Estimate        │
├─────────────────────┤
│ - work_description  │
│ - visit_date        │
│ - estimated_cost    │
│ - status            │
└─────────────────────┘
         │ 1
         │
         │ 1
┌─────────────────────┐      ┌─────────────────────┐
│       Job           │  *   │      Worker         │
├─────────────────────┤──────┤─────────────────────│
│ - job_title         │      │ - worker_type       │
│ - start_date        │      │ - hourly_rate       │
│ - end_date          │      │ - is_available      │
│ - status            │      └─────────────────────┘
└─────────────────────┘
         │ 1              │ *
         │                └────────┐
         │ 1                       │
┌─────────────────────┐    ┌──────────────────┐
│     Invoice         │    │    Material      │
├─────────────────────┤    ├──────────────────┤
│ - invoice_number    │    │ - name           │
│ - labor_cost        │    │ - quantity       │
│ - material_cost     │    │ - unit_cost      │
│ - due_date          │    │ - is_delivered   │
│ - status            │    └──────────────────┘
└─────────────────────┘
         │ 1
         │
         │ *
┌─────────────────────┐
│      Payment        │
├─────────────────────┤
│ - amount            │
│ - payment_method    │
│ - payment_date      │
└─────────────────────┘
```

### 4.3 Sequence Diagram - Estimate to Job Workflow

```
Customer    Proprietor    System         Database
   │            │            │              │
   │──Contact──>│            │              │
   │            │──Create────>│              │
   │            │  Estimate  │──Store──────>│
   │            │            │              │
   │            │──Schedule  │              │
   │            │  Visit     │──Update─────>│
   │            │            │              │
   │<──Visit────│            │              │
   │  Property  │            │              │
   │            │            │              │
   │            │──Add Detail│              │
   │            │  & Cost    │──Update─────>│
   │            │            │              │
   │<──Send─────│            │              │
   │  Estimate  │            │              │
   │            │            │              │
   │──Accept────>│            │              │
   │  Estimate  │──Update────>│              │
   │            │  Status    │──Update─────>│
   │            │            │              │
   │            │──Create────>│              │
   │            │  Job       │──Store──────>│
   │            │            │              │
   │<──Confirm──│            │              │
   │  Start Date│            │              │
```

### 4.4 State Diagram - Estimate Status

```
        [New Contact]
              │
              ▼
        ┌──────────┐
        │ PENDING  │
        └──────────┘
              │
              │ (Property Visit)
              ▼
        ┌──────────┐
        │ VISITED  │
        └──────────┘
              │
              │ (Send Estimate)
              ▼
        ┌──────────┐
        │   SENT   │
        └──────────┘
              │
         ┌────┴────┐
         │         │
(Customer         (Customer
 Accepts)         Rejects)
         │         │
         ▼         ▼
    ┌────────┐ ┌─────────┐
    │ACCEPTED│ │REJECTED │
    └────────┘ └─────────┘
         │
         │ (Create Job)
         ▼
    [Job Created]
```

### 4.5 State Diagram - Job Status

```
    [Job Created]
         │
         ▼
   ┌──────────┐
   │SCHEDULED │
   └──────────┘
         │
         │ (Confirm)
         ▼
   ┌──────────┐
   │CONFIRMED │
   └──────────┘
         │
         │ (Start)
         ▼
   ┌───────────┐
   │IN_PROGRESS│
   └───────────┘
         │
         │ (Complete)
         ▼
   ┌──────────┐
   │COMPLETED │
   └──────────┘
         │
         │ (Generate Invoice)
         ▼
   [Invoice Created]
```

### 4.6 Entity-Relationship Diagram

```
Customer ||──o{ Estimate : "requests"
Estimate ||──o| Job : "converts to"
Job ||──o{ Material : "requires"
Job }o──o{ Worker : "assigned to"
Material }o──|| Supplier : "supplied by"
Job ||──o| Invoice : "generates"
Invoice ||──o{ Payment : "receives"
User ||──o| Worker : "has profile"
```

---

## 5. Non-Functional Requirements

### 5.1 Performance Requirements
- **NFR-P-001**: API response time shall not exceed 2 seconds for 95% of requests
- **NFR-P-002**: System shall support at least 100 concurrent users
- **NFR-P-003**: Dashboard charts shall generate within 5 seconds
- **NFR-P-004**: Database queries shall be optimized with proper indexing

### 5.2 Security Requirements
- **NFR-S-001**: All passwords shall be hashed using industry-standard algorithms
- **NFR-S-002**: System shall use HTTPS for all communications in production
- **NFR-S-003**: JWT tokens shall expire after 5 hours
- **NFR-S-004**: System shall implement CSRF protection
- **NFR-S-005**: System shall implement XSS protection
- **NFR-S-006**: System shall sanitize all user inputs
- **NFR-S-007**: System shall log all authentication attempts

### 5.3 Reliability Requirements
- **NFR-R-001**: System shall have 99% uptime
- **NFR-R-002**: System shall perform daily database backups
- **NFR-R-003**: System shall handle errors gracefully with appropriate messages
- **NFR-R-004**: System shall log all errors for debugging

### 5.4 Usability Requirements
- **NFR-U-001**: API shall provide clear, consistent error messages
- **NFR-U-002**: System shall provide comprehensive API documentation
- **NFR-U-003**: API endpoints shall follow RESTful conventions
- **NFR-U-004**: System shall provide interactive API testing interface (Swagger)

### 5.5 Maintainability Requirements
- **NFR-M-001**: Code shall follow PEP 8 style guidelines
- **NFR-M-002**: System shall have modular architecture
- **NFR-M-003**: All models shall have clear documentation
- **NFR-M-004**: Database migrations shall be version controlled

### 5.6 Scalability Requirements
- **NFR-SC-001**: System architecture shall support horizontal scaling
- **NFR-SC-002**: Database shall be optimized for growing data volumes
- **NFR-SC-003**: System shall support multiple database backends

---

## 6. External Interface Requirements

### 6.1 User Interfaces
- RESTful API (no traditional UI, API-first approach)
- Swagger UI for API documentation and testing
- Django Admin interface for administrative tasks

### 6.2 Hardware Interfaces
- Standard web server hardware
- Database server
- No specialized hardware required

### 6.3 Software Interfaces
- **Operating System**: Linux/Windows/macOS
- **Web Server**: WSGI-compatible (Gunicorn, uWSGI)
- **Database**: SQLite (development), PostgreSQL (production)
- **Python**: Version 3.8 or higher
- **Browser**: Modern browsers for Swagger UI

### 6.4 Communication Interfaces
- **Protocol**: HTTP/HTTPS
- **Data Format**: JSON
- **Authentication**: JWT Bearer tokens
- **API Style**: RESTful

---

## Appendices

### Appendix A: Glossary
- **Estimate**: A detailed cost calculation for proposed construction work
- **Job**: A scheduled construction project based on an accepted estimate
- **Worker**: A skilled tradesperson employed by the company
- **Material**: Building supplies required for a job
- **Invoice**: A bill sent to customer upon job completion
- **Payment**: Money received from customer against an invoice

### Appendix B: Analysis Models
All UML diagrams and models are provided in Section 4.

---

**Document Approval:**

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Project Manager | Benjamin Karanja | BSCNRB185323 | 12/11/2025 |
| Lead Developer | Cyrus Ndirangu | BSCNRB279820 | 12/11/2025 |
| Client Representative | Morgan Otieno | BSCNRB547823 | 10/11/2025 |
| System Architect | Gladys Maseki | BSCNRB116424 | 10/11/2025 |

**Document History:**

| Version | Date | Author | Description |
|---------|------|--------|-------------|
| 1.0 | 2025-11-12 | Development Team | Initial SRS document |

