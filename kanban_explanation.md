# kanban_explanation.md — Kanban Board Explanation
## Smart Academic Library Assistance System (SALAS)

> Assignment 7: Kanban Board Explanation
> Building on Assignments 3–6 | Version 1.0 | April 2026

---

## 1. What is a Kanban Board?

A Kanban board is a visual project management tool that represents the stages of a
workflow as columns, with each task shown as a card that moves from left to right
as it progresses through those stages. The word "Kanban" comes from Japanese and
means "visual signal" or "card" — the idea being that the board itself communicates
the state of all work at a glance, without needing a meeting or a status report.

At its core, a Kanban board does three things: it makes work visible, it limits how
much work can be in progress at any one time, and it exposes bottlenecks before they
become blockers. A task that sits in "In Progress" for three days without moving is
immediately visible on a Kanban board in a way it never would be in a spreadsheet or
a meeting agenda.

---

## 2. SALAS Custom Kanban Board Design

### 2.1 Board Columns

The SALAS Kanban board uses the Automated Kanban template as its base, extended with
two custom columns to reflect the full development lifecycle of the system.

| Column | Purpose | WIP Limit |
|---|---|---|
| **Backlog** | All user stories not yet scheduled for the current sprint. Contains Sprint 2, 3, and 4 stories. | No limit |
| **To Do** | Stories selected for the current sprint (Sprint 1) that have not been started. | 6 cards max |
| **In Progress** | Stories actively being developed. Auto-populated when a linked PR is opened. | 3 cards max |
| **Testing** | *(Custom)* Stories where development is complete and acceptance criteria are being verified against the test cases defined in TEST_CASES.md. | 3 cards max |
| **Blocked** | *(Custom)* Stories that cannot proceed due to a dependency, technical issue, or external blocker. Cards here include a comment explaining the blocker. | No limit |
| **Done** | Stories that have passed testing and meet the Definition of Done from AGILE_PLANNING.md. Auto-populated when the linked issue is closed. | No limit |

### 2.2 Why These Custom Columns Were Added

**Testing column:** The assignment rubric and SALAS's Definition of Done both require
that acceptance criteria are verified before a story is closed. Without a dedicated
Testing column, stories would jump directly from In Progress to Done, skipping the
verification step. The Testing column makes QA a visible, explicit stage in the
workflow rather than an afterthought. It maps directly to the 14 test cases defined
in TEST_CASES.md from Assignment 5.

**Blocked column:** In real Agile development, tasks frequently get stuck due to
unresolved dependencies, unclear requirements, or external factors. Without a Blocked
column, blocked tasks either sit in In Progress (making the board misleading) or get
moved back to To Do (losing context). A dedicated Blocked column makes impediments
visible so they can be resolved quickly. For SALAS, this is particularly relevant for
stories with dependencies — for example, US-003 (Borrow/Reserve) depends on US-001
(Search) being complete, and US-005 (Recommendations) depends on sufficient
borrowing data existing.

---

## 3. How the Board Visualizes Workflow

Each column represents a distinct stage in the SALAS development process. A user
story (GitHub Issue) starts in Backlog when it is created, moves to To Do when it
is selected for a sprint, progresses to In Progress when a developer opens a pull
request, moves to Testing when the PR is merged and acceptance criteria are being
checked, and finally lands in Done when the issue is closed and all criteria are met.

The horizontal flow of cards from left to right gives an immediate picture of sprint
health. If many cards are clustered in In Progress and none are reaching Testing or
Done, it signals that the team is taking on too much work simultaneously. If cards
are piling up in Blocked, it signals that dependency management needs attention. The
board makes these patterns visible without requiring anyone to ask for a status update.

---

## 4. How the Board Limits Work-in-Progress (WIP)

WIP limits are set on the active workflow columns as follows:

- **To Do:** Maximum 6 cards — ensures the sprint is realistically scoped
- **In Progress:** Maximum 3 cards — enforces focus; no starting new work until existing work moves forward
- **Testing:** Maximum 3 cards — prevents a testing backlog from building up

These limits are enforced through team discipline (GitHub Projects does not natively
enforce hard WIP limits, but the limits are documented and visible). When the In
Progress column reaches 3 cards, no new cards should be moved in until one moves to
Testing. This prevents the common Agile failure mode where work starts but never
finishes — also known as "starting everything, completing nothing."

For Sprint 1, the four selected stories (US-001, US-002, US-010, US-013) fit
comfortably within these limits, with a maximum of two stories in progress at any
one time given their dependencies.

---

## 5. How the Board Supports Agile Principles

**Continuous delivery:** The board's flow from To Do → In Progress → Testing → Done
mirrors the Agile principle of delivering working software incrementally. Each story
that reaches Done represents a tested, working piece of the SALAS system.

**Adaptability:** The Blocked column supports Agile's emphasis on responding to
change. When a blocker is identified, the card moves to Blocked immediately and a
comment is added explaining the issue. This makes the problem visible to all
stakeholders and prompts rapid resolution rather than silent delay.

**Transparency:** GitHub's Automated Kanban is publicly visible on the repo, meaning
the lecturer (acting as product owner in this academic context) can see the real-time
state of Sprint 1 work at any time without requesting a report.

**Traceability:** Every card on the board is linked to a GitHub Issue, which is
linked to a user story in AGILE_PLANNING.md, which is linked to a functional
requirement in SRD.md, which is linked to a stakeholder concern in STAKEHOLDERS.md.
This end-to-end traceability from board card to stakeholder need is a core Agile
quality assurance principle.

---

## 6. Sprint 1 Board Population

The following issues from Assignment 6 are linked to the SALAS Kanban board for
Sprint 1:

| Card | GitHub Issue | Label | Sprint Column | Story Points |
|---|---|---|---|---|
| US-002 Student registration and login | #2 | must-have, sprint-1 | To Do | 3 |
| US-010 Role-based access control | #10 | must-have, sprint-1 | To Do | 3 |
| US-013 AES-256 encryption and TLS | #13 | must-have, sprint-1 | To Do | 2 |
| US-001 Search library catalogue | #1 | must-have, sprint-1 | To Do | 5 |
| US-003 Borrow/reserve a book | #3 | must-have | Backlog | 5 |
| US-004 Student personal dashboard | #4 | must-have | Backlog | 5 |
| US-005 Personalized recommendations | #5 | should-have | Backlog | 8 |
| US-006 Librarian catalogue management | #6 | must-have | Backlog | 5 |
| US-007 Automated overdue notifications | #7 | must-have | Backlog | 3 |
| US-008 Usage reports and analytics | #8 | should-have | Backlog | 5 |
| US-009 REST API for external integration | #9 | should-have | Backlog | 5 |
| US-011 Student reading list | #11 | could-have | Backlog | 2 |
| US-012 Accessible interface | #12 | must-have | Backlog | 3 |
| US-014 Bulk CSV import | #14 | should-have | Backlog | 3 |
