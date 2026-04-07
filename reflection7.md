# reflection7.md — Reflection on Kanban Board Implementation
## Smart Academic Library Assistance System (SALAS)

> Assignment 7: Reflection
> Building on Assignments 3–6 |12 April 2026

---

## Challenges in Selecting and Customizing the Template

The first challenge in this assignment was resisting the instinct to choose the most
feature-rich template available. The Team Planning template has five columns and looks
impressive, but when I mapped it against the SALAS sprint plan from Assignment 6, its
columns did not align cleanly with the workflow I had already defined. Choosing a
template because it looks comprehensive, rather than because it fits the actual work,
is a trap that wastes more time in customization than it saves in structure.

The Automated Kanban was the right choice not because it was the most sophisticated,
but because it was the most appropriate, its automation matched exactly the
PR-based development workflow I intended to use for SALAS, and its simplicity left
room for meaningful customization rather than requiring me to undo structure that did
not apply.

The customization itself presented a different kind of challenge. Adding the Testing
column was straightforward to justify, the Definition of Done in AGILE_PLANNING.md
explicitly requires acceptance criteria verification before a story is closed, so
Testing had to be a visible stage. The Blocked column was harder to justify to myself
because it felt pessimistic: why plan for things going wrong before development has
even started? But the dependencies between SALAS stories, particularly US-003
depending on US-001, and US-005 depending on sufficient data from US-003, make
blocking a real, predictable risk rather than a hypothetical one. A board that has
no way to represent blocked work is a board that lies about the state of the project.

The most difficult part of the customization was deciding what NOT to add. There was
a temptation to add columns for "Code Review," "Deployed to Staging," and
"Awaiting Feedback," all of which would be appropriate in a real production team.
But for a solo academic project, those columns would have no cards in them for
most of the sprint, making the board cluttered rather than clear. Kanban's power
comes from simplicity, a board with eight columns where six are always empty is
worse than a board with five columns that accurately reflects where the work is.

---

## Comparing GitHub Projects to Other Tools

Having worked through this assignment using GitHub Projects, it is useful to compare
it against the two most commonly used alternatives: Trello and Jira.

**GitHub Projects vs Trello**

Trello is more visually polished and easier to set up for someone new to Kanban. Its
drag-and-drop interface is more intuitive than GitHub Projects, and it supports
custom backgrounds, card covers, and power-ups that make boards more engaging.
However, Trello is a standalone tool with no native connection to code. When managing
a software project, linking a Trello card to a GitHub commit or pull request requires
third-party integrations or manual updates. GitHub Projects eliminates this problem
entirely, every card is a GitHub Issue, every Issue can be linked to a PR, and the
board updates automatically when code events happen. For SALAS, where every user
story already exists as a GitHub Issue with labels and milestones, GitHub Projects
is the natural choice. Using Trello would mean maintaining two systems in parallel,
which introduces inconsistency and wastes time.

**GitHub Projects vs Jira**

Jira is the industry standard for enterprise Agile project management and is
significantly more powerful than GitHub Projects. It supports custom workflows,
story point tracking, burndown charts, velocity reporting, epic and story hierarchies,
and deep integration with CI/CD pipelines. For a large team managing hundreds of
stories across multiple sprints, Jira's reporting capabilities are indispensable.

However, Jira's power comes with significant complexity. Setting up a Jira project
correctly, defining issue types, workflows, screens, and permission schemes can
take days and requires a dedicated project administrator. For SALAS, which has 14
user stories and a single developer, this overhead is completely disproportionate
to the size of the project. GitHub Projects provides 80% of what Jira offers for
sprint planning at 10% of the setup cost. The automation features, milestone
integration, and label-based filtering in GitHub Projects are sufficient for the
SALAS workflow at this stage of development.

The honest conclusion is that tool choice should be driven by team size, project
complexity, and existing infrastructure. GitHub Projects is the right tool for SALAS
now. If SALAS grew into a real product with a five-person development team, migrating
to Jira would be a reasonable decision but that migration should be triggered by
actual need, not by the assumption that more powerful tools are always better.

---

## Lessons Learned

**Fit over features.** The best template is the one that matches your actual
workflow, not the one with the most columns or automation rules.

**Make problems visible.** The Blocked column taught me that good project management
tools do not hide problems they surface them so they can be resolved quickly.
A board that always looks green is not a healthy project; it is a project with
hidden problems.

**Simplicity is a feature.** A Kanban board with fewer, well-used columns is more
useful than one with many columns that are rarely populated. The discipline of
deciding what not to include is as important as deciding what to include.

**Tooling should follow process.** I initially tried to fit the SALAS workflow into
the template rather than fitting the template to the workflow. When I reversed this
and started from the sprint plan in AGILE_PLANNING.md, the right customizations
became obvious immediately.
