# Workflow Governance and Completion Gates

This document answers three questions: how should governance documents be layered, which work requires a Spec, ExecPlan, and task checklist, and when may work be called complete?

## Document Layers

| Document | Responsibility | Rule |
|----------|----------------|------|
| `AGENTS.md` | Automatically loaded entry-point map | Keep concise: Quick Entry, core beliefs, common commands, and key constraint summaries |
| `WORKFLOW.md` | How the project advances tasks | Defines the default workflow and lightweight path |
| `docs/EXECUTION_GATES.md` | What counts as complete | Defines hard gates, soft gates, and final-delivery format |
| `docs/DESIGN.md` | Stable design standards | Long-lived design and code boundaries across features |
| `docs/SECURITY.md` | Stable security baseline | Generate for authentication, secrets, storage, permissions, or external input |
| `docs/design-docs/` | Durable design decisions | Cross-task architecture decisions, not chronological logs |
| `docs/product-specs/` | User-visible intent | Goals, scope, non-goals, scenarios, constraints, acceptance criteria |
| `docs/exec-plans/` | Implementation plans and recovery context | `active/` for current work; `completed/` for finished, cancelled, or superseded history |
| `docs/references/` | External material and interface references | LLM-friendly vendor docs, SOPs, and API descriptions |

AGENTS.md is an entry point, not an encyclopedia. Put detailed rules in `docs/` and link to them. Quick Entry lists only real relative paths. Update `index.md` when moving documents or adding indexed entries. Before describing implemented behavior as fact, inspect the corresponding code.

## Constitution

Before non-trivial work in a mature project, read the stable context: root `AGENTS.md`, `docs/design-docs/core-beliefs.md`, `docs/ARCHITECTURE.md` or the AGENTS.md Architecture section, `docs/DESIGN.md`, `docs/SECURITY.md`, and the nearest module-level `AGENTS.md` for the affected area.

In a small project with no separate `docs/`, put 3–5 core beliefs, architecture invariants, and security constraints in root AGENTS.md. Split them out only when the project grows.

## Default Five-Stage Workflow

Unless the task is clearly low risk:

1. **Constitution and context:** start at root AGENTS.md and read the narrowest relevant rules, architecture, security, and design baseline.
2. **Spec:** when work changes user-visible behavior, introduces a boundary, or affects security, data, or deployment, create or update `docs/product-specs/YYYY-MM-DD-<slug>.md`.
3. **Technical plan:** create `docs/exec-plans/active/<slug>-plan.md` describing file scope, sequence, validation, and decisions that must remain current.
4. **Task breakdown:** split the plan into small verifiable tasks; use `docs/exec-plans/active/<slug>-tasks.md` for a larger list.
5. **Implementation and validation:** inspect first, make the smallest end-to-end change, validate progressively, and keep the active ExecPlan current.

Pause for human confirmation after creating or materially changing a Spec or ExecPlan, or when a task breakdown exposes a decision that changes scope or risk. After explicit approval, execute the plan autonomously and pause again only for an external or irreversible action, a material scope or risk change, an unresolved error, or a missing decision. A task on the lightweight path may proceed without a planning pause when its intent is already clear.

## What Counts as Non-Trivial?

Any one condition makes the work non-trivial and requires a reviewable Spec and plan before implementation:

| Dimension | Criterion | Example |
|-----------|-----------|---------|
| User-visible impact | Changes behavior or experience | New feature, UI interaction, API response format |
| New boundary | Adds a product, architecture, data, deployment, or security boundary | New module, table, external service |
| Risk | Affects authentication, permissions, persistence, data safety, or deployment | Authentication or authorization logic |
| Scope | Changes multiple modules or directories | `ui/`, `service/`, and `repo/` together |
| Time | Estimated over 30 minutes | Multi-hour or multi-day feature |
| Architecture | Adds a layer, dependency direction, or abstraction | Pattern adoption or core refactor |

### Common Scenarios

| Scenario | Non-Trivial? | Workflow |
|----------|--------------|----------|
| Fix typo or adjust copy | ❌ | Lightweight |
| Change internals of one function without changing its interface | ❌ | Lightweight |
| Add API endpoint | ✅ | Full, with Spec |
| Refactor core module architecture | ✅ | Full, with design document |
| Change database schema | ✅ | Full, with Spec |
| Adjust UI styling without interaction changes | ❌ | Lightweight |
| Add user-visible functionality | ✅ | Full, with Spec |
| Change authentication logic | ✅ | Full, with Spec |
| Update a non-breaking dependency | ❌ | Lightweight |
| Cross-module refactor | ✅ | Full, with ExecPlan |

### Lightweight Path Conditions

Skip Spec → plan → tasks only when **all** conditions hold: low risk with no effect on authentication, permissions, data safety, or core functionality; one module or directory only with no shared interface/type changes; no new boundary; no substantive change to persistence, API contracts, or runtime behavior; estimated under 30 minutes.

The lightweight path still requires reading the constitution and nearest AGENTS.md, inspecting the affected code or documents, making the smallest end-to-end fix, running focused validation, and reporting passed checks, checks not run, and residual risk. Documentation or process changes still run document-structure validation.

## Product Spec Standard

Write a Product Spec first when work changes user-visible behavior, introduces a boundary, affects authentication/permissions/data/deployment/security, or requires human confirmation of feature scope. Name it `docs/product-specs/YYYY-MM-DD-<feature-slug>.md`.

