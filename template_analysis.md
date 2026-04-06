# template_analysis.md — GitHub Project Template Analysis
## Smart Academic Library Assistance System (SALAS)

> Assignment 7: GitHub Project Templates and Kanban Board Implementation
> Building on Assignments 3–6 | Version 1.0 | April 2026

---

## 1. GitHub Project Template Comparison

The following table compares four GitHub project templates evaluated for use in managing
the SALAS sprint backlog and Agile workflow.

| Feature | Basic Kanban | Automated Kanban | Bug Triage | Team Planning |
|---|---|---|---|---|
| **Default Columns** | To Do, In Progress, Done | To Do, In Progress, Done | Needs Triage, High Priority, Low Priority, Closed | Backlog, Ready, In Progress, In Review, Done |
| **Number of Columns** | 3 | 3 | 4 | 5 |
| **Automation** | None — all movement is manual | Auto-moves issues to In Progress when a PR is opened; auto-moves to Done when PR is merged or issue is closed | Auto-moves closed issues to Closed column | No automation — manual movement |
| **Issue Linking** | Manual | Automatic via PR and issue events | Manual | Manual |
| **WIP Limits** | Not built-in | Not built-in | Not built-in | Not built-in |
| **Milestone Support** | Yes | Yes | Yes | Yes |
| **Label Support** | Yes | Yes | Yes | Yes |
| **Best For** | Simple personal projects with no automation needs | Teams using pull requests frequently; CI/CD workflows | Open source projects managing bug reports | Large teams planning across multiple sprints |
| **Agile Suitability** | Low — no sprint tracking, no automation | High — aligns with iterative development and PR-based workflows | Medium — useful for QA but not general sprint management | High — supports full sprint lifecycle but requires customization |
| **Customization Needed** | High — needs many columns added | Low — minor additions needed | High — needs full restructure for sprint work | Medium — needs Testing and Blocked columns |

---

## 2. Chosen Template: Automated Kanban

### Justification

The **Automated Kanban** template was selected for the SALAS project for the following reasons:

**Automation reduces manual overhead.** As a solo developer managing all Scrum roles simultaneously, automation is critical. The Automated Kanban template automatically moves issues to "In Progress" when a linked pull request is opened, and to "Done" when the PR is merged or the issue is closed. This eliminates the risk of forgetting to update the board and keeps the workflow accurate with zero extra effort.

**Alignment with sprint-based development.** SALAS follows a sprint structure defined in Assignment 6 with Sprint 1 focusing on authentication and search. The Automated Kanban maps directly to this — each user story (GitHub Issue) progresses from To Do → In Progress → Done as development proceeds, mirroring the sprint lifecycle.

**Issue and PR traceability.** All 14 user stories from Assignment 6 already exist as GitHub Issues with labels, milestones, and story points. The Automated Kanban integrates directly with these Issues, giving a live view of sprint progress without maintaining a separate tracking system.

**Extensibility.** The base template's three columns are a clean foundation that can be extended with custom columns (Testing, Blocked, In Review) to reflect the full SALAS development workflow without overcomplicating the board.

**Industry relevance.** Automated Kanban mirrors the workflow used by professional engineering teams on GitHub. Learning this template directly prepares for real-world Agile collaboration.

### Why the other templates were not chosen

- **Basic Kanban** was rejected because it has no automation, requiring every card to be moved manually. This introduces human error and is inefficient for a project already using GitHub Issues and PRs.
- **Bug Triage** was rejected because it is designed for managing defect reports, not sprint planning. Its columns (Needs Triage, High Priority, Low Priority) do not map to SALAS's development workflow.
- **Team Planning** was rejected because it requires significant customization to match a sprint model and does not offer automation. Its five-column structure adds complexity without adding value for a solo project.
