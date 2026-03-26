# USE_CASE_SPECIFICATIONS.md — Use Case Specifications
## Smart Academic Library Assistance System (SALAS)

> Assignment 5: Detailed Use Case Specifications  
> Building on Assignments 3 & 4 — SALAS  
> Version: 1.0 | Date: March 2026

---

## UC01 — Register and Login

| Field | Detail |
|---|---|
| **Use Case ID** | UC01 |
| **Use Case Name** | Register and Login |
| **Actor(s)** | Student, Librarian, External System |
| **Related FR** | FR-01 |
| **Description** | Allows users to create a new account using their university email or log in to an existing account. The system issues a JWT token upon successful authentication for session management. |
| **Preconditions** | User has access to a valid university email address. System is online and reachable. |
| **Postconditions** | User is authenticated. A valid JWT access token and refresh token are issued and stored client-side. User is redirected to their role-appropriate home page (Student → Dashboard, Librarian → Admin Panel). |

### Basic Flow
1. User navigates to the SALAS login/register page.
2. New user selects "Register" and enters their university email, full name, and password.
3. System validates that the email domain matches `@university.ac.za` (or configured domain).
4. System validates password strength: minimum 8 characters, at least one number and one special character.
5. System creates the account, assigns the default "Student" role, and sends a verification email.
6. User clicks the verification link in their email.
7. User is redirected to the login page and enters credentials.
8. System verifies credentials, generates a signed JWT (24-hour expiry) and refresh token (7-day expiry).
9. User is redirected to their dashboard.

### Alternative Flows

**AF-01: Invalid email domain**
- At Step 3, if the email domain is not recognised, the system displays: *"Please use your university email address to register."*
- Registration is blocked until a valid email is provided.

**AF-02: Incorrect password on login**
- At Step 8, if the password is incorrect, the system increments a failed attempt counter and displays: *"Incorrect email or password."*
- After 5 consecutive failures, the account is locked for 15 minutes and an unlock email is sent.

**AF-03: Unverified email**
- If the user attempts to log in before verifying their email, the system displays: *"Please verify your email before logging in."* with an option to resend the verification link.

---

## UC02 — Search Library Catalogue

| Field | Detail |
|---|---|
| **Use Case ID** | UC02 |
| **Use Case Name** | Search Library Catalogue |
| **Actor(s)** | Student, Accessibility User |
| **Related FR** | FR-02 |
| **Description** | Allows authenticated students to search the full library catalogue using natural language queries or specific filters. Results include real-time availability status for each resource. |
| **Preconditions** | Student is logged in. Elasticsearch index is populated and reachable. |
| **Postconditions** | A ranked list of matching resources is displayed with title, author, availability status, and location. Search query is logged for recommendation model training. |

### Basic Flow
1. Student navigates to the Search page.
2. Student types a natural language query (e.g., "machine learning textbooks for beginners") into the search bar.
3. System sends the query to the Elasticsearch service.
4. Elasticsearch returns ranked results based on relevance scoring.
5. System enriches each result with real-time availability data from PostgreSQL.
6. Results are displayed within 2 seconds, showing title, author, genre, year, availability badge, and cover image.
7. Student may apply filters (author, genre, year, availability) to narrow results without page reload.
8. Student clicks a result to view the full resource detail page.

### Alternative Flows

**AF-01: No results found**
- At Step 4, if Elasticsearch returns zero results, the system displays: *"No resources found for your query."*
- System suggests related popular resources based on the query keywords.
- System suggests broadening the search or checking spelling.

**AF-02: Search service unavailable**
- At Step 3, if Elasticsearch is unreachable, the system falls back to a basic PostgreSQL full-text search.
- A banner is displayed: *"Search is currently running in limited mode. Results may be slower."*

**AF-03: Accessible search (keyboard/screen reader)**
- Accessibility User navigates to the search bar using Tab key.
- Search results are announced to the screen reader via ARIA live regions as they load.
- All filter controls are operable via keyboard.

---

## UC03 — Borrow / Reserve a Book

| Field | Detail |
|---|---|
| **Use Case ID** | UC03 |
| **Use Case Name** | Borrow / Reserve a Book |
| **Actor(s)** | Student, Librarian |
| **Related FR** | FR-03 |
| **Description** | Allows a student to borrow an available physical book or place a reservation on an unavailable one. Includes eligibility checking and automated confirmation email. |
| **Preconditions** | Student is logged in. Resource detail page is open. Student has fewer than 3 overdue items and no unpaid fines exceeding R100. |
| **Postconditions** | If borrowed: inventory is decremented, loan record created with due date (14 days), confirmation email sent. If reserved: reservation record created, book held for 48 hours, confirmation email sent. |

