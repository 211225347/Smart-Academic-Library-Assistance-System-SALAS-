# TEST_CASES.md — Test Case Development
## Smart Academic Library Assistance System (SALAS)

> Assignment 5: Test Case Development  
> Building on Assignments 3 & 4 — SALAS  
> Version: 1.0 | Date: March 2026

---

## 1. Introduction

This document defines test cases to validate the functional and non-functional requirements specified in `SRD.md`. Each test case is directly traceable to a requirement ID. Test cases cover both happy-path (expected) scenarios and edge cases/error paths.

---

## 2. Functional Test Cases

| Test Case ID | Requirement ID | Description | Pre-conditions | Test Steps | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|---|---|
| **TC001** | FR-01 | Student registers with a valid university email | System is online. User has no existing account. | 1. Navigate to `/register`. 2. Enter `student@university.ac.za`, full name, and password `Test@1234`. 3. Click "Register". 4. Open verification email and click link. | Account is created. Verification email received. User is redirected to login page. Success message displayed. | — | Pending |
| **TC002** | FR-01 | Login blocked after 5 failed attempts | Valid account exists. User not currently locked. | 1. Navigate to `/login`. 2. Enter correct email and wrong password 5 times in a row. | After the 5th attempt, account is locked for 15 minutes. Message displayed: *"Too many failed attempts. Try again in 15 minutes."* Lock email is sent. | — | Pending |
| **TC003** | FR-02 | Search returns relevant results within 2 seconds | Student is logged in. Elasticsearch index has at least 1,000 records. | 1. Navigate to `/search`. 2. Type "introduction to algorithms" in the search bar. 3. Press Enter. 4. Note the time taken. | Results appear within 2 seconds. At least 1 result with matching title/author is shown. Each result displays availability badge (Available / Borrowed / Reserved). | — | Pending |
| **TC004** | FR-02 | Search filter by availability narrows results | Student is logged in. At least some resources are marked "Available". | 1. Search for "data structures". 2. Apply filter: Availability = "Available". 3. Review results. | All displayed results show "Available" status badge. Results update without full page reload. | — | Pending |
| **TC005** | FR-03 | Student successfully borrows an available book | Student is logged in. Target book has ≥ 1 available copy. Student has no overdue fines > R100. | 1. Search for "Clean Code". 2. Open resource detail page. 3. Click "Borrow". 4. Confirm dialog. | Loan record created with 14-day due date. Available copy count decremented by 1. Success message shown. Book appears on student dashboard under "Active Loans". Confirmation email received within 60 seconds. | — | Pending |
| **TC006** | FR-03 | Reservation blocked for ineligible student | Student is logged in. Student has 3 overdue items on their account. | 1. Navigate to any resource detail page. 2. Click "Borrow" or "Reserve". | System blocks the action. Error message displayed: *"You cannot borrow at this time. You have 3 overdue items."* Button is disabled. | — | Pending |
| **TC007** | FR-04 | Dashboard displays active loans and due dates | Student is logged in. Student has at least 1 active loan. | 1. Log in. 2. Observe dashboard. 3. Check load time using browser DevTools (Network tab). | Dashboard loads within 2 seconds. Active loans displayed with correct titles and due dates. Items due within 3 days are highlighted in red. | — | Pending |
| **TC008** | FR-05 | New student receives course-based recommendations | New student account registered within the last hour. No borrowing history. | 1. Register new student account with course = "Computer Science". 2. Wait up to 1 hour. 3. Log in and view dashboard. | At least 10 recommendations appear in the "Recommended for You" section. Recommended resources are relevant to Computer Science topics. | — | Pending |
| **TC009** | FR-06 | Librarian adds a new resource to catalogue | Librarian is logged in. Resource does not already exist in catalogue. | 1. Navigate to Admin Panel → Catalogue Management. 2. Click "Add New Resource". 3. Fill in: Title = "Design Patterns", Author = "Gang of Four", ISBN = "9780201633610", Copies = 3. 4. Click Save. | Resource saved to database. Record appears in librarian catalogue view. Resource is searchable via student search within 30 seconds. Audit log entry created. | — | Pending |
| **TC010** | FR-06 | Delete resource with active loans is blocked | Librarian is logged in. Target resource has at least 1 active loan. | 1. Navigate to Catalogue Management. 2. Find resource with active loans. 3. Click "Delete". | System displays error: *"Cannot delete: this resource has active loans."* Resource is not deleted from database or search index. | — | Pending |
| **TC011** | FR-07 | Overdue notification sent 3 days before due date | Student has an active loan due in exactly 3 days. Notification Service is running. | 1. Create a loan with a due date 3 days from now. 2. Trigger or wait for the hourly notification job to run. 3. Check student email inbox. | Student receives an email with subject "Reminder: Your book is due soon". Email contains book title, due date, and a dashboard link. Email arrives within 5 minutes of the job run. | — | Pending |
| **TC012** | FR-08 | Admin generates and exports usage report as CSV | Administrator is logged in. Report data has been refreshed. | 1. Navigate to Reports section. 2. Select "Top 20 Borrowed Resources". 3. Set date range: last 3 months. 4. Click "Export" → "CSV". | CSV file downloads within 10 seconds. File contains correct column headers: Resource Title, Author, Times Borrowed, Department. Data matches on-screen report. | — | Pending |

