[README_A10.md](https://github.com/user-attachments/files/26971690/README_A10.md)
# Smart Academic Library Assistance System (SALAS)

An intelligent library platform for university students.

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

### Assignment 8 — Dynamic Modeling
| Document | Description |
|---|---|
| [STATE_TRANSITION_DIAGRAMS.md](./STATE_TRANSITION_DIAGRAMS.md) | 8 UML state transition diagrams |
| [ACTIVITY_DIAGRAMS.md](./ACTIVITY_DIAGRAMS.md) | 8 UML activity workflow diagrams |
| [assignment8_reflection.md](./assignment8_reflection.md) | Reflection |

### Assignment 9 — Domain Modeling
| Document | Description |
|---|---|
| [DOMAIN_MODEL.md](./DOMAIN_MODEL.md) | Domain entities, attributes, business rules |
| [CLASS_DIAGRAM.md](./CLASS_DIAGRAM.md) | Mermaid.js class diagram |
| [assignment9_reflection.md](./assignment9_reflection.md) | Reflection |

### Assignment 10 — Implementation and Creational Patterns
| Document | Description |
|---|---|
| [src/models.py](./src/models.py) | All 12 domain classes implemented in Python |
| [creational_patterns/simple_factory.py](./creational_patterns/simple_factory.py) | Simple Factory — UserFactory for Student/Librarian creation |
| [creational_patterns/factory_method.py](./creational_patterns/factory_method.py) | Factory Method — NotificationCreator subclasses |
| [creational_patterns/abstract_factory.py](./creational_patterns/abstract_factory.py) | Abstract Factory — CSV and PDF report export families |
| [creational_patterns/builder.py](./creational_patterns/builder.py) | Builder — ResourceBuilder with chained optional configuration |
| [creational_patterns/prototype.py](./creational_patterns/prototype.py) | Prototype — ResourceCache with deep-clone templates |
| [creational_patterns/singleton.py](./creational_patterns/singleton.py) | Singleton — Thread-safe DatabaseConnection |
| [tests/test_all.py](./tests/test_all.py) | 108 unit tests — 84% coverage |
| [CHANGELOG.md](./CHANGELOG.md) | Version history and bug tracking |
| [assignment10_reflection.md](./assignment10_reflection.md) | Reflection on implementation and patterns |

## Language Choice
**Python 3.12** was chosen for the following reasons:
- Clean, readable syntax that maps directly to UML class diagrams
- First-class support for OOP: inheritance, composition, encapsulation
- `pytest` provides an expressive, zero-boilerplate testing framework
- `pytest-cov` generates coverage reports with minimal configuration
- No compilation step — fast iteration during development

## Creational Pattern Justifications
| Pattern | Applied To | Reason |
|---|---|---|
| Simple Factory | `UserFactory` | Centralises Student/Librarian creation from role string (FR-01) |
| Factory Method | `NotificationCreator` | Each event type (DueSoon, Overdue) needs a dedicated creator (FR-07) |
| Abstract Factory | `ReportExportFactory` | CSV and PDF exports require consistent formatter+renderer families (FR-08) |
| Builder | `ResourceBuilder` | Resources have 8+ fields; Builder makes optional config readable (FR-06) |
| Prototype | `ResourceCache` | Bulk import clones pre-configured templates instead of rebuilding (US-014) |
| Singleton | `DatabaseConnection` | Only one connection pool must exist across 1,000 concurrent users (NFR-07) |

## Running Tests
```bash
pip install pytest pytest-cov
pytest tests/test_all.py -v
pytest tests/test_all.py --cov=src --cov=creational_patterns --cov-report=term-missing
```

## Author
**Phola Qwalana 211225347** | Software Engineering | April 2026
