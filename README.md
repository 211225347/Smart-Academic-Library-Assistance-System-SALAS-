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

| Document | Description |
|---|---|
| [SPECIFICATION.md](./SPECIFICATION.md) | Full system specification including domain, problem statement, functional & non-functional requirements, and use cases |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | C4 architectural diagrams (Context, Container, Component, Code) modeled using Mermaid |

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
├── SPECIFICATION.md
├── ARCHITECTURE.md
├── frontend/          # React student dashboard
├── backend/           # Express REST API
├── recommendation/    # Python ML recommendation service
├── search/            # Elasticsearch integration
└── docs/              # Additional documentation
```

---

## 👤 Author

**[Your Name]**  
Software Engineering — Assignment 3  
Submitted: March 2026