---

## 3. Non-Functional Test Cases

### NFR Test 1: Performance — Concurrent User Load Test

| Field | Detail |
|---|---|
| **Test Case ID** | TC-NFR-01 |
| **Requirement ID** | NFR-07 (Concurrent User Support) |
| **Description** | Verify the system maintains acceptable response times when 1,000 students simultaneously search for library resources, simulating peak semester-start usage. |
| **Pre-conditions** | System deployed in staging environment. Elasticsearch index populated with 50,000+ records. Database seeded with 1,000 student accounts. Load testing tool configured (e.g., Apache JMeter or k6). |
| **Test Steps** | 1. Configure k6 to simulate 1,000 virtual users (VUs). 2. Each VU performs: login → search for a random keyword → open first result → return to search. 3. Ramp up from 0 to 1,000 VUs over 2 minutes. 4. Hold at 1,000 VUs for 5 minutes. 5. Record p50, p95, p99 response times and error rate throughout. |
| **Expected Result** | Average API response time ≤ 300ms at 1,000 concurrent users. p95 search response time ≤ 2,000ms. Error rate < 1%. No service crashes or memory leaks detected. |
| **Actual Result** | — |
| **Status** | Pending |

---

### NFR Test 2: Security — Brute Force and JWT Validation

| Field | Detail |
|---|---|
| **Test Case ID** | TC-NFR-02 |
| **Requirement ID** | NFR-10 (Authentication Security) |
| **Description** | Verify that the system correctly enforces JWT authentication on all protected endpoints and activates account lockout after 5 failed login attempts, preventing brute-force attacks. |
| **Pre-conditions** | System deployed in staging environment. A valid student account exists. A security testing tool is available (e.g., Postman, OWASP ZAP). |
| **Test Steps** | **Part A — JWT Enforcement:** 1. Using Postman, send a GET request to `/api/v1/dashboard` with no Authorization header. 2. Send same request with an expired JWT token. 3. Send same request with a tampered JWT token (modified payload). 4. Send same request with a valid JWT token. **Part B — Brute Force Protection:** 1. Attempt to log in with the correct email and a wrong password 5 times consecutively. 2. Attempt a 6th login with the correct password. 3. Wait 15 minutes and attempt login again with correct credentials. |
| **Expected Result** | **Part A:** Requests 1–3 return HTTP 401 Unauthorized with message "Invalid or expired token". Request 4 returns HTTP 200 with dashboard data. **Part B:** After 5th failed attempt, account is locked. 6th attempt (even with correct password) returns HTTP 403 with lockout message. After 15 minutes, correct credentials succeed and return HTTP 200. |
| **Actual Result** | — |
| **Status** | Pending |

---

## 4. Test Coverage Summary

| Requirement | Test Case(s) | Coverage |
|---|---|---|
| FR-01 (Authentication) | TC001, TC002 | ✅ Registration + lockout |
| FR-02 (Search) | TC003, TC004 | ✅ Search + filtering |
| FR-03 (Borrow/Reserve) | TC005, TC006 | ✅ Happy path + ineligibility |
| FR-04 (Dashboard) | TC007 | ✅ Load + display |
| FR-05 (Recommendations) | TC008 | ✅ Cold-start scenario |
| FR-06 (Catalogue Management) | TC009, TC010 | ✅ Add + delete protection |
| FR-07 (Notifications) | TC011 | ✅ Scheduled trigger |
| FR-08 (Reporting) | TC012 | ✅ Export functionality |
| NFR-07 (Performance) | TC-NFR-01 | ✅ 1,000 concurrent users |
| NFR-10 (Security) | TC-NFR-02 | ✅ JWT + brute force |
