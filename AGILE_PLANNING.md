# AGILE_PLANNING.md Agile Planning Document
## Smart Academic Library Assistance System (SALAS)

> Assignment 6: Agile User Stories, Backlog, and Sprint Planning
> Building on Assignments 3–5 — SALAS
> Date:5 April 2026

---

## Executive Summary

This document translates the system requirements (Assignment 4: SRD.md) and use cases (Assignment 5: USE_CASE_SPECIFICATIONS.md) into an actionable Agile backlog. All 14 user stories follow the INVEST criteria and trace directly to functional requirements (FR-01 to FR-12) and use cases. Sprint 1 focuses on MVP essentials: authentication, RBAC, encryption, search, borrowing, dashboard, and accessibility.

---

## 1. User Story Creation 

### 1.1 User Stories Table
**Format:** "As a [role], I want [action] so that [benefit]."

All stories linked to Assignment 4 (SRD.md) Functional Requirements and Assignment 5 (USE_CASE_SPECIFICATIONS.md) Use Cases.

| Story ID | User Story | Linked FR/UC | Acceptance Criteria | Priority | INVEST |
|---|---|---|---|---|---|
| **US-001** | As a **student**, I want to search for books by title, author, or ISBN so that I can quickly find academic resources. | FR-02 / UC02 | Search returns results within ≤2 seconds Display real-time availability status Keyboard & screen reader accessible Filter by author, genre, year | High | Independent, Testable, Valuable |
| **US-002** | As a **student**, I want to register using my university email and securely log in so that my account is linked to my institution. | FR-01 / UC01 | Registration blocks non-university emails JWT tokens expire after 24hrs Account lockout after 5 failed attempts Login response ≤ 1 second | High | Independent, Estimable, Testable |
| **US-003** | As a **student**, I want to borrow or reserve available books online so that I don't have to visit the library in person. | FR-03 / UC03 | Borrowing confirmation within 60 seconds Inventory decremented immediately Hold expiry after 48 hours Auto-activate next reservation | High | Negotiable, Small, Valuable |
| **US-004** | As a **student**, I want to view my personal dashboard so that I can see my active loans, due dates, and overdue notices in one place. | FR-04 / UC04 | Dashboard loads within 2 seconds Due items within 3 days highlighted in red 12-month borrowing history Fully responsive mobile/tablet/desktop | High | Independent, Testable, Small |
| **US-005** | As a **student**, I want to receive personalized book recommendations so that I can discover relevant resources aligned with my courses. | FR-05 / UC05 | Minimum 10 recommendations shown Updated every 24 hours New students receive defaults within 1 hour Dismissal feeds back into model | Medium | Valuable, Estimable, Testable |
| **US-006** | As a **librarian**, I want to add, edit, and delete books from the catalogue so that the inventory stays accurate and up-to-date. | FR-06 / UC06 | New resources indexed in Elasticsearch within 30 seconds ISBN validation enforced Deletion blocked if active loans exist CSV bulk import (up to 1,000 rows) | High | Independent, Negotiable, Testable |
| **US-007** | As a **student**, I want to receive email reminders before my book is due so that I can return it on time and avoid fines. | FR-07 / UC07 | Emails sent 3 days before, on due date, 1 day after Include resource title and dashboard link Deliver within 5 minutes Configurable preferences | High | Small, Valuable, Testable |
| **US-008** | As an **admin**, I want to generate and export usage reports so that I can make data-driven decisions about resource procurement. | FR-08 / UC08 | Reports filterable by date, department, resource type PDF/CSV exports within 10 seconds At least 4 standard reports RBAC protected | Medium | Valuable, Estimable, Testable |
| **US-009** | As an **external developer**, I want access to a RESTful API with OpenAPI documentation so that I can integrate library features into the university portal. | FR-09 / UC09 | Swagger UI at `/api/v1/docs` All endpoints documented Sandbox environment 24/7 Rate limiting 100 req/min | Medium | Negotiable, Estimable, Testable |
| **US-010** | As an **IT administrator**, I want role-based access control enforced so that users can only access features appropriate for their role. | FR-10 / UC10 | Students cannot access admin/catalogue endpoints HTTP 403 on unauthorized requests Role changes audit-logged Three roles: Student, Librarian, Admin | High | Independent, Testable, Valuable |
| **US-011** | As a **student**, I want to save resources to reading lists so that I can keep track of books I want to read. | FR-11 / UC11 | Save in 1 click Create up to 10 collections Export as APA/Harvard bibliography Persist across sessions | Low | Small, Valuable, Testable |
| **US-012** | As a **student with a disability**, I want the interface to be fully keyboard-navigable and screen-reader compatible so that I can use the library independently. | FR-12 / UC02, UC04 | Lighthouse accessibility score ≥95 All elements reachable via keyboard 4.5:1 color contrast ARIA live regions | High | Independent, Testable, Valuable |
| **US-013** | As a **system administrator**, I want all student data encrypted with AES-256 and transmitted over TLS so that security and POPIA compliance are maintained. | NFR-09 | Zero plaintext personal data in DB SSL Labs Grade A TLS on all endpoints POPIA audit completed | High | Estimable, Testable, Independent |
| **US-014** | As a **librarian**, I want to bulk import resources from CSV files so that I can add large acquisitions quickly without manual entry. | FR-06 / UC06a | Process up to 1,000 rows ✓ Invalid rows flagged in error report Valid records indexed within 60 seconds All changes logged | Medium | Negotiable, Valuable, Testable |

