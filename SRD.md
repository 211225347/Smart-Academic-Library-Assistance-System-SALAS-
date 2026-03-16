# SRD.md — System Requirements Document
## Smart Academic Library Assistance System (SALAS)

> Assignment 4: System Requirements Document  
> Building on Assignment 3 — SALAS  
> Version: 1.0 | Date: March 2026

---

## 1. Introduction

### 1.1 Purpose
This System Requirements Document (SRD) defines the complete functional and non-functional requirements for SALAS. It serves as the authoritative reference for development, testing, and acceptance of the system. All requirements are directly traceable to stakeholder needs identified in `STAKEHOLDERS.md`.

### 1.2 Scope
SALAS is a web-based intelligent library management and resource discovery platform for university students and library staff. It encompasses a student-facing web application, an admin portal, a RESTful backend API, a recommendation engine, a full-text search service, and supporting data infrastructure.

### 1.3 Definitions

| Term | Definition |
|---|---|
| SRD | System Requirements Document |
| FR | Functional Requirement |
| NFR | Non-Functional Requirement |
| SALAS | Smart Academic Library Assistance System |
| WCAG | Web Content Accessibility Guidelines |
| JWT | JSON Web Token — used for stateless authentication |
| CTR | Click-Through Rate — metric for recommendation effectiveness |
| POPIA | Protection of Personal Information Act (South Africa) |

---

## 2. Functional Requirements

> Each requirement follows the format: **"The system shall…"**  
> Stakeholder traceability is noted for each requirement.

---

### FR-01: Student Registration and Authentication
**Statement:** The system shall allow students and librarians to register and log in using their university email and password, with support for JWT-based session management.

**Stakeholder:** University Student, Librarian

**Acceptance Criteria:**
- Registration requires a valid university email domain (e.g., `@university.ac.za`)
- Passwords must be at least 8 characters and include one number and one special character
- JWT tokens expire after 24 hours; refresh tokens are valid for 7 days
- Failed login attempts are limited to 5 before a 15-minute lockout is triggered
- Login response time must be ≤ 1 second under normal load

---

### FR-02: Natural Language and Filtered Resource Search
**Statement:** The system shall allow students to search the library catalogue using natural language queries, with optional filters for author, title, ISBN, genre, year of publication, and availability status.

**Stakeholder:** University Student, Student with Accessibility Needs

**Acceptance Criteria:**
- Search results are returned within 2 seconds for queries against a catalogue of up to 500,000 records
- Results are ranked by relevance using Elasticsearch scoring
- Availability status (available / borrowed / reserved) is displayed in real time on each result
- Filters can be combined and applied simultaneously without page reload
- Search input is accessible via keyboard and screen reader

---

### FR-03: Book Borrowing and Reservation
**Statement:** The system shall allow authenticated students to borrow available physical books and place reservations on unavailable books, with automated hold expiry after 48 hours if not collected.

**Stakeholder:** University Student, University Librarian

**Acceptance Criteria:**
- Borrowing is blocked if the student has 3 or more overdue items or unpaid fines exceeding R100
- A reservation confirmation email is sent within 60 seconds of placement
- Inventory count is decremented immediately upon borrowing and incremented upon return
- Reserved books are held for exactly 48 hours; after expiry, the next queued reservation is activated automatically
- Librarian can manually override reservation status

---

### FR-04: Student Personal Dashboard
**Statement:** The system shall provide each student with a personal dashboard displaying their active loans, due dates, borrowing history, saved reading list, overdue notices, and personalized recommendations.

**Stakeholder:** University Student

**Acceptance Criteria:**
- Dashboard loads all data within 2 seconds
- Due date alerts are highlighted in red for items due within 3 days
- Borrowing history displays a minimum of the last 12 months
- Reading list allows students to add, remove, and reorder saved items
- Dashboard is fully responsive on mobile, tablet, and desktop viewports

---

