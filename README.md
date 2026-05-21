[README_A14.md](https://github.com/user-attachments/files/28105743/README_A14.md)
# Smart Academic Library Assistance System (SALAS)

[![CI/CD Pipeline](https://github.com/211225347/Smart-Academic-Library-Assistance-System-SALAS-/actions/workflows/ci.yml/badge.svg)](https://github.com/211225347/Smart-Academic-Library-Assistance-System-SALAS-/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://python.org)

An intelligent library management platform for university students —
featuring smart search, borrowing management, personalized recommendations,
and a REST API built with FastAPI.

---

## Getting Started

### Prerequisites
- Python 3.12+
- Git

### Quick Setup

```bash
# 1. Clone the repository
git clone https://github.com/211225347/Smart-Academic-Library-Assistance-System-SALAS-.git
cd Smart-Academic-Library-Assistance-System-SALAS-

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run all tests
pytest tests/ -v
# Expected: 289 tests passing

# 5. Start the API server
uvicorn api.main:app --reload --port 8000
# Swagger UI: http://localhost:8000/docs
```

---

## Features for Contribution

Want to contribute? Here are the open features:

| Feature | Difficulty | Label | Description |
|---|---|---|---|
| Reservation API endpoints | ⭐ Beginner | `good-first-issue` | Add POST/GET/DELETE for reservations |
| Fine management API | ⭐ Beginner | `good-first-issue` | Add pay/waive fine endpoints |
| Email notifications | ⭐ Beginner | `good-first-issue` | Implement overdue email reminders |
| Admin reporting dashboard | ⭐ Beginner | `good-first-issue` | Add top-borrowed and overdue reports |
| Docker containerisation | ⭐ Beginner | `good-first-issue` | Create Dockerfile and docker-compose.yml |
| PostgreSQL backend | 🔥 Intermediate | `feature-request` | Replace in-memory storage with PostgreSQL |
| JWT authentication | 🔥 Intermediate | `feature-request` | Add token-based auth to all endpoints |
| Elasticsearch search | 🔥 Intermediate | `feature-request` | Replace keyword search with Elasticsearch |
| Redis caching | 🔥 Intermediate | `feature-request` | Cache search results and recommendations |
| Recommendation engine | 🚀 Advanced | `feature-request` | Collaborative filtering for book suggestions |

Read [CONTRIBUTING.md](./CONTRIBUTING.md) to get started.

---

## How to Run Tests

```bash
# All 289 tests
pytest tests/ -v

# Individual suites
pytest tests/test_all.py -v            # 108 domain model tests
pytest tests/test_repositories.py -v   # 87 repository tests
pytest tests/services/ -v              # 55 service tests
pytest tests/api/ -v                   # 39 API integration tests

# With coverage report
pytest tests/ --cov=src --cov=repositories \
  --cov=factories --cov=services --cov=api \
  --cov-report=term-missing
```

---

## How the CI/CD Pipeline Works

```
Push to any branch
       ↓
CI: Run 289 tests automatically
       ↓
   All pass? → PR can be reviewed and merged
   Any fail? → PR is BLOCKED
       ↓
Merged to main
       ↓
CD: Build release artifact (zip + wheel)
       ↓
GitHub Release created automatically
```

Pipeline config: [.github/workflows/ci.yml](./.github/workflows/ci.yml)

---

## API Endpoints (19 total)

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/users/register/student` | Register student |
| POST | `/api/users/register/librarian` | Register librarian |
| POST | `/api/users/login` | Login |
| GET | `/api/users` | Get all users |
| GET | `/api/users/{id}` | Get user by ID |
| PUT | `/api/users/{id}` | Update profile |
| DELETE | `/api/users/{id}` | Delete user |
| GET | `/api/resources` | Search/filter catalogue |
| POST | `/api/resources` | Add resource |
| GET | `/api/resources/{id}` | Get resource |
| GET | `/api/resources/{id}/availability` | Check availability |
| PUT | `/api/resources/{id}` | Update resource |
| DELETE | `/api/resources/{id}` | Delete resource |
| GET | `/api/loans` | All loans |
| POST | `/api/loans/checkout` | Checkout resource |
| POST | `/api/loans/{id}/return` | Return resource |
| POST | `/api/loans/{id}/renew` | Renew loan |
| GET | `/api/loans/{id}/fine` | Fine details |
| GET | `/api/students/{id}/loans` | Student loans |

Full API docs: [docs/openapi.md](./docs/openapi.md) |
Live Swagger: `http://localhost:8000/docs`

---

## Project Documents

### Assignment 3
| Document | Description |
|---|---|
| [SPECIFICATION.md](./SPECIFICATION.md) | System specification |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | C4 architecture diagrams |

### Assignment 4
| Document | Description |
|---|---|
| [STAKEHOLDERS.md](./STAKEHOLDERS.md) | Stakeholder analysis |
| [SRD.md](./SRD.md) | System requirements document |
| [REFLECTION.md](./REFLECTION.md) | Reflection |

### Assignment 5
| Document | Description |
|---|---|
| [USE_CASE_DIAGRAM.md](./USE_CASE_DIAGRAM.md) | Use case diagram |
| [USE_CASE_SPECIFICATIONS.md](./USE_CASE_SPECIFICATIONS.md) | Use case specifications |
| [TEST_CASES.md](./TEST_CASES.md) | Test cases |
| [REFLECTION5.md](./REFLECTION5.md) | Reflection |

### Assignment 6
| Document | Description |
|---|---|
| [AGILE_PLANNING.md](./AGILE_PLANNING.md) | Agile planning document |
| [REFLECTION6.md](./REFLECTION6.md) | Reflection |

### Assignment 7
| Document | Description |
|---|---|
| [template_analysis.md](./template_analysis.md) | GitHub template comparison |
| [kanban_explanation.md](./kanban_explanation.md) | Kanban board explanation |
| [reflection7.md](./reflection7.md) | Reflection |

### Assignment 8
| Document | Description |
|---|---|
| [STATE_TRANSITION_DIAGRAMS.md](./STATE_TRANSITION_DIAGRAMS.md) | State transition diagrams |
| [ACTIVITY_DIAGRAMS.md](./ACTIVITY_DIAGRAMS.md) | Activity workflow diagrams |
| [assignment8_reflection.md](./assignment8_reflection.md) | Reflection |

### Assignment 9
| Document | Description |
|---|---|
| [DOMAIN_MODEL.md](./DOMAIN_MODEL.md) | Domain model |
| [CLASS_DIAGRAM.md](./CLASS_DIAGRAM.md) | Class diagram |
| [assignment9_reflection.md](./assignment9_reflection.md) | Reflection |

### Assignment 10
| Document | Description |
|---|---|
| [src/models.py](./src/models.py) | Domain classes |
| [creational_patterns/simple_factory.py](./creational_patterns/simple_factory.py) | Simple Factory |
| [creational_patterns/factory_method.py](./creational_patterns/factory_method.py) | Factory Method |
| [creational_patterns/abstract_factory.py](./creational_patterns/abstract_factory.py) | Abstract Factory |
| [creational_patterns/builder.py](./creational_patterns/builder.py) | Builder |
| [creational_patterns/prototype.py](./creational_patterns/prototype.py) | Prototype |
| [creational_patterns/singleton.py](./creational_patterns/singleton.py) | Singleton |
| [tests/test_all.py](./tests/test_all.py) | 108 unit tests |
| [CHANGELOG.md](./CHANGELOG.md) | Version history |

### Assignment 11
| Document | Description |
|---|---|
| [repositories/base_repository.py](./repositories/base_repository.py) | Generic Repository interface |
| [repositories/interfaces.py](./repositories/interfaces.py) | Entity-specific interfaces |
| [repositories/inmemory/inmemory_repositories.py](./repositories/inmemory/inmemory_repositories.py) | In-memory implementations |
| [repositories/filesystem/filesystem_repositories.py](./repositories/filesystem/filesystem_repositories.py) | Filesystem stub |
| [factories/repository_factory.py](./factories/repository_factory.py) | Repository factory |
| [tests/test_repositories.py](./tests/test_repositories.py) | 87 repository tests |
| [assignment11_class_diagram.md](./assignment11_class_diagram.md) | Repository class diagram |

### Assignment 12
| Document | Description |
|---|---|
| [services/user_service.py](./services/user_service.py) | UserService |
| [services/resource_service.py](./services/resource_service.py) | ResourceService |
| [services/loan_service.py](./services/loan_service.py) | LoanService |
| [api/main.py](./api/main.py) | FastAPI REST API |
| [docs/openapi.md](./docs/openapi.md) | API documentation |
| [tests/services/test_services.py](./tests/services/test_services.py) | 55 service tests |
| [tests/api/test_api.py](./tests/api/test_api.py) | 39 API tests |

### Assignment 13
| Document | Description |
|---|---|
| [.github/workflows/ci.yml](./.github/workflows/ci.yml) | GitHub Actions CI/CD workflow |
| [PROTECTION.md](./PROTECTION.md) | Branch protection rules |
| [requirements.txt](./requirements.txt) | Python dependencies |
| [assignment13_reflection.md](./assignment13_reflection.md) | Reflection |

### Assignment 14
| Document | Description |
|---|---|
| [CONTRIBUTING.md](./CONTRIBUTING.md) | Contribution guidelines |
| [ROADMAP.md](./ROADMAP.md) | Future features and development roadmap |
| [LICENSE](./LICENSE) | MIT License |
| [VOTING_RESULTS.md](./VOTING_RESULTS.md) | Peer engagement results |
| [REFLECTION14.md](./REFLECTION14.md) | Reflection on open-source collaboration |

---

## Contributing

We welcome contributions! Please read [CONTRIBUTING.md](./CONTRIBUTING.md)
for setup instructions, coding standards, and how to submit a PR.

Good first issues are labelled `good-first-issue` in the
[Issues tab](https://github.com/211225347/Smart-Academic-Library-Assistance-System-SALAS-/issues).

---

## License

This project is licensed under the MIT License —
see [LICENSE](./LICENSE) for details.

---

## Author
**Phola Qwalana 211225347** | Software Engineering | May 2026