### 1.2 INVEST Criteria Compliance

**Independent:** Each story can be developed independently. US-002 (auth) is foundation but negotiable scope.  
**Negotiable:** All stories have refinable acceptance criteria. Stakeholder can adjust details (e.g., US-005 recommendation frequency).  
**Valuable:** All deliver measurable business value (e.g., US-001 addresses student pain point: "finding resources quickly").  
**Estimable:** Clear scope; team can estimate story points confidently.  
**Small:** Each story completes within single sprint (~3-8 points max).  
**Testable:** All acceptance criteria verifiable (e.g., "within 2 seconds" is measurable via performance testing).

---

## 2. Product Backlog Creation 

### 2.1 Prioritized Backlog with MoSCoW & Story Points

| Story ID | User Story (Summary) | MoSCoW | Story Points (Fibonacci) | Dependencies | Justification |
|---|---|---|---|---|---|
| **US-002** | Student & librarian authentication | Must-have | 3 | None | Foundation for all protected features; enables system access. |
| **US-010** | Role-based access control | Must-have | 3 | US-002 | Security baseline; enables multi-role system. |
| **US-013** | AES-256 encryption + TLS | Must-have | 2 | US-002 | Legal requirement (POPIA); non-negotiable. |
| **US-001** | Search library catalogue | Must-have | 5 | US-002 | Core MVP value proposition; directly solves #1 student pain point from STAKEHOLDERS.md. |
| **US-003** | Borrow / reserve a book | Must-have | 5 | US-001, US-002 | Critical user workflow; replaces manual library processes. |
| **US-004** | Student personal dashboard | Must-have | 5 | US-002, US-003 | Students need unified view of loans & due dates; drives engagement. |
| **US-006** | Librarian catalogue management | Must-have | 5 | US-010 | Librarians need inventory control; system has no data without this. |
| **US-007** | Automated overdue notifications | Must-have | 3 | US-003 | Reduces overdue rates; key success metric for librarian stakeholder (STAKEHOLDERS.md). |
| **US-012** | Accessible interface (WCAG 2.1 AA) | Must-have | 3 | US-001, US-004 | Legal obligation; inclusive design non-negotiable. |
| **US-005** | Personalized recommendations | Should-have | 8 | US-001, US-003 | High value but depends on borrowing history; deferred to Sprint 2. |
| **US-008** | Usage reports and analytics | Should-have | 5 | US-003, US-006 | Valuable for admin but not required for MVP launch. |
| **US-009** | REST API for external integration | Should-have | 5 | US-002, US-001 | Needed for portal integration but not MVP-critical. |
| **US-014** | Bulk CSV import for librarians | Should-have | 3 | US-006 | Speeds up large acquisitions; low priority initially. |
| **US-011** | Student reading list | Could-have | 2 | US-001, US-002 | Nice-to-have; low impact on core workflows. |

**Total Must-have:** 9 stories, 34 points | **Total Should-have:** 4 stories, 21 points | **Total Could-have:** 1 story, 2 points | **TOTAL:** 14 stories, 57 points

### 2.2 Prioritization Justification

**Must-have Stories (9, 34 points)** form the MVP core functionality that directly serves stakeholder needs identified in STAKEHOLDERS.md: students finding resources efficiently, librarians managing inventory accurately, IT admins maintaining security.

**Should-have Stories (4, 21 points)** deliver significant value but can defer to Sprint 2/3 without blocking MVP delivery. Recommendations require historical data; Analytics are useful only after 6+ months.

**Could-have Stories (1, 2 points)** are nice-to-have enhancements with low business impact. Reading lists are low priority until core workflows are validated.

---

## 3. Sprint 1 Plan 