### FR-05: Personalized Resource Recommendations
**Statement:** The system shall generate and display personalized academic resource recommendations for each student based on their borrowing history, search history, and course enrollment data, using a collaborative filtering algorithm.

**Stakeholder:** University Student, Data Science Team

**Acceptance Criteria:**
- Recommendations are updated at least every 24 hours
- New students with no history receive course-based default recommendations within 1 hour of registration
- A minimum of 10 recommendations are shown per student session
- Students can dismiss a recommendation, which feeds back into the model
- Recommendation data used for training is anonymized before processing

---

### FR-06: Library Catalogue Management (Librarian)
**Statement:** The system shall allow authenticated librarians to add, edit, and delete resource entries in the library catalogue, including title, author, ISBN, genre, number of copies, physical location, and cover image.

**Stakeholder:** University Librarian

**Acceptance Criteria:**
- New resources are indexed in Elasticsearch within 30 seconds of being added
- ISBN validation is enforced using standard ISBN-10/ISBN-13 check digit rules
- Deletion of a resource is blocked if active loans exist for that resource
- Bulk import of resources is supported via CSV upload (up to 1,000 records per batch)
- All catalogue changes are logged with the librarian's user ID and timestamp

---

### FR-07: Automated Overdue Notifications
**Statement:** The system shall automatically send email notifications to students 3 days before a loan is due, on the due date, and 1 day after the due date if not returned.

**Stakeholder:** University Student, University Librarian

**Acceptance Criteria:**
- Notification emails are delivered within 5 minutes of the scheduled trigger time
- Emails include the resource title, due date, and a direct link to the student dashboard
- Students can configure notification preferences (email only, in-app only, or both)
- Librarians receive a daily digest of all overdue items each morning at 08:00
- Notification delivery failures are logged and retried up to 3 times

---

### FR-08: Usage Reporting and Analytics (Admin)
**Statement:** The system shall provide university administrators and librarians with a reporting dashboard showing resource borrowing trends, most-borrowed items, overdue rates, and student engagement metrics, exportable as PDF or CSV.

**Stakeholder:** University Administrator, University Librarian

**Acceptance Criteria:**
- Reports can be filtered by date range, department, resource type, and student cohort
- Data in reports is refreshed daily at midnight
- PDF and CSV exports are generated within 10 seconds for reports covering up to 12 months
- At least the following reports are available: Top 20 Borrowed Resources, Overdue Rate by Month, Active Users by Faculty, New Acquisitions vs Demand
- Admin-only reports are protected by role-based access control (RBAC)

---

### FR-09: RESTful API for External Integration
**Statement:** The system shall expose a versioned RESTful API (v1) with OpenAPI 3.0 documentation, enabling external systems (university portal, mobile app) to authenticate users, search resources, and retrieve student borrowing data.

**Stakeholder:** External Integration Partners

**Acceptance Criteria:**
- All endpoints are documented in a publicly accessible Swagger UI at `/api/v1/docs`
- API versioning is maintained; v1 endpoints remain functional for a minimum of 12 months after a v2 release
- All API requests require a valid JWT; unauthenticated requests return HTTP 401
- A sandbox environment mirrors the production API and is available 24/7
- Rate limiting is enforced at 100 requests/minute per API key, with clear HTTP 429 responses

---

### FR-10: Role-Based Access Control (RBAC)
**Statement:** The system shall enforce role-based access control with at minimum three roles — Student, Librarian, and Admin — each with clearly scoped permissions, ensuring no role can access functionality outside their scope.

**Stakeholder:** IT Administrator, University Administrator

**Acceptance Criteria:**
- Students cannot access catalogue management or reporting endpoints
- Librarians can manage catalogue and view reports but cannot manage user accounts
- Admins have full system access including user management and system configuration
- Role assignments are logged and auditable
- Unauthorized access attempts return HTTP 403 and are logged as security events

---

### FR-11: Reading List and Resource Saving
**Statement:** The system shall allow students to save any resource to a personal reading list, organize saved items into custom collections, and share a reading list with other students via a unique link.

