[README_A5_updated.md](https://github.com/user-attachments/files/26273303/README_A5_updated.md)
# 📚 Smart Academic Library Assistance System (SALAS)

> An intelligent, AI-powered academic library platform designed to help university students efficiently discover, access, and manage academic resources — books, journals, research papers, and more.

## Overview

University students often waste valuable time searching through outdated library catalogues and disconnected resource systems. **SALAS** solves this by unifying the library experience into a single smart platform with personalized recommendations, real-time search, and a student-friendly dashboard.

Once completed, this system will allow students to:
- Search the full library catalogue using natural language and filters
- Receive personalized book and resource recommendations
- Manage borrowing, reservations, and reading history via a personal dashboard
- Access the system through a REST API (for integration with mobile apps and university portals)
- Enable librarians to manage inventory and monitor usage analytics

---

## 📄 Project Documents

### Assignment 3 — System Specification & Architecture

| Document | Description |
|---|---|
| [SPECIFICATION.md](./SPECIFICATION.md) | Full system specification including domain, problem statement, functional & non-functional requirements, and use cases |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | C4 architectural diagrams (Context, Container, Component, Code) modeled using Mermaid |

### Assignment 4 — Stakeholder & System Requirements

| Document | Description |
|---|---|
| [STAKEHOLDERS.md](./STAKEHOLDERS.md) | Detailed stakeholder analysis: roles, key concerns, pain points, and success metrics for 7 stakeholders |
| [SRD.md](./SRD.md) | System Requirements Document — 12 functional requirements with acceptance criteria + 14 non-functional requirements across 6 quality categories |
| [REFLECTION.md](./REFLECTION.md) | Reflection on challenges faced in balancing competing stakeholder needs during requirements elicitation |

### Assignment 5 — Use Case Modeling & Test Case Development

| Document | Description |
|---|---|
| [USE_CASE_DIAGRAM.md](./USE_CASE_DIAGRAM.md) | UML use case diagram (Mermaid) with 7 actors and 12+ use cases, plus written explanation of relationships and stakeholder alignment |
| [USE_CASE_SPECIFICATIONS.md](./USE_CASE_SPECIFICATIONS.md) | Detailed specifications for 8 critical use cases: preconditions, postconditions, basic flows, and alternative flows |
| [TEST_CASES.md](./TEST_CASES.md) | 12 functional test cases + 2 non-functional test cases (performance and security) in full table format |
| [REFLECTION5.md](./REFLECTION5.md) | Reflection on challenges in translating requirements into use cases and test cases |

---

## 🛠️ Planned Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React.js + Tailwind CSS |
| Backend API | Node.js + Express.js |
| Database | PostgreSQL |
| Search Engine | Elasticsearch |
| Recommendation Engine | Python (scikit-learn / collaborative filtering) |
| Authentication | JWT + OAuth 2.0 |
| Deployment | Docker + AWS / Render |

---

## 📁 Repository Structure (Planned)

```
smart-academic-library/
├── README.md
├── SPECIFICATION.md              # Assignment 3
├── ARCHITECTURE.md               # Assignment 3
├── STAKEHOLDERS.md               # Assignment 4
├── SRD.md                        # Assignment 4
├── REFLECTION.md                 # Assignment 4
├── USE_CASE_DIAGRAM.md           # Assignment 5
├── USE_CASE_SPECIFICATIONS.md    # Assignment 5
├── TEST_CASES.md                 # Assignment 5
├── REFLECTION5.md                # Assignment 5
├── frontend/                     # React student dashboard
├── backend/                      # Express REST API
├── recommendation/               # Python ML recommendation service
├── search/                       # Elasticsearch integration
└── docs/                         # Additional documentation
```

---

## 👤 Author

**Phola Qwalana 211225347**  
Software Engineering — Assignments 3, 4 & 5  
Submitted: March 2026
