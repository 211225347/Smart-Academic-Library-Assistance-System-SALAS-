[PROTECTION.md](https://github.com/user-attachments/files/27629619/PROTECTION.md)
# PROTECTION.md — Branch Protection Rules
## Smart Academic Library Assistance System (SALAS)

> Assignment 13: CI/CD with GitHub Actions
> Version: 1.0 | May 2026

---

## What Branch Protection Rules Are Applied

The `main` branch of the SALAS repository is protected with the
following rules configured under **Settings → Branches → Branch
protection rules**:

| Rule | Setting | Purpose |
|---|---|---|
| Require pull request reviews | At least 1 approval required | Ensures no unreviewed code reaches main |
| Require status checks to pass | CI workflow must pass | Blocks merges if any test fails |
| Require branches to be up to date | Enabled | PR must include latest main changes |
| Restrict direct pushes | Enabled | All changes must go through a PR |
| Include administrators | Enabled | Rules apply to everyone including repo owner |

---

## How to Set Up Branch Protection (Step-by-Step)

1. Go to your repository on GitHub
2. Click **Settings** (top menu, far right)
3. Click **Branches** (left sidebar)
4. Click **"Add branch protection rule"**
5. In **"Branch name pattern"** type: `main`
6. Enable the following checkboxes:
   - ✅ **Require a pull request before merging**
     - Set "Required number of approvals" to **1**
   - ✅ **Require status checks to pass before merging**
     - Search for and select: **"Run All Tests"** (your CI job name)
     - ✅ Require branches to be up to date before merging
   - ✅ **Do not allow bypassing the above settings**
7. Click **"Create"** (green button at the bottom)

---

## Why These Rules Matter

### 1. Require Pull Request Reviews
Every change to the `main` branch must be reviewed and approved by at
least one other developer before it can be merged. This prevents a
single developer from introducing bugs or breaking changes without a
second set of eyes. In a team project, this is the primary mechanism
for knowledge sharing and maintaining code quality standards.

For SALAS, this means that any new service method, API endpoint, or
business rule change must be reviewed against the existing requirements
(from Assignments 4–12) before it becomes part of the production
codebase.

### 2. Require Status Checks to Pass
The CI pipeline must complete successfully before a PR can be merged.
This means all 289 unit and integration tests must pass. If even one
test fails — whether in the domain model, repository layer, service
layer, or API — the merge is automatically blocked.

This directly enforces the quality standard defined in Assignment 12:
"no buggy code reaches main." Without this rule, a developer could
technically merge a PR even if the tests are failing, which defeats the
entire purpose of having automated tests.

### 3. Disable Direct Pushes to Main
Requiring all changes to go through pull requests ensures there is
always a documented record of what changed, why it changed, and who
approved it. Direct pushes bypass the review process and the CI
pipeline entirely, which means untested code could reach production.

For SALAS, this is especially important because the service layer
enforces critical business rules (BR-01: max 5 loans, BR-02: fine
threshold, BR-10: fine calculation). A direct push that breaks one of
these rules would immediately affect all student borrowing operations.

### 4. Include Administrators
By default, repository administrators can bypass branch protection
rules. Enabling "Include administrators" ensures the rules apply to
everyone equally, including the repo owner. This prevents the temptation
to bypass the process "just this once" when under deadline pressure —
which is exactly when mistakes are most likely to happen.

---

## How the CI/CD Pipeline Works With Branch Protection

```
Developer makes a change
        ↓
Creates a feature branch (e.g., feature/add-reservation-endpoint)
        ↓
Pushes to the feature branch
        ↓
CI pipeline runs automatically (all 289 tests)
        ↓
Developer opens a Pull Request to main
        ↓
CI pipeline runs again on the PR
        ↓
    Tests pass? ──── NO ──→ PR is BLOCKED — merge button is greyed out
        │
       YES
        ↓
Reviewer approves the PR
        ↓
PR is merged to main
        ↓
CD pipeline runs — builds and uploads release artifact v1.0.X
        ↓
GitHub Release created with zip and wheel artifacts
```

---

## Relationship to Prior Assignments

| Assignment | What's Protected |
|---|---|
| Assignment 10 — Domain model | `tests/test_all.py` must pass (108 tests) |
| Assignment 11 — Repository layer | `tests/test_repositories.py` must pass (87 tests) |
| Assignment 12 — Service and API | `tests/services/` and `tests/api/` must pass (94 tests) |
| All assignments — Business rules | BR-01 through BR-10 tested on every PR |

The branch protection rules ensure that the architectural integrity built
up across 12 assignments cannot be accidentally broken by a single
unreviewed commit.
