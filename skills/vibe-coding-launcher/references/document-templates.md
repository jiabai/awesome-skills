# Core Document Templates (Phase 3)

This document defines mandatory and conditional core-set templates for root governance. See `docs-templates.md` for conditional `docs/` documents, CONTEXT.md, and ADR templates; `workflow-governance.md` for Product Specs; and `execplan-format.md` for ExecPlans and the `docs/exec-plans/` structure.

## AGENTS.md (Simplified)

This is an agent entry-point map, not an encyclopedia. Keep it under 150 lines. **Every project must generate it.**

Use this template for the root `AGENTS.md`. Child or module-level `AGENTS.md` files inherit project metadata—especially the `Constraint Mechanism`—from the root and do not need to duplicate it.

### Template

```markdown
# {Project Name} AI Collaboration Rules

## Quick Entry

<!-- List only documents that exist. Omit missing paths to prevent dead links. -->
- Architecture: see `docs/ARCHITECTURE.md` when generated; CLI/single-file projects use the Architecture section below
- Design standards: see `docs/DESIGN.md` when generated
- Core beliefs: see `docs/design-docs/core-beliefs.md` when generated; otherwise see below
- Execution checklist: see `TASKS.md` when present; delete after all tasks are complete
- Workflow: see `WORKFLOW.md` when generated
- Completion gates: see `docs/EXECUTION_GATES.md` when generated
- Deployment: see `docs/DEPLOYMENT.md` when generated
- Execution plans: see `docs/exec-plans/active/` when generated
- Technical debt: see `docs/exec-plans/tech-debt-tracker.md` when generated

## Core Beliefs

<3–5 non-negotiable principles>

## Development Workflow

<Brief description: describe task → run agent → create PR → agent review>

MUST NOT skip documentation for non-trivial tasks. Create spec → plan → tasks before writing code. Lightweight path ONLY for trivial changes as defined in WORKFLOW.md.

Formal coding starts only after reading the approved active ExecPlan and its sibling task checklist when present. Treat the active ExecPlan as the execution source of truth for scope, sequence, acceptance, validation, and constraints. Update its progress and decisions after each meaningful batch; pause, update the plan, and obtain approval before continuing when implementation requires a plan change.

## Architecture

<!-- Required only for CLI/single-file projects, replacing docs/ARCHITECTURE.md. Keep under 20 lines. -->
<!-- Remove this section in multi-file projects and put architecture in docs/ARCHITECTURE.md. -->

Overview: {one sentence describing the project}
Key Files: `{main filename}`
Architecture Invariants:
- {Invariant 1}
- {Invariant 2}

## Constraint Mechanism

<!-- Every project must retain this machine-readable section. -->
- Mode: `{agents-only or linter+agents}`
- Configuration: `{N/A or ruff.toml / eslint.config.js / analysis_options.yaml / pyproject.toml}`

## Common Commands

- `{command}` — explanation
```

Key points:

- The Development Workflow section must preserve the `MUST NOT` rule above verbatim. Never soften it to wording such as "Follow the workflow" or omit it. `WORKFLOW.md` defines eligibility for the lightweight path.
- The Active ExecPlan Execution rule must preserve the `Formal coding starts only after...` and `Treat the active ExecPlan as the execution source of truth...` markers so formal coding cannot silently leave the approved plan.
- The Architecture section is required only for CLI/single-file projects and contains only an overview, key files, and 2–3 invariants.
- In `agents-only` mode, Configuration must be `N/A`. In `linter+agents` mode, it must be the path to a real constraint file.

## WORKFLOW.md

Defines how the project normally advances work. **Generate by default.** A tiny one-off script may omit it only if AGENTS.md explicitly defines the lightweight workflow.

