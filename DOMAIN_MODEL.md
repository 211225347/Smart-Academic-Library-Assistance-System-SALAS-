# DOMAIN_MODEL.md — Domain Model
## Smart Academic Library Assistance System (SALAS)

> Assignment 9: Domain Modeling and Class Diagram Development
> Building on Assignments 3–8 |26 April 2026

---

## 1. Overview

The SALAS domain model represents the core entities, their attributes, responsibilities,
and relationships that form the business logic of the Smart Academic Library Assistance
System. These entities were derived from the functional requirements in Assignment 4,
the use cases in Assignment 5, the user stories in Assignment 6, and the state/activity
diagrams in Assignment 8.

---

## 2. Domain Entities

### Entity 1: User

| Property | Detail |
|---|---|
| **Description** | Represents any person with an account in the system. Specialised into Student and Librarian via inheritance. |
| **Attributes** | `userId: String`, `name: String`, `email: String`, `passwordHash: String`, `role: Enum (STUDENT, LIBRARIAN, ADMIN)`, `accountStatus: Enum (ACTIVE, LOCKED, SUSPENDED, DEACTIVATED)`, `createdAt: Date` |
| **Methods** | `register()`, `login()`, `logout()`, `updateProfile()`, `deactivateAccount()` |
| **Relationships** | A User (Student) has zero or many Loans. A User (Student) has zero or many Reservations. A User (Student) owns one ReadingList. A User (Librarian) manages many Resources. |

---

### Entity 2: Student *(extends User)*

| Property | Detail |
|---|---|
| **Description** | A university-enrolled user who searches for, borrows, and reserves library resources. Inherits all User attributes and methods. |
| **Attributes** | `studentNumber: String`, `courseEnrollment: List<String>`, `outstandingFines: Double`, `borrowingCount: Integer` |
| **Methods** | `searchCatalogue()`, `borrowResource()`, `reserveResource()`, `viewDashboard()`, `getDismissRecommendation()` |
| **Relationships** | Inherits from User. Associated with Loan, Reservation, ReadingList, and Recommendation. |

---

### Entity 3: Librarian *(extends User)*

| Property | Detail |
|---|---|
| **Description** | A library staff member who manages the catalogue, processes returns, and monitors borrowing activity. |
| **Attributes** | `staffId: String`, `department: String` |
| **Methods** | `addResource()`, `editResource()`, `deleteResource()`, `processReturn()`, `generateReport()`, `bulkImportCSV()` |
| **Relationships** | Inherits from User. Manages many Resources. Generates many Reports. |

---

### Entity 4: Resource *(Book/Journal/Article)*

| Property | Detail |
|---|---|
| **Description** | Any physical or digital academic material catalogued in the library system. |
| **Attributes** | `resourceId: String`, `title: String`, `author: String`, `isbn: String`, `genre: String`, `publishedYear: Integer`, `totalCopies: Integer`, `availableCopies: Integer`, `location: String`, `coverImageUrl: String`, `resourceStatus: Enum (AVAILABLE, BORROWED, RESERVED, UNDER_MAINTENANCE, LOST)` |
| **Methods** | `checkAvailability()`, `checkOut()`, `returnResource()`, `reserve()`, `validateISBN()`, `updateIndexInElasticsearch()` |
| **Relationships** | A Resource is involved in zero or many Loans. A Resource is subject to zero or many Reservations. A Resource belongs to one Catalogue. |

---

### Entity 5: Loan

| Property | Detail |
|---|---|
| **Description** | Records the borrowing transaction between a Student and a Resource. Tracks due dates and overdue status. |
| **Attributes** | `loanId: String`, `borrowedDate: Date`, `dueDate: Date`, `returnedDate: Date`, `status: Enum (ACTIVE, DUE_SOON, OVERDUE, RETURNED, ARCHIVED)`, `renewalCount: Integer` |
| **Methods** | `createLoan()`, `returnLoan()`, `renewLoan()`, `isOverdue()`, `calculateFine()`, `archiveLoan()` |
| **Relationships** | A Loan belongs to exactly one Student. A Loan is associated with exactly one Resource. A Loan generates zero or one Fine. |

---

### Entity 6: Reservation

| Property | Detail |
|---|---|
| **Description** | Records a student's request to hold a Resource that is currently unavailable. |
| **Attributes** | `reservationId: String`, `reservedDate: Date`, `expiryDate: Date`, `queuePosition: Integer`, `status: Enum (PENDING, CONFIRMED, QUEUED, COLLECTED, EXPIRED, CANCELLED)` |
| **Methods** | `createReservation()`, `cancelReservation()`, `fulfillReservation()`, `expireReservation()`, `activateNextInQueue()` |
| **Relationships** | A Reservation belongs to exactly one Student. A Reservation is for exactly one Resource. |

