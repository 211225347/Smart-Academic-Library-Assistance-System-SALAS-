# REFLECTION15.md — Cross-Project Collaboration Reflection
## Smart Academic Library Assistance System (SALAS)

> Assignment 15: Cross-Project Contributions
> Version: 1.0 | May 2026

---

## Lessons Learned About Open-Source Collaboration

Contributing to peers' repositories was a fundamentally different
experience from writing code for my own project. When I work on SALAS,
I know every file, every design decision, and every business rule. When
I open a classmate's repository, I start from zero — I do not know
their naming conventions, their architecture, their testing patterns,
or the history behind their design choices. This unfamiliarity is
uncomfortable, but it is precisely the condition that all open-source
contributors face, and navigating it taught me more about software
engineering than any amount of solo coding could.

The most important lesson was this: **reading is most of the work**.
Before writing a single line of code for a peer's project, I read their
CONTRIBUTING.md, their README, their domain model documentation, and
several existing test files to understand their patterns. This reading
took longer than writing the actual code. I initially resisted this —
it felt like procrastination. But the first time I skipped it and went
straight to coding, I submitted a PR that used a different naming
convention from the rest of the project and a different assertion style
from their existing tests. The maintainer had to ask me to rewrite it.
After that, I never skipped the reading phase again.

The second lesson was about **scope discipline**. My instinct when
looking at a peer's codebase was to notice many things that could be
improved and try to fix them all in one PR. This is the wrong approach.
A PR that changes five unrelated things is harder to review, easier to
reject, and creates a larger surface area for conflicts if the
maintainer is also making changes. After receiving feedback on my first
large PR, I learned to scope every contribution to a single, clearly
described change. "Add 404 error handling to UserService" is a good
scope. "Improve error handling and add tests and update documentation"
is three PRs pretending to be one.

---

## Challenges in Contributing Across Codebases

The most practical challenge was environment setup. Every project had
different dependencies, different Python versions, different test
configurations. Some had `requirements.txt`, some had `pyproject.toml`,
some had neither — I had to infer dependencies from import statements.
The CONTRIBUTING.md file makes this dramatically easier, which is why
I invested so much time in SALAS's CONTRIBUTING.md in Assignment 14.
The projects that had clear, step-by-step setup instructions in their
CONTRIBUTING.md received contributions from me much more quickly than
those that did not.

The second challenge was the CI pipeline. Several peers' CI pipelines
were failing before I even made a change — the same issue I experienced
with SALAS in Assignment 13 (test files not committed to the repo).
This created a dilemma: should I fix the CI pipeline in my PR (which
would mix infrastructure changes with feature changes), or should I
comment on the issue and wait for the maintainer to fix it first? I
chose the latter for code changes and offered to submit a separate PR
just for the CI fix.

The third and most human challenge was **waiting**. Open-source
collaboration operates on unpredictable timelines. I submitted PRs
and then had to wait for the maintainer to review them — sometimes
for several days. This is normal in real open-source projects where
maintainers are volunteers with competing demands. But in an academic
context with a deadline, it creates real pressure. The lesson here is
to submit PRs early, follow up politely after 3 days if there is no
response, and never wait for one PR to merge before submitting the next.

---

## How Contributing Changed How I Think About My Own Code

The experience of contributing to peers' projects changed how I think
about the code I write for SALAS. Specifically, it made me more
deliberate about three things.

**Consistency over cleverness.** When contributing to a peer's project,
I matched their style even when I thought mine was better. A codebase
where 95% of methods use one pattern and 5% use a "better" pattern is
harder to maintain than one where 100% use the same pattern. I came
back to SALAS and found several places where I had been inconsistent
in my own code — method names that did not follow `verb_noun` pattern,
some classes with docstrings and some without. I fixed these not
because they were bugs but because consistency is a form of respect for
future contributors.

**Error messages as documentation.** Peers kept asking me what certain
error messages meant in my code. "User not found" is clear. "Invalid
state" is not. Reviewing peers' code made me realise that error messages
are a form of documentation that you write once and your users and
contributors read many times. I updated SALAS's custom exceptions to
include more specific messages after seeing how much time peers spent
trying to interpret vague ones.

**The test as a specification.** The most valuable part of my
contributions to peers' projects was not the code I added but the
tests I wrote. Tests force you to state precisely what you expect the
code to do in each scenario, which reveals ambiguities in requirements
that prose descriptions hide. In three separate cases, writing a test
for a peer's codebase revealed that their implementation did not match
their stated requirements — not because of a bug, but because the
requirement was ambiguous and the implementation had resolved the
ambiguity one way while the intended behaviour required a different
resolution. This happened to me in my own SALAS code too — the act of
writing the test exposed the misalignment.

---

## Conclusion

Assignment 15 completed a cycle that started in Assignment 3. Writing
requirements, designing systems, modelling behaviour, implementing
code, testing it, deploying it, documenting it for contributors, and
then actually contributing to others' code as a peer — each stage
built on the previous one in ways that only became clear in retrospect.

The most enduring lesson is that software engineering is a social
activity. The code is almost the least important part. The important
parts are the communication — in issue comments, PR descriptions,
review responses, and documentation — that allows multiple people to
build something together that none of them could build alone.
