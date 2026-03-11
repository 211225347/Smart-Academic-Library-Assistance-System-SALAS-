# ARCHITECTURE.md — Smart Academic Library Assistance System (SALAS)

> C4 Model Architectural Diagrams using Mermaid  
> Covers: Context → Container → Component → Code (Class Diagram)

---

## Project Title
**Smart Academic Library Assistance System (SALAS)**

## Domain
**University Library / Higher Education**

The university library domain involves students, faculty, and librarians interacting with physical and digital academic resources. The system integrates with institutional infrastructure such as email services and university portals to provide a seamless resource access experience.

## Problem Statement
Students struggle to efficiently find, borrow, and track academic resources due to fragmented, unintelligent library systems. SALAS unifies search, recommendations, borrowing, and resource management into one cohesive platform.

## Individual Scope
SALAS is decomposed into independently buildable modules (Search, Recommendation Engine, Student Dashboard, Resource Management, Library API), making it feasible for a single developer to implement incrementally over one semester.

---

## C4 Level 1 — System Context Diagram

> Shows who uses SALAS and what external systems it interacts with.

```mermaid
C4Context
    title System Context Diagram — Smart Academic Library Assistance System (SALAS)

    Person(student, "University Student", "Searches for resources, borrows books, views recommendations and manages their academic reading")
    Person(librarian, "Librarian / Admin", "Manages the library catalogue, monitors borrowing activity, and generates usage reports")

    System(salas, "SALAS", "Smart Academic Library Assistance System — provides intelligent search, personalized recommendations, borrowing management, and a student dashboard")

    System_Ext(emailService, "Email Service", "Sends notifications for due dates, reservations, and new arrivals (e.g., SendGrid / SMTP)")
    System_Ext(universityPortal, "University Portal", "External university system that links student enrollment and course data")
    System_Ext(openLibraryAPI, "Open Library API", "External API used to enrich resource metadata: cover images, abstracts, ISBNs")

    Rel(student, salas, "Searches resources, borrows books, views dashboard", "HTTPS")
    Rel(librarian, salas, "Manages catalogue, views reports", "HTTPS")
    Rel(salas, emailService, "Sends email notifications", "SMTP / REST API")
    Rel(salas, universityPortal, "Fetches student course enrollment data", "REST API")
    Rel(salas, openLibraryAPI, "Fetches book metadata and cover images", "REST API")
```

---

## C4 Level 2 — Container Diagram

> Shows the major deployable units (containers) inside SALAS and how they communicate.

```mermaid
C4Container
    title Container Diagram — Smart Academic Library Assistance System (SALAS)

    Person(student, "University Student", "Uses the web app to search, borrow, and track resources")
    Person(librarian, "Librarian", "Manages catalogue and views reports via the web app")

    System_Boundary(salas, "SALAS System Boundary") {

        Container(webApp, "Student Web App", "React.js + Tailwind CSS", "Responsive single-page application providing the student dashboard, search interface, and resource browsing")

        Container(adminApp, "Admin / Librarian Web App", "React.js", "Interface for librarians to manage catalogue inventory, view borrowing logs, and generate reports")

        Container(apiGateway, "Library REST API", "Node.js + Express.js", "Central backend API that handles authentication, search queries, borrowing logic, and resource management. Exposes endpoints for web apps and external integrations")

        Container(recommendationService, "Recommendation Engine", "Python + Flask + scikit-learn", "Microservice that computes personalized resource recommendations using collaborative filtering on student borrowing and search history")

        Container(searchEngine, "Search Service", "Elasticsearch", "Full-text search engine that indexes all library resources and returns ranked, filtered results in under 2 seconds")

        Container(database, "Primary Database", "PostgreSQL", "Stores all persistent data: users, resources, loans, reservations, reading lists, and recommendation logs")

        Container(cache, "Cache Layer", "Redis", "Caches frequent search results, session tokens, and recommendation outputs to reduce latency")
    }

    System_Ext(emailService, "Email Service (SendGrid)", "External email delivery service")
    System_Ext(openLibraryAPI, "Open Library API", "External book metadata service")

    Rel(student, webApp, "Uses", "HTTPS")
    Rel(librarian, adminApp, "Uses", "HTTPS")

    Rel(webApp, apiGateway, "API calls", "REST / JSON / HTTPS")
    Rel(adminApp, apiGateway, "API calls", "REST / JSON / HTTPS")

    Rel(apiGateway, database, "Reads and writes data", "SQL / TCP")
    Rel(apiGateway, searchEngine, "Sends search queries", "REST / HTTP")
    Rel(apiGateway, cache, "Caches sessions and results", "Redis Protocol")
    Rel(apiGateway, recommendationService, "Requests recommendations", "REST / HTTP")
    Rel(apiGateway, emailService, "Triggers email notifications", "REST API")
    Rel(apiGateway, openLibraryAPI, "Fetches book metadata", "REST API")

    Rel(recommendationService, database, "Reads borrowing and search history", "SQL / TCP")
    Rel(searchEngine, database, "Syncs resource index", "JDBC / Logstash")
```

---

## C4 Level 3 — Component Diagram (Library REST API)

> Zooms into the Library REST API container and shows its internal components.

