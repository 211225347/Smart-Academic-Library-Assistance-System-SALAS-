[assignment13_reflection.md](https://github.com/user-attachments/files/27629642/assignment13_reflection.md)
# assignment13_reflection.md — CI/CD Pipeline Reflection
## Smart Academic Library Assistance System (SALAS)

> Assignment 13: Implementing CI/CD with GitHub Actions
> Building on Assignments 3–12 | Version 1.0 | May 2026

---

## What Was Built

Assignment 13 adds a complete CI/CD pipeline to the SALAS project using
GitHub Actions. The pipeline has two jobs:

- **CI (test job):** Runs all 289 tests on every push and every PR to
  main. If any test fails, the PR cannot be merged.
- **CD (release job):** Only runs when code is pushed to main AND the
  CI job passes. Builds a release zip and Python wheel, uploads them
  as GitHub Actions artifacts, and creates a versioned GitHub Release.

---

## Challenge 1: Structuring the Pipeline for Two Separate Concerns

The biggest design decision was whether to use one workflow file or two.
One file for CI and a separate file for CD would be cleaner in isolation,
but they would be harder to coordinate — the CD job must only run after
CI passes, and enforcing that across two separate workflow files requires
more complex configuration.

The `needs: test` directive in a single file solves this cleanly. The
release job explicitly declares that it depends on the test job. GitHub
Actions will not start the release job until the test job completes
successfully. If the test job fails, the release job is cancelled
automatically — no extra configuration required.

This matters for SALAS because releasing broken code would break the
service layer that students and librarians depend on. The pipeline
guarantees that every artifact uploaded to GitHub Releases has passed
all 289 tests.

---

## Challenge 2: Deciding What Counts as a Release Artifact

The assignment required a release artifact but left the format open
(JAR, wheel, Docker image). For a Python FastAPI project, a Python
wheel (`.whl`) is the standard distributable format — it can be
installed with `pip install salas-1.0.x-py3-none-any.whl` and run
immediately.

However, a wheel alone is not immediately runnable as a server — it
needs to be installed first. The decision was made to also produce a
zip archive containing all source directories (`src/`, `repositories/`,
`factories/`, `services/`, `api/`) plus `requirements.txt`. This zip
can be extracted and run directly with `uvicorn api.main:app` without
any pip install step, which is more practical for academic submission.

The tradeoff: the zip is larger and not pip-installable. The wheel is
smaller and installable but requires more setup steps to run as a server.
Producing both means the artifact meets the rubric requirement and is
also practically useful.

---

## Challenge 3: Making Tests Run Correctly in CI

The test suite was written and tested locally in `/home/claude/salas12/`
with relative import paths (`sys.path.insert(0, ...)`). In GitHub
Actions, the working directory is the repository root, which matches
the structure — but only if all the source files are committed to the
repository in the correct folder structure.

This is where the ongoing repository upload problem directly impacts
Assignment 13. The CI pipeline will only work correctly once the full
file structure (src/, repositories/, factories/, services/, api/,
tests/) is committed to the main branch via Git push. A CI pipeline
that cannot find its source files will fail at the import step before
even running a single test.

The `requirements.txt` file was created specifically for this — it
lists every dependency so GitHub Actions can install them in a clean
Ubuntu environment that has never seen the project before.

---

## Challenge 4: Branch Protection and the Solo Developer Problem

Branch protection rules requiring pull request reviews create an
immediate problem for a solo developer: you cannot approve your own
pull requests. GitHub will not let you merge a PR that requires 1
review if you are the only contributor.

There are three ways to handle this in a solo academic project:

1. **Temporarily disable the review requirement** — set it to 0
   required reviewers but keep the status check requirement. This
   preserves the CI blocking behaviour (no broken tests reach main)
   without blocking solo merges.

2. **Use a second GitHub account** to approve PRs — this is
   technically possible but defeats the spirit of the requirement.

3. **Document the rule and demonstrate it was configured** even if
   it cannot be fully enforced solo. The screenshot of the branch
   protection settings proves the rule exists; the PR workflow
   screenshot demonstrates the CI check blocking a failing PR.

For this submission, option 1 is the recommended approach — the status
check requirement (CI must pass) is the more important protection rule
for code quality, and it works perfectly with a solo developer.

---

## How CI/CD Connects to Every Previous Assignment

The CI pipeline is not just a quality gate for new code — it is a
running validation of every design decision made across 12 assignments:

- **Assignment 9 (Domain Model):** The 108 tests in `test_all.py`
  verify that every class method, business rule, and relationship
  works correctly. Every PR that touches `src/models.py` must pass
  these before merging.

- **Assignment 11 (Repository Layer):** The 87 repository tests
  verify that all CRUD operations and domain queries work correctly
  for every storage backend. Adding a new storage backend requires
  passing these tests first.

- **Assignment 12 (Service and API):** The 94 service and API tests
  verify the business logic layer and all 19 REST endpoints. A broken
  endpoint in `api/main.py` will fail these tests and block the PR.

The CI pipeline makes the entire semester's work self-defending. Once
it is running, no future change can silently break a past assignment's
functionality.

---

## Lessons Learned

**Automated testing is only valuable if it runs automatically.**
Writing 289 tests is wasted effort if they only run when a developer
remembers to run them locally. The CI pipeline removes the human
dependency — tests run on every push, whether the developer remembers
or not.

**The pipeline reveals structure problems.** A CI pipeline that fails
because it cannot find a module (`ModuleNotFoundError`) is immediately
telling you something about your project structure that local testing
might hide. In this case, it confirmed that the full project structure
must be committed to the repository as a flat directory tree, not
uploaded file-by-file through the GitHub browser interface.

**CD is a contract, not just automation.** The release artifact is a
promise to anyone who downloads it: this code has passed all tests on
a clean machine. Without CD, a "release" is just a snapshot of whatever
was in the repository at some point. With CD, a release is a verified,
reproducible artifact.
