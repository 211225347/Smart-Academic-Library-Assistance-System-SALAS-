# SPECIFICATION.md Smart Academic Library Assistance System (SALAS)

---

## 1. Project Title

**Smart Academic Library Assistance System (SALAS)**

---

## 2. Domain

**Domain:** University Library / Higher Education

University libraries are the academic backbone of any institution of higher learning. They provide students, researchers, and faculty with access to physical and digital resources including textbooks, journals, dissertations, e-books, and periodicals. Managing, discovering, and accessing these resources efficiently is critical to academic success.

Modern university libraries face challenges with fragmented catalogue systems, low discoverability of digital resources, long wait times for physical book reservations, and limited personalization. The domain spans library science, information retrieval, academic management, and student services.

---

## 3. Problem Statement

University students frequently struggle to locate academic resources efficiently. Common pain points include:

- **Poor discoverability**: Students cannot easily find relevant resources using traditional library catalogues that rely on exact title/author matching.
- **Fragmented access**: Physical catalogues, e-book platforms, journal databases, and research repositories exist as disconnected silos.
- **No personalization**: Students receive no tailored recommendations based on their course of study, borrowing history, or interests.
- **Manual reservation processes**: Requesting and tracking physical book loans is slow, opaque, and error-prone.
- **Limited student visibility**: Students lack a unified dashboard to track due dates, borrowing history, fines, or saved resources.

**SALAS** addresses these problems by providing a unified, intelligent system that integrates search, resource management, personalized recommendations, and a student self-service dashboard.

---

## 4. Individual Scope & Feasibility Justification

This project is scoped for individual development over a single semester. Its feasibility is justified as follows:

| Factor | Justification |
|---|---|
| **Modular design** | The system is composed of clearly separated services (Search, Auth, Recommendation, Dashboard, Library API), each independently buildable and testable |
| **Existing libraries** | Elasticsearch, JWT, and collaborative filtering libraries significantly reduce development complexity |
| **Focused MVP** | The semester deliverable focuses on core functionality: search, dashboard, basic recommendations, and resource management. Full ML tuning and mobile apps are post-MVP |
| **Well-understood domain** | Library systems are a well-documented domain with public datasets (e.g., Open Library API) for prototyping |
| **Solo-friendly stack** | React + Node.js + PostgreSQL is a productive full-stack combination for a solo developer |

---

## 5. Functional Requirements

### 5.1 Student Features

| ID | Requirement |
|---|---|
| FR-01 | Students must be able to register and log in securely using university credentials or email/password |
| FR-02 | Students must be able to search for books, journals, and resources using keywords, filters (author, genre, year, availability), and natural language |
| FR-03 | Students must be able to view detailed resource pages (title, author, abstract, availability, location) |
| FR-04 | Students must be able to reserve/borrow available physical books |
| FR-05 | Students must be able to view their borrowing history, active loans, and due dates on a personal dashboard |
| FR-06 | Students must be able to save resources to a personal reading list or wishlist |
| FR-07 | Students must receive personalized resource recommendations based on borrowing history and course enrollment |
| FR-08 | Students must receive email/in-app notifications for due dates, reservation confirmations, and new arrivals |

### 5.2 Librarian / Admin Features

| ID | Requirement |
|---|---|
| FR-09 | Librarians must be able to add, update, and remove library resources from the catalogue |
| FR-10 | Librarians must be able to view borrowing activity, overdue items, and generate usage reports |
| FR-11 | Admins must be able to manage student accounts and role permissions |

### 5.3 System Features

| ID | Requirement |
|---|---|
| FR-12 | The system must expose a RESTful API for integration with mobile apps and the university portal |
| FR-13 | The search engine must return results within 2 seconds for standard queries |
| FR-14 | The recommendation engine must update student recommendations at least daily |

---

## 6. Non-Functional Requirements

| ID | Category | Requirement |
|---|---|---|
| NFR-01 | Performance | Search results must be returned in under 2 seconds for up to 10,000 concurrent users |
| NFR-02 | Scalability | The system must support horizontal scaling of API and search services |
| NFR-03 | Security | All user data must be encrypted in transit (TLS) and at rest; authentication uses JWT |
| NFR-04 | Availability | The system must maintain 99.5% uptime during academic semesters |
| NFR-05 | Usability | The student dashboard must be usable with no training; key actions within 3 clicks |
| NFR-06 | Maintainability | All services must be containerized (Docker) and independently deployable |
| NFR-07 | Compatibility | The web frontend must support Chrome, Firefox, Safari, and Edge (latest 2 versions) |

---

## 7. Use Cases

### UC-01: Search for a Resource
- **Actor:** Student
- **Precondition:** Student is logged in
- **Main Flow:** Student enters a keyword → system queries Elasticsearch → returns ranked results with cover images and availability status
- **Alternative Flow:** No results found → system suggests related terms or popular resources

### UC-02: Borrow a Book
- **Actor:** Student
- **Precondition:** Book is available; student has no overdue fines exceeding limit
- **Main Flow:** Student selects book → clicks "Reserve" → system updates inventory → sends confirmation email → book is held for 48 hours

### UC-03: View Personalized Recommendations
- **Actor:** Student
- **Precondition:** Student has at least 3 borrowing/search history entries
- **Main Flow:** Student opens dashboard → Recommendation Engine returns top 10 resources → displayed as a "Recommended for You" section

### UC-04: Add Resource to Catalogue
- **Actor:** Librarian
- **Precondition:** Librarian is authenticated with LIBRARIAN role
- **Main Flow:** Librarian fills in resource form (title, author, ISBN, copies, location) → system validates → resource added to PostgreSQL and indexed in Elasticsearch

---

## 8. Constraints and Assumptions

- The system assumes a stable internet connection for students accessing digital resources.
- Physical book availability is manually updated by librarians; RFID integration is out of scope for this semester.
- The recommendation engine will use a simple collaborative filtering approach in the MVP; deep learning models are future work.
- The system will be deployed in a cloud environment (Docker on Render or AWS EC2 free tier).
- University SSO (Single Sign-On) integration is a stretch goal, not required for MVP.

---

## 9. Glossary

| Term | Definition |
|---|---|
| Resource | Any library item: book, e-book, journal, article, or research paper |
| Borrowing | The act of checking out a physical book for a defined loan period |
| Reservation | Placing a hold on an unavailable resource to be notified when returned |
| Dashboard | The student's personal home page showing loans, recommendations, and saved items |
| Recommendation Engine | A backend service that computes personalized resource suggestions |
| Library API | The RESTful backend API exposed to frontend and external integrations |
