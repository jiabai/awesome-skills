# Task Management Standard

This document governs how `TASKS.md` records and advances work. See `ai-coding-workflow.md` for execution and commit policy, and `validation-standards.md` for validation depth.

## Contents

- [TASKS.md vs. ExecPlan](#tasksmd-vs-execplan)
- [TASKS.md Format](#tasksmd-format)
- [Task Writing Rules](#task-writing-rules)
- [Vertical Slices and Dependencies](#vertical-slices-and-dependencies)
- [Usage Rules](#usage-rules)
- [Knowledge Freshness](#knowledge-freshness)
- [Commit Policy](#commit-policy)
- [Progressive Validation](#progressive-validation)

---

## TASKS.md vs. ExecPlan

| Dimension | TASKS.md | ExecPlan Progress |
|-----------|----------|-------------------|
| Role | Lightweight execution checklist | Feature-level planning document |
| Granularity | 1–30 minute execution tasks such as installing Flask | 30-minute to multi-hour milestones such as API framework ready |
| Format | Checkbox list | Full document with Purpose, Progress, Steps, and Validation |
| Best for | Bugs, small changes, configuration, dependencies, and session recovery | Features, architecture changes, and multi-step development |
| Location | Root `TASKS.md` | `docs/exec-plans/active/` |
| Lifecycle | Delete when all work completes; ExecPlan preserves history | Move to `completed/` after completion |
| Update | Check immediately after each task | Mark a milestone after its task batch passes |

## TASKS.md Format

```markdown
# Tasks

## In Progress
- [ ] Install Flask ✅ `pip install flask && python -c "import flask; print(flask.__version__)"`
- [ ] Add `/health` endpoint ✅ `curl localhost:5000/health` returns 200

## To Do
- [ ] Configure `.gitignore` ✅ `cat .gitignore` contains `__pycache__`, `.env`, and `node_modules`
- [ ] Add environment-variable support ✅ `python -c "from config import SETTINGS; print(SETTINGS)"` exits successfully

## Completed
- [x] Initialize project structure (2026-04-17) ✅ `ls AGENTS.md TASKS.md docs/` finds every file
- [x] Create AGENTS.md (2026-04-17) ✅ `wc -l AGENTS.md` reports ≤150
```

## Task Writing Rules

Every task includes a completion check:

```
- [ ] Task description ✅ validation command or acceptance condition
```

| Type | Format | Example |
|------|--------|---------|
| Command | `✅ <command> <expected output>` | `✅ pip install flask` exits without error |
| File | `✅ cat/ls <file> contains/exists` | `✅ cat .gitignore` contains node_modules |
| Behavior | `✅ <observable runtime behavior>` | `✅ Browser opens /health and receives 200` |

Do not write:

- Vague tasks without validation, such as "improve performance" or "clean up code." Split them into concrete outcomes.
- Tasks that cannot finish within 30 minutes. Split them or promote the work to an ExecPlan.
- Blocked tasks in In Progress. Put later dependent work under To Do.

Change `- [ ]` to `- [x]` only after the condition following `✅` actually passes. Run the command or observe the behavior; never check a task by intuition.

## Vertical Slices and Dependencies

**Vertical slice:** each milestone or batch crosses all necessary layers and produces behavior the user can verify. The test is simple: after completion, can you say, "You can now try X"?

| Split | Example | Consequence |
|-------|---------|-------------|
| ❌ Horizontal | Build every backend endpoint, then every frontend page | Intermediate states cannot be validated; integration problems arrive late |
| ✅ Vertical | One expense path: form → storage → list | Every slice is testable and exposes misunderstandings early |

Organize ExecPlan batches and TASKS.md groups as vertical slices.

When tasks block one another, put prerequisites first and state the dependency in one sentence. Ordering plus prose is sufficient; do not invent a dependency schema.

**Exception—large mechanical changes:** a repository-wide rename or shared-type migration may not form a vertical slice. Migrate by directory or module, keeping the project runnable after each batch, then remove the old form in the final batch.

## Usage Rules

- Put small work in root TASKS.md. Use an ExecPlan plus `docs/exec-plans/active/<feature-slug>-tasks.md` for large work, with milestones in ExecPlan Progress.
- For formal work, read the approved active ExecPlan and its sibling checklist when present before coding; otherwise use the plan's `Progress` as the checklist. The plan governs scope, sequence, acceptance, validation, and constraints.
- Derive execution tasks from milestones: define the milestone, then split it into independently verifiable tasks. The two levels differ and are not duplicates.
- Read TASKS.md at conversation start and update it at the end. Delete it after everything completes; the archived ExecPlan preserves history.
- For large work, use a sibling checklist beside the ExecPlan. Keep root TASKS.md short and focused on recovering the current execution context.
- Each checklist names affected files/modules, dependencies, and validation expectations.

### Execution

1. Work through TASKS.md or the active plan's sibling checklist.
2. Complete one task → run its validation → update its checkbox and the active plan records.
3. When the user or repository policy authorizes commits, stage only the verified task's files and commit a meaningful batch.
4. Repeat until every task completes.
5. Delete a fully complete root TASKS.md; archive a plan-level checklist with its ExecPlan.

## Knowledge Freshness

- Stale documentation is more dangerous than missing documentation.
- Before ending a conversation, inspect TASKS.md progress, AGENTS.md Quick Entry, and `docs/ARCHITECTURE.md` or the AGENTS.md Architecture section.
- When modules or interfaces change, update the relevant documentation. See `validation-standards.md` for complete rules.

## Commit Policy

Create commits only when the user or repository workflow authorizes them. Prefer a meaningful, independently verifiable batch over a commit for every checkbox. Stage explicit task-scoped paths with `git add -- <path>...`, inspect `git diff --cached`, and leave unrelated or incomplete work unstaged.

Before committing, confirm:

1. TASKS.md is current.
2. The validation command passed.
3. AGENTS.md does not require synchronization.
4. The active ExecPlan records current Progress, decisions, and validation when a plan governs the work.

## Progressive Validation

Keep the sequence minimum → expanded → full. See `ai-coding-workflow.md` for selection criteria.

- Single-module code: test that module first.
- Cross-module interface: test both modules, then integration.
- Shared DTO/type: typecheck every consumer, then run the full suite.

## Relationship to Completion Gates

Checking every task does not make the overall work complete. Before closing, satisfy `workflow-governance.md`:

- Affected paths were inspected.
- Minimum effective validation passed.
- Document structure validation passed.
- Active ExecPlan Progress, Decision Log, and validation records are current.
- Final delivery reports Passed, Not run, and Residual risk; non-trivial work also includes separate Spec and Standards review lines.