```mermaid
C4Component
    title Component Diagram — Library REST API (Node.js / Express.js)

    Container_Boundary(api, "Library REST API") {

        Component(authController, "Auth Controller", "Express Router + JWT", "Handles student and librarian login, registration, token refresh, and logout. Issues signed JWT tokens")

        Component(searchController, "Search Controller", "Express Router", "Receives search requests from the frontend, applies filters (author, year, availability), and forwards to the Search Service")

        Component(resourceController, "Resource Controller", "Express Router", "Handles CRUD operations for library resources: create, update, delete catalogue items (librarian only)")

        Component(borrowController, "Borrow & Reservation Controller", "Express Router", "Manages book borrowing lifecycle: check availability, create loan record, update inventory, trigger due-date notifications")

        Component(dashboardController, "Student Dashboard Controller", "Express Router", "Returns consolidated dashboard data: active loans, due dates, borrowing history, saved items, and notification feed")

        Component(recommendController, "Recommendation Controller", "Express Router", "Proxies recommendation requests to the Python Recommendation Engine and returns personalized resource lists")

        Component(authMiddleware, "Auth Middleware", "JWT Verification", "Validates JWT tokens on all protected routes and attaches the authenticated user context to each request")

        Component(notificationService, "Notification Service", "Node.js Service Class", "Schedules and dispatches email notifications via the external email provider for due dates and reservation updates")

        Component(dataAccessLayer, "Data Access Layer", "Sequelize ORM", "Abstracts all SQL queries to PostgreSQL. Provides models for User, Resource, Loan, Reservation, and ReadingList")
    }

    ContainerDb(database, "PostgreSQL Database", "PostgreSQL", "Persistent storage for all entities")
    Container(searchEngine, "Elasticsearch", "Search Engine", "Full-text search index")
    Container(recommendationService, "Recommendation Engine", "Python / Flask", "ML recommendation microservice")
    System_Ext(emailService, "Email Service", "SendGrid")

    Rel(authController, dataAccessLayer, "Validates credentials, creates users")
    Rel(searchController, searchEngine, "Forwards search queries", "REST")
    Rel(resourceController, dataAccessLayer, "CRUD for resources")
    Rel(resourceController, searchEngine, "Re-indexes updated resources", "REST")
    Rel(borrowController, dataAccessLayer, "Creates/updates loan records")
    Rel(borrowController, notificationService, "Triggers due-date emails")
    Rel(dashboardController, dataAccessLayer, "Reads loans, history, saved items")
    Rel(recommendController, recommendationService, "GET /recommendations/{studentId}", "REST")
    Rel(notificationService, emailService, "Sends email via API", "REST")
    Rel(dataAccessLayer, database, "SQL queries", "TCP")
    Rel(authMiddleware, authController, "Validates tokens for protected routes")
```

---

## C4 Level 4 — Code Diagram (Resource Entity & Data Access)

> Illustrates the key classes and relationships for the Resource domain model.

```mermaid
classDiagram
    direction TB

    class User {
        +String userId
        +String name
        +String email
        +String passwordHash
        +String role
        +Date enrollmentDate
        +register()
        +login()
        +getProfile()
        +updateProfile()
    }

    class Resource {
        +String resourceId
        +String title
        +String author
        +String isbn
        +String genre
        +String domain
        +int totalCopies
        +int availableCopies
        +String location
        +Date publishedYear
        +String coverImageUrl
        +addResource()
        +updateResource()
        +deleteResource()
        +checkAvailability()
    }

    class Loan {
        +String loanId
        +String userId
        +String resourceId
        +Date borrowedDate
        +Date dueDate
        +Date returnedDate
        +String status
        +createLoan()
        +returnLoan()
        +renewLoan()
        +isOverdue()
    }

    class Reservation {
        +String reservationId
        +String userId
        +String resourceId
        +Date reservedDate
        +Date expiryDate
        +String status
        +createReservation()
        +cancelReservation()
        +fulfillReservation()
    }

    class ReadingList {
        +String listId
        +String userId
        +String listName
        +List~Resource~ savedResources
        +addResource()
        +removeResource()
        +getResources()
    }

    class RecommendationEngine {
        +String studentId
        +List~Resource~ recommendations
        +generateRecommendations()
        +updateModel()
        +getRankedResources()
    }

    class SearchService {
        +String query
        +Map filters
        +List~Resource~ results
        +search()
        +applyFilters()
        +rankResults()
        +indexResource()
    }

    class NotificationService {
        +String recipientEmail
        +String message
        +String type
        +sendDueDateReminder()
        +sendReservationConfirmation()
        +sendNewArrivalAlert()
    }

    User "1" --> "0..*" Loan : has
    User "1" --> "0..*" Reservation : places
    User "1" --> "1" ReadingList : owns
    Resource "1" --> "0..*" Loan : involved in
    Resource "1" --> "0..*" Reservation : subject of
    ReadingList "1" --> "0..*" Resource : contains
    RecommendationEngine --> User : reads history of
    RecommendationEngine --> Resource : recommends
    SearchService --> Resource : indexes and searches
    Loan --> NotificationService : triggers reminders
    Reservation --> NotificationService : triggers confirmation
```

---

## Architecture Summary

| C4 Level | Diagram | Key Insight |
|---|---|---|
| **Level 1 — Context** | System in its environment | SALAS serves students & librarians; integrates with email, university portal, and Open Library API |
| **Level 2 — Container** | Deployable services | 7 containers: React SPA, Admin SPA, REST API, Recommendation Engine, Elasticsearch, PostgreSQL, Redis |
| **Level 3 — Component** | API internals | 8 components inside the API: Auth, Search, Resource, Borrow, Dashboard, Recommendation, Notification, Data Access Layer |
| **Level 4 — Code** | Class-level design | 8 core classes covering users, resources, loans, reservations, reading lists, recommendations, search, and notifications |

The architecture follows a **microservices-lite** pattern: a central REST API handles most logic, while the computationally intensive Recommendation Engine is separated as an independent Python microservice. This maximises simplicity for solo development while enabling scalability.
