# Smart Academic Library Assistance System (SALAS)

An intelligent library platform for university students.

---

## Project Documents

### Assignment 3 — System Specification & Architecture
| Document | Description |
|---|---|
| [SPECIFICATION.md](./SPECIFICATION.md) | System specification, domain, problem statement |
| [ARCHITECTURE.md](./ARCHITECTURE.md) | C4 diagrams in Mermaid |

### Assignment 4 — Stakeholder & System Requirements
| Document | Description |
|---|---|
| [STAKEHOLDERS.md](./STAKEHOLDERS.md) | 7 stakeholders with roles, concerns, pain points |
| [SRD.md](./SRD.md) | 12 functional + 14 non-functional requirements |
| [REFLECTION.md](./REFLECTION.md) | Reflection on balancing stakeholder needs |

### Assignment 5 — Use Case Modeling & Test Cases
| Document | Description |
|---|---|
| [USE_CASE_DIAGRAM.md](./USE_CASE_DIAGRAM.md) | UML use case diagram with 7 actors and 12 use cases |
| [USE_CASE_SPECIFICATIONS.md](./USE_CASE_SPECIFICATIONS.md) | 8 detailed use case specifications |
| [TEST_CASES.md](./TEST_CASES.md) | 12 functional + 2 non-functional test cases |
| [REFLECTION5.md](./REFLECTION5.md) | Reflection on use cases and tests |

### Assignment 6 — Agile Planning
| Document | Description |
|---|---|
| [AGILE_PLANNING.md](./AGILE_PLANNING.md) | 14 user stories, MoSCoW backlog, Sprint 1 plan |
| [REFLECTION6.md](./REFLECTION6.md) | Reflection on Agile prioritization |

### Assignment 7 — Kanban Board
| Document | Description |
|---|---|
| [template_analysis.md](./template_analysis.md) | GitHub template comparison and justification |
| [kanban_explanation.md](./kanban_explanation.md) | Kanban board definition and workflow explanation |
| [reflection7.md](./reflection7.md) | Reflection on Kanban implementation |

### Assignment 8 — Dynamic Modeling
| Document | Description |
|---|---|
| [STATE_TRANSITION_DIAGRAMS.md](./STATE_TRANSITION_DIAGRAMS.md) | 8 UML state transition diagrams |
| [ACTIVITY_DIAGRAMS.md](./ACTIVITY_DIAGRAMS.md) | 8 UML activity workflow diagrams |
| [assignment8_reflection.md](./assignment8_reflection.md) | Reflection on dynamic modeling |

### Assignment 9 — Domain Modeling
| Document | Description |
|---|---|
| [DOMAIN_MODEL.md](./DOMAIN_MODEL.md) | 10 domain entities with attributes and business rules |
| [CLASS_DIAGRAM.md](./CLASS_DIAGRAM.md) | Full Mermaid class diagram |
| [assignment9_reflection.md](./assignment9_reflection.md) | Reflection on OO design |

### Assignment 10 — Implementation and Creational Patterns
| Document | Description |
|---|---|
| [src/models.py](./src/models.py) | 12 domain classes implemented in Python |
| [creational_patterns/simple_factory.py](./creational_patterns/simple_factory.py) | Simple Factory — UserFactory |
| [creational_patterns/factory_method.py](./creational_patterns/factory_method.py) | Factory Method — NotificationCreator |
| [creational_patterns/abstract_factory.py](./creational_patterns/abstract_factory.py) | Abstract Factory — Report export families |
| [creational_patterns/builder.py](./creational_patterns/builder.py) | Builder — ResourceBuilder |
| [creational_patterns/prototype.py](./creational_patterns/prototype.py) | Prototype — ResourceCache |
| [creational_patterns/singleton.py](./creational_patterns/singleton.py) | Singleton — DatabaseConnection |
| [tests/test_all.py](./tests/test_all.py) | 108 unit tests |
| [CHANGELOG.md](./CHANGELOG.md) | Version history and issue tracking |
| [assignment10_reflection.md](./assignment10_reflection.md) | Reflection on implementation |

### Assignment 11 — Repository Layer
| Document | Description |
|---|---|
| [repositories/base_repository.py](./repositories/base_repository.py) | Generic `Repository[T, ID]` — single canonical interface |
| [repositories/interfaces.py](./repositories/interfaces.py) | Entity-specific interfaces extending base |
| [repositories/inmemory/inmemory_repositories.py](./repositories/inmemory/inmemory_repositories.py) | HashMap in-memory implementations of all 8 repositories |
| [repositories/filesystem/filesystem_repositories.py](./repositories/filesystem/filesystem_repositories.py) | Filesystem JSON implementation + Database stub |
| [factories/repository_factory.py](./factories/repository_factory.py) | RepositoryFactory — switches between MEMORY/FILESYSTEM/DATABASE |
| [tests/test_repositories.py](./tests/test_repositories.py) | 87 repository unit tests |
| [assignment11_class_diagram.md](./assignment11_class_diagram.md) | Updated class diagram showing repository hierarchy |

---

## Repository Pattern Design
A generic `Repository[T, ID]` interface was introduced to encapsulate
standard CRUD operations and avoid duplication across entity repositories.
Entity-specific repositories extend this interface to preserve type safety
while maintaining a consistent persistence contract.

A **Factory Pattern** is used to abstract storage backends, allowing seamless
switching between in-memory, filesystem, and future database implementations
without impacting business logic.

## Running Tests
```bash
pip install pytest pytest-cov
pytest tests/ -v
pytest tests/ --cov=src --cov=repositories --cov=factories --cov-report=term-missing
```
**Result: 195 tests passing — 87% coverage**

## Language
**Python 3.12** — clean OOP, ABC for interfaces, dict as HashMap, pytest for tests.

## Author
**Phola Qwalana 211225347** | Software Engineering | April 2026
