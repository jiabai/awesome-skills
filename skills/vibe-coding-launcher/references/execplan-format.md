# ExecPlan Format Standard

## Contents

- [Required Sections](#required-sections)
- [Section Requirements](#section-requirements)
- [First ExecPlan](#first-execplan)
- [Completion and Archival](#completion-and-archival)
- [docs/exec-plans Templates](#docsexec-plans-templates)
- [Advanced Development Loop](#advanced-development-loop)

---

## Required Sections

Every plan contains:

```markdown
# <Short, Action-Oriented Description>

This ExecPlan is a living document and the execution source of truth while active. The sections Progress, Surprises & Discoveries,
Decision Log, and Outcomes & Retrospective must be kept up to date as work proceeds.

## Purpose / Big Picture
What new thing can the user do afterward, and how can they see it work?

## Progress
- [ ] Incomplete milestone with timestamp

## Surprises & Discoveries
New facts, evidence, and impact discovered during the work.

## Decision Log
Important decisions, rationale, date, and author.

## Outcomes & Retrospective
Actual results, validation, residual risk, and follow-up work.

## Context and Orientation
Current state, key files, terminology, and prerequisite context.

## Plan of Work
Ordered implementation batches.

## Concrete Steps
Working directory, complete commands, and expected output.

## Validation and Acceptance
Startup instructions, observable behavior, test commands, and expected results.
```

## Section Requirements

**Purpose / Big Picture:** In one or two sentences, answer what new capability the user gains and how they will observe it. Describe user-visible outcomes, not technical details.

**Progress:** List every milestone with `- [ ]`; change to `- [x]` with a timestamp when complete. A milestone is a verifiable sub-feature, such as "API framework ready" or "database schema complete," corresponding to a batch of execution tasks in root TASKS.md or a sibling task file. Mark it complete only when all corresponding tasks and validation pass.

**Surprises & Discoveries:** Record newly discovered facts with Evidence. Never present a guess as a conclusion.

**Decision Log:** Record choices that affect future maintenance. Recommended fields: Decision / Rationale / Date / Author.

**Outcomes & Retrospective:** Update when the plan completes, is abandoned, or is superseded. State what was completed, what was and was not validated, and remaining risk.

**Context and Orientation:** List relevant paths and why they matter. In recovery mode, read this and Progress first.

**Plan of Work:** Describe implementation batches so humans can review scope.

While active, follow the approved plan's scope, sequence, acceptance, validation, and constraints. Record approved deviations in the Decision Log before implementing them.

**Concrete Steps:** Every step names its working directory relative to project root, a complete copyable command, and representative expected output. Write `pip install flask`, not "run the install command."

**Validation and Acceptance:** Include how to start the project, observable behavior, test commands, and expected results.

## First ExecPlan

Start with the smallest runnable version:

- Web app: one accessible page returning "Hello World."
- API service: `/health` returns 200.
- CLI: one command that prints help.
- AI application: one script that calls the API and returns a result.
- Single-file script: one `main` function that runs and prints output.

Save under `docs/exec-plans/active/` as `YYYY-MM-DD-short-description.md`.

## Completion and Archival

After a plan completes:

1. Update `Outcomes & Retrospective` with passed validation, checks not run, and residual risks.
2. Move the file from `docs/exec-plans/active/` to `docs/exec-plans/completed/`.
3. Update `active/index.md` and `completed/index.md`.
4. Record cross-task technical debt in `docs/exec-plans/tech-debt-tracker.md`.
5. Do not leave completed plans in `active/`.

## docs/exec-plans Templates

### index.md

```markdown
# Exec Plans

## Purpose

Exec plans capture task-specific implementation intent, progress, and recovery context.

## Entry Points

- Active plans: `active/index.md`
- Completed plans: `completed/index.md`
- Shared debt list: `tech-debt-tracker.md`

## Rules

- Keep active work in `active/`.
- Move completed work to `completed/`.
- Capture cross-cutting debt in `tech-debt-tracker.md`.
```

Both `active/index.md` and `completed/index.md` list File and Focus:

```markdown
# {Active|Completed} Exec Plans

| File | Focus |
|------|-------|
```

### tech-debt-tracker.md

```markdown
# Tech Debt Tracker

Last updated: {YYYY-MM-DD}

## High Priority

| Topic | Why it matters | Source | Removal Condition |
|-------|----------------|--------|-------------------|

## Medium Priority

| Topic | Why it matters | Source | Removal Condition |
|-------|----------------|--------|-------------------|

## Debt Handling Rules

- Add debt here when it spans more than one file or more than one task.
- Remove or downgrade debt when a change clearly addresses it.
- Link back to the plan, design document, or code path that best explains the issue.
```

## Advanced Development Loop

After the first ExecPlan and once routine iteration begins, adopt:

```
Describe task → Run agent against ExecPlan → Validate → Address feedback → Merge
```

| Principle | Meaning |
|-----------|---------|
| Short lifecycle | Each ExecPlan covers one feature and finishes quickly |
| Minimum blocking | One failed test does not block unrelated progress; address it in the next run |
| Corrections are cheap; waiting is expensive | Finish, then optimize; avoid perfectionism |
| Agent self-review | The agent runs lints and tests before human review |

Routine ExecPlans may omit Context and Orientation because AGENTS.md already provides it, but Purpose, Progress, Concrete Steps, and Validation remain mandatory.