**Stakeholder:** University Student

**Acceptance Criteria:**
- Saving a resource takes no more than 1 click from any resource detail page
- Students can create up to 10 named collections within their reading list
- Shared reading list links are publicly accessible without requiring login
- Reading list data persists across sessions and devices
- Students can export their reading list as a formatted bibliography (APA or Harvard style)

---

### FR-12: Accessibility-Compliant Interface
**Statement:** The system shall implement a fully accessible user interface compliant with WCAG 2.1 Level AA, including screen reader support, full keyboard navigation, sufficient color contrast ratios, and descriptive alt-text on all images.

**Stakeholder:** Student with Accessibility Needs, University Administrator

**Acceptance Criteria:**
- Lighthouse accessibility audit score ≥ 95 on all primary pages
- All interactive elements are reachable and operable via keyboard alone
- Color contrast ratio meets a minimum of 4.5:1 for normal text (WCAG AA)
- Dynamic content changes (e.g., search results loading) are announced to screen readers via ARIA live regions
- All book cover images include descriptive alt-text auto-populated from metadata

---

## 3. Non-Functional Requirements

---

### 3.1 Usability

**NFR-01: Accessibility Compliance**
The system interface shall comply with WCAG 2.1 Level AA accessibility standards across all pages and user flows.
- *Metric:* Lighthouse accessibility score ≥ 95; zero critical WCAG violations in annual audit.
- *Stakeholder:* Student with Accessibility Needs, University Administrator

**NFR-02: Learnability**
A first-time student user shall be able to complete a book search and reservation without any training or documentation.
- *Metric:* ≥ 85% of new users complete a search and reservation in under 5 minutes in usability testing.
- *Stakeholder:* University Student

---

### 3.2 Deployability

**NFR-03: Cross-Platform Deployment**
The system shall be deployable on both Linux (Ubuntu 22.04+) and Windows Server 2019+ environments using Docker containers, with a single `docker-compose up` command standing up the full stack.
- *Metric:* Full environment setup time under 15 minutes on a clean server.
- *Stakeholder:* IT Administrator

**NFR-04: Cloud Portability**
The system shall be deployable on any major cloud provider (AWS, Azure, GCP) or on-premise infrastructure without code changes, using environment variables for all configuration.
- *Metric:* Zero hardcoded environment-specific values in application code.
- *Stakeholder:* IT Administrator, University Administrator

---

### 3.3 Maintainability

**NFR-05: API Documentation**
The system shall maintain a complete, up-to-date OpenAPI 3.0 specification for all REST API endpoints, auto-generated from code annotations and published at `/api/v1/docs`.
- *Metric:* 100% of endpoints documented; documentation updated within 24 hours of any API change.
- *Stakeholder:* External Integration Partners, IT Administrator

**NFR-06: Code Modularity**
Each system service (API, Recommendation Engine, Search, Frontend) shall be independently deployable and testable, with no direct cross-service database access (service boundaries enforced via API calls only).
- *Metric:* Any single service can be restarted or redeployed without restarting other services.
- *Stakeholder:* IT Administrator, Data Science Team

---

### 3.4 Scalability

**NFR-07: Concurrent User Support**
The system shall support a minimum of 1,000 concurrent users during peak academic periods (semester start, exam periods) without degradation in response time.
- *Metric:* Average API response time remains ≤ 300ms at 1,000 concurrent users in load testing.
- *Stakeholder:* IT Administrator, University Administrator

**NFR-08: Horizontal Scaling**
The REST API and Search Service shall support horizontal scaling by adding additional container instances behind a load balancer, with no application-level changes required.
- *Metric:* Throughput increases linearly (±10%) as instances are added from 1 to 5.
- *Stakeholder:* IT Administrator

---

### 3.5 Security

**NFR-09: Data Encryption**
All student personal data and authentication credentials shall be encrypted at rest using AES-256, and all data in transit shall be protected using TLS 1.2 or higher.
- *Metric:* Zero plaintext personal data stored in the database; TLS enforced on all endpoints verified by SSL Labs Grade A.
- *Stakeholder:* IT Administrator, University Administrator