---

### Entity 7: Fine

| Property | Detail |
|---|---|
| **Description** | A financial penalty generated when a Loan becomes overdue. Blocks further borrowing when it exceeds R100. |
| **Attributes** | `fineId: String`, `amount: Double`, `issuedDate: Date`, `paidDate: Date`, `status: Enum (PENDING, PAID, WAIVED)` |
| **Methods** | `calculateAmount()`, `payFine()`, `waiveFine()`, `isBorrowingBlocked()` |
| **Relationships** | A Fine belongs to exactly one Loan. A Fine is associated with one Student. |

---

### Entity 8: ReadingList

| Property | Detail |
|---|---|
| **Description** | A personal collection of saved Resources maintained by a Student. Supports custom named collections. |
| **Attributes** | `listId: String`, `listName: String`, `createdDate: Date`, `isShared: Boolean`, `shareableLink: String` |
| **Methods** | `addResource()`, `removeResource()`, `reorderResources()`, `exportBibliography()`, `generateShareLink()` |
| **Relationships** | A ReadingList is owned by exactly one Student (composition). A ReadingList contains zero or many Resources. |

---

### Entity 9: Recommendation

| Property | Detail |
|---|---|
| **Description** | A personalised resource suggestion generated by the Recommendation Engine for a specific Student based on borrowing history and course enrollment. |
| **Attributes** | `recommendationId: String`, `generatedDate: Date`, `status: Enum (PENDING, READY, DISPLAYED, DISMISSED, ACTIONED)`, `score: Double`, `isColdStart: Boolean` |
| **Methods** | `generate()`, `display()`, `dismiss()`, `recordFeedback()`, `updateModel()` |
| **Relationships** | A Recommendation belongs to one Student. A Recommendation references one Resource. |

---

### Entity 10: Notification

| Property | Detail |
|---|---|
| **Description** | An automated email or in-app alert sent to a Student or Librarian triggered by system events (due date approaching, overdue, reservation ready). |
| **Attributes** | `notificationId: String`, `type: Enum (DUE_SOON, OVERDUE, RESERVATION_CONFIRMED, NEW_ARRIVAL)`, `sentDate: Date`, `status: Enum (SCHEDULED, DELIVERED, FAILED, ARCHIVED)`, `retryCount: Integer`, `channel: Enum (EMAIL, IN_APP)` |
| **Methods** | `schedule()`, `send()`, `retry()`, `archive()`, `triggerFallback()` |
| **Relationships** | A Notification is sent to one User. A Notification is triggered by one Loan or one Reservation. |

---

## 3. Business Rules

| Rule ID | Business Rule | Enforced By |
|---|---|---|
| BR-01 | A student may have a maximum of 5 active loans at any time | `Loan.createLoan()` guard |
| BR-02 | Borrowing is blocked if outstanding fines exceed R100 | `Fine.isBorrowingBlocked()` |
| BR-03 | A reservation hold expires automatically after 48 hours | `Reservation.expireReservation()` |
| BR-04 | A resource cannot be deleted from the catalogue if it has active loans | `Resource.delete()` guard |
| BR-05 | ISBN must pass ISBN-10 or ISBN-13 check digit validation before a resource is saved | `Resource.validateISBN()` |
| BR-06 | A student account is locked for 15 minutes after 5 consecutive failed login attempts | `User.login()` guard |
| BR-07 | All personal data must be erased within 30 days of account deactivation | `User.deactivateAccount()` |
| BR-08 | New students receive course-based recommendations within 1 hour of registration if no borrowing history exists | `Recommendation.generate()` cold-start logic |
| BR-09 | A loan renewal is only permitted if no other student has a reservation for the same resource | `Loan.renewLoan()` guard |
| BR-10 | Overdue fine = R5 per day beyond the due date, capped at R200 | `Fine.calculateAmount()` |

---

## 4. Entity Relationship Summary

| Relationship | Type | Multiplicity |
|---|---|---|
| Student borrows Resource | Association via Loan | Student 1 — 0..* Loan; Loan 1 — 1 Resource |
| Student places Reservation | Association | Student 1 — 0..* Reservation |
| Student owns ReadingList | Composition | Student 1 — 1 ReadingList |
| ReadingList contains Resource | Association | ReadingList 1 — 0..* Resource |
| Loan generates Fine | Association | Loan 1 — 0..1 Fine |
| Student receives Recommendation | Association | Student 1 — 0..* Recommendation |
| Recommendation references Resource | Association | Recommendation 0..* — 1 Resource |
| Notification triggered by Loan | Dependency | Notification 0..* — 1 Loan |
| Librarian manages Resource | Association | Librarian 1 — 0..* Resource |
| Student is-a User | Inheritance | Student extends User |
| Librarian is-a User | Inheritance | Librarian extends User |