### index.md Template

```markdown
# Product Specs Index

## Purpose

Product specs describe user-visible intent and boundaries before or alongside implementation work.

## Current Specs

| File | Scope |
|------|-------|
```

### Individual Spec Template

```markdown
# {Feature Title}

## Background

## Goals

## User Stories

{Numbered list: "As a <role>, I want <capability> so that <benefit>." Omit only when the project has not performed requirements elicitation.}

## Non-Goals

## Usage Scenarios

## Constraints

## Acceptance Criteria
```

Rules:

- A Spec says what is wanted and not wanted. Implementation progress belongs in the ExecPlan.
- Use canonical terms from `CONTEXT.md` when it exists; never drift to aliases marked Avoid.
- Update `docs/product-specs/index.md` when the index exists.

## ExecPlan Lifecycle

An active ExecPlan is the execution source of truth. Before formal coding, read the approved plan and its sibling task checklist when present; when no sibling exists, use the plan's `Progress` as the task checklist. Follow the plan's file scope, sequence, acceptance, validation, and constraints. Keep `Progress`, `Surprises & Discoveries`, `Decision Log`, and validation records current after each meaningful batch. If implementation requires a scope, sequence, acceptance, or constraint change, pause, update the active ExecPlan, and obtain approval before continuing.

After completion, move it to `docs/exec-plans/completed/`, update both indexes, and preserve validation results, residual risks, and follow-up work. Move cancelled or superseded plans to completed as well, with the reason recorded.

## Task Checklist Standard

The checklist may live in ExecPlan `Progress` or in `docs/exec-plans/active/<feature-slug>-tasks.md` beside the plan.

Every task is concrete and independently verifiable, names dependencies, identifies affected files or modules, and attaches validation expectations to every meaningful batch. Use root `TASKS.md` for execution-level tasks. Never duplicate the same granularity in two locations.

## Technical Debt

Record issues that span multiple files or tasks, or cannot fit the active plan, in `docs/exec-plans/tech-debt-tracker.md`; see `execplan-format.md`.

Link debt to the plan, design document, or code location that best explains it. Remove or downgrade debt when addressed. Keep task-local TODOs in the active ExecPlan rather than the global tracker.

## Completion Gates

### Hard Gates

Completion requires every hard gate below. An ERROR cannot be waived. Resolve each WARN or record explicit acceptance with its reason and residual risk; accepted WARNs remain visible and cannot be reported as a clean validation pass:

- Affected code paths or documentary sources were inspected.
- The minimum effective tests or checks for affected areas passed.
- Document validation completed with `python scripts/validate_agents_docs.py --level WARN`: no ERROR remains, and every WARN is resolved or explicitly accepted with its reason and residual risk.
- Every touched active ExecPlan has current Progress, Decision Log, and validation records.
- Non-trivial work completed the independent two-axis review below; findings were fixed or recorded as debt.
- Architecture, security, workflow, runtime contract, and operational changes were synchronized to their durable documents.

### Soft Gates

Run when relevant and explain any skip: broader regression tests, manual runtime checks, dependency/security scans, and coverage reports.

### Two-Axis Review for Non-Trivial Work

Before completion, review all changes independently along both axes. Passing one never hides failure on the other.

**Spec axis:** compare every acceptance criterion and user story with the implementation, or compare an internal refactor with the ExecPlan Purpose. Report missing or partial requirements, unrequested scope, and behavior that does not match the description.

**Standards axis:** compare changes with root AGENTS.md core beliefs, dependency directions from `architecture-constraints.md`, `docs/DESIGN.md` when present, and the smell baseline below. Treat each as a judgment, not a universal law; skip mechanically enforced checks and honor explicit project decisions.

| Smell | Signal | Response |
|-------|--------|----------|
| Mysterious naming | Name does not reveal purpose | Rename; inability to name honestly signals a muddled design |
| Duplication | The same logic shape appears in multiple places | Extract once and call from both |
| Speculative generality | Abstractions, parameters, or configuration serve no real requirement | Remove until a real need exists |
| Shotgun modification | One logical change forces small edits across many files | Consolidate ownership into one module |

Put the two review conclusions in the final Validation block below. They state findings only and do not repeat validation commands.

## Risk-Based Validation

Run the minimum effective check first, then expand with risk:

| Change Scope | Default Validation |
|--------------|--------------------|
| Documents / rules / plans | `python scripts/validate_agents_docs.py --level WARN` |
| Backend / API / data | Focused tests → full tests, lint, typecheck |
| Frontend / UI / runtime configuration | Lint and related tests; build when affected |
| Desktop | Related tests; build/typecheck when packaging or types are affected |
| Cross-area contract | Run each area's gates and synchronize Spec, architecture, and references |

Choose concrete commands from the project's stack and record common validation commands in AGENTS.md and the ExecPlan `Validation and Acceptance` section.

## Final Delivery Format

Every final report transparently states:

```text
Validation:
- Passed: <command or check>
- Not run: <command or check> because <reason>
- Residual risk: <risk, or none>
Spec review: <per-requirement conclusion, or "no findings">
Standards review: <findings and resolutions, or "no findings">
```

The first three lines are required for every task. The two review lines are required only for non-trivial work. This block is the single source of truth for final-delivery format; other documents link here instead of duplicating it. A tiny documentation change may compress the report to one sentence but must still state validation results.
