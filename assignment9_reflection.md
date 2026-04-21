# assignment9_reflection.md — Reflection on Domain Modeling and Class Diagram Design
## Smart Academic Library Assistance System (SALAS)

> Assignment 9: Reflection
> Building on Assignments 3–8 | Version 1.0 | April 2026

---

## Challenge 1: Deciding the Level of Abstraction

The first and most persistent challenge in this assignment was deciding the right
level of abstraction for the domain model. Domain modeling sits between requirements
(which describe what the system must do) and implementation (which describes how it
does it), and it is tempting to slide too far in either direction.

The most concrete example of this tension was the Resource class. An early draft of
the domain model had separate classes for Book, Journal, EBook, and ResearchPaper,
each with slightly different attributes. This felt true to the real world — a journal
article has a volume and issue number that a book does not. However, when I mapped
these classes against the functional requirements in Assignment 4, every single
requirement referred generically to "resources" without distinguishing between types.
FR-02 says students shall search the catalogue; FR-06 says librarians shall manage
catalogue entries. Neither requirement cares whether the entry is a book or a journal.

Introducing four subclasses to model a distinction that the requirements do not need
would have made the class diagram significantly more complex without adding any value
to the system. I consolidated everything into a single Resource class with a `type`
attribute. This is a deliberate trade-off: simplicity over completeness. If future
requirements distinguish between resource types, inheritance can be introduced at
that point — a principle aligned with Agile's "build what you need now" approach.

---

## Challenge 2: Composition vs Association for ReadingList

The relationship between Student and ReadingList was one of the hardest modeling
decisions in the assignment. Both composition and association are technically valid,
and the choice has downstream consequences for data persistence and deletion behaviour.

Composition (filled diamond) means the ReadingList cannot exist without the Student
— if the Student is deleted, the ReadingList is deleted with it. Association means
the ReadingList has independent existence and could theoretically outlive the Student.

The business rule that drove the decision was BR-07 and NFR-11: POPIA requires all
personal data to be erased within 30 days of account deactivation. A reading list is
personal data — it reveals a student's academic interests and reading patterns. If
ReadingList were an independent association, a deletion routine would need to
explicitly find and delete it. Composition makes this automatic and impossible to
forget during implementation.

This is the kind of decision that domain modeling makes visible. It is not obvious
from the requirements text, but it becomes clear the moment you try to draw the
relationship line and ask: "can this object exist without the other?"

---

## Alignment with Previous Assignments

One of the most satisfying aspects of this assignment was seeing how cleanly the
class diagram aligns with work from earlier in the semester.

The state diagrams from Assignment 8 map directly onto the class diagram. The Loan
state machine (Active, DueSoon, Overdue, Returned, Archived) becomes the `status`
attribute and the `isOverdue()`, `calculateFine()`, `archiveLoan()` methods on the
Loan class. The guard condition `fineExceedsR100` from the Overdue → Escalated
transition becomes the `Fine.isBorrowingBlocked()` method. The state diagram
describes what can happen; the class diagram describes what structure makes it
possible.

The activity diagrams from Assignment 8 map onto the methods. The "Return a Book"
activity diagram has action nodes for "Calculate fine amount," "Record fine on
student account," and "Increment available copy count" — these become
`Fine.calculateAmount()`, `Fine.payFine()`, and the `availableCopies` attribute on
Resource respectively. Writing the class diagram after the activity diagrams meant
that every method had a clear behavioural specification already — the activity diagram
told me what the method needed to do before I named it.

The use cases from Assignment 5 map onto the class methods most directly. UC03
(Borrow/Reserve a Book) required `Student.borrowResource()`, `Loan.createLoan()`,
`Resource.checkOut()`, and `Notification.schedule()`. Every action in a use case
basic flow becomes a method call in the class diagram.

---

## Trade-offs Made

**Fine as a separate class vs attributes on Loan.** As discussed in the design
decisions section, Fine became its own class because it has an independent lifecycle
and its own business logic. The trade-off is a slightly more complex class diagram
with an extra relationship. The benefit is cleaner separation of concerns and the
ability to query, report on, and manage fines independently of loans — which the
administrator's reporting requirements (FR-08) demand.

**Notification as a standalone class vs embedded in Loan.** Notification could have
been implemented as a method on Loan that fires an email directly. Making it a
standalone class with its own status, retry count, and channel attribute means the
system can track, audit, and retry notifications independently. The trade-off is
additional complexity; the benefit is the reliability and auditability required by
FR-07's acceptance criteria (3-retry rule, delivery logging).

**Catalogue as a separate class.** In many library systems, the catalogue is just
a database query. Making it a first-class domain entity with `searchByKeyword()`,
`applyFilters()`, and `indexResource()` methods makes the Elasticsearch integration
an explicit architectural concern rather than an implementation detail. The trade-off
is one more class; the benefit is that the class diagram accurately represents how
the search service interacts with resources — which matters for Assignment 8's
activity diagram on catalogue management.

---

## Lessons Learned About Object-Oriented Design

**Relationships are harder than classes.** Every class in the diagram was easy to
identify from the requirements. The relationships — particularly deciding between
aggregation and composition, or choosing the correct multiplicity — required
understanding the business rules, not just the requirements text. Domain modeling
taught me that UML relationship types are not cosmetic choices; they encode business
logic.

**Business rules are the hidden requirements.** The ten business rules documented in
DOMAIN_MODEL.md are not explicitly stated in any single functional requirement in
Assignment 4. They emerge from combining requirements — BR-02 (borrowing blocked at
R100) comes from FR-03's acceptance criteria; BR-10 (fine calculation formula) is
implied but never stated. Domain modeling forces these implicit rules to the surface
where they can be validated and agreed upon before implementation begins.

**The class diagram is a contract.** Once written, the class diagram defines what
every developer on the team must implement. Method signatures, attribute types, and
relationship multiplicities become binding agreements. This experience gave me a new
appreciation for why enterprise software teams invest heavily in domain modeling
before writing code — a wrong relationship in the class diagram is far cheaper to fix
on paper than in a running system with thousands of records.

**Agile and domain modeling complement each other.** Agile methodology might seem
to conflict with upfront domain modeling — "working software over comprehensive
documentation." But the domain model and class diagram are not documentation for its
own sake; they are design tools that enable faster, more confident implementation
of Sprint 2 and Sprint 3 user stories. US-003 (Borrow/Reserve a book) can only be
implemented correctly if the developer knows the exact relationship between Student,
Loan, Resource, Reservation, Fine, and Notification. The class diagram provides that
knowledge in a format that takes minutes to read and saves hours of confused
implementation.
