[assignment8_reflection.md](https://github.com/user-attachments/files/26781262/assignment8_reflection.md)
# assignment8_reflection.md — Reflection on State and Activity Modeling
## Smart Academic Library Assistance System (SALAS)

> Assignment 8: Reflection
> Building on Assignments 3–7 |19 April 2026

---

## Challenge 1: Choosing the Right Level of Granularity

The most persistent challenge across both diagram types was deciding how detailed each
diagram should be. State transition diagrams and activity diagrams can both be drawn
at many levels of abstraction, and the wrong level makes them either useless (too
high-level) or unreadable (too detailed).

For the Book object state diagram, an early draft had twelve states including
sub-states like "Reserved-PickupReady" and "Borrowed-RenewalPending." While these
states are technically valid, they added cognitive load without adding clarity. The
final diagram consolidated these into six clean states with clearly labelled
transitions. The rule I settled on was: a state is worth including if it changes what
the system can or cannot do. "Reserved" and "Borrowed" are meaningfully different
because different actions are available in each. "Reserved-PickupReady" is not
different enough from "Reserved" to justify a separate state box.

For the activity diagrams, the opposite problem appeared. The Return Book workflow
initially had just four steps: scan book, check loan, update inventory, notify. This
was too abstract to be useful for implementation. Expanding it to include the overdue
fine calculation, the reservation queue check, and the Elasticsearch update step
produced a diagram that a developer could actually translate into code. The lesson
here is that activity diagrams should be detailed enough that a developer can map
each action node to a specific function or API call.

---

## Challenge 2: Aligning Diagrams with Agile User Stories

The assignment required traceability between the diagrams and the user stories from
Assignment 6. This alignment was not always natural. User stories are written from
a user perspective, "As a student, I want to borrow a book", while state and
activity diagrams are written from a system perspective, "the Loan object
transitions from Active to Overdue when the due date passes."

Bridging this gap required going back to the acceptance criteria in AGILE_PLANNING.md
rather than the user story titles. The acceptance criteria are written in testable,
system-level language ("inventory count is decremented immediately upon borrowing")
that maps cleanly onto diagram transitions and action nodes. This reinforced the
value of writing precise acceptance criteria in Assignment 6, they are not just
for testers, they are the link between user intent and system behaviour.

The most difficult alignment was for US-013 (AES-256 encryption and TLS). This is
a non-functional requirement that does not naturally fit into a state diagram for a
specific object or an activity diagram for a specific workflow. It appears implicitly
in every diagram as a background constraint rather than as an explicit state or
action. I addressed this by noting its presence in the User Account diagram (the
Deactivated → data erasure transition maps to NFR-11) and documenting the NFR
mapping in the Integration section of the README.

---

## State Diagrams vs Activity Diagrams: A Comparison

These two diagram types model different aspects of the same system and complement
each other rather than overlapping.

**State transition diagrams** answer the question: "What can this object be, and
what causes it to change?" They are object-centric. The Book diagram does not care
who borrowed the book or what steps were involved, it only cares that the book is
now in a Borrowed state and what that means for what can happen next. State diagrams
are most useful for objects that have a meaningful lifecycle: things that are created,
modified, and destroyed, or that have different rules depending on their current
condition. In SALAS, the Loan, Reservation, and User Account objects all have
non-trivial lifecycles where the current state directly controls what actions are
permitted.

**Activity diagrams** answer the question: "What steps happen to complete this
process, and in what order?" They are process-centric. The Borrow a Book activity
diagram does not care about the long-term state of the Loan object, it only cares
about the sequence of steps from the student clicking "Borrow" to the confirmation
email being sent. Activity diagrams are most useful for workflows that involve
decisions, parallel actions, and multiple actors. In SALAS, the overdue notification
workflow and the report generation workflow both involve branching logic and multiple
system components that are better described as a flow than as a state machine.

The two diagram types work together: the state diagram for the Loan object defines
the lifecycle, while the activity diagram for the Return Book workflow defines the
process that causes one of those lifecycle transitions. Neither is complete without
the other. A developer implementing the return functionality would consult both: the
activity diagram to understand the steps to implement, and the state diagram to
understand what constraints apply at each step.

---

## Lessons Learned

**Requirements are living documents.** Modelling the Notification workflow revealed
that FR-07 did not specify what happens when all three retry attempts fail. The
in-app fallback was added as an implicit requirement that the state diagram made
visible. Diagramming is a form of requirements validation.

**Parallel actions are harder to diagram than to describe.** The dashboard load
workflow looks simple in prose ("load all data simultaneously") but required careful
diagramming to show that the four parallel fetches must all complete before the
dashboard renders — except in the degraded mode where partial data is shown. Getting
this right in the diagram before implementation prevents a common bug where the
dashboard blocks on the slowest service.

**Guard conditions are the bridge between requirements and code.** Every guard
condition in the state diagrams corresponds directly to a conditional check in the
application code. The "active loans exist" guard on catalogue deletion, the "fines
exceed R100" guard on borrowing eligibility, and the "3 retries exhausted" guard on
notification failure are all directly implementable as database queries or counter
checks. Writing them as guards in the diagram makes them impossible to overlook
during implementation.

---

## Agile Connection

The diagrams produced in this assignment map directly to the Sprint 2 user stories defined in AGILE_PLANNING.md. For example, the Borrow Book activity diagram directly supports Sprint 2 user stories focused on real-time availability checks and transaction processing (US-003), while the Student Dashboard Load diagram supports US-004 and its 2-second performance acceptance criteria. State diagrams for the Loan and Reservation objects provide the implementation contract for the same stories, developers can read both the activity diagram (what steps to implement) and the state diagram (what constraints apply at each step) to fully understand a user story before writing a single line of code.
