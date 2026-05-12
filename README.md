[README_A13.md](https://github.com/user-attachments/files/27629665/README_A13.md)
# Smart Academic Library Assistance System (SALAS)

[![CI/CD Pipeline](https://github.com/211225347/Smart-Academic-Library-Assistance-System-SALAS-/actions/workflows/ci.yml/badge.svg)](https://github.com/211225347/Smart-Academic-Library-Assistance-System-SALAS-/actions/workflows/ci.yml)

An intelligent library platform for university students.

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
| [api/main.py](./api/main.py) | FastAPI REST API — 19 endpoints |
| [docs/openapi.md](./docs/openapi.md) | API documentation |
| [tests/services/test_services.py](./tests/services/test_services.py) | 55 service tests |
| [tests/api/test_api.py](./tests/api/test_api.py) | 39 API tests |

### Assignment 13 — CI/CD Pipeline
| Document | Description |
|---|---|
| [.github/workflows/ci.yml](./.github/workflows/ci.yml) | GitHub Actions CI/CD workflow |
| [PROTECTION.md](./PROTECTION.md) | Branch protection rules and justification |
| [requirements.txt](./requirements.txt) | Python dependencies |
| [assignment13_reflection.md](./assignment13_reflection.md) | Reflection on CI/CD implementation |

---

## CI/CD Pipeline

### How It Works

```
Push to any branch
       ↓
CI Job: Run all 289 tests
       ↓
   Tests pass?
   NO  → PR blocked, cannot merge
   YES → PR can be reviewed and merged
       ↓
Merged to main
       ↓
CD Job: Build release artifact
       ↓
GitHub Release created with zip + wheel
```

### CI Pipeline (runs on every push and PR)
- Sets up Python 3.12 on Ubuntu
- Installs all dependencies from `requirements.txt`
- Runs domain model tests (108 tests)
- Runs repository tests (87 tests)
- Runs service layer tests (55 tests)
- Runs API integration tests (39 tests)
- Generates coverage report (minimum 70% required)
- Uploads test results and coverage as artifacts

### CD Pipeline (runs only when merged to main)
- Builds a release zip containing all source packages
- Builds a Python wheel (`.whl`) artifact
- Creates a versioned GitHub Release (v1.0.X)
- Uploads both artifacts to the release

### Branch Protection Rules
- ✅ Pull request review required (1 approval)
- ✅ CI status check must pass before merge
- ✅ Direct pushes to main are blocked
- ✅ Rules apply to administrators

---

## How to Run Tests Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov=repositories --cov=factories \
  --cov=services --cov=api --cov-report=term-missing

# Run specific test suites
pytest tests/test_all.py -v           # Domain model (108 tests)
pytest tests/test_repositories.py -v  # Repository layer (87 tests)
pytest tests/services/ -v             # Service layer (55 tests)
pytest tests/api/ -v                  # API integration (39 tests)
```

**Expected result: 289 tests passing**

---

## How to Run the API

```bash
# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn api.main:app --reload --port 8000

# Open Swagger UI
# http://localhost:8000/docs

# OpenAPI JSON
# http://localhost:8000/openapi.json
```

---

## Author
**Phola Qwalana 211225347** | Software Engineering | May 2026
