# CONTRIBUTION_PLAN.md — Cross-Project Contribution Plan
## Smart Academic Library Assistance System (SALAS)

> Assignment 15: Cross-Project Contributions and Collaborative Development
> Building on Assignment 14 | Version 1.0 | May 2026

---

## Overview

This document outlines my strategy for contributing to classmates'
repositories as part of Assignment 15. The goal is to submit at least
3 high-quality Pull Requests to peer projects, focusing on
well-scoped, achievable contributions that add real value.

---

## Projects Selected for Contribution

### Project 1 — Peer Repository A
**Repository:** `https://github.com/[CLASSMATE_1]/[THEIR_PROJECT]`
**Why selected:** Has clear CONTRIBUTING.md, labelled issues, and
active CI pipeline. The project is in a similar domain (academic
management) so my domain knowledge applies directly.

**Selected Issues:**

| Issue | Label | Type | My approach |
|---|---|---|---|
| Add input validation to registration | `good-first-issue` | Bug fix | Add email format check and password strength validation |
| Write missing unit tests for UserService | `good-first-issue` | Tests | Add tests for edge cases: empty email, duplicate username |
| Fix typo in README setup instructions | `good-first-issue` | Docs | Correct installation steps and update code examples |

**Strategy:** Start with the documentation fix (lowest risk, builds
trust with the maintainer), then move to the test contribution
(demonstrates understanding of their codebase), then tackle the
validation bug fix (highest value, touches actual business logic).

---

### Project 2 — Peer Repository B
**Repository:** `https://github.com/[CLASSMATE_2]/[THEIR_PROJECT]`
**Why selected:** Has `help-wanted` labelled issues and a clear
roadmap. The project uses Python/FastAPI which matches my skill set.

**Selected Issues:**

| Issue | Label | Type | My approach |
|---|---|---|---|
| Add error handling for 404 responses | `good-first-issue` | Bug fix | Wrap service calls with try/except and return proper HTTP 404 |
| Add GET /api/users endpoint | `feature-request` | Feature | Implement endpoint following their existing patterns |
| Update API documentation | `good-first-issue` | Docs | Add missing request/response examples to their docs/ folder |

**Strategy:** Comment on each issue before starting ("I'll work on
this!"). Begin with the 404 error handling since it is isolated and
well-scoped. The feature PR will be the most impactful but requires
understanding their codebase first — tackle it last.

---

### Project 3 — Peer Repository C
**Repository:** `https://github.com/[CLASSMATE_3]/[THEIR_PROJECT]`
**Why selected:** The CONTRIBUTING.md mentions needing test coverage
improvements. Writing tests is something I can do confidently after
writing 289 tests for SALAS.

**Selected Issues:**

| Issue | Label | Type | My approach |
|---|---|---|---|
| Increase test coverage for repository layer | `good-first-issue` | Tests | Add missing CRUD tests following their existing test patterns |
| Add requirements.txt | `good-first-issue` | Docs | Create requirements file from their import statements |
| Fix CI pipeline failing on Python 3.12 | `help-wanted` | Bug fix | Update GitHub Actions workflow to use correct Python version |

**Strategy:** Start with the requirements.txt (5 minutes, immediate
value). Fix the CI pipeline next — this unblocks the maintainer's
development workflow and will be highly appreciated. Finish with
the test coverage contribution.

---

## General Contribution Strategy

### Before Writing Any Code
1. **Read the CONTRIBUTING.md** fully before touching anything
2. **Comment on the issue** to avoid duplicate work:
   > "Hi! I'd like to work on this issue. I'll have a PR ready by [date]. Let me know if you have any preferences on the approach."
3. **Check existing PRs** — make sure nobody else is already working on it

### Writing the Code
1. **Fork first** — never clone the original repo directly
2. **Create a descriptive branch name:**
   - `fix/add-404-error-handling`
   - `feat/get-users-endpoint`
   - `docs/update-contributing-guide`
   - `test/add-user-service-tests`
3. **Match the project's code style exactly** — tabs vs spaces,
   naming conventions, docstring format
4. **Keep PRs small and focused** — one issue per PR, never bundle
   multiple unrelated changes

### PR Quality Standards
- Title follows the project's convention
- Description links to the issue: "Closes #XX"
- All existing tests pass (CI must be green ✅)
- New code has tests (if applicable)
- No unrelated files changed

### Responding to Review Feedback
- Respond within 24 hours
- Thank the reviewer for their feedback
- Ask for clarification if the feedback is unclear
- Make requested changes on the same branch (the PR updates automatically)

---

## Timeline

| Week | Activity |
|---|---|
| Week 1 | Fork all 3 repos, read CONTRIBUTINGs, comment on issues |
| Week 1–2 | Submit docs and test PRs (lower risk, faster to merge) |
| Week 2 | Submit feature/bug fix PRs (higher value, takes longer) |
| Week 2–3 | Respond to review feedback, iterate until merged |
| Week 3 | Update MERGED_PRS.md with final results |

---

## Risk Management

| Risk | Mitigation |
|---|---|
| PR not reviewed in time | Submit early, follow up politely after 3 days |
| My approach conflicts with maintainer's vision | Discuss in issue comments before coding |
| CI pipeline fails in peer's repo | Read their workflow file and test locally first |
| Issue is already taken | Comment before starting, pick a backup issue |
