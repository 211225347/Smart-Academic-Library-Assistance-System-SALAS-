# ARCHITECTURE.md Smart Academic Library Assistance System (SALAS)

> C4 Model Architectural Diagrams using GitHub-compatible Mermaid syntax  
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

## C4 Level 1: System Context Diagram

> Shows who uses SALAS and what external systems it interacts with.

```mermaid
flowchart TD
    student(["👤 University Student\n─────────────────\nSearches resources, borrows\nbooks, views recommendations\nand manages reading lists"])
    librarian(["👤 Librarian / Admin\n─────────────────\nManages catalogue, monitors\nborrowing activity, generates\nusage reports"])

    salas["🏛️ SALAS\n─────────────────\nSmart Academic Library\nAssistance System\n─────────────────\nProvides intelligent search,\npersonalized recommendations,\nborrowing management, and\na student dashboard"]

    email["📧 Email Service\n─────────────────\nSends notifications for\ndue dates, reservations,\nand new arrivals\n(SendGrid / SMTP)"]
    portal["🏫 University Portal\n─────────────────\nExternal university system\nthat provides student\nenrollment and course data"]
    openlib["📖 Open Library API\n─────────────────\nExternal API that provides\nbook metadata, cover images,\nand ISBN data"]

    student -- "Searches, borrows, views dashboard [HTTPS]" --> salas
    librarian -- "Manages catalogue, views reports [HTTPS]" --> salas
    salas -- "Sends email notifications [SMTP / REST]" --> email
    salas -- "Fetches student course data [REST API]" --> portal
    salas -- "Fetches book metadata [REST API]" --> openlib

    style salas fill:#1168BD,color:#fff,stroke:#0b4884
    style student fill:#08427B,color:#fff,stroke:#052e56
    style librarian fill:#08427B,color:#fff,stroke:#052e56
    style email fill:#666,color:#fff,stroke:#444
    style portal fill:#666,color:#fff,stroke:#444
    style openlib fill:#666,color:#fff,stroke:#444
```

---

## C4 Level 2: Container Diagram

> Shows the major deployable containers inside SALAS and how they communicate.

```mermaid
flowchart TD
    student(["👤 University Student"])
    librarian(["👤 Librarian / Admin"])

    subgraph salas["SALAS — System Boundary"]
        webApp["🖥️ Student Web App\n─────────────────\nReact.js + Tailwind CSS\n─────────────────\nResponsive SPA providing\nsearch, dashboard, and\nresource browsing"]

        adminApp["🖥️ Admin Web App\n─────────────────\nReact.js\n─────────────────\nInterface for librarians\nto manage catalogue and\nview usage reports"]

        apiGateway["⚙️ Library REST API\n─────────────────\nNode.js + Express.js\n─────────────────\nCentral backend handling auth,\nsearch, borrowing, resource\nmanagement, and notifications"]

        recommendEngine["🤖 Recommendation Engine\n─────────────────\nPython + Flask + scikit-learn\n─────────────────\nComputes personalized resource\nrecommendations using\ncollaborative filtering"]

        searchEngine["🔍 Search Service\n─────────────────\nElasticsearch\n─────────────────\nFull-text search index for\nall library resources"]

        database[("🗄️ Primary Database\n─────────────────\nPostgreSQL\n─────────────────\nStores users, resources,\nloans, reservations,\nand reading lists")]

        cache[("⚡ Cache Layer\n─────────────────\nRedis\n─────────────────\nCaches search results,\nsession tokens, and\nrecommendation outputs")]
    end

    email["📧 Email Service\n(SendGrid)"]
    openlib["📖 Open Library API"]

    student -- "HTTPS" --> webApp
    librarian -- "HTTPS" --> adminApp
    webApp -- "REST/JSON" --> apiGateway
    adminApp -- "REST/JSON" --> apiGateway
    apiGateway -- "SQL/TCP" --> database
    apiGateway -- "REST/HTTP" --> searchEngine
    apiGateway -- "Redis Protocol" --> cache
    apiGateway -- "REST/HTTP" --> recommendEngine
    apiGateway -- "REST API" --> email
    apiGateway -- "REST API" --> openlib
    recommendEngine -- "SQL/TCP" --> database
    searchEngine -- "Logstash Sync" --> database

    style webApp fill:#438DD5,color:#fff,stroke:#2b6cb0
    style adminApp fill:#438DD5,color:#fff,stroke:#2b6cb0
    style apiGateway fill:#438DD5,color:#fff,stroke:#2b6cb0
    style recommendEngine fill:#438DD5,color:#fff,stroke:#2b6cb0
    style searchEngine fill:#438DD5,color:#fff,stroke:#2b6cb0
    style database fill:#438DD5,color:#fff,stroke:#2b6cb0
    style cache fill:#438DD5,color:#fff,stroke:#2b6cb0
    style student fill:#08427B,color:#fff,stroke:#052e56
    style librarian fill:#08427B,color:#fff,stroke:#052e56
    style email fill:#666,color:#fff,stroke:#444
    style openlib fill:#666,color:#fff,stroke:#444
```

