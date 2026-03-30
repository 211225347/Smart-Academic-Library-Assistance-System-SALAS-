# REFLECTION6.md — Reflection on Assignment 6: Agile Planning

## Assignment 6 Reflection: Agile User Stories, Backlog, and Sprint Planning
### Smart Academic Library Assistance System (SALAS)

> Date: March 2026 | Student: Phola Qwalana (211225347)

---

## Overview

Assignment 6 challenged me to translate system requirements and use cases into actionable Agile work. This reflection examines the challenges faced in prioritization, estimation, and aligning Agile methodology with stakeholder needs. As the sole stakeholder, I had to overcome personal biases and make difficult trade-off decisions.

---

## Challenge 1: Prioritization in a Solo Stakeholder Environment

### The Dilemma

With 16 potential user stories and only capacity for 7 in Sprint 1, I faced prioritization paralysis. Every story seemed important:
- Students want personalized recommendations
- Librarians want bulk import capabilities
- Admins want analytics and reporting
- Everyone wants reading lists and bookmarks

But INVEST criteria demand **small, independent stories**. How do I choose?

### My Approach: MoSCoW + Personas

I applied MoSCoW (Must/Should/Could/Won't) prioritization and created two detailed personas:

**Persona 1 - Ava (Student, 20, CS Major)**
- Pain point: "I waste 15 minutes searching the library catalog for one book"
- Success metric: "Find books faster in SALAS than Googling"
- Needs: Fast search, easy borrowing, due date reminders

**Persona 2 - Martin (Librarian, 15 years experience)**
- Pain point: "70% of borrowed books are returned late; managing fines is painful"
- Success metric: "Reduce overdue rates by 20%"
- Needs: Accurate inventory, automated reminders, bulk import

This exercise was transformative. It forced me to deprioritize technically interesting features (e.g., collaborative filtering recommendations) in favor of **their** needs.

### Resolution

**Must-haves (9 stories):** Authentication, RBAC, search, borrowing, dashboard, notifications, accessibility, encryption, catalogue management.  
**Should-haves (4 stories):** Recommendations, analytics, API, bulk import.  
**Could-haves (1 story):** Reading lists.

**Lesson Learned:** Even solo stakeholders benefit from personas. They force you out of your own head and into users' shoes. The personas became my internal "devil's advocate" when I wanted to include technically cool but user-unnecessary features.

---

## Challenge 2: Estimation Under Uncertainty

### The Estimation Struggle

Story point estimation was humbling. For US-002 (Authentication), I oscillated between 3, 5, and 8 points:

- **3 points:** Basic login validation (email/password check)
- **5 points:** Login + JWT + refresh tokens + brute-force protection (actual MVP scope)
- **8 points:** Add OAuth, multi-factor auth, SSO (over-scoped)

I settled on **3 points** by ruthlessly scoping to "must-have" authentication. This taught me that **story points reflect scope within the sprint, not theoretical perfection**.

### Unknown Unknowns

As I broke US-001 (Search) into 7 tasks, I discovered hidden complexity:
- Elasticsearch cluster setup (assumed DevOps owned it separately, but integration testing requires my involvement)
- Real-time availability sync (inventory decrement on borrow must immediately reflect in search results)
- Performance testing infrastructure (measuring p95 latency under load requires stress testing tools)

I padded the estimate to 5 points and **still worried I was underestimating**. This revealed: **first-sprint stories often carry hidden complexity**.

### Task Breakdown Granularity

I experimented with different task sizes:
- **T-001 through T-038:** Ranged from 1-6 hours per task
- **Too coarse** (20-hour tasks) → Visibility into daily progress lost
- **Too fine** (0.5-hour tasks) → Task management overhead
- **Goldilocks** (3-4 hours per task) → Daily standup visibility, reasonable async hand-offs

For a 2-week sprint with daily standups, 3-4 hour tasks enabled mid-sprint course corrections and reduced integration surprises.

### Resolution

I accepted that **estimation improves iteratively**. Sprint 1 velocity might be 13 points (conservative); Sprint 2-3 might stabilize at 18-20 points as the team learns the codebase and deployment process. Over-estimate early; refine with actuals.

**Lesson Learned:** Story points are relative estimates with inherent uncertainty (Fibonacci scale reflects this). Accuracy isn't the goal; consistency is. What matters is that the team learns to estimate themselves relative to past work.

---

## Challenge 3: Security vs. Usability Trade-Offs

### The Temptation

Looking at effort estimates, I was tempted to minimize US-013 (Encryption/TLS) to maximize US-001 (Search). Security felt like overhead compared to student-facing features.

But stakeholder analysis from STAKEHOLDERS.md showed:
- **IT Administrator pain point:** "I'm liable if student data is breached"
- **Success metric:** "Zero security vulnerabilities; POPIA compliance verified"

### The Reality Check

POPIA (Protection of Personal Information Act) is legally mandated in South Africa. There's no trade-off here; security is **non-negotiable**. Moreover, retrofitting security later costs exponentially more:
- Building secure from scratch: Integrate encryption during schema design
- Retrofitting security: Migrate encrypted/unencrypted data, update APIs, re-test everything

I accepted that:
- Passwords must be hashed (bcrypt), never plaintext
- TLS on all endpoints (no exceptions)
- RBAC from day 1 (not retrofitted later)

### Resolution

Security became a **Must-have**, not a Could-have. This decision actually simplified prioritization: non-negotiable requirements are easy to prioritize (they go first).

**Lesson Learned:** Legal/compliance requirements are not negotiable trade-offs. Build them in from the start, even if they delay other features. The cost of insecurity far exceeds the cost of development delays.

---

## Challenge 4: MVP vs. Perfection Dilemma

### The Cutting Decision

I had 16 stories and Sprint capacity for 7. Which 9 do I cut?

Two stories particularly hurt to defer:
- **Reading Lists (US-011):** Only 2 story points! Easy to implement, nice UX improvement.
- **Analytics (US-008):** Useful for admin procurement decisions, aligns with stakeholder needs.

But looking at dependencies and MVP definition, both were deferrable:
- **Reading lists** distract from core workflow (search → borrow → return). Nice-to-have ≠ must-have.
- **Analytics** require 6+ months of borrowing data to be useful. Pointless in Sprint 1.

### The Deference Decision

I explicitly marked both for Sprint 4. This wasn't failure; it was **strategic focus**. Imperfect MVP that works beats delayed perfection that hypothetically might.

### Resolution

Deferred 2 stories to Sprints 2-4. Sprint 1 focuses on MVP essentials: authentication, search, borrowing, dashboard, accessibility.

**Lesson Learned:** MVP is about **learning from real users**, not building everything you can think of. User feedback from Sprint 1 might invalidate my assumptions. Better to gather that feedback early than waste effort on features no one wants.

---

## Challenge 5: Maintaining Traceability in a Solo Project

### The Traceability Matrix

With 14 user stories, 12 requirements, and multiple use cases, I risked creating a tangled mess. I built a traceability matrix:

| US-001 | FR-02 | UC02 | Sprint 1 |
| US-002 | FR-01 | UC01 | Sprint 1 |
| ... | ... | ... | ... |

This matrix serves two purposes:
1. **Accountability:** Every user story traces back to a stakeholder need (FR) and use case
2. **Completeness verification:** No requirements are orphaned; no user stories are untethered

### Resolution

Traceability matrix ensured nothing fell through cracks. Every story has a "why" (FR) and a "how" (UC).

**Lesson Learned:** Traceability is not bureaucracy; it's **accountability and clarity**. Takes 30 minutes to build; saves hours of confusion later.

---

## Key Takeaways

1. **Agile is discipline, not chaos.** MoSCoW forces hard "no" decisions. Harder than saying "yes" to everything.

2. **MVP requires ruthless scope management.** 14 user stories is already aggressive; 7 for Sprint 1 is appropriate. Focus beats breadth.

3. **Estimation improves iteratively.** First estimates are educated guesses. Accuracy isn't the goal; consistency is.

4. **Stakeholder voices (even personas) prevent tunnel vision.** One person can't think of everything. External perspectives—real or imagined—are vital.

5. **Security is non-negotiable.** Legal/compliance requirements aren't trade-offs. Build them in from the start.

6. **Traceability ensures accountability.** Map every user story to requirements and use cases. Prevents orphaned work.

7. **User feedback beats hypothetical perfection.** Deliver MVP early; gather feedback; iterate based on reality, not assumptions.

---

## Conclusion

Assignment 6 reinforced that **Agile is fundamentally about discipline and pragmatism**. It forces you to say "no" to good ideas in service of great ones. Prioritization, estimation, and trade-off decisions are not one-time activities; they're ongoing conversations with stakeholders, users, and the development team.

The toughest lesson: **Imperfect MVP beats delayed perfection.** As a solo stakeholder, I had to fight my perfectionist tendency to include every good idea. Deferring reading lists and analytics to future sprints felt like failure initially. But it's actually **strategic focus**: deliver 70% of core features excellently rather than 30% of everything.

Going forward, I'll remember: Agile succeeds not through perfect planning, but through **iterative learning and stakeholder alignment**.

---

## Appendices

### A. Prioritization Decision Log

| Decision | Reasoning | Outcome |
|---|---|---|
| Defer Recommendations to Sprint 2 | Requires 6+ months borrowing history; MVP doesn't need yet | Must-have → Should-have |
| Prioritize Search over Analytics | Students need search; admins can wait for analytics | High → Medium |
| Include Accessibility (WCAG) in Sprint 1 | Legal obligation; inclusive design is non-negotiable | Deferred → Must-have |
| Defer Reading Lists to Sprint 4 | Low business impact; distracts from core workflow | Could-have → Won't-have (Sprint 4) |

### B. Estimation Assumptions

- **Auth endpoint:** Assumes bcrypt password hashing, JWT issue/validate, Redis lockout counter
- **Search:** Assumes Elasticsearch already provisioned; estimates integration and UI only
- **Borrowing:** Assumes synchronous inventory updates; async queues for email notifications
- **Dashboard:** Assumes PostgreSQL query performance is acceptable (no query optimization)

### C. Risk Mitigations

| Risk | Mitigation |
|---|---|
| Elasticsearch delay | Pre-provision cluster before Sprint 1 starts |
| Real-time sync failure | Implement async cache layer; accept eventual consistency |
| JWT security flaws | Use well-tested libraries (e.g., PyJWT, jsonwebtoken.js); security review before launch |
| Task underestimation | Conservative velocity in Sprint 1; adjust for Sprints 2+ |
