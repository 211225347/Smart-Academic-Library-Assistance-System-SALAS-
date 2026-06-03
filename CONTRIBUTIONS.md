# CONTRIBUTIONS.md — Cross-Project Collaboration Summary
## Smart Academic Library Assistance System (SALAS)

> Assignment 15: Cross-Project Contributions and Collaborative Development
> This is the master submission file combining all Assignment 15 deliverables.
> Version: 1.0 | May 2026

---

## My Repository

**SALAS:** `https://github.com/211225347/Smart-Academic-Library-Assistance-System-SALAS-`

This repository was prepared for open-source collaboration in Assignment 14
with CONTRIBUTING.md, ROADMAP.md, labelled issues, and a CI/CD pipeline.
It is ready to receive contributions from peers.

---

## Contribution Plan

See full plan: [CONTRIBUTION_PLAN.md](./CONTRIBUTION_PLAN.md)

**Projects targeted for contribution:**

| Project | Repo URL | Issues selected |
|---|---|---|
| Project A | `https://github.com/[CLASSMATE_1]/[PROJECT]` | 3 issues |
| Project B | `https://github.com/[CLASSMATE_2]/[PROJECT]` | 3 issues |
| Project C | `https://github.com/[CLASSMATE_3]/[PROJECT]` | 3 issues |

**Strategy summary:** Start with documentation and test contributions
(lower risk, builds credibility), then tackle feature/bug PRs (higher
value). Comment on issues before starting to avoid duplication. Keep
PRs small and focused — one issue per PR.

---

## Pull Requests Submitted

| # | Repository | PR Link | Type | Status |
|---|---|---|---|---|
| 1 | Project A | [PR link] | Bug fix / Docs / Tests | ⏳ Pending / ✅ Merged |
| 2 | Project A | [PR link] | Bug fix / Docs / Tests | ⏳ Pending / ✅ Merged |
| 3 | Project B | [PR link] | Bug fix / Docs / Tests | ⏳ Pending / ✅ Merged |
| 4 | Project B | [PR link] | Feature | ⏳ Pending / ✅ Merged |
| 5 | Project C | [PR link] | Bug fix / Docs / Tests | ⏳ Pending / ✅ Merged |
| 6 | Project C | [PR link] | Bug fix / Docs / Tests | ⏳ Pending / ✅ Merged |

---

## Merged PRs Summary

See full details: [MERGED_PRS.md](./MERGED_PRS.md)

| PR | Project | Changes made | Merged? |
|---|---|---|---|
| PR 1 | Project A | [description] | ✅ / ⏳ |
| PR 2 | Project B | [description] | ✅ / ⏳ |
| PR 3 | Project C | [description] | ✅ / ⏳ |

---

## PRs Received on My Repository (SALAS)

| Contributor | PR Link | Changes | Status |
|---|---|---|---|
| [Classmate name] | [PR link] | [description] | Merged / Reviewed |
| [Classmate name] | [PR link] | [description] | Merged / Reviewed |

---

## Step-by-Step PR Workflow

Here is the exact workflow I followed for every contribution:

### Step 1 — Find an issue and comment
```
# Go to the peer's Issues tab
# Find a good-first-issue or help-wanted issue
# Comment: "Hi! I'd like to work on this. I'll have a PR ready by [date]."
```

### Step 2 — Fork and clone
```bash
# Fork on GitHub (click Fork button)
git clone https://github.com/MY_USERNAME/THEIR_PROJECT.git
cd THEIR_PROJECT
```

### Step 3 — Create a feature branch
```bash
git checkout -b fix/descriptive-branch-name
# Examples:
# git checkout -b fix/add-404-error-handling
# git checkout -b feat/get-users-endpoint
# git checkout -b test/add-user-service-tests
# git checkout -b docs/fix-setup-instructions
```

### Step 4 — Make changes and test
```bash
# Make your changes following their coding standards
# Run their test suite
pytest tests/ -v
# Make sure all tests pass before committing
```

### Step 5 — Commit with issue reference
```bash
git add .
git commit -m "Close #ISSUE_NUMBER: Brief description of change"
git push origin fix/descriptive-branch-name
```

### Step 6 — Open Pull Request
```
Title: Fix: Add proper 404 error handling to UserService
Body:
  ## What does this PR do?
  Adds try/except blocks to UserService methods that call the repository,
  returning HTTP 404 when a user is not found instead of a 500 error.

  ## Related Issue
  Closes #[ISSUE_NUMBER]

  ## Type of change
  - [x] Bug fix

  ## Testing
  - [x] All existing tests pass
  - [x] Added 2 new tests for the 404 scenario
  - [x] CI pipeline is green

  ## Checklist
  - [x] Code follows the project's PEP 8 style
  - [x] Docstrings added to new code
  - [x] No unrelated files changed
```

### Step 7 — Respond to review feedback
```bash
# Reviewer requests a change
git checkout fix/descriptive-branch-name
# Make the requested changes
git add .
git commit -m "Address review: [what was changed]"
git push origin fix/descriptive-branch-name
# PR updates automatically — no need to open a new one
```

---

## Reflection

See full reflection: [REFLECTION15.md](./REFLECTION15.md)

**Key lessons learned:**
- Reading CONTRIBUTING.md before touching any code saves hours of rework
- Small, focused PRs merge faster than large ones
- Commenting on issues before starting prevents duplicated effort
- CI pipelines make contributions safer — you know immediately if you
  broke something
- Responding quickly to review feedback is as important as the code itself