### 3.1 Sprint Goal Statement

> **"Deliver a secure, user-friendly authentication system, role-based access control, encryption, core book search functionality, and borrowing workflow so that students can securely register, discover resources, and borrow books—forming the foundation of the SALAS MVP."**

**Sprint Duration:** 2 weeks | **Sprint Velocity:** 18 story points | **Selected Stories:** 7 stories, 26 points

### 3.2 Sprint Backlog — Task Breakdown 

| Task ID | Story ID | Task Description | Est. Hours | Priority | Status |
|---|---|---|---|---|---|
| T-001 | US-002 | Design PostgreSQL User table schema | 2 | High | To Do |
| T-002 | US-002 | Implement POST `/api/v1/auth/register` endpoint | 4 | High | To Do |
| T-003 | US-002 | Implement POST `/api/v1/auth/login` endpoint with JWT | 4 | High | To Do |
| T-004 | US-002 | Implement login brute-force protection (Redis) | 3 | High | To Do |
| T-005 | US-002 | Build React registration form | 5 | High | To Do |
| T-006 | US-002 | Build React login form with JWT persistence | 4 | High | To Do |
| T-007 | US-002 | Write unit tests for auth endpoints | 3 | High | To Do |
| T-008 | US-010 | Define RBAC middleware | 3 | High | To Do |
| T-009 | US-010 | Create role-permission matrix | 2 | High | To Do |
| T-010 | US-010 | Return HTTP 403 on unauthorized access | 2 | High | To Do |
| T-011 | US-010 | Write integration tests for RBAC | 3 | High | To Do |
| T-012 | US-013 | Configure TLS certificate on API server | 2 | High | To Do |
| T-013 | US-013 | Implement AES-256 encryption for DB fields | 3 | High | To Do |
| T-014 | US-013 | Verify SSL Labs Grade A on staging | 1 | High | To Do |
| T-015 | US-001 | Set up Elasticsearch cluster | 4 | High | To Do |
| T-016 | US-001 | Implement GET `/api/v1/search?q=&filters=` endpoint | 6 | High | To Do |
| T-017 | US-001 | Enrich search results with real-time availability | 3 | High | To Do |
| T-018 | US-001 | Build React search bar component | 6 | High | To Do |
| T-019 | US-001 | Build React search results page | 5 | High | To Do |
| T-020 | US-001 | Write performance test for search (≤2s) | 3 | High | To Do |
| T-021 | US-001 | Seed Elasticsearch with 500 test records | 2 | High | To Do |
| T-022 | US-003 | Design Loan table schema | 2 | High | To Do |
| T-023 | US-003 | Implement POST `/api/v1/loans/borrow` endpoint | 5 | High | To Do |
| T-024 | US-003 | Implement POST `/api/v1/loans/reserve` endpoint | 4 | High | To Do |
| T-025 | US-003 | Implement automatic hold expiry (cron job) | 3 | High | To Do |
| T-026 | US-003 | Send borrowing confirmation email (async queue) | 3 | High | To Do |
| T-027 | US-003 | Build React "Borrow" modal | 3 | High | To Do |
| T-028 | US-003 | Build React "Reserve" component | 3 | High | To Do |
| T-029 | US-003 | Write integration tests for borrowing | 3 | High | To Do |
| T-030 | US-004 | Design Dashboard DB schema | 2 | High | To Do |
| T-031 | US-004 | Implement GET `/api/v1/dashboard/student` endpoint | 4 | High | To Do |
| T-032 | US-004 | Build React Dashboard component | 5 | High | To Do |
| T-033 | US-004 | Build borrowing history section | 3 | High | To Do |
| T-034 | US-004 | Implement mobile-responsive design | 3 | High | To Do |
| T-035 | US-004 | Write performance test (Dashboard ≤2s) | 2 | High | To Do |
| T-036 | US-012 | Run Lighthouse accessibility audit | 2 | High | To Do |
| T-037 | US-012 | Implement ARIA labels & keyboard navigation | 4 | High | To Do |
| T-038 | US-012 | Test with NVDA/JAWS screen readers | 3 | High | To Do |

**Total Estimated Hours:** 145 hours | **Team Capacity:** 160 hours (2 devs × 80 hrs) | **Utilization:** 91%

### 3.3 Sprint 1 Definition of Done

A user story is **Done** when:
- All task code written, tested locally, and peer reviewed
- Unit tests (≥80% coverage) + integration tests passing
- Code reviewed and approved by ≥1 peer
- Code merged to `main` branch via pull request
- Feature tested in staging environment by QA
- **All** acceptance criteria verified and met
- No critical/high-severity bugs open
- Documentation updated (API docs, README)
- Technical debt logged for future sprints