### Basic Flow
1. Student opens a resource detail page from search results.
2. Student clicks "Borrow" (if available) or "Reserve" (if unavailable).
3. System checks borrow eligibility: verifies no outstanding overdue items ≥ 3 and no fines > R100.
4. Eligibility confirmed.
5. **If borrowing:** System decrements available copy count, creates a Loan record with a 14-day due date, and displays: *"Successfully borrowed! Due date: [date]."*
6. **If reserving:** System creates a Reservation record with a 48-hour hold window and places the student in the queue.
7. System triggers the Notification Service to send a confirmation email within 60 seconds.
8. Student is redirected to their dashboard where the new loan/reservation appears.

### Alternative Flows

**AF-01: Student ineligible to borrow**
- At Step 3, if eligibility check fails, the system displays: *"You cannot borrow at this time. You have [X] overdue items / outstanding fines of R[amount]."*
- The "Borrow" button is replaced with a link to the student's dashboard to resolve issues.

**AF-02: Last copy just taken (race condition)**
- At Step 5, if the last available copy was taken by another user between search and borrow click, the system automatically switches to the reservation flow and notifies the student.

**AF-03: Reservation expiry**
- If a reserved book is not collected within 48 hours, the system automatically cancels the reservation, notifies the student, and activates the next queued reservation.

---

## UC04 — View Student Dashboard

| Field | Detail |
|---|---|
| **Use Case ID** | UC04 |
| **Use Case Name** | View Student Dashboard |
| **Actor(s)** | Student, Accessibility User |
| **Related FR** | FR-04 |
| **Description** | Provides each student with a unified personal dashboard showing active loans, due dates, borrowing history, saved reading list, overdue notices, and personalized recommendations — all in one view. |
| **Preconditions** | Student is logged in. Dashboard data services (API, database, recommendation engine) are reachable. |
| **Postconditions** | Dashboard is fully rendered within 2 seconds showing current, accurate data for the logged-in student. |

### Basic Flow
1. Student logs in and is automatically redirected to their dashboard.
2. System simultaneously fetches: active loans, upcoming due dates, overdue notices, reading list, and recommendation data via parallel API calls.
3. Dashboard renders within 2 seconds with all sections populated.
4. Due date alerts within 3 days are highlighted in red with a warning icon.
5. Overdue items are displayed prominently at the top with a "Return Now" call-to-action.
6. Recommendations section displays at least 10 personalized resources.
7. Student may click any loan to see full resource details, or click "View Borrowing History" to see the last 12 months.

### Alternative Flows

**AF-01: No borrowing history (new student)**
- Borrowing history section shows: *"No borrowing history yet. Start exploring the catalogue!"*
- Recommendations section shows course-based default recommendations.

**AF-02: API timeout on one section**
- If one data section (e.g., recommendations) fails to load within 3 seconds, that section displays a loading skeleton with: *"Unable to load recommendations. Retrying…"*
- Other dashboard sections render normally without being blocked.

---

## UC05 — Receive Personalized Recommendations

| Field | Detail |
|---|---|
| **Use Case ID** | UC05 |
| **Use Case Name** | Receive Personalized Recommendations |
| **Actor(s)** | Student, Recommendation Engine |
| **Related FR** | FR-05 |
| **Description** | The Recommendation Engine automatically generates and refreshes personalized academic resource recommendations for each student based on their borrowing history, search behavior, and course enrollment. Students can view, act on, or dismiss these recommendations. |
| **Preconditions** | Student is logged in. Recommendation Engine has completed its latest batch run (updated within 24 hours). |
| **Postconditions** | Student sees at least 10 personalized recommendations on their dashboard. Any dismissal is recorded and fed back to the model. |

### Basic Flow
1. Recommendation Engine runs a daily batch job processing all active student profiles.
2. For each student, the engine applies collaborative filtering using borrowing history, search history, and course enrollment data.
3. Top 10+ ranked resource recommendations are stored in the database per student.
4. When the student loads their dashboard, the system fetches their pre-computed recommendations.
5. Recommendations are displayed as a horizontal scroll with cover image, title, author, and a "Borrow" shortcut button.
6. Student may click a recommendation to go to the full resource detail page.
7. Student may click "Not Interested" (dismiss) on any recommendation.
8. Dismissal is recorded in the model's feedback loop for the next batch run.

### Alternative Flows

**AF-01: New student with no history (cold start)**
- At Step 2, if the student has fewer than 3 interaction records, the engine falls back to course-based defaults.
- Recommendations are populated within 1 hour of registration based on enrolled course subjects.

**AF-02: Recommendation Engine batch delayed**
- If the batch job has not run within 24 hours, the system displays the most recent cached recommendations with a note: *"Recommendations last updated [time]."*

---

## UC06 — Manage Library Catalogue

| Field | Detail |
|---|---|
| **Use Case ID** | UC06 |
| **Use Case Name** | Manage Library Catalogue |
| **Actor(s)** | Librarian |
| **Related FR** | FR-06 |
| **Description** | Allows authenticated librarians to add new resources, edit existing entries, delete resources, and bulk import records via CSV upload. All changes are immediately reflected in the search index. |
| **Preconditions** | Librarian is logged in with the LIBRARIAN role. Elasticsearch and PostgreSQL are reachable. |
| **Postconditions** | Resource is saved to PostgreSQL and indexed in Elasticsearch within 30 seconds. All changes are audit-logged with librarian ID and timestamp. |

