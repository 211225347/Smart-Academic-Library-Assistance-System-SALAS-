[ACTIVITY_DIAGRAMS.md](https://github.com/user-attachments/files/26781208/ACTIVITY_DIAGRAMS.md)
# ACTIVITY_DIAGRAMS.md — Activity Workflow Modeling
## Smart Academic Library Assistance System (SALAS)

> Assignment 8: Object State Modeling and Activity Workflow Modeling
> Building on Assignments 3–7 |19 April 2026

---

## 1. User Registration Workflow

```mermaid
flowchart TD
    A([Start]) --> B[Student enters email, name and password]
    B --> C{Valid university\nemail domain?}
    C -- Yes --> D{Password meets\nstrength requirements?}
    C -- No --> E[Show error: use university email]
    E --> B
    D -- Yes --> F[System creates Unverified account]
    D -- No --> G[Show password requirements]
    G --> B
    F --> H[System sends verification email]
    H --> I[Student clicks verification link]
    I --> J{Link expired?\n7 days}
    J -- No --> K[Account activated]
    J -- Yes --> L[Show error: link expired]
    L --> M[Resend verification email]
    M --> I
    K --> N[Student redirected to dashboard]
    N --> Z([End])

    style A fill:#2d6a4f,color:#fff
    style Z fill:#2d6a4f,color:#fff
    style C fill:#e9c46a,color:#000
    style D fill:#e9c46a,color:#000
    style J fill:#e9c46a,color:#000
```

### Explanation

**Swimlane roles:** Student, System, Email Service

**Workflow summary:** This activity covers FR-01. Two decision nodes enforce password strength and university email domain validation. The email verification loop handles link expiry with an automatic resend path.

**Stakeholder Value**
This workflow ensures only enrolled university students can create accounts, protecting the system from unauthorised access while providing a smooth self-service onboarding experience. IT administrators benefit from the built-in lockout and verification controls that enforce security policy without manual intervention.

**Related Functional Requirements**
- FR-01: User registration and authentication
- NFR-10: Brute-force and authentication security

**Sprint Traceability:** US-002 (Student registration and login) | Sprint 1

---

## 2. Search Library Catalogue Workflow

```mermaid
flowchart TD
    A([Start]) --> B[Student enters search query]
    B --> C[System sends query to Elasticsearch]
    C --> D{Results found?}
    D -- Yes --> E[Enrich results with real-time\navailability from PostgreSQL]
    D -- No --> F[Display: No results found]
    F --> G[Suggest related resources]
    G --> H[Student refines query]
    H --> B
    E --> I[Display ranked results within 2 seconds]
    I --> J{Student applies\nfilters?}
    J -- Yes --> K[Apply filters: author, genre,\nyear, availability]
    K --> L[Refresh results without page reload]
    L --> M[Student views filtered results]
    J -- No --> M
    M --> N{Student selects\na resource?}
    N -- Yes --> O[Open resource detail page]
    N -- No --> P[Student refines or exits search]
    O --> Z([End])
    P --> Z

    style A fill:#2d6a4f,color:#fff
    style Z fill:#2d6a4f,color:#fff
    style D fill:#e9c46a,color:#000
    style J fill:#e9c46a,color:#000
    style N fill:#e9c46a,color:#000
```

### Explanation

**Swimlane roles:** Student, Search Service (Elasticsearch), Database (PostgreSQL)

**Workflow summary:** This covers FR-02. Elasticsearch returns ranked results which are enriched with live availability data from PostgreSQL. Filters are applied without a page reload, meeting the usability acceptance criteria.

**Stakeholder Value**
This workflow directly addresses the primary student pain point: finding resources quickly. The 2-second response requirement (NFR-12) is enforced at the display step. Librarians benefit from accurate real-time availability being surfaced automatically, reducing enquiries at the desk.

**Related Functional Requirements**
- FR-02: Natural language and filtered resource search
- NFR-12: Search response time under 2 seconds

**Sprint Traceability:** US-001 (Search library catalogue) | Sprint 1

---

## 3. Borrow / Reserve a Book Workflow

```mermaid
flowchart TD
    A([Start]) --> B[Student opens resource detail page]
    B --> C{Student\nauthenticated?}
    C -- No --> D[Redirect to login page]
    D --> Z([End])
    C -- Yes --> E{Borrow eligibility\ncheck passed?}
    E -- No --> F[Show error: resolve fines or returns first]
    F --> Z
    E -- Yes --> G{Book available?}
    G -- Yes --> H[Student clicks Borrow]
    H --> I[System decrements available copy count]
    I --> J[Create Loan record with 14-day due date]
    J --> K[Send confirmation email within 60 seconds]
    K --> L[Show success: book borrowed]
    G -- No --> M[Student clicks Reserve]
    M --> N{Other reservations\nin queue?}
    N -- Yes --> O[Add student to reservation queue]
    N -- No --> P[Create Reservation record]
    O --> Q[Send queue confirmation email]
    P --> R[Send reservation confirmation email]
    Q --> S[Start 48-hour hold timer]
    R --> S
    L --> Z
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

**Workflow summary:** This covers FR-03. The eligibility check blocks borrowing when fines exceed R100 or overdue items exceed 3. Parallel flows handle borrowing vs reserving from a single entry point. This workflow directly supports the Sprint 2 user story focused on real-time availability checks and transaction processing.

**Stakeholder Value**
Students benefit from a fully online borrow and reserve process, eliminating the need for in-person visits. Librarians benefit from real-time inventory accuracy — the immediate decrement of available copies prevents double-booking. The automated confirmation email reduces front-desk enquiries and supports scalability.

**Related Functional Requirements**
- FR-03: Book borrowing and reservation
- FR-07: Automated confirmation notifications

**Sprint Traceability:** US-003 (Borrow/reserve a book) | Sprint 2

---

## 4. Return a Book Workflow

```mermaid
flowchart TD
    A([Start]) --> B[Librarian scans or enters book ISBN]
    B --> C{Book found\nin system?}
    C -- No --> D[Show error: ISBN not recognised]
    D --> Z([End])
    C -- Yes --> E{Book currently\non loan?}
    E -- No --> F[Show error: book not on loan]
    F --> Z
    E -- Yes --> G{Book overdue?}
    G -- Yes --> H[Calculate fine amount]
    H --> I[Record fine on student account]
    I --> J[Notify student of fine via email]
    G -- No --> K[Mark loan as Returned]
    J --> K
    K --> L[Increment available copy count]
    L --> M{Reservations\nin queue?}
    M -- Yes --> N[Activate next reservation]
    N --> O[Notify next student: book ready]
    M -- No --> P[Set book status to Available]
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

**Workflow summary:** This covers UC12. The overdue check automatically calculates and records fines. The queue check activates the next reservation immediately upon return, minimising wait times.

**Stakeholder Value**
Librarians benefit from a fast, accurate return process that handles fines and queue activation automatically, reducing manual work. Students on the reservation queue benefit from immediate notification when a book becomes available. The Elasticsearch update ensures search results reflect the returned book within 30 seconds, supporting real-time accuracy for all users.

**Related Functional Requirements**
- FR-03: Borrowing and reservation lifecycle
- FR-07: Automated overdue fine notification

**Sprint Traceability:** UC12 (Return Borrowed Book) | Sprint 2

---

## 5. Student Dashboard Load Workflow

```mermaid
flowchart TD
    A([Start]) --> B[Student logs in successfully]
    B --> C[Initiate parallel data fetch]
    C --> D[Fetch active loans\nand due dates]
    C --> E[Fetch overdue notices]
    C --> F[Fetch recommendations\nfrom cache]
    C --> G[Fetch reading list items]
    D --> H{All sections\nloaded within 2s?}
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

**Workflow summary:** This covers FR-04. All four data sources are fetched in parallel to achieve the 2-second load requirement (NFR-13). The skeleton loading pattern ensures the dashboard remains usable even if one service is slow.

**Stakeholder Value**
Students benefit from a fast, unified view of all their library activity in a single screen. The parallel fetch architecture directly addresses the NFR-13 performance requirement. IT administrators benefit from the graceful degradation pattern, a slow recommendation service will not block the entire dashboard, maintaining perceived reliability during peak usage periods.

**Related Functional Requirements**
- FR-04: Student personal dashboard
- NFR-13: Dashboard load time under 2 seconds

**Sprint Traceability:** US-004 (Student personal dashboard) | Sprint 2

---

## 6. Automated Overdue Notification Workflow

```mermaid
flowchart TD
    A([Start]) --> B[Notification scheduler runs every hour]
    B --> C[Query all active loans from database]
    C --> D{Loans due\nin exactly 3 days?}
    D -- Yes --> E[Queue Due Soon email]
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
    P --> Q[Trigger in-app notification fallback]
    M --> R{Is it 08:00?}
    Q --> R
    J --> R
    R -- Yes --> S[Generate librarian daily digest]
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

**Swimlane roles:** Notification Scheduler, Database, Email Service, Librarian

**Workflow summary:** This covers FR-07. Three trigger conditions are checked in a single scheduler run. The 3-retry loop with exponential backoff ensures reliable delivery. The 08:00 guard triggers the librarian digest exactly once per day.

**Stakeholder Value**
Students benefit from timely, automated reminders that reduce overdue fines without requiring manual follow-up. Librarians benefit from a consolidated daily digest that gives full overdue visibility without needing to query the system manually. The retry and fallback logic ensures notification reliability even when the email service experiences downtime, supporting the IT administrator's uptime requirements.

**Related Functional Requirements**
- FR-07: Automated overdue notifications and retry logic

**Sprint Traceability:** US-007 (Automated overdue notifications) | Sprint 2

---

## 7. Librarian Catalogue Management Workflow

```mermaid
flowchart TD
    A([Start]) --> B[Librarian navigates to Catalogue Management]
    B --> C{Action selected?}
    C -- Add New --> D[Librarian fills resource form]
    D --> E{ISBN valid?}
    E -- No --> F[Show ISBN validation error]
    F --> D
    E -- Yes --> G[Save resource to PostgreSQL]
    G --> H[Trigger Elasticsearch indexing]
    H --> I[Resource searchable within 30 seconds]
    I --> J[Write audit log entry]
    C -- Edit --> K[Librarian modifies resource fields]
    K --> L[Save updated record]
    L --> M[Re-index in Elasticsearch]
    M --> J
    C -- Delete --> N{Active loans exist?}
    N -- Yes --> O[Block deletion: show loan count]
    O --> Z([End])
    N -- No --> P[Delete from PostgreSQL]
    P --> Q[Remove from Elasticsearch index]
    Q --> J
    C -- Bulk Import --> R[Librarian uploads CSV]
    R --> S[Validate each row]
    S --> T[Import valid rows]
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

**Workflow summary:** This covers FR-06. Four action paths branch from a single entry. The deletion guard prevents data integrity issues. All changes are audit-logged.

**Stakeholder Value**
Librarians benefit from a fast, multi-action catalogue tool that handles validation, indexing, and audit logging automatically. The bulk import path addresses the pain point of large acquisitions. University administrators benefit from the audit log, which supports compliance and accountability. The Elasticsearch re-indexing ensures students always see accurate catalogue data within 30 seconds of any change.

**Related Functional Requirements**
- FR-06: Library catalogue management
- FR-02: Search relies on the Searchable state produced by this workflow

**Sprint Traceability:** US-006 (Librarian catalogue management), US-014 (Bulk CSV import) | Sprint 2 and Sprint 3

---

## 8. Generate and Export Usage Report Workflow

```mermaid
flowchart TD
    A([Start]) --> B[Admin or Librarian selects report type]
    B --> C[Apply filters: date range, department, type]
    C --> D{User has\npermission?}
    D -- No --> E[Return HTTP 403: Access Denied]
    E --> Z([End])
    D -- Yes --> F[Query reporting database]
    F --> G{Query successful?}
    G -- No --> H[Show error: unable to generate]
    H --> Z
    G -- Yes --> I[Render report as chart and table]
    I --> J[Display report on screen]
    J --> K{Admin requests\nexport?}
    K -- No --> Z
    K -- Yes --> L[Admin selects PDF or CSV]
    L --> M{Report covers\nmore than 12 months?}
    M -- No --> N[Generate export file]
    N --> O{File ready\nwithin 10 seconds?}
    O -- Yes --> P[Trigger browser download]
    O -- No --> Q[Queue as background job]
    M -- Yes --> Q
    Q --> R[Email download link when ready]
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

**Workflow summary:** This covers FR-08. The RBAC check enforces FR-10 at entry. The background queue handles large reports exceeding the 10-second SLA. All decision branches are explicitly labelled Yes/No.

**Stakeholder Value**
University administrators benefit from data-driven procurement insights through filterable, exportable reports. The RBAC check ensures sensitive system-wide reports are restricted to authorised roles, satisfying IT administrator security requirements. The background export queue ensures even large historical reports are always deliverable, supporting the administrator's need for complete data access without system timeouts.

**Related Functional Requirements**
- FR-08: Usage reporting and analytics
- FR-10: Role-based access control enforced at the permission check

**Sprint Traceability:** US-008 (Usage reports and analytics) | Sprint 3