---

## 4. Traceability Summary 

### 4.1 Requirements to User Stories Mapping

| User Story | Assignment 4 FR | Assignment 5 UC | Sprint |
|---|---|---|---|
| US-001 | FR-02 | UC02 | Sprint 1 |
| US-002 | FR-01 | UC01 | Sprint 1 |
| US-003 | FR-03 | UC03 | Sprint 1 |
| US-004 | FR-04 | UC04 | Sprint 1 |
| US-005 | FR-05 | UC05 | Sprint 2 |
| US-006 | FR-06 | UC06 | Sprint 2 |
| US-007 | FR-07 | UC07 | Sprint 2 |
| US-008 | FR-08 | UC08 | Sprint 3 |
| US-009 | FR-09 | UC09 | Sprint 3 |
| US-010 | FR-10 | UC10 | Sprint 1 |
| US-011 | FR-11 | UC11 | Sprint 4 |
| US-012 | FR-12 | UC02, UC04 | Sprint 1 |
| US-013 | NFR-09 | — | Sprint 1 |
| US-014 | FR-06 | UC06a | Sprint 3 |

### 4.2 Cross-Reference Documentation

- **Functional Requirements:** See `SRD.md` Section 2 (FR-01 through FR-12)
- **Non-Functional Requirements:** See `SRD.md` Section 3 (NFR-01 through NFR-14)
- **Use Case Specifications:** See `USE_CASE_SPECIFICATIONS.md`
- **Stakeholder Success Metrics:** See `STAKEHOLDERS.md`

---

## 5. Risk Register

| Risk ID | Risk | Impact | Likelihood | Mitigation |
|---|---|---|---|---|
| R-001 | Elasticsearch setup delays | High | Medium | Pre-provision cluster in Week 0 |
| R-002 | Real-time availability sync fails | High | Medium | Build async cache layer |
| R-003 | JWT token security flaws | Critical | Low | Security review before release |
| R-004 | RBAC complexity underestimated | Medium | Medium | 1-day spike before Sprint 1 |
| R-005 | Search latency exceeds 2 seconds | High | Medium | Optimize queries + add caching |

---

## 6. Reflection on Agile Prioritization & Estimation 

### 6.1 Challenges in Prioritization

**Challenge 1: Balancing Competing Needs as Solo Stakeholder**  
As the sole stakeholder, I had to actively resist feature bloat. My initial draft had 16 stories; I cut 2 (Could-haves) to focus on MVP essentials. Difficult decisions included:

- **Personalized Recommendations (US-005):** Tempting because it's "AI-powered" and impressive-sounding. However, students need functional **search first**. There's no point recommending books if the search is slow or incomplete. Deferred to Sprint 2 when we have borrowing history data.
- **Analytics Dashboard (US-008):** Useful for admins making procurement decisions, but doesn't directly serve students. Deferred to Sprint 3 after MVP validation.
- **Reading Lists (US-011):** Nice UX improvement but adds complexity without critical value. Deferred to Sprint 4.

**Lesson Learned:** MoSCoW prioritization forces **ruthless discipline**. "Won't-have" is not failure; it's **strategic focus**. MVP means "minimum viable," not "everything nice-to-have." The key insight: delivering 70% on core features beats 30% on everything. Users prefer a working MVP they can provide feedback on over an incomplete kitchen sink.

**Challenge 2: Security vs. Usability Trade-off**  
Initially, I considered downplaying US-013 (Encryption/TLS) effort to maximize US-001 (Search) story points. But stakeholder analysis from STAKEHOLDERS.md made clear: IT administrators and university administrators have **compliance as a non-negotiable success metric**. POPIA (Protection of Personal Information Act) compliance is legally mandated in South Africa.

I had to accept that:
- Passwords must be hashed with bcrypt, never plaintext
- TLS must be enforced on all endpoints from day 1
- RBAC must be enforced from day 1 (retrofitting later is exponentially harder)

**Lesson Learned:** Security is a **Must-have**, not a Could-have. The cost of retrofitting security later is exponential. Better to build secure from the start, even if it delays other features.

### 6.2 Challenges in Estimation

**Challenge 1: Fibonacci Sequence and Story Point Inflation**  
I initially struggled with story points. For US-002 (Authentication), I vacillated wildly:
- **3 points:** Basic login (just check email/password)
- **5 points:** Login + JWT + refresh tokens + brute-force protection (actual MVP scope)
- **8 points:** Add OAuth, multi-factor auth, SSO (over-scoped for MVP)

