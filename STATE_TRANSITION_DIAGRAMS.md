[STATE_TRANSITION_DIAGRAMS.md](https://github.com/user-attachments/files/26707030/STATE_TRANSITION_DIAGRAMS.md)
# STATE_TRANSITION_DIAGRAMS.md — Object State Modeling
## Smart Academic Library Assistance System (SALAS)

> Assignment 8: Object State Modeling and Activity Workflow Modeling
> Building on Assignments 3–7 |19 April 2026

---

## 1. Book / Resource Object

```mermaid
stateDiagram-v2
    [*] --> Available : Librarian adds resource (FR-06)

    Available --> Reserved : Student places reservation (FR-03)
    Available --> Borrowed : Student borrows book (FR-03)
    Available --> UnderMaintenance : Librarian flags for repair

    Reserved --> Borrowed : Student collects at desk (FR-03)
    Reserved --> Available : Reservation expires after 48 hours (FR-03)
    Reserved --> Available : Student cancels reservation

    Borrowed --> Overdue : Due date passes without return (FR-07)
    Borrowed --> Available : Student returns book (UC03)

    Overdue --> Available : Student returns overdue book
    Overdue --> Lost : Librarian marks as lost

    UnderMaintenance --> Available : Librarian marks repair complete
    Lost --> [*] : Resource permanently removed from catalogue

    Available --> [*] : Librarian deletes resource (no active loans) (FR-06)
```

### Explanation

**Key States:** Available, Reserved, Borrowed, Overdue, UnderMaintenance, Lost

**Key Transitions:**
- A book starts as Available when added to the catalogue by a librarian (FR-06)
- It moves to Reserved when a student places an online reservation (FR-03)
- Reserved books that are not collected within 48 hours automatically revert to Available, this guard condition prevents inventory from being locked indefinitely
- A Borrowed book becomes Overdue when the due date passes without a return, triggering the notification workflow (FR-07)
- A Lost book exits the lifecycle entirely and is removed from the catalogue

**FR Mapping:**
- FR-03 (Borrowing and Reservation) governs the Available → Reserved → Borrowed transitions
- FR-06 (Catalogue Management) governs the creation and deletion of the resource
- FR-07 (Overdue Notifications) is triggered by the Borrowed → Overdue transition

---

## 2. Loan Object

```mermaid
stateDiagram-v2
    [*] --> Active : Student borrows book (FR-03)

    Active --> DueSoon : 3 days before due date (FR-07)
    Active --> Renewed : Student renews loan before due date
    Active --> Returned : Student returns book on time

    DueSoon --> Overdue : Due date passes (FR-07)
    DueSoon --> Returned : Student returns before due date

    Renewed --> Active : Renewal confirmed (new due date set)
    Renewed --> DueSoon : New due date is within 3 days

    Overdue --> Returned : Student returns overdue book
    Overdue --> Escalated : Fine exceeds R100 (FR-03 guard condition)

    Escalated --> Returned : Student pays fine and returns book
    Returned --> Archived : Loan record archived

    Archived --> [*]
```

### Explanation

**Key States:** Active, DueSoon, Renewed, Overdue, Escalated, Returned, Archived

**Key Transitions:**
- A Loan is created Active when a student borrows a book
- The system automatically transitions the loan to DueSoon 3 days before the due date, triggering an email notification (FR-07)
- The guard condition on the Overdue → Escalated transition enforces FR-03: borrowing is blocked when fines exceed R100
- The Returned state transitions to Archived, an explicit UML terminal state, which records that the loan is complete and increments the available copy count

**FR Mapping:**
- FR-03: Controls the Active, Overdue, and Escalated states with fine-based guard conditions
- FR-07: Triggers transitions to DueSoon and Overdue states via the notification scheduler

---

## 3. User Account Object

```mermaid
stateDiagram-v2
    [*] --> Unverified : Student registers (FR-01)

    Unverified --> Active : Student verifies email (FR-01)
    Unverified --> [*] : Verification link expires (7 days)

    Active --> Locked : 5 consecutive failed logins (FR-01 / NFR-10)
    Active --> Suspended : Librarian suspends account
    Active --> Deactivated : Student requests account deletion (NFR-11)

    Locked --> Active : 15 minute lockout expires (NFR-10)
    Locked --> Active : Admin manually unlocks account

    Suspended --> Active : Admin reinstates account
    Suspended --> Deactivated : Admin permanently deactivates

    Deactivated --> [*] : Personal data erased within 30 days (NFR-11 / POPIA)
```

### Explanation

**Key States:** Unverified, Active, Locked, Suspended, Deactivated

**Key Transitions:**
- Registration creates an Unverified account; email verification moves it to Active (FR-01)
- 5 consecutive failed logins trigger a Locked state for 15 minutes, a guard condition enforcing brute-force protection (NFR-10)
- Deactivated accounts trigger POPIA-compliant data erasure within 30 days (NFR-11)

**FR Mapping:**
- FR-01 (Authentication): Governs Unverified → Active and Active → Locked transitions
- NFR-10 (Auth Security): Defines the lockout guard condition
- NFR-11 (POPIA): Governs the Deactivated → erasure lifecycle

---

## 4. Reservation Object

```mermaid
stateDiagram-v2
    [*] --> Pending : Student submits reservation (FR-03)

    Pending --> Confirmed : Book is available and reserved (FR-03)
    Pending --> Queued : Book already reserved by another student

    Confirmed --> Collected : Student collects book within 48 hours
    Confirmed --> Expired : 48 hours pass without collection (FR-03)

    Queued --> Confirmed : Earlier reservation expires or is cancelled
    Queued --> Cancelled : Student cancels while in queue

    Expired --> [*] : Next queued reservation activated automatically
    Collected --> [*] : Reservation fulfilled, Loan object created
    Cancelled --> [*] : Reservation removed from queue
```

### Explanation

**Key States:** Pending, Confirmed, Queued, Collected, Expired, Cancelled

**Key Transitions:**
- A reservation moves from Pending to Confirmed if a copy is available, or to Queued if all copies are reserved
- The guard condition on Confirmed → Expired enforces the 48-hour hold window from FR-03
- When a Confirmed reservation expires, the system automatically activates the next Queued reservation

**FR Mapping:**
- FR-03: Governs the entire reservation lifecycle including the 48-hour expiry guard

---

## 5. Notification Object

```mermaid
stateDiagram-v2
    [*] --> Scheduled : Notification trigger condition met (FR-07)

    Scheduled --> Sending : Scheduler dispatches to email service
    Sending --> Delivered : Email service confirms delivery
    Sending --> Failed : Email service returns delivery error

    Failed --> Retrying : System retries (attempt 1 of 3) (FR-07)
    Retrying --> Delivered : Retry succeeds
    Retrying --> Failed : Retry fails
    Failed --> PermanentFailure : 3 retries exhausted (FR-07)

    Delivered --> Archived : Delivery logged and archived
    PermanentFailure --> FallbackDelivered : In-app fallback notification triggered

    Archived --> [*]
    FallbackDelivered --> [*]
```

### Explanation

**Key States:** Scheduled, Sending, Delivered, Failed, Retrying, PermanentFailure, Archived, FallbackDelivered

**Key Transitions:**
- Notifications are Scheduled when a trigger condition is met (3 days before due date, on due date, 1 day after)
- Failed deliveries are automatically Retried up to 3 times (FR-07 acceptance criteria)
- After 3 failed retries, the system moves to PermanentFailure and triggers an in-app fallback, ending in FallbackDelivered
- Successfully delivered notifications end in Archived, an explicit terminal state confirming the record is logged and the lifecycle is complete

**FR Mapping:**
- FR-07: Defines all notification trigger conditions and the 3-retry guard condition

---

## 6. Recommendation Object

```mermaid
stateDiagram-v2
    [*] --> Pending : Batch job begins processing student profile (FR-05)

    Pending --> Generating : Collaborative filtering algorithm runs
    Generating --> Ready : Recommendations computed and stored (FR-05)
    Generating --> FallbackMode : Insufficient history (cold start) (FR-05)

    FallbackMode --> Ready : Course-based defaults assigned within 1 hour

    Ready --> Displayed : Student opens dashboard (FR-04)
    Displayed --> Dismissed : Student clicks Not Interested (FR-05)
    Displayed --> Actioned : Student clicks through to borrow resource

    Dismissed --> FeedbackRecorded : Negative signal logged for next batch run
    Actioned --> FeedbackRecorded : Positive signal logged for next batch run

    FeedbackRecorded --> [*]
```

### Explanation

**Key States:** Pending, Generating, Ready, FallbackMode, Displayed, Dismissed, Actioned, FeedbackRecorded

**Key Transitions:**
- The FallbackMode state handles the cold-start problem for new students with no borrowing history (FR-05 acceptance criteria)
- Both Dismissed and Actioned transitions converge on the explicit FeedbackRecorded terminal state, which confirms the student's interaction signal has been logged before the lifecycle ends
- FeedbackRecorded is the UML-compliant named final state, making it clear the object has completed its purpose rather than simply disappearing

**FR Mapping:**
- FR-05: Governs the entire recommendation lifecycle including cold-start handling
- FR-04: The Displayed state is triggered when the student's dashboard loads

---

## 7. Library Catalogue Entry Object

```mermaid
stateDiagram-v2
    [*] --> Draft : Librarian begins adding resource (FR-06)

    Draft --> Active : Librarian submits valid entry with ISBN (FR-06)
    Draft --> [*] : Librarian discards draft

    Active --> Indexing : Elasticsearch indexing job triggered
    Indexing --> Searchable : Indexed within 30 seconds (FR-06)
    Indexing --> IndexFailed : Elasticsearch indexing error

    IndexFailed --> Indexing : Automatic retry

    Searchable --> Updating : Librarian edits resource details (FR-06)
    Updating --> Searchable : Update indexed successfully

    Searchable --> PendingDeletion : Librarian requests deletion (FR-06)
    PendingDeletion --> Searchable : Active loans exist — deletion blocked (FR-06 guard)
    PendingDeletion --> [*] : No active loans — resource deleted and de-indexed
```

### Explanation

**Key States:** Draft, Active, Indexing, Searchable, IndexFailed, Updating, PendingDeletion

**Key Transitions:**
- The guard condition on PendingDeletion → Searchable enforces FR-06: deletion is blocked if active loans exist
- The Indexing state ensures resources appear in search results within 30 seconds of being added

**FR Mapping:**
- FR-06: Governs the full catalogue entry lifecycle including the deletion guard condition
- FR-02: The Searchable state enables student search functionality

---

## 8. Report Object

```mermaid
stateDiagram-v2
    [*] --> Requested : Admin or Librarian requests report (FR-08)

    Requested --> Generating : System queries reporting database
    Generating --> Ready : Report data compiled successfully (FR-08)
    Generating --> Failed : Database query timeout or error

    Failed --> Requested : Admin retries report generation
    Ready --> Displayed : Report rendered on screen

    Displayed --> Exporting : Admin clicks Export PDF or CSV (FR-08)
    Exporting --> Exported : File generated within 10 seconds (FR-08)
    Exporting --> QueuedExport : Report too large, export queued

    QueuedExport --> Exported : Background job completes, download link emailed
    Exported --> [*] : File downloaded and archived
    Displayed --> [*] : Admin closes report without exporting
```

### Explanation

**Key States:** Requested, Generating, Ready, Displayed, Exporting, Exported, QueuedExport

**Key Transitions:**
- The QueuedExport state handles large reports (more than 12 months of data) that exceed the 10-second generation limit (FR-08 alternative flow)
- The guard on Exporting → Exported enforces the 10-second export SLA

**FR Mapping:**
- FR-08: Governs the full report lifecycle including generation, display, and export
