# ACTIVITY_DIAGRAMS.md — Activity Workflow Modeling
## Smart Academic Library Assistance System (SALAS)

> Assignment 8: Object State Modeling and Activity Workflow Modeling
> Building on Assignments 3–7 | Version 1.0 | April 2026

---

## 1. User Registration Workflow

```mermaid
flowchart TD
    A([Start]) --> B[Student enters email, name and password]
    B --> C{Valid university\nemail domain?}
    C -- No --> D[Show error: use university email]
    D --> B
    C -- Yes --> E{Password meets\nstrength requirements?}
    E -- No --> F[Show password requirements]
    F --> B
    E -- Yes --> G[System creates Unverified account]
    G --> H[System sends verification email]
    H --> I[Student clicks verification link]
    I --> J{Link expired?\n7 days}
    J -- Yes --> K[Show error: link expired]
    K --> L[Resend verification email]
    L --> I
    J -- No --> M[Account activated]
    M --> N[Student redirected to dashboard]
    N --> Z([End])

    style A fill:#2d6a4f,color:#fff
    style Z fill:#2d6a4f,color:#fff
    style C fill:#e9c46a,color:#000
    style E fill:#e9c46a,color:#000
    style J fill:#e9c46a,color:#000
```

### Explanation

**Swimlane roles:** Student, System, Email Service

**Workflow summary:** This activity covers FR-01 (Student Registration). The two decision nodes enforce password strength and university email domain validation. The email verification loop handles the case where a student's verification link expires before use.

**Stakeholder concern addressed:** Students need a secure, institution-linked account. The domain validation guard ensures only enrolled students can access the system.

**US traceability:** US-002 (Student registration and login) | Sprint 1

---

## 2. Search Library Catalogue Workflow

```mermaid
flowchart TD
    A([Start]) --> B[Student enters search query]
    B --> C[System sends query to Elasticsearch]
    C --> D{Results\nfound?}
    D -- No --> E[Display: No results found]
    E --> F[Suggest related resources]
    F --> G[Student refines query]
    G --> B
    D -- Yes --> H[Enrich results with real-time\navailability from PostgreSQL]
    H --> I[Display ranked results within 2 seconds]
    I --> J{Student applies\nfilters?}
    J -- Yes --> K[Apply filters: author, genre,\nyear, availability]
    K --> L[Refresh results without page reload]
    L --> M[Student views filtered results]
    J -- No --> M
    M --> N{Student selects\na resource?}
    N -- No --> O[Student refines or exits search]
    O --> Z([End])
    N -- Yes --> P[Open resource detail page]
    P --> Z

    style A fill:#2d6a4f,color:#fff
    style Z fill:#2d6a4f,color:#fff
    style D fill:#e9c46a,color:#000
    style J fill:#e9c46a,color:#000
    style N fill:#e9c46a,color:#000
```

### Explanation

**Swimlane roles:** Student, Search Service (Elasticsearch), Database (PostgreSQL)

**Workflow summary:** This covers FR-02 (Search). The parallel enrichment step — combining Elasticsearch relevance scoring with real-time availability from PostgreSQL — is a key architectural pattern ensuring results are both relevant and accurate.

**Stakeholder concern addressed:** Students' top pain point is finding resources quickly. The 2-second response time requirement (NFR-12) is enforced at the display step.

**US traceability:** US-001 (Search library catalogue) | Sprint 1

---

## 3. Borrow / Reserve a Book Workflow

```mermaid
flowchart TD
    A([Start]) --> B[Student opens resource detail page]
    B --> C{Student\nauthenticated?}
    C -- No --> D[Redirect to login page]
    D --> Z([End])
    C -- Yes --> E{Check borrow\neligibility}
    E -- Ineligible\nfines or overdues --> F[Show error: resolve fines or returns first]
    F --> Z
    E -- Eligible --> G{Book\navailable?}
    G -- Yes --> H[Student clicks Borrow]
    H --> I[System decrements available copy count]
    I --> J[Create Loan record with 14-day due date]
    J --> K[Send confirmation email within 60 seconds]
    K --> L[Show success: book borrowed]
    G -- No --> M[Student clicks Reserve]
    M --> N{Other reservations\nexist?}
    N -- Yes --> O[Add student to reservation queue]
    N -- No --> P[Create Reservation record]
    O --> Q[Send queue position confirmation email]
    P --> R[Send reservation confirmation email]
    Q --> S[Start 48-hour hold timer]
    R --> S
    S --> Z

    style A fill:#2d6a4f,color:#fff
    style Z fill:#2d6a4f,color:#fff
    style C fill:#e9c46a,color:#000
    style E fill:#e9c46a,color:#000
    style G fill:#e9c46a,color:#000
    style N fill:#e9c46a,color:#000
```

### Explanation

**Swimlane roles:** Student, System API, Database, Notification Service

**Workflow summary:** This covers FR-03 (Borrowing and Reservation). The eligibility check enforces the guard condition from FR-03: borrowing is blocked if the student has 3+ overdue items or fines exceeding R100. The parallel flows for borrowing vs reserving show how the system handles both scenarios from a single entry point.