---

## C4 Level 3: Component Diagram (Library REST API)

> Zooms into the Library REST API container and shows its internal components.

```mermaid
flowchart TD
    webApp(["🖥️ Student Web App"])
    adminApp(["🖥️ Admin Web App"])

    subgraph api["Library REST API — Node.js / Express.js"]
        authMiddleware["🔒 Auth Middleware\n─────────────────\nJWT Verification\n─────────────────\nValidates tokens on all\nprotected routes"]

        authController["🔑 Auth Controller\n─────────────────\nExpress Router + JWT\n─────────────────\nHandles login, registration,\ntoken refresh and logout"]

        searchController["🔍 Search Controller\n─────────────────\nExpress Router\n─────────────────\nReceives queries, applies\nfilters, forwards to\nElasticsearch"]

        resourceController["📚 Resource Controller\n─────────────────\nExpress Router\n─────────────────\nCRUD operations for\ncatalogue items\n(librarian only)"]

        borrowController["📋 Borrow Controller\n─────────────────\nExpress Router\n─────────────────\nManages loan lifecycle:\ncheck, create, update\ninventory"]

        dashboardController["📊 Dashboard Controller\n─────────────────\nExpress Router\n─────────────────\nReturns loans, due dates,\nhistory, saved items\nfor student view"]

        recommendController["🤖 Recommendation Controller\n─────────────────\nExpress Router\n─────────────────\nProxies requests to\nPython Recommendation\nEngine"]

        notificationService["📧 Notification Service\n─────────────────\nNode.js Service\n─────────────────\nSchedules and sends\nemail notifications\nfor due dates"]

        dal["🗃️ Data Access Layer\n─────────────────\nSequelize ORM\n─────────────────\nAbstracts all SQL queries\nModels: User, Resource,\nLoan, Reservation"]
    end

    db[("🗄️ PostgreSQL")]
    es["🔍 Elasticsearch"]
    rec["🤖 Recommendation Engine"]
    emailSvc["📧 Email Service"]

    webApp --> authMiddleware
    adminApp --> authMiddleware
    authMiddleware --> authController
    authMiddleware --> searchController
    authMiddleware --> resourceController
    authMiddleware --> borrowController
    authMiddleware --> dashboardController
    authMiddleware --> recommendController

    authController --> dal
    searchController --> es
    resourceController --> dal
    resourceController --> es
    borrowController --> dal
    borrowController --> notificationService
    dashboardController --> dal
    recommendController --> rec
    notificationService --> emailSvc
    dal --> db

    style authMiddleware fill:#85BBF0,color:#000,stroke:#5a9fd4
    style authController fill:#438DD5,color:#fff,stroke:#2b6cb0
    style searchController fill:#438DD5,color:#fff,stroke:#2b6cb0
    style resourceController fill:#438DD5,color:#fff,stroke:#2b6cb0
    style borrowController fill:#438DD5,color:#fff,stroke:#2b6cb0
    style dashboardController fill:#438DD5,color:#fff,stroke:#2b6cb0
    style recommendController fill:#438DD5,color:#fff,stroke:#2b6cb0
    style notificationService fill:#438DD5,color:#fff,stroke:#2b6cb0
    style dal fill:#438DD5,color:#fff,stroke:#2b6cb0
    style db fill:#1168BD,color:#fff,stroke:#0b4884
    style es fill:#1168BD,color:#fff,stroke:#0b4884
    style rec fill:#1168BD,color:#fff,stroke:#0b4884
    style emailSvc fill:#666,color:#fff,stroke:#444
```

---

## C4 Level 4: Code Diagram (Class Diagram)

> Illustrates the key classes and relationships for the core domain model.

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
| **Level 1: Context** | System in its environment | SALAS serves students and librarians; integrates with email, university portal, and Open Library API |
| **Level 2: Container** | Deployable services | 7 containers: React SPA, Admin SPA, REST API, Recommendation Engine, Elasticsearch, PostgreSQL, Redis |
| **Level 3: Component** | API internals | 8 components inside the API: Auth Middleware, Auth, Search, Resource, Borrow, Dashboard, Recommendation, Notification, and Data Access Layer |
| **Level 4: Code** | Class-level design | 8 core classes covering users, resources, loans, reservations, reading lists, recommendations, search, and notifications |

The architecture follows a **microservices-lite** pattern: a central REST API handles most logic, while the computationally intensive Recommendation Engine is separated as an independent Python microservice. This maximises simplicity for solo development while enabling scalability.
