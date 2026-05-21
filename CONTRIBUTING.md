[CONTRIBUTING.md](https://github.com/user-attachments/files/28105455/CONTRIBUTING.md)
# Contributing to SALAS
## Smart Academic Library Assistance System

Thank you for your interest in contributing to SALAS! This document
provides everything you need to get started as a contributor.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Project Structure](#project-structure)
- [Coding Standards](#coding-standards)
- [How to Pick an Issue](#how-to-pick-an-issue)
- [How to Submit a Pull Request](#how-to-submit-a-pull-request)
- [Running Tests](#running-tests)
- [Getting Help](#getting-help)

---

## Prerequisites

Before contributing, make sure you have the following installed:

| Tool | Version | How to install |
|---|---|---|
| Python | 3.12+ | https://python.org/downloads |
| Git | Latest | https://git-scm.com/downloads |
| pip | Latest | Comes with Python |

---

## Setup Instructions

### Step 1 — Fork the repository

1. Go to `https://github.com/211225347/Smart-Academic-Library-Assistance-System-SALAS-`
2. Click the **"Fork"** button (top right)
3. This creates your own copy of the repo under your GitHub account

### Step 2 — Clone your fork

```bash
git clone https://github.com/YOUR_USERNAME/Smart-Academic-Library-Assistance-System-SALAS-.git
cd Smart-Academic-Library-Assistance-System-SALAS-
```

### Step 3 — Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 4 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 5 — Verify everything works

```bash
# Run the full test suite
pytest tests/ -v

# Expected: 289 tests passing
```

### Step 6 — Start the API server

```bash
uvicorn api.main:app --reload --port 8000
# Open http://localhost:8000/docs to see the Swagger UI
```

---

## Project Structure

```
SALAS/
├── src/                        # Domain model (12 classes)
│   └── models.py
├── repositories/               # Repository layer (Assignment 11)
│   ├── base_repository.py      # Generic Repository[T, ID] interface
│   ├── interfaces.py           # Entity-specific interfaces
│   ├── inmemory/               # In-memory HashMap implementations
│   └── filesystem/             # Filesystem JSON implementations
├── factories/                  # Repository factory (storage switching)
│   └── repository_factory.py
├── services/                   # Business logic layer (Assignment 12)
│   ├── user_service.py
│   ├── resource_service.py
│   └── loan_service.py
├── api/                        # FastAPI REST API (Assignment 12)
│   └── main.py
├── creational_patterns/        # 6 design patterns (Assignment 10)
├── tests/                      # All test files
│   ├── test_all.py             # 108 domain model tests
│   ├── test_repositories.py    # 87 repository tests
│   ├── services/               # 55 service tests
│   └── api/                    # 39 API integration tests
├── docs/                       # API documentation
├── .github/workflows/          # CI/CD pipeline
│   └── ci.yml
├── requirements.txt
├── CONTRIBUTING.md             # This file
├── ROADMAP.md
└── README.md
```

---

## Coding Standards

### Python Style
- Follow **PEP 8** — 4 spaces for indentation, no tabs
- Maximum line length: **100 characters**
- Use **type hints** on all function signatures
- Use **docstrings** on all classes and public methods

### Example of good code style:

```python
def find_by_email(self, email: str) -> Optional[User]:
    """
    Find a user by email address (case-insensitive).
    Maps to FR-01 (Authentication).
    """
    email_lower = email.lower()
    for user in self._storage.values():
        if user.email.lower() == email_lower:
            return user
    return None
```

### Naming Conventions
- Classes: `PascalCase` (e.g., `UserService`, `InMemoryLoanRepository`)
- Methods and variables: `snake_case` (e.g., `find_by_id`, `student_id`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `MAX_BORROW_LIMIT = 5`)
- Private attributes: prefix with `_` (e.g., `self._storage`)

### Testing Requirements
- Every new method **must** have at least one unit test
- Every new API endpoint **must** have at least one integration test
- Tests must follow the pattern: **Arrange → Act → Assert**
- Test function names must describe what is being tested:
  - ✅ `test_checkout_blocked_when_max_loans_reached`
  - ❌ `test_checkout_2`

### Business Rules
Before implementing any borrowing or loan logic, read the business
rules in `DOMAIN_MODEL.md`. Key rules:

| Rule | Description |
|---|---|
| BR-01 | Maximum 5 active loans per student |
| BR-02 | Borrowing blocked if fines exceed R100 |
| BR-04 | Cannot delete resource with active loans |
| BR-05 | ISBN must pass check digit validation |
| BR-10 | Fine = R5/day, capped at R200 |

---

## How to Pick an Issue

1. Go to the **Issues** tab on the repository
2. Filter by label:
   - **`good-first-issue`** — Simple tasks, perfect for new contributors
   - **`feature-request`** — New features to implement
   - **`bug`** — Something is broken and needs fixing
3. Read the issue description fully before starting
4. **Comment on the issue** to let others know you are working on it:
   > "I am working on this issue. Expected completion: [date]."
5. Only pick one issue at a time

---

## How to Submit a Pull Request

### Step 1 — Create a feature branch

```bash
# Always branch from the latest main
git checkout main
git pull origin main
git checkout -b feature/your-feature-name

# Examples:
# git checkout -b feature/add-reservation-endpoint
# git checkout -b fix/loan-fine-calculation
# git checkout -b docs/update-api-documentation
```

### Step 2 — Make your changes

Write your code following the coding standards above.

### Step 3 — Write or update tests

```bash
# Run your tests to make sure they pass
pytest tests/ -v

# Check coverage
pytest tests/ --cov=src --cov=services --cov-report=term-missing
```

### Step 4 — Commit your changes

```bash
git add .
git commit -m "Close #ISSUE_NUMBER: Brief description of change"

# Examples:
# git commit -m "Close #36: Add reservation endpoint to API"
# git commit -m "Close #37: Fix fine calculation for leap years"
```

### Step 5 — Push to your fork

```bash
git push origin feature/your-feature-name
```

### Step 6 — Open a Pull Request

1. Go to your fork on GitHub
2. Click **"Compare & pull request"**
3. Fill in the PR description using this template:

```
## What does this PR do?
Brief description of the change.

## Related Issue
Closes #ISSUE_NUMBER

## Type of change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Test improvement

## Testing
- [ ] I have run pytest tests/ and all tests pass
- [ ] I have added tests for my new code
- [ ] Coverage has not decreased

## Checklist
- [ ] My code follows PEP 8 style
- [ ] I have added docstrings to new methods
- [ ] I have updated relevant documentation
```

4. Wait for the CI pipeline to run — all tests must pass ✅
5. Wait for a reviewer to approve the PR

---

## Running Tests

```bash
# All tests
pytest tests/ -v

# Specific test suite
pytest tests/test_all.py -v           # Domain model
pytest tests/test_repositories.py -v  # Repository layer
pytest tests/services/ -v             # Service layer
pytest tests/api/ -v                  # API endpoints

# With coverage
pytest tests/ --cov=src --cov=repositories \
  --cov=factories --cov=services --cov=api \
  --cov-report=term-missing
```

---

## Getting Help

- **Read the docs first:** Check `README.md`, `DOMAIN_MODEL.md`,
  and `docs/openapi.md`
- **Search existing issues:** Your question may already be answered
- **Open a new issue:** Label it `question` and describe what you
  need help with
- **Be specific:** Include error messages, file names, and line numbers

---

## Code of Conduct

- Be respectful and constructive in all communications
- Review others' PRs with kindness — suggest improvements, don't
  criticise the person
- Give credit where it is due — if you build on someone else's idea,
  mention it
- Everyone was a beginner once — welcome new contributors warmly
