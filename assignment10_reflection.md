# assignment10_reflection.md — Reflection on Code Implementation and Creational Patterns
## Smart Academic Library Assistance System (SALAS)

> Assignment 10: From Class Diagrams to Code with All Creational Patterns
> Building on Assignments 3–9 |03 May 2026

---

## Challenge 1: Translating UML to Working Code

The most immediate challenge when moving from the class diagram in
Assignment 9 to actual Python code was confronting the gap between
UML notation and language-specific implementation details. UML is
language-agnostic, it shows that Student "owns" ReadingList via
composition, but it does not tell you whether ReadingList should be
instantiated in Student's `__init__`, passed as a constructor argument,
or lazily created on first access.

Every design decision that was clean in the diagram became a concrete
question in code. The `+borrowResource()` method on Student shows it
returns a Loan, but the diagram does not show whether the Loan is also
stored on the Student, on the Resource, or in a separate repository.
Making this explicit in code revealed that Loan needs to be stored on
both the Student (to check eligibility) and referenced by Resource (to
block deletion with active loans). The bidirectional reference that was
implicit in the UML relationship had to be made explicit in code.

This translation process is genuinely useful because it forces decisions
that good design requires but that diagrams allow you to defer. Every
ambiguity in the class diagram becomes a compiler error or a failed test.

---

## Challenge 2: Choosing the Right Creational Pattern for Each Problem

Each of the six patterns solves a different object-creation problem, and
the challenge was identifying which problem existed in SALAS rather than
forcing patterns onto the system where they did not fit.

The **Simple Factory** for UserFactory was the most natural fit — the
system needs to create either a Student or Librarian based on a role
string that arrives from an API request. One central place to make that
decision is exactly what Simple Factory provides.

The **Singleton** for DatabaseConnection was also clear — only one
connection pool should ever exist. But implementing it correctly in
Python was harder than expected. The standard pattern of calling
`cls.__new__(cls)` and then `cls.__init__()` created a problem: the
`__init__` method includes a guard that raises `RuntimeError` when
called after the instance exists, which is exactly what the second
`__init__` call was triggering. The fix — using `object.__new__(cls)`
and a private `_init()` method — taught me that Python's object
construction model separates allocation (`__new__`) from initialisation
(`__init__`) in a way that UML class diagrams do not represent at all.

The **Builder** for Resource was the pattern I initially resisted most.
A constructor with 8 parameters is ugly but functional. The Builder
pattern adds more code (a separate builder class, a director class) for
what feels like a cosmetic improvement. But writing the tests changed my
view — testing a Builder-constructed Resource is dramatically cleaner
than testing one built with positional arguments. `ResourceBuilder("r1",
"Title", "Author", "ISBN").with_copies(3).with_genre("Fiction").build()`
is self-documenting in a way that `Resource("r1", "Title", "Author",
"ISBN", "Fiction", 2024, 3, "Shelf")` is not.

---

## Challenge 3: Test-Driven Discovery of Implementation Bugs

Writing unit tests before the implementation was complete exposed two
bugs that would not have been caught by manual testing:

The **Singleton double-init bug** only manifests in tests because the
test fixture calls `reset_instance()` between tests. In production, the
singleton is only initialised once and the bug never fires. But with
tests resetting state between each test case, the second call to
`get_instance()` after a reset was triggering `__init__` on the newly
created object, which raised the guard exception. This is the exact
scenario that thread-safety also requires handling — two concurrent
threads calling `get_instance()` simultaneously. The fix (using
`object.__new__` and a private `_init`) was more correct than the
original pattern.

The **ISBN edge case** (all-zeros passing ISBN-10 validation) was a
genuine implementation oversight. The ISBN-10 algorithm computes
`sum((10-i) * digit[i] for i in range(9)) + check_digit` and checks
if it's divisible by 11. All zeros gives 0, which is divisible by 11.
The fix was using a truly invalid ISBN in the test. But more
importantly, this revealed that the business rule "ISBN must be valid"
requires more rigorous test coverage than one happy-path test and one
trivially-invalid input.

---

## Alignment with Previous Assignments

The implementation aligns directly with every prior assignment:

The **state diagrams from Assignment 8** became method implementations.
The `Loan` state machine (Active → DueSoon → Overdue → Returned →
Archived) maps to `isOverdue()`, `calculateFine()`, `returnLoan()`, and
`archiveLoan()`. The guard condition `fineExceedsR100` became
`Fine.is_borrowing_blocked()` and the `Student.is_eligible_to_borrow()`
check.

The **activity diagrams from Assignment 8** became method sequences.
The Return Book activity diagram (scan ISBN → check if on loan → check
if overdue → calculate fine → update inventory → check queue) maps
directly to `Librarian.process_return()` calling `Loan.return_loan()`
which calls `Fine.calculateAmount()` and `Resource.return_resource()`.

The **user stories from Assignment 6** drove the test cases. US-003
(Borrow/Reserve a book) generated tests for eligibility blocking, fine
threshold enforcement, inventory decrement, and confirmation.

---

## Lessons Learned

**Creational patterns are about managing complexity, not adding it.**
Each pattern I initially saw as "extra code" turned out to solve a
real problem I encountered during implementation. The Builder made
Resource construction testable. The Factory Method made notification
creation extensible. The Singleton prevented a class of concurrency bug.

**Tests are the best documentation.** The 108 unit tests document every
business rule, every edge case, and every expected behaviour in
executable form. When a new developer joins the project, reading the
test file tells them what the system does more accurately than any
written specification.

**The distance between design and code is where bugs live.** Every
ambiguity left in the class diagram, every implicit relationship, every
unstated business rule, became a potential bug in implementation. The
domain model and class diagram from Assignment 9 were excellent starting
points, but the code forced every deferred decision to be made explicit.
