# Project Plan and GANTT Chart
## Bidii Quality Builders Construction Management System

**Version:** 2.0  
**Date:** November 13, 2025  
**Project:** SWE-II Final Year Project  
**Timeline:** 4 Weeks (Intensive Development)


## 1. Project Overview

### 1.1 Project Summary
Development of a comprehensive construction management system for Bidii Quality Builders using Django REST Framework, implementing estimate processing, job scheduling, worker management, material ordering, and invoice processing with dashboard analytics. The project was completed in an intensive 4-week development cycle using agile methodologies.

### 1.2 Project Objectives
- Computerize building work management processes
- Automate estimate workflow and tracking
- Implement job scheduling system
- Track workers, materials, and suppliers
- Automate invoice generation and payment tracking
- Provide business intelligence through dashboards
- Follow secure coding practices
- Deliver complete documentation

### 1.3 Project Deliverables
1. Functional Django REST Framework application
2. Software Requirements Specification (SRS)
3. Requirements Traceability Matrix (RTM)
4. Software Architecture and Design Document
5. Test Plan with test cases
6. Project Plan with GANTT chart
7. Complete source code with documentation
8. User manual and API documentation
9. Deployment guide



## 2. Project Phases

### Phase 1: Planning, Requirements & Design (Week 1)
**Duration**: 1 week

**Activities**:
- Requirements gathering from case study
- Requirements documentation and system modeling
- Database schema design
- API endpoint design
- System architecture design
- Security design
- Technology stack selection

**Deliverables**:
- SRS document with UML diagrams
- Architecture and Design Document
- Database schema
- Project plan with GANTT chart

### Phase 2: Development Sprint 1 - Core Modules (Week 2)
**Duration**: 1 week

**Activities**:
- Project setup (Django + DRF)
- Database models implementation (all 8 models)
- Authentication system (JWT)
- Customer management module
- Worker management module
- Estimate processing module
- Basic unit tests

**Deliverables**:
- Working authentication
- Customer, Worker, Estimate CRUD operations
- Database migrations
- Initial test cases

### Phase 3: Development Sprint 2 - Advanced Features (Week 3)
**Duration**: 1 week

**Activities**:
- Job scheduling module
- Material and supplier management
- Invoice generation module
- Payment processing module
- Dashboard implementation with Matplotlib
- API documentation (Swagger)
- Business logic implementation
- Integration tests

**Deliverables**:
- Complete job management workflow
- Material tracking system
- Invoice and payment system
- Dashboard with visualizations
- Interactive API documentation
- Comprehensive test suite

### Phase 4: Testing, Documentation & Finalization (Week 4)
**Duration**: 1 week

**Activities**:
- Unit and integration testing completion
- Security testing
- Requirements Traceability Matrix
- Test plan documentation
- Code documentation
- Bug fixing and optimization
- Final review and presentation preparation

**Deliverables**:
- Test plan document with test cases
- Requirements Traceability Matrix (RTM)
- Complete documentation suite
- Test execution reports
- Project presentation
- Final project report



## 3. GANTT Chart

```
Task                               Day: 1-2  3-4  5-7 | 1-2  3-4  5-7 | 1-2  3-4  5-7 | 1-2  3-4  5-7
                                      Week 1        |    Week 2      |    Week 3      |    Week 4
=====================================================================================================
Phase 1: Planning & Design
  Requirements Analysis & SRS        [====]
  System Modeling (UML)              [====]
  Architecture Design                      [====]
  Database & API Design                    [====]
  Project Plan                                 [==]

Phase 2: Development Sprint 1
  Project Setup (Django/DRF)                      | [==]
  Database Models (8 models)                      |     [====]
  Authentication (JWT)                            |          [===]
  Customer & Worker Modules                       |          [===]
  Estimate Module                                 |              [==]

Phase 3: Development Sprint 2
  Job Module                                      |                 | [====]
  Material & Supplier Modules                     |                 |     [===]
  Invoice & Payment Modules                       |                 |         [====]
  Dashboard & Matplotlib Charts                   |                 |             [===]
  Swagger Documentation                           |                 |                [=]

Phase 4: Testing & Finalization
  Unit & Integration Tests                        |                 |                   | [====]
  Security Testing                                |                 |                   |     [==]
  RTM & Test Plan Docs                            |                 |                   |     [===]
  Bug Fixes & Optimization                        |                 |                   |         [===]
  Final Review & Presentation                     |                 |                   |             [==]

Legend: [=] ≈ 1 day of work  |  Phases run in parallel where possible
```