**Stakeholder concern addressed:** Students want to reserve resources without visiting the library. Librarians need inventory accuracy. Both are addressed by the immediate inventory decrement and confirmation email steps.

**US traceability:** US-003 (Borrow/reserve a book) | Sprint 2

---

## 4. Return a Book Workflow

```mermaid
flowchart TD
    A([Start]) --> B[Librarian scans or enters book ISBN]
    B --> C{Book found\nin system?}
    C -- No --> D[Show error: ISBN not recognised]
    D --> Z([End])
    C -- Yes --> E{Book checked out\nto a student?}
    E -- No --> F[Show error: book not currently on loan]
    F --> Z
    E -- Yes --> G{Book\noverdue?}
    G -- Yes --> H[Calculate fine amount]
    H --> I[Record fine on student account]
    I --> J[Notify student of fine via email]
    G -- No --> K[Mark loan as Returned]
    J --> K
    K --> L[Increment available copy count]
    L --> M{Reservations\nin queue?}
    M -- Yes --> N[Activate next reservation]
    N --> O[Notify next student: book is ready]
    M -- No --> P[Book status set to Available]
    O --> P
    P --> Q[Update Elasticsearch availability index]
    Q --> Z

    style A fill:#2d6a4f,color:#fff
    style Z fill:#2d6a4f,color:#fff
    style C fill:#e9c46a,color:#000
    style E fill:#e9c46a,color:#000
    style G fill:#e9c46a,color:#000
    style M fill:#e9c46a,color:#000
```

### Explanation

**Swimlane roles:** Librarian, System API, Database, Notification Service

**Workflow summary:** This covers the return lifecycle from UC12 (Return Borrowed Book). The decision at the overdue check automatically calculates and records fines. The queue check ensures reservations are activated immediately upon return, minimising wait time for the next student.

**Stakeholder concern addressed:** Librarians need accurate, real-time inventory. The immediate Elasticsearch update (last step) ensures search results reflect the returned book within 30 seconds.

**US traceability:** UC12 (Return Borrowed Book) | Sprint 2

---

## 5. Student Dashboard Load Workflow

```mermaid
flowchart TD
    A([Start]) --> B[Student logs in successfully]
    B --> C[System initiates parallel data fetch]

    C --> D[Fetch active loans\nand due dates]
    C --> E[Fetch overdue\nnotices]
    C --> F[Fetch recommendations\nfrom cache]
    C --> G[Fetch reading\nlist items]

    D --> H{All data\nloaded within 2s?}
    E --> H
    F --> H
    G --> H

    H -- Yes --> I[Render complete dashboard]
    H -- No --> J[Render available sections\nShow skeleton for slow sections]
    J --> K[Retry failed sections in background]
    K --> L[Update dashboard when data arrives]
    L --> I

    I --> M{Items due\nwithin 3 days?}
    M -- Yes --> N[Highlight due items in red]
    M -- No --> O[Display dashboard normally]
    N --> O
    O --> Z([End])

    style A fill:#2d6a4f,color:#fff
    style Z fill:#2d6a4f,color:#fff
    style H fill:#e9c46a,color:#000
    style M fill:#e9c46a,color:#000
```

### Explanation

**Swimlane roles:** Student, API Gateway, Multiple Backend Services

**Workflow summary:** This covers FR-04 (Student Dashboard). The parallel fetch step is critical — all four data sources are queried simultaneously rather than sequentially, enabling the 2-second load time (NFR-13). The skeleton loading pattern ensures the dashboard is usable even if one service is slow.

**Stakeholder concern addressed:** Students need a fast, unified view of their library activity. The parallel architecture directly addresses NFR-13 (Dashboard Load Time ≤ 2 seconds).

**US traceability:** US-004 (Student personal dashboard) | Sprint 2

---

## 6. Automated Overdue Notification Workflow

```mermaid
flowchart TD
    A([Start]) --> B[Notification scheduler runs every hour]
    B --> C[Query all active loans from database]
    C --> D{Loans due\nin exactly 3 days?}
    D -- Yes --> E[Queue Due Soon email for each student]
    D -- No --> F{Loans due\ntoday?}
    F -- Yes --> G[Queue Due Today email]
    F -- No --> H{Loans 1 day\noverdue?}
    H -- Yes --> I[Queue Overdue email]
    H -- No --> J[No action required]

    E --> K[Send emails via SendGrid]
    G --> K
    I --> K

    K --> L{Delivery\nsuccessful?}
    L -- Yes --> M[Log delivery confirmation]
    L -- No --> N{Retry count\nless than 3?}
    N -- Yes --> O[Increment retry counter]
    O --> K
    N -- No --> P[Log permanent failure]
    P --> Q[Trigger in-app notification as fallback]

    M --> R{Is it\n08:00?}
    Q --> R
    J --> R
    R -- Yes --> S[Generate librarian daily digest email]
    S --> T[Send digest to all librarians]
    R -- No --> Z([End])
    T --> Z

    style A fill:#2d6a4f,color:#fff
    style Z fill:#2d6a4f,color:#fff
    style D fill:#e9c46a,color:#000
    style F fill:#e9c46a,color:#000
    style H fill:#e9c46a,color:#000
    style L fill:#e9c46a,color:#000
    style N fill:#e9c46a,color:#000
    style R fill:#e9c46a,color:#000
```