```markdown
# Project Workflow

## Purpose

This document defines the project's default workflow. Non-trivial changes form reviewable intent and a plan before implementation begins.

## Mandatory Rule

Unless the task is a low-risk, small-scope change with no new boundary, follow:

1. Constitution and context
2. Spec
3. Technical plan
4. Task breakdown
5. Implementation and validation

## Constitution

- `AGENTS.md`
- `docs/ARCHITECTURE.md` or the root Architecture section
- `docs/DESIGN.md` when present
- `docs/SECURITY.md` when present
- The nearest relevant module-level `AGENTS.md` when present

## Spec

When work changes user-visible behavior, introduces a boundary, or affects authentication, permissions, data, deployment, or security, create or update a Spec in `docs/product-specs/`.

## Plan

For non-trivial work, create an ExecPlan in `docs/exec-plans/active/` and implement only after the plan is confirmed.

## Active ExecPlan Execution

Formal coding begins only after reading the approved active ExecPlan and its sibling task checklist when present. Follow the plan's file scope, sequence, acceptance criteria, validation commands, and constraints. After each meaningful batch, update Progress, Surprises & Discoveries, Decision Log, and validation records. When implementation needs a scope, sequence, acceptance, or constraint change, pause, update the plan, and obtain approval before continuing.

## Lightweight Path

Lightweight work may be implemented directly, but still requires inspection, minimum validation, necessary document synchronization, and a final validation report.

## File Placement

- User intent: `docs/product-specs/`
- Design decisions: `docs/design-docs/`
- External references: `docs/references/`
- Active plans: `docs/exec-plans/active/`
- Completed plans: `docs/exec-plans/completed/`
- Technical debt: `docs/exec-plans/tech-debt-tracker.md`
```

## TASKS.md

A temporary execution checklist at the project root—never `docs/TASKS.md`. Create it only while concrete execution tasks exist.

Lifecycle: create when work is ready for execution → update throughout execution → delete after all tasks are complete. Omit it before tasks are defined. See `task-management.md` for format and writing rules.

```markdown
# Tasks

## In Progress
- [ ] {Task description} ✅ {validation command or acceptance condition}

## To Do
- [ ] {Task description} ✅ {validation command or acceptance condition}

## Completed
- [x] {Task description} ({YYYY-MM-DD}) ✅ {validation command or acceptance condition}
```

## scripts/validate_agents_docs.py

**Every project must generate this core file.** Read this skill's `scripts/validate_agents_docs.py` and copy it verbatim into the user's project. Do not customize it.

It validates core documents after Phase 5 constraints are established, checks knowledge freshness before ending a conversation, and confirms document state during recovery.

```bash
python scripts/validate_agents_docs.py --level ERROR   # ERROR only
python scripts/validate_agents_docs.py --level WARN    # ERROR + WARN
python scripts/validate_agents_docs.py --project /path/to/project
```

The `--level` option filters displayed findings only. Every ERROR blocks progress. A WARN requires resolution or an explicit acceptance record with its reason and residual risk; use `--level WARN` for completion gates.

The script uses only the Python standard library. By default, it treats the parent of its own directory as project root. See `validation-standards.md` for validation rules.

## AGENTS.md (Mature Project)

Use when any condition is met: more than three modules, multiple collaborators, or multiple AI tools. The full root AGENTS.md stays at or below 140 lines. Module-level files may reuse this structure while inheriting the root Constraint Mechanism.

| Section | Content | Count |
|---------|---------|-------|
| **Scope** | Applicable scope and boundaries | 2–4 items |
| **Do** | Required practices | 3–5 items |
| **Avoid** | Anti-patterns | 3–5 items |
| **Constraint Mechanism** | Explicit constraint mode and configuration | 2 items |
| **Commands** | Common commands | 4–8 items |
| **Tests** | Validation strategy | 2–4 items |
| **Related Skills** | Relevant reference links | 2–4 items |

As in the simplified version, the first Avoid item must preserve the hard workflow rule below verbatim.

```markdown
# {Module Name} AI Collaboration Rules

<!-- Generated by vibe-coding-launcher. Edit project metadata to change it. -->

## Scope

- [Scope description]
- [Boundary description]

## Do

- [Required practice 1]
- [Required practice 2]
- [Required practice 3]

## Avoid

- MUST NOT skip documentation for non-trivial tasks. Create spec → plan → tasks before writing code. Lightweight path ONLY for trivial changes as defined in WORKFLOW.md.
- [Anti-pattern 1]
- [Anti-pattern 2]

## Constraint Mechanism

- Mode: `linter+agents`
- Configuration: `{ruff.toml or eslint.config.js / analysis_options.yaml / pyproject.toml, selected from the mapping table}`

## Commands

- `{command}` [description]
- `{command}` [description]

## Tests

- [Validation strategy 1]
- [Validation strategy 2]

## Related Skills

- `{related document path}` [description]
- `{related document path}` [description]
```

## Choosing a Template

- New project with three or fewer modules → simplified version (≤150 lines).
- Growing project with more than three modules, multiple AI tools, multiple collaborators, or cross-module coordination → mature version (≤140 lines).
- Hierarchical inheritance: module-level AGENTS.md contains only module-specific rules. Shared rules live above it. Local rules override parent rules; otherwise parent rules are inherited.