I settled on **3 points** by ruthlessly scoping to "must-have." This forced me to separate MVP authentication from "would-be-nice" OAuth. It reinforced that **story points reflect scope within the sprint**, not theoretical perfection. MVP features are smaller; polish comes in future sprints.

**Lesson Learned:** Story points are **relative estimates of effort**, not absolute predictions. The Fibonacci scale (1, 2, 3, 5, 8, 13) reflects increasing uncertainty. Estimation improves with team velocity feedback from actual sprints.

**Challenge 2: Unknown Unknowns**  
I estimated US-001 (Search) at 5 story points. As I broke it into tasks, I realized I hadn't accounted for:
- Elasticsearch cluster setup and configuration complexity
- Real-time availability synchronization (inventory decrement on borrow, increment on return)
- Performance testing infrastructure (necessary to verify 2-second SLA)
- Integration with existing database

I padded the estimate to 5 points and **still worried I was underestimating**. This revealed a fundamental truth: **first-sprint stories often carry hidden complexity**.

**Lesson Learned:** Sprint 1 velocities are unreliable predictors of future capacity. Velocity stabilizes in Sprint 2-3 as the team learns the codebase, tech stack, and deployment process. Over-estimate early; learn from actuals.

**Challenge 3: Task Breakdown Granularity**  
I experimented with different task sizes:
- **Too coarse:** "Implement Search" (1 task, 20 hours) → Blocks visibility; hard to track daily progress
- **Too fine:** 50+ micro-tasks ("Create search input box," "Add query button," etc.) → Overhead in task management
- **Goldilocks:** **2-6 hour tasks** → Daily standup updates possible, reasonable async hand-offs

For a 2-week sprint with daily standups, 3-4 hour tasks proved ideal. Allows frontend/backend devs to work async without blocking each other; enables mid-sprint course corrections.

**Lesson Learned:** Task granularity should match sprint length and team communication rhythm. 2-week sprints → 3-4 hour tasks.

### 6.3 Aligning Agile with Stakeholder Needs

**Challenge 1: Combating Solo Stakeholder Tunnel Vision**  
As the sole stakeholder, I had to actively combat my own biases. I created two detailed personas to pressure-test my prioritization:

- **Ava (20, CS Major, Student):** Primary needs are fast search, easy borrowing, due date reminders. Doesn't care about analytics or bulk import. Her success metric: "I find books faster in SALAS than Googling."
- **Martin (Librarian, 15 years):** Primary needs are accurate inventory control, reducing overdue rates, bulk resource import. Doesn't care about personalization. His success metric: "Overdue returns decreased by 20%."

This exercise forced me to deprioritize features I found technically interesting (e.g., "fancy collaborative filtering algorithm") and focus on **their** needs first. It reduced scope from 16 to 14 stories.

**Lesson Learned:** Even one stakeholder benefits from creating detailed personas. Forces you out of your own head and into users' shoes.

**Challenge 2: MVP vs. Perfection Temptation**  
I had to explicitly **cut** two good ideas:
- **Reading Lists (US-011):** Nice UX improvement, only 2 story points. But it distracts from core workflow (search → borrow → return).
- **Analytics (US-008):** Useful for admins, 5 points. But useless until 6+ months of borrowing data exist.

By deferring these to Sprint 4, I preserved focus. Imperfect MVP beats delayed perfection. User feedback from Sprint 1 might invalidate my assumptions anyway.

**Lesson Learned:** MVP is about **learning from real users**, not building everything. Gather feedback early; avoid sunk-cost fallacy of completing features no one wants.

### 6.4 Key Takeaways

1. **Agile is about discipline, not chaos.** MoSCoW prioritization forced hard "no" decisions. Harder than saying "yes" to everything.
2. **MVP requires ruthless scope management.** 14 user stories is a lot; 7 for Sprint 1 is appropriate. Focus beats breadth.
3. **Estimation improves iteratively.** First estimates are guesses; retrospectives and velocity data refine future estimates.
4. **Stakeholder voices (even personas) prevent tunnel vision.** One person can't think of everything; external perspectives are vital.
5. **Traceability ensures accountability.** Mapping user stories → requirements → use cases prevents features from falling through cracks.

---

## Conclusion

This Agile plan balances **technical excellence** (security, performance, accessibility) with **user-centric value** (search, borrowing, notifications). Sprint 1 focuses on MVP essentials; later sprints build on this foundation. Every user story traces to Assignment 4 requirements and Assignment 5 use cases, ensuring accountability and clarity.

**Repository:** https://github.com/211225347/Smart-Academic-Library-Assistance-System-SALAS-