### Basic Flow
1. Librarian navigates to the Catalogue Management section of the Admin Panel.
2. Librarian clicks "Add New Resource" and fills in the resource form: title, author, ISBN, genre, number of copies, physical location, and cover image.
3. System validates the ISBN using ISBN-10/ISBN-13 check digit rules.
4. Validation passes. System saves the resource record to PostgreSQL.
5. System triggers an Elasticsearch re-index job for the new resource.
6. Resource appears in search results within 30 seconds.
7. All changes are written to the audit log.

### Alternative Flows

**AF-01: Invalid ISBN**
- At Step 3, if ISBN validation fails, the system displays: *"Invalid ISBN. Please check and re-enter."*
- The form is not submitted until a valid ISBN is provided.

**AF-02: Delete resource with active loans**
- If librarian attempts to delete a resource that has active loans, the system blocks the action and displays: *"Cannot delete: this resource has [X] active loans. Please wait until all copies are returned."*

**AF-03: Bulk CSV import**
- Librarian clicks "Bulk Import" and uploads a CSV file (max 1,000 rows).
- System validates each row for required fields and ISBN format.
- Valid rows are imported; invalid rows are flagged in an error report displayed to the librarian.
- Successful records are indexed in Elasticsearch within 60 seconds.

---

## UC07 — Automated Overdue Notifications

| Field | Detail |
|---|---|
| **Use Case ID** | UC07 |
| **Use Case Name** | Receive Overdue Notifications |
| **Actor(s)** | Student, Librarian, Notification Service (automated) |
| **Related FR** | FR-07 |
| **Description** | The system automatically sends email notifications to students at three scheduled intervals relative to their loan due date. Librarians receive a daily digest of all overdue items. |
| **Preconditions** | Student has at least one active loan. Notification Service and Email Service are operational. |
| **Postconditions** | Student receives a timely notification email. Notification delivery is logged. Failures are retried up to 3 times. |

### Basic Flow
1. Notification Service runs a scheduled job every hour checking loan due dates.
2. For any loan due in exactly 3 days: system queues a "Due Soon" email to the student.
3. For any loan due today: system queues a "Due Today" email.
4. For any loan 1 day overdue and not returned: system queues an "Overdue" email.
5. Each email includes: resource title, due date, student name, and a deep link to the dashboard.
6. Email is dispatched via SendGrid within 5 minutes of the trigger.
7. Delivery confirmation is logged. If delivery fails, the system retries up to 3 times with exponential backoff.
8. Each morning at 08:00, librarians receive a digest email listing all currently overdue items.

### Alternative Flows

**AF-01: Email delivery failure**
- If SendGrid returns a delivery failure after 3 retries, the system logs the failure as a critical notification error.
- An in-app notification is shown to the student on their next dashboard visit as a fallback.

**AF-02: Student opts out of email notifications**
- If the student has disabled email notifications in preferences, the system delivers in-app notifications only.
- Due date alerts are still shown on the dashboard in red.

---

## UC08 — Generate Usage Reports

| Field | Detail |
|---|---|
| **Use Case ID** | UC08 |
| **Use Case Name** | Generate Usage Reports |
| **Actor(s)** | Administrator, Librarian |
| **Related FR** | FR-08 |
| **Description** | Allows administrators and librarians to view and export usage analytics reports including borrowing trends, most-borrowed items, overdue rates, and student engagement metrics. |
| **Preconditions** | User is logged in with LIBRARIAN or ADMIN role. Reporting data has been refreshed (daily at midnight). |
| **Postconditions** | Report is displayed on screen. If export is requested, a PDF or CSV file is generated and made available for download within 10 seconds. |

### Basic Flow
1. Administrator or Librarian navigates to the Reports section of the Admin Panel.
2. User selects a report type from the available options: Top 20 Borrowed Resources, Overdue Rate by Month, Active Users by Faculty, New Acquisitions vs Demand.
3. User applies filters: date range, department, resource type, or student cohort.
4. System queries the reporting database (refreshed nightly) and renders the report as a chart and summary table within 5 seconds.
5. User reviews the report on screen.
6. User optionally clicks "Export" and selects PDF or CSV.
7. System generates the export file within 10 seconds and triggers a browser download.

### Alternative Flows

**AF-01: Insufficient permissions**
- If a Librarian attempts to access an Admin-only report (e.g., system-wide user management report), the system returns HTTP 403 and displays: *"You do not have permission to view this report."*

**AF-02: No data for selected filters**
- If the filter combination returns no records, the system displays: *"No data available for the selected filters. Try adjusting the date range or department."*

**AF-03: Export timeout**
- If a report covering more than 12 months of data takes longer than 10 seconds to generate, the system queues the export and emails a download link to the user when ready.
