# Smart Academic Library Assistance System (SALAS)

An intelligent library platform for university students.

## Project Documents

### Assignment 3 — 9 (Previous)
| Assignment | Documents |
|---|---|
| A3 | [SPECIFICATION.md](./SPECIFICATION.md), [ARCHITECTURE.md](./ARCHITECTURE.md) |
| A4 | [STAKEHOLDERS.md](./STAKEHOLDERS.md), [SRD.md](./SRD.md), [REFLECTION.md](./REFLECTION.md) |
| A5 | [USE_CASE_DIAGRAM.md](./USE_CASE_DIAGRAM.md), [USE_CASE_SPECIFICATIONS.md](./USE_CASE_SPECIFICATIONS.md), [TEST_CASES.md](./TEST_CASES.md), [REFLECTION5.md](./REFLECTION5.md) |
| A6 | [AGILE_PLANNING.md](./AGILE_PLANNING.md), [REFLECTION6.md](./REFLECTION6.md) |
| A7 | [template_analysis.md](./template_analysis.md), [kanban_explanation.md](./kanban_explanation.md), [reflection7.md](./reflection7.md) |
| A8 | [STATE_TRANSITION_DIAGRAMS.md](./STATE_TRANSITION_DIAGRAMS.md), [ACTIVITY_DIAGRAMS.md](./ACTIVITY_DIAGRAMS.md), [assignment8_reflection.md](./assignment8_reflection.md) |
| A9 | [DOMAIN_MODEL.md](./DOMAIN_MODEL.md), [CLASS_DIAGRAM.md](./CLASS_DIAGRAM.md), [assignment9_reflection.md](./assignment9_reflection.md) |

### Assignment 10 — Implementation and Creational Patterns
| File | Description |
|---|---|
| [src/models.py](./src/models.py) | 12 domain classes in Python |
| [creational_patterns/simple_factory.py](./creational_patterns/simple_factory.py) | Simple Factory |
| [creational_patterns/factory_method.py](./creational_patterns/factory_method.py) | Factory Method |
| [creational_patterns/abstract_factory.py](./creational_patterns/abstract_factory.py) | Abstract Factory |
| [creational_patterns/builder.py](./creational_patterns/builder.py) | Builder |
| [creational_patterns/prototype.py](./creational_patterns/prototype.py) | Prototype |
| [creational_patterns/singleton.py](./creational_patterns/singleton.py) | Singleton |
| [tests/test_all.py](./tests/test_all.py) | 108 unit tests |

### Assignment 11 — Repository Layer
| File | Description |
|---|---|
| [repositories/interfaces.py](./repositories/interfaces.py) | Generic `Repository[T,ID]` + 8 entity-specific interfaces |
| [repositories/inmemory/inmemory_repositories.py](./repositories/inmemory/inmemory_repositories.py) | HashMap-based implementations of all 8 repositories |
| [repositories/filesystem/filesystem_repositories.py](./repositories/filesystem/filesystem_repositories.py) | Filesystem JSON implementation + Database stub (future-proofing) |
| [factories/repository_factory.py](./factories/repository_factory.py) | RepositoryFactory — switches between MEMORY/FILESYSTEM/DATABASE backends |
| [tests/test_repositories.py](./tests/test_repositories.py) | 87 repository unit tests |
| [CHANGELOG.md](./CHANGELOG.md) | Version history and issue tracking |

## Repository Design Decisions
**Generic Interface:** `Repository[T, ID]` uses Python Generics to avoid code
duplication — all 8 entity repos share the same `save/find_by_id/find_all/delete`
contract.

**Factory over DI:** `RepositoryFactory` was chosen over a DI framework because it
provides explicit, readable backend configuration for a solo project. Switching
backends requires only changing one string: `get_resource_repo("DATABASE")`.

**In-Memory First:** All business logic is tested against in-memory repos — no
database required for unit tests. This directly satisfies NFR-07 (fast test cycles).

**Future-Proofing:** `FileSystemResourceRepository` (functional JSON) and
`DatabaseResourceRepository` (stub) show that swapping backends never changes
the service layer — it only changes the factory call.

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
