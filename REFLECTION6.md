# REFLECTION6.md — Agile Planning Reflection
## Smart Academic Library Assistance System (SALAS)

> Assignment 6: Reflection
> Version: 1.0 | Date: March 2026

---

## Challenges in Prioritization, Estimation, and Aligning Agile with Stakeholder Needs

Working through Assignment 6 — translating the requirements and use cases from Assignments 4 and 5 into a structured Agile backlog and sprint plan — revealed a set of internal tensions that are worth reflecting on honestly. The assignment note acknowledges that in a real project, Scrum roles are played by different people. As the sole developer, product owner, and Scrum master simultaneously, I found that the conflicts these roles normally resolve through team discussion had to be resolved entirely within my own reasoning. That internal negotiation turned out to be one of the most instructive parts of the process.

## The Prioritization Paradox

The first and most persistent challenge was prioritization. MoSCoW forces you to make binary decisions — a feature is either Must-have or it isn't — but the reality is that almost every feature felt important when I was the one who had designed it from the ground up across three prior assignments. I had a personal stake in every user story because I had been the one to write the requirements they came from.

The internal resistance was strongest around US-005 (Personalized Recommendations), which I downgraded to Should-have with 8 story points. The recommendation engine is architecturally one of the most interesting parts of SALAS — it was a central selling point in the original specification. Deprioritizing it felt like betraying the vision of the system. But when I applied the product owner mindset rigorously — asking "can the system deliver value to students without this?" — the answer was clearly yes. Students can search, borrow, and return books without recommendations. The librarian can manage the catalogue. The core library function works. The recommendation engine is an enhancement, not a foundation, and placing it in Sprint 1 would have consumed resources that the must-have features needed.

This tension between the designer's attachment to features and the product owner's responsibility to deliver working software early is something I now understand experientially rather than theoretically.

## The Estimation Problem

Estimating story points without a team was genuinely difficult. Story point estimation in Scrum is supposed to be a social process — Planning Poker exists because individual estimates are unreliable and team discussion surfaces hidden complexity. Without a team, I had to estimate entirely from my own reading of the technical requirements.

The story that caused the most internal debate was US-001 (Search Library Catalogue), which I estimated at 5 points. Elasticsearch integration, API endpoint development, real-time availability enrichment, and a React search UI are four distinct technical workstreams. A more cautious estimate might have been 8 or even 13 points. I settled on 5 because I was trying to keep Sprint 1 achievable — but I am aware that this might reflect optimism bias rather than genuine technical assessment. In a real Scrum team, someone with Elasticsearch experience would likely push back on a 5-point estimate and the discussion would produce a more accurate number.

The lesson here is that solo estimation is structurally biased toward underestimation. You tend to estimate based on how long it would take if everything goes right, which is almost never how software development works.

## Aligning Agile with Upfront Documentation

A deeper tension ran through the entire assignment: Agile methodology values working software over comprehensive documentation, yet this entire project has been documentation-only for six assignments. Writing a sprint plan for code that doesn't exist yet — and that I am not immediately going to write — felt like going through the motions of Agile without the substance of it.

The honest internal resistance here was to the artificiality of the exercise. Real sprint planning is valuable because it commits a team to delivering specific working functionality within a fixed timebox, with daily standups, impediment removal, and a sprint review where stakeholders see running software. None of that feedback loop exists here.

What I found useful, despite this artificiality, was that the sprint planning process forced a level of specificity about implementation that the requirements phase did not. Writing Task T-004 ("Implement account lockout after 5 failed login attempts using Redis counter") required me to think about *how* the feature would actually be built — what technology, what endpoint, what data structure — in a way that "FR-01: The system shall support JWT authentication" did not. The task breakdown is where requirements meet reality, and that translation exercise has genuine value even in a solo academic context.

## What I Would Do Differently

If I were starting the Agile planning phase again, I would use GitHub Projects from the beginning of the assignment rather than treating it as a submission step at the end. Creating issues, labelling them, assigning story points, and organizing them into a project board as I wrote the backlog would have made the process feel more authentic and would have produced better-organized traceability between the GitHub Issues and the markdown documents.

I would also set a stricter sprint velocity cap earlier — the temptation to include more stories in Sprint 1 to make the plan look comprehensive had to be actively resisted. A sprint that overcommits is worse than one that undercommits, because overcommitment normalizes missed targets.

Agile, at its core, is about honest self-assessment: what can we actually deliver, what have we learned, and how do we improve? This reflection is my attempt to apply that principle to the planning process itself.