## 4. Detailed Task Breakdown

### 4.1 Week-by-Week Schedule

#### Week 1: Planning, Requirements & Design
| Task | Duration | Assigned To | Status |
|-|-|-|-|
| Analyze case study & identify requirements | 1 day | Team |  Complete |
| Create use case & class diagrams | 1 day | Designer |  Complete |
| Write SRS document | 2 days | Team |  Complete |
| Design system architecture | 1 day | Architect |  Complete |
| Design database schema & API endpoints | 1 day | Backend Lead |  Complete |
| Write architecture document | 1 day | Team |  Complete |

#### Week 2: Development Sprint 1 - Core Modules
| Task | Duration | Assigned To | Status |
|-|-|-|-|
| Set up Django + DRF project | 0.5 days | Backend Dev |  Complete |
| Implement all 8 database models | 1 day | Backend Dev |  Complete |
| Implement JWT authentication | 1 day | Backend Dev |  Complete |
| Implement Customer module & API | 1 day | Backend Dev |  Complete |
| Implement Worker module & API | 1 day | Backend Dev |  Complete |
| Implement Estimate module & API | 1.5 days | Backend Dev |  Complete |
| Write initial unit tests | 1 day | Backend Dev |  Complete |

#### Week 3: Development Sprint 2 - Advanced Features
| Task | Duration | Assigned To | Status |
|-|-|-|-|
| Implement Job module & API | 1.5 days | Backend Dev |  Complete |
| Implement Material & Supplier modules | 1 day | Backend Dev |  Complete |
| Implement Invoice module & API | 1.5 days | Backend Dev |  Complete |
| Implement Payment module & API | 1 day | Backend Dev |  Complete |
| Implement dashboard with Matplotlib | 1.5 days | Backend Dev |  Complete |
| Set up Swagger API documentation | 0.5 days | Backend Dev |  Complete |

#### Week 4: Testing, Documentation & Finalization
| Task | Duration | Assigned To | Status |
|-|-|-|-|
| Complete unit & integration tests | 2 days | Backend Dev |  Complete |
| Security testing & validation | 1 day | Security Team |  Complete |
| Create RTM document | 1 day | Team |  Complete |
| Write Test Plan document | 1 day | Team |  Complete |
| Code documentation & cleanup | 1 day | Backend Dev |  Complete |
| Bug fixing & optimization | 1 day | Backend Dev |  Complete |
| Prepare final presentation | 0.5 days | Team |  Complete |



## 5. Resource Allocation

### 5.1 Team Structure
| Role | Responsibility | Allocation |
|-|-|-|
| Project Lead | Overall coordination, planning, development | Full-time (Weeks 1-4) |
| Backend Developer | Core development, testing | Full-time (Weeks 2-4) |
| System Architect | Requirements, architecture, design | Week 1 |
| Security Specialist | Security review & validation | Week 4 |
| Technical Writer | Documentation (concurrent) | Weeks 3-4 |

### 5.2 Technology Resources
- Development machines
- Testing servers
- Production servers
- Database servers
- Version control system (Git)
- Project management tools
- Communication tools



## 6. Risk Management

### 6.1 Identified Risks

| Risk | Probability | Impact | Mitigation Strategy |
|-|-|-|-|
| Scope creep | Medium | High | Clear requirements document, change control |
| Technology learning curve | Low | Medium | Training, documentation, mentoring |
| Integration issues | Medium | Medium | Early integration testing, modular design |
| Security vulnerabilities | Low | High | Security review, penetration testing |
| Performance issues | Low | Medium | Performance testing, optimization |
| Resource availability | Medium | Medium | Cross-training, buffer time |
| Deployment issues | Low | Medium | Staging environment, deployment scripts |

### 6.2 Risk Response Plan
- **Regular monitoring**: Weekly risk review meetings
- **Early detection**: Continuous integration and testing
- **Quick response**: Dedicated time for risk mitigation
- **Communication**: Regular stakeholder updates



## 7. Quality Assurance

