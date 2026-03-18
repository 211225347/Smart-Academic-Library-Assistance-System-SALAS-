# REFLECTION.md Challenges in Balancing Stakeholder Needs
## Smart Academic Library Assistance System (SALAS)

> Assignment 4: Reflection  
> Building on Assignment 3 SALAS

---

## Introduction

Conducting stakeholder analysis and requirements elicitation for SALAS revealed that building a system for multiple user groups is far more complex than building for a single audience. Each stakeholder brings legitimate but sometimes contradictory needs, and navigating these trade-offs required careful prioritization and creative compromise. This reflection documents the key challenges encountered and the reasoning behind the decisions made.

---

## Challenge 1: Student Privacy vs. Recommendation Engine Data Needs

One of the most significant tensions was between **students' right to data privacy** and the **Data Science team's need for rich behavioral data** to build an effective recommendation model.

Students and university administrators (under POPIA compliance obligations) want minimal personal data collected and the right to have all data deleted upon request. The recommendation engine, however, depends on detailed borrowing history, search patterns, and course enrollment data to produce meaningful suggestions, the more data, the better the model.

**How I balanced this:**
The requirement was resolved by mandating full anonymization of all data before it enters the training pipeline (FR-05, NFR-11). Student profiles used for model training are pseudonymized with no direct identifiers. A cold-start solution was also added: new students with no history receive course-based default recommendations, reducing the pressure to collect personal data immediately. The right to erasure is implemented as a "delete my data" feature that removes personal records within 30 days, while anonymized aggregate signals may be retained.

---

## Challenge 2: IT Administrator's Uptime Requirements vs. Continuous Feature Delivery

IT administrators require **99.5% system uptime**, especially during peak academic periods like semester starts and exam weeks. However, the development team (and the Agile methodology being applied) requires the ability to deploy updates and new features frequently without lengthy downtime windows.

These goals conflict directly: frequent deployments introduce risk, and the most critical periods for uptime are exactly when the system is under the heaviest use.

**How I balanced this:**
The deployability requirements (NFR-03, NFR-06) were written to enforce a fully containerized, microservices-lite architecture where each service can be redeployed independently. This means a new version of the Recommendation Engine can be deployed without touching the REST API or the frontend. Blue-green deployment and rolling updates (achievable with Docker Swarm or Kubernetes) allow zero-downtime releases. A formal deployment freeze policy during exam periods (communicated to the team) was also recommended as a process-level safeguard.

---

## Challenge 3: Student Desire for Instant Notifications vs. IT Bandwidth Constraints

Students want **real-time push notifications** for every event: reservation confirmations, due date reminders, new arrivals in their area of interest, and recommendation updates. From a user experience perspective, immediacy drives engagement.

However, the IT administrator raised concerns about email delivery bandwidth and the cost of high-frequency notification systems during peak periods when thousands of students may trigger events simultaneously.

**How I balanced this:**
FR-07 was scoped to three specifically timed email triggers (3 days before due, on due date, 1 day after) rather than real-time push for every event. Students can configure their notification preferences to reduce volume. A daily digest model was implemented for librarians (one email per day) instead of per-event alerts. In-app notifications (served from a cached feed, not live push) were offered as an alternative to high-cost real-time delivery. This satisfies student engagement needs while keeping infrastructure costs and bandwidth manageable.

---

## Challenge 4: Librarian Efficiency vs. Data Integrity Controls

Librarians want a **fast, frictionless catalogue management tool**, they need to add, update, and delete resources quickly, especially during large new acquisitions. Imposing too many validation steps or confirmation dialogs slows them down significantly.

On the other hand, the university administrator and IT administrator need strong **data integrity controls**: accidental deletions, duplicate entries, and unvalidated ISBNs cause downstream problems in search accuracy, inventory counts, and reporting.

**How I balanced this:**
FR-06 introduces ISBN validation and bulk CSV import to speed up large data entry tasks, while the deletion block on resources with active loans prevents accidental removal of in-use items without adding friction to normal operations. Rather than confirmation dialogs for every action, a **soft-delete and undo window** approach was proposed, deletions are reversible within 60 seconds, after which they are committed. This gives librarians speed and trust without sacrificing data integrity.

---

## Challenge 5: Accessibility Requirements vs. Development Complexity

The accessibility stakeholder (students with disabilities) requires a fully WCAG 2.1 AA compliant interface. While this is ethically non-negotiable and legally important, implementing full accessibility, ARIA live regions, keyboard navigation, screen reader testing, sufficient contrast, significantly increases frontend development time and complexity for a solo developer.

**How I balanced this:**
Rather than treating accessibility as a post-launch audit, NFR-01 and FR-12 embed accessibility as a core requirement from the start. Using a React component library with built-in accessibility (such as Radix UI or Headless UI) means most accessibility patterns are handled at the component level without custom implementation. Automated Lighthouse CI checks are included in the deployment pipeline to catch regressions early. This approach makes accessibility achievable within solo development constraints while maintaining compliance.

---

## Key Lessons Learned

**Requirements conflict is normal.** Every stakeholder has legitimate needs. The job of a requirements engineer is not to pick a winner but to find solutions that partially satisfy all parties and clearly document the trade-offs made.

**Specificity prevents arguments.** Vague requirements like "the system should be fast" create ambiguity that leads to disputes during testing. Writing measurable acceptance criteria (e.g., "p95 search latency ≤ 2,000ms") forces clarity upfront and makes it impossible to argue about whether a requirement has been met.

**Priority frameworks help.** Using MoSCoW (Must Have / Should Have / Could Have / Won't Have) to categorize requirements made it easier to make trade-off decisions when stakeholder needs conflicted, lower-priority needs simply gave way to higher-priority ones rather than creating deadlock.

**Technical and human concerns are equally important.** The most interesting challenges in this assignment were not purely technical, they were human. Balancing a student's desire for personalization with their right to privacy, or a librarian's need for speed with an administrator's need for control, required empathy and design thinking as much as software engineering knowledge.
