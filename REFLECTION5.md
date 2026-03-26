# REFLECTION5.md — Challenges in Translating Requirements to Use Cases and Tests
## Smart Academic Library Assistance System (SALAS)

> Assignment 5: Reflection  
> Building on Assignments 3, 4 & 5 — SALAS  
> Version: 1.0 | Date: March 2026

---

Translating the stakeholder concerns and system requirements from Assignment 4 into use case diagrams, specifications, and test cases was a significantly different kind of challenge from writing requirements. Requirements describe *what* the system must do; use cases and tests must describe *how* it does it, *who* initiates it, and *how we know* it worked. Bridging that gap revealed several tensions and difficulties that are worth reflecting on in depth.

## Challenge 1: Deciding the Right Level of Granularity for Use Cases

The first and most persistent challenge was deciding how detailed each use case should be. On one extreme, every button click could be its own use case. On the other extreme, "Student uses the library system" could be one giant use case that captures nothing useful. Finding the right level of abstraction required several iterations.

For example, "Search Library Catalogue" (UC02) initially included authentication, filtering, viewing results, and borrowing — all in one flow. This was too broad to be useful for testing or implementation. Breaking it apart into UC02 (Search), UC03 (Borrow/Reserve), and connecting them with include/extend relationships produced a much cleaner model. However, drawing these lines required a deep understanding of which steps were truly independent actions and which were mandatory sub-steps — a distinction that is not always obvious from requirements alone.

The lesson learned is that use case granularity should be driven by *actor intent*: each use case should represent one complete, meaningful goal a user is trying to achieve. If you can describe the goal in one sentence from the actor's perspective, you have the right level.

## Challenge 2: Modelling the Recommendation Engine as an Actor

A non-obvious challenge arose with the Recommendation Engine. Unlike the other actors (students, librarians, admins), the Recommendation Engine is not a human — it is an automated internal service. Standard UML use case diagrams typically show external actors, but the Recommendation Engine clearly initiates use case UC05 (Receive Personalized Recommendations) from the system's perspective.

The decision to include it as a system actor was justified by the fact that it operates independently on a schedule and produces outputs that affect what students see. Treating it as a secondary actor with a dashed boundary correctly communicates that it is an automated participant. This was a judgment call that required going back to the stakeholder analysis from Assignment 4, where the Data Science Team was identified as a distinct stakeholder with its own concerns — confirming that the recommendation pipeline deserved representation in the use case model.

## Challenge 3: Writing Meaningful Alternative Flows

Writing the basic flow of each use case was straightforward — it is essentially the happy path. The real difficulty was in alternative flows. The temptation is to write alternative flows only for obvious error cases (wrong password, book not found), but truly useful alternative flows cover edge cases that are only discovered by thinking adversarially about the system.

For instance, the race condition in UC03 (Borrow a Book) — where the last copy of a book is taken between the moment a student clicks "Borrow" and the moment the server processes the request — was not captured in any of the Assignment 4 requirements. Modelling the use case forced this scenario to the surface. Without an alternative flow to handle it, the system would either show a confusing error or silently fail. Writing the use case specification effectively acted as a requirements gap analysis, revealing an implicit requirement that had been missed.

This experience reinforced that use case specifications are not just documentation of what has already been decided — they are a discovery tool that surfaces hidden requirements and ambiguities.

## Challenge 4: Designing Testable Test Cases

The move from use cases to test cases introduced a different challenge: specificity. A use case can describe a flow at a relatively high level. A test case must be precise enough for someone who has never seen the system to execute it and produce a binary pass/fail result. This meant every test case needed concrete data (e.g., "enter password `Test@1234`"), specific navigation paths, measurable expected outcomes, and unambiguous success criteria.

The non-functional test cases were particularly difficult to specify. NFR-07 (1,000 concurrent users) sounds straightforward until you try to write a test for it. What tool do you use? How do you ramp users up? What exactly do the virtual users do? What counts as a "pass"? Each of these questions had to be answered explicitly, turning a one-line NFR into a multi-step test procedure. The process of writing TC-NFR-01 alone clarified several aspects of the performance requirement that had been left implicit in the SRD.

## Challenge 5: Maintaining Traceability Across Three Assignments

A recurring structural challenge across this assignment was maintaining consistency with Assignments 3 and 4. Every use case had to align with a functional requirement from the SRD. Every test case had to reference a requirement ID. Every actor had to correspond to a stakeholder from the stakeholder analysis. When any element was added or adjusted in Assignment 5, it had the potential to create inconsistencies upstream.

For example, when writing UC06 (Manage Library Catalogue), the bulk CSV import alternative flow was added — but this feature was already listed in FR-06's acceptance criteria from Assignment 4, so it was consistent. However, the export timeout scenario in UC08 (Generate Reports) extended beyond what FR-08 explicitly covered, requiring a judgment call about whether to add it as an implicit requirement or leave it as an implementation detail.

Managing this traceability manually across five documents is already challenging; in a real project with dozens of requirements and hundreds of test cases, this is where requirements management tools like Jira, Confluence, or dedicated traceability matrices become essential. This assignment gave a concrete appreciation for why such tooling exists.

## Conclusion

The process of creating use case diagrams, specifications, and test cases for SALAS demonstrated that requirements engineering is not a linear process. Each artifact — stakeholder analysis, SRD, use case model, test cases — feeds back into the others, revealing gaps and ambiguities that were invisible at earlier stages. The most valuable outcome of this assignment was not the documents themselves, but the thinking that producing them forced.