### 7.1 Quality Metrics
- **Code Coverage**: Target 80%
- **Bug Density**: < 1 bug per 100 lines of code
- **API Response Time**: < 2 seconds
- **Security**: Zero critical vulnerabilities
- **Documentation**: 100% API coverage

### 7.2 Quality Control Activities
- Code reviews
- Automated testing
- Security audits
- Performance monitoring
- Documentation review



## 8. Project Milestones

| Milestone | Target Date | Status | Deliverables |
|--|-|--|--|
| M1: Requirements & Design Complete | End of Week 1 |  Complete | SRS, Architecture Doc, UML Diagrams |
| M2: Core Development Complete | End of Week 2 |  Complete | Auth, Customer, Worker, Estimate modules |
| M3: Advanced Features Complete | End of Week 3 |  Complete | Job, Material, Invoice, Payment, Dashboard |
| M4: Testing & Documentation Complete | End of Week 4 |  Complete | Test Reports, RTM, All Documentation |
| M5: Project Complete | End of Week 4 |  Complete | Final Deliverables & Presentation |



## 9. Communication Plan

### 9.1 Meetings Schedule
- **Daily Standup**: 15 minutes, every workday
- **Sprint Planning**: 2 hours, start of each sprint
- **Sprint Review**: 1 hour, end of each sprint
- **Stakeholder Update**: 1 hour, bi-weekly
- **Risk Review**: 30 minutes, weekly

### 9.2 Reporting
- **Daily**: Progress updates in standup
- **Weekly**: Status report to stakeholders
- **Bi-weekly**: Detailed progress report
- **Ad-hoc**: Critical issues and blockers



## 10. Success Criteria

The project will be considered successful when:

1.  All functional requirements implemented (69/69 requirements)
2.  All modules passing unit tests (21/21 model tests)
3.  Integration tests passing (15+ API tests)
4.  Security audit passed (JWT, CORS, CSRF, XSS protection)
5.  Performance targets met (< 2 second response time)
6.  Complete documentation delivered (90+ pages)
7.  API documentation complete (Swagger/OpenAPI)
8.  System deployable (production-ready)
9.  Sample data and demos prepared
10.  Presentation materials ready

**Project Status**:  ALL SUCCESS CRITERIA MET



## 11. Project Status Summary

**Overall Progress**: 100% Complete

### Completed (Week 1):
-  Requirements Analysis & Documentation (SRS)
-  System Design & Architecture
-  UML Modeling (Use Case, Class, Sequence, State Diagrams)
-  Database Schema Design
-  Project Plan with GANTT Chart

### Completed (Week 2):
-  Django + DRF Project Setup
-  All 8 Database Models Implemented
-  JWT Authentication System
-  Customer Management Module (Full CRUD)
-  Worker Management Module (Full CRUD)
-  Estimate Processing Module (Full CRUD)
-  Initial Unit Tests

### Completed (Week 3):
-  Job Scheduling Module (Full CRUD + Actions)
-  Material & Supplier Management
-  Invoice Generation Module
-  Payment Processing Module
-  Dashboard with Matplotlib Visualizations (5 charts)
-  Swagger/OpenAPI Documentation
-  Integration Tests

### Completed (Week 4):
-  Comprehensive Test Suite (36+ tests, all passing)
-  Security Testing & Validation
-  Requirements Traceability Matrix (RTM)
-  Test Plan Documentation
-  Code Documentation & Comments
-  Bug Fixes & Optimization
-  Final Presentation Materials



**Document Approval:**

| Role | Name | Signature | Date |
|-|-|--|-|
| Project Manager | Benjamin Karanja | BSCNRB185323 | 10/11/2025 |
| Project Sponsor | Cecilia Nafuka | | 13/11/2025 |
| Technical Lead | Cyrus Ndirangu | BSCNRB279820 | 10/11/2025 |
| System Architect | Gladys Maseki | BSCNRB116424 | 10/11/2025 |
| QA Lead | Morgan Otieno | BSCNRB547823 | 10/11/2025 |


**Document History:**

| Version | Date | Author | Changes |
|-|-|--|-|
| 1.0 | 2025-11-12 | Project Team | Initial project plan (15-week timeline) |
| 2.0 | 2025-11-13 | Project Team | Refactored to 4-week intensive timeline |