**NFR-10: Authentication Security**
The system shall implement JWT-based authentication with token expiry, refresh token rotation, and brute-force protection (account lockout after 5 failed attempts).
- *Metric:* 100% of protected endpoints reject requests without valid JWT; lockout triggered reliably in security testing.
- *Stakeholder:* IT Administrator, University Student

**NFR-11: POPIA / Data Privacy Compliance**
The system shall comply with the South African Protection of Personal Information Act (POPIA), including data minimization, purpose limitation, and the right to erasure for student accounts.
- *Metric:* Privacy impact assessment completed before launch; student account deletion removes all personal data within 30 days.
- *Stakeholder:* University Administrator, Data Science Team

---

### 3.6 Performance

**NFR-12: Search Response Time**
The search service shall return results for any query against a catalogue of up to 500,000 records within 2 seconds at the 95th percentile under normal load.
- *Metric:* p95 search latency ≤ 2,000ms verified by load testing with realistic query patterns.
- *Stakeholder:* University Student

**NFR-13: Dashboard Load Time**
The student dashboard shall load all data (loans, recommendations, history) within 2 seconds on a standard broadband connection (≥ 10 Mbps).
- *Metric:* Time to Interactive (TTI) ≤ 2,000ms measured by Lighthouse on a simulated Fast 3G profile.
- *Stakeholder:* University Student

**NFR-14: Recommendation Engine Throughput**
The recommendation engine shall process and update recommendations for all active students (up to 10,000) within a 24-hour batch window.
- *Metric:* Batch job completes within 4 hours for 10,000 student profiles, verified in staging environment.
- *Stakeholder:* Data Science Team

---

## 4. Requirements Traceability Matrix

| Requirement ID | Description | Stakeholder(s) | Priority |
|---|---|---|---|
| FR-01 | Student & librarian authentication | Student, Librarian | Must Have |
| FR-02 | Natural language + filtered search | Student, Accessibility | Must Have |
| FR-03 | Borrowing and reservation | Student, Librarian | Must Have |
| FR-04 | Student personal dashboard | Student | Must Have |
| FR-05 | Personalized recommendations | Student, Data Science | Should Have |
| FR-06 | Catalogue management (librarian) | Librarian | Must Have |
| FR-07 | Automated overdue notifications | Student, Librarian | Must Have |
| FR-08 | Usage reporting & analytics | Admin, Librarian | Should Have |
| FR-09 | RESTful API for external integration | Integration Partners | Should Have |
| FR-10 | Role-based access control | IT Admin, Admin | Must Have |
| FR-11 | Reading list & resource saving | Student | Could Have |
| FR-12 | Accessible interface | Accessibility, Admin | Must Have |
| NFR-01 | WCAG 2.1 AA compliance | Accessibility, Admin | Must Have |
| NFR-02 | Learnability | Student | Should Have |
| NFR-03 | Cross-platform deployment | IT Admin | Must Have |
| NFR-04 | Cloud portability | IT Admin, Admin | Should Have |
| NFR-05 | API documentation | Integration, IT Admin | Must Have |
| NFR-06 | Code modularity | IT Admin, Data Science | Should Have |
| NFR-07 | 1,000 concurrent users | IT Admin, Admin | Must Have |
| NFR-08 | Horizontal scaling | IT Admin | Should Have |
| NFR-09 | AES-256 + TLS encryption | IT Admin, Admin | Must Have |
| NFR-10 | JWT auth + brute-force protection | IT Admin, Student | Must Have |
| NFR-11 | POPIA compliance | Admin, Data Science | Must Have |
| NFR-12 | Search ≤ 2s (p95) | Student | Must Have |
| NFR-13 | Dashboard load ≤ 2s | Student | Must Have |
| NFR-14 | Recommendation batch ≤ 4hrs | Data Science | Should Have |