### Explanation

**Swimlane roles:** Notification Scheduler, Database, Email Service (SendGrid), Librarian

**Workflow summary:** This covers FR-07 (Automated Overdue Notifications). The three-retry loop with exponential backoff ensures reliable delivery. The 08:00 guard condition triggers the librarian digest exactly once per day.

**Stakeholder concern addressed:** Librarians want automated overdue tracking. Students want timely reminders. The parallel checking of three trigger conditions (3 days, due today, 1 day overdue) handles all cases in a single scheduler run.

**US traceability:** US-007 (Automated overdue notifications) | Sprint 2

---

## 7. Librarian Catalogue Management Workflow

```mermaid
flowchart TD
    A([Start]) --> B[Librarian navigates to Catalogue Management]
    B --> C{Action\nselected?}
    C -- Add New --> D[Librarian fills resource form]
    D --> E{ISBN\nvalid?}
    E -- No --> F[Show ISBN validation error]
    F --> D
    E -- Yes --> G[Save resource to PostgreSQL]
    G --> H[Trigger Elasticsearch indexing job]
    H --> I[Resource searchable within 30 seconds]
    I --> J[Write audit log entry]

    C -- Edit --> K[Librarian modifies resource fields]
    K --> L[Save updated record to PostgreSQL]
    L --> M[Re-index resource in Elasticsearch]
    M --> J

    C -- Delete --> N{Active loans\nexist?}
    N -- Yes --> O[Block deletion: show active loans count]
    O --> Z([End])
    N -- No --> P[Delete resource from PostgreSQL]
    P --> Q[Remove from Elasticsearch index]
    Q --> J

    C -- Bulk Import --> R[Librarian uploads CSV file]
    R --> S[Validate each row: required fields and ISBN]
    S --> T[Import valid rows to PostgreSQL]
    T --> U[Flag invalid rows in error report]
    U --> H

    J --> Z

    style A fill:#2d6a4f,color:#fff
    style Z fill:#2d6a4f,color:#fff
    style C fill:#e9c46a,color:#000
    style E fill:#e9c46a,color:#000
    style N fill:#e9c46a,color:#000
```

### Explanation

**Swimlane roles:** Librarian, System API, PostgreSQL, Elasticsearch

**Workflow summary:** This covers FR-06 (Library Catalogue Management). Four parallel action paths (Add, Edit, Delete, Bulk Import) branch from a single entry point. The deletion guard condition (active loans check) is a critical safety mechanism that prevents data integrity issues.

**Stakeholder concern addressed:** Librarians need fast, accurate catalogue management. The Elasticsearch re-indexing step ensures search results stay current within 30 seconds of any change (FR-06 acceptance criteria).

**US traceability:** US-006 (Librarian catalogue management), US-014 (Bulk CSV import) | Sprint 2 and Sprint 3

---

## 8. Generate and Export Usage Report Workflow

```mermaid
flowchart TD
    A([Start]) --> B[Admin or Librarian selects report type]
    B --> C[Apply filters: date range, department, resource type]
    C --> D{User has\npermission for this report?}
    D -- No --> E[Return HTTP 403: Access Denied]
    E --> Z([End])
    D -- Yes --> F[Query reporting database]
    F --> G{Query\nsuccessful?}
    G -- No --> H[Show error: unable to generate report]
    H --> Z
    G -- Yes --> I[Render report as chart and summary table]
    I --> J[Display report on screen]
    J --> K{Admin requests\nexport?}
    K -- No --> Z
    K -- Yes --> L[Admin selects format: PDF or CSV]
    L --> M{Report covers\nmore than 12 months?}
    M -- No --> N[Generate export file]
    N --> O{File ready\nwithin 10 seconds?}
    O -- Yes --> P[Trigger browser download]
    O -- No --> Q[Queue export as background job]
    Q --> R[Email download link to admin when ready]
    M -- Yes --> Q
    P --> Z
    R --> Z

    style A fill:#2d6a4f,color:#fff
    style Z fill:#2d6a4f,color:#fff
    style D fill:#e9c46a,color:#000
    style G fill:#e9c46a,color:#000
    style K fill:#e9c46a,color:#000
    style M fill:#e9c46a,color:#000
    style O fill:#e9c46a,color:#000
```

### Explanation

**Swimlane roles:** Administrator, Librarian, System API, Reporting Database, Email Service

**Workflow summary:** This covers FR-08 (Usage Reporting and Analytics). The RBAC check at the start enforces FR-10 — admin-only reports return HTTP 403 for librarians. The large-report queue handles the alternative flow from UC08 where exports exceeding 12 months are processed as background jobs.

**Stakeholder concern addressed:** University administrators need data-driven procurement insights. The export functionality with background queuing ensures even large, complex reports are always deliverable.

**US traceability:** US-008 (Usage reports and analytics) | Sprint 3
