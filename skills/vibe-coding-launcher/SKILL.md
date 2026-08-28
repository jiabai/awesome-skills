---
name: vibe-coding-launcher
description: Use when launching a software project from scratch, choosing a stack for a non-programmer, establishing AI-agent project governance, or recovering an existing project from AGENTS.md, TASKS.md, or ExecPlans. Excludes routine implementation, debugging, bug fixes, isolated features, refactoring, and programming questions after governance exists.
---

# Vibe Coding Launcher

Establish an AI-agent-friendly project system. Core principle: **Humans steer. Agents execute.**

## Route

1. **Launch:** new project, undecided stack, or governance setup.
2. **Recovery:** an existing project has `AGENTS.md` and the user asks to resume or locate the stopping point.
3. Otherwise exit this workflow and follow existing project instructions.

Read only current-phase references. Add `references/phase-guidance.md` for interaction examples and special-case references when applicable.

## Human Gates

Pause for decisions about requirements, stack, document set, Product Spec, and ExecPlan. Always pause after a recovery summary.

After approval of an ExecPlan or lightweight task, execute through meaningful milestones. Pause for a missing decision, authorization for an external or irreversible action, material scope or risk changes, or an unresolved error. Guided deployment remains one user-executed command per confirmation.

## Formal Coding Gate

Formal coding starts only after reading the approved active ExecPlan and its sibling task checklist when present. Treat the active ExecPlan as the execution source of truth for scope, sequence, acceptance, validation, and constraints. Update its progress and decisions after each meaningful batch. If work needs a plan change, pause, update it, and obtain approval before continuing.

## Recovery

1. Read root `AGENTS.md`, optional `TASKS.md`, and any ExecPlan needed to locate the stopping point.
2. Attempt `python scripts/validate_agents_docs.py --level WARN`. If the project script is missing, use this skill's validator with `--project <project-root>` or record the missing validator as an uncertainty.
3. Inspect relevant implementation and tests to verify document claims.
4. Summarize sources, stopping point, completed work, next step, blockers, validation findings, and one specific continuation question.

The first recovery turn is orientation only: preserve project files and wait after the summary. “Continue development” authorizes orientation, not implementation.

## Launch Phases

| Phase | Action | Checkable completion criterion | Read |
|------|--------|--------------------------------|------|
| 1 | Capture project goal, user language familiarity, and OS | All three answers are recorded | `references/tech-stack-recommendations.md` |
| 1.5 | Elicit user stories, terms, coverage, and draft acceptance | Stories, applicable coverage, and acceptance are explicitly confirmed | `references/requirements-elicitation.md` |
| 2 | Recommend the simplest suitable stack with tradeoffs | The user selects a stack | `references/tech-stack-recommendations.md` |
| 3 | Generate the mandatory core set and conditionally create `TASKS.md` | Required files, validator, and root `Constraint Mechanism` exist; the user confirms the file set | `references/project-structure.md`, `references/document-templates.md`, `references/architecture-constraints.md` |
| 4 | Generate only applicable extended documents | Each applicable document is non-empty and every Quick Entry link resolves | `references/docs-templates.md`, `references/deployment-spec.md` |
| 5 | Configure architecture constraints | The declared mode is valid; `linter+agents` names an existing configuration | `references/architecture-constraints.md`; add `references/architecture-special-cases.md` when applicable |
| 5.1 | Validate documents | No ERROR remains; every WARN is resolved or explicitly accepted with a reason and residual risk | `references/validation-standards.md` |
| 6 | Classify the workflow | Full or lightweight path and completion gates are recorded | `references/workflow-governance.md` |
| 7 | Write the first Spec and/or ExecPlan | Required artifacts and validation steps exist; the user approves the execution plan | `references/workflow-governance.md`, `references/execplan-format.md`, `references/task-management.md` |
| 8 | Execute the approved work | Tests and hard gates pass, active records are current, and delivery reports validation and residual risk | `references/ai-coding-workflow.md`, `references/execplan-format.md`, `references/workflow-governance.md`, `references/deployment-spec.md` |

Write a Product Spec before the ExecPlan for user-visible behavior or a new product, data, security, or deployment boundary. Durable architecture decisions also need a design document.

## Rules

- Phase 7 plans; Phase 8 implements.
- Generate documents only when their stated conditions are met. Create `TASKS.md` while execution tasks exist, keep it current, and delete it after completion.
- Non-trivial work requires a reviewable Spec when applicable, an ExecPlan, and verifiable task breakdown before code changes.
- Keep root `AGENTS.md` concise. Summarize child-document constraints in its core beliefs; root `AGENTS.md` is authoritative when rules conflict.
- Completion claims list passed checks, checks not run, accepted WARNs, and residual risks. A failing hard gate prevents a completion claim.

## Validation

At each document gate, run `python scripts/validate_agents_docs.py --level WARN`. Resolve every ERROR. Resolve every WARN or record why it is accepted, together with the residual risk. Report accepted WARNs explicitly; they are not a clean zero-finding pass. See `references/validation-standards.md` for severity and command details.
