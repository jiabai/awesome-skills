# AI Coding Execution Workflow

This document defines execution, decision rules, and write-back behavior. See `task-management.md` for TASKS.md structure and `validation-standards.md` for validation criteria.

## Contents

- [Design Principles](#design-principles)
- [Execution Workflow](#execution-workflow)
- [Key Steps](#key-steps)
- [Validation Strategy](#validation-strategy)
- [Bugs During Execution](#bugs-during-execution)
- [Relationship to ExecPlans](#relationship-to-execplans)

---

## Design Principles

- **Entry-point map:** AGENTS.md is the default entry point and key constraint summary. Child documents expand details without conflicting rules.
- **Hierarchical inheritance:** start with the nearest AGENTS.md and inherit upward. Module-level documents contain only local differences.
- **No duplication:** shared rules live above; local documents add only differences.
- **Write-back trigger:** after adding or changing a child document, inspect and update AGENTS.md summaries when needed.
- **Generated annotation:** generated documents include a comment directing edits to the source rather than the artifact.
- **Layered entry points:** AGENTS.md is the map, WORKFLOW.md contains the process, and `docs/EXECUTION_GATES.md` defines completion.

### Constraint Priority

Resolve conflicts in this order:

```
AGENTS.md core beliefs > mechanically enforced linter configuration > child-document details
```

- AGENTS.md core beliefs have highest priority; child documents never contradict them.
- Linter constraints mechanically enforce the next priority.
- Child documents may be more specific, but never looser or opposite.

### Write-Back Triggers

Inspect and update AGENTS.md when:

1. A child document is added—summarize its core constraints in AGENTS.md core beliefs.
2. A child constraint changes—update the corresponding summary.
3. A child document conflicts with AGENTS.md—correct the child using AGENTS.md as authority. If relaxation is truly required, change AGENTS.md first.

## Execution Workflow

### Routine Development

1. Locate and read the nearest AGENTS.md, then inherit parent rules.
2. Inspect the implementation, call sites, tests, and relevant documents.
3. Route durable intent to a Product Spec, architecture rationale to a design document, implementation sequencing to an ExecPlan, and active execution to root TASKS.md or a sibling plan checklist.
4. Decide whether a Product Spec is needed. User-visible behavior, new boundaries, or changes to security/data/deployment semantics require `docs/product-specs/` first.
5. Execute at the right granularity: implement small work directly; for non-trivial work, formal coding follows the approved active ExecPlan and its sibling checklist when present.
6. Update TASKS.md after each task; create task-scoped commits only when authorized.
7. Validate minimum → expanded → full.
8. Before delivery, check AGENTS.md, document synchronization, constraint consistency, and completion gates.

## Key Steps

### 1. Locate the Nearest AGENTS.md

- Search upward from the working directory.
- Read the nearest file first, then inherit uncovered parent rules.

### 2. Inspect the Existing Implementation

- Before changing code, read the current implementation, adjacent call sites, nearest tests, and relevant documents.
- Never edit code from assumptions alone.

### 3. Design Decision

- **Cross-module change:** when multiple directories or shared interfaces/types change, create `docs/exec-plans/active/<slug>-plan.md` and, for a larger task list, a sibling `<slug>-tasks.md`. Keep root TASKS.md focused on current recovery context.
- **Architecture decision:** when adding a durable layer, dependency direction, or abstraction, create `docs/design-docs/<slug>.md` explaining the decision and constraints.
- **User-visible behavior:** create or update `docs/product-specs/YYYY-MM-DD-<slug>.md` and confirm goals, non-goals, and acceptance criteria first.
- **Non-trivial implementation:** use `docs/exec-plans/active/<slug>-plan.md` according to `workflow-governance.md` and execute after human confirmation.
- **Formal coding gate:** before writing code, read the approved active ExecPlan and its sibling checklist when present. Follow their scope, sequence, acceptance, validation, and constraints; pause for any required plan change.
- **Small single-module change:** implement directly when one directory changes and no shared interface/type is touched.

First list files expected to change, group them by directory, and identify shared types and interfaces.

### 4. Execution Tracking

- TASKS.md records execution-level tasks; see `task-management.md`.
- Check each item immediately after completion instead of batching updates.
- Update the active ExecPlan's Progress, Decision Log, and validation records after each meaningful batch.

### 5. Commit Policy

- Commit only when the user or repository workflow authorizes it.
- Stage explicit task-scoped paths and commit a meaningful independently verifiable batch. Keep unrelated and incomplete work out of the commit.

### 6. Progressive Validation

- Run the smallest check first, then decide whether to expand.
- See `validation-standards.md` for layers and skip criteria.

### 7. Document Synchronization

- Before delivery or an authorized commit, determine whether AGENTS.md needs an update.
- Add new rules, remove stale ones, and resolve conflicts in favor of AGENTS.md.

## Validation Strategy

Keep only one ordering: minimum → expanded → full. See `validation-standards.md` for detailed checks, commands, and severities.

## Bugs During Execution

Core discipline: **build the smallest stable reproduction loop before attempting a fix.** Reading code and forming theories before making the failure appear is guessing. Stop immediately if that happens.

1. **Reproduce:** find an action or command that reliably triggers the issue, such as refreshing a page, curling an endpoint, or running a script. Increase the reproduction rate of intermittent failures by looping or applying load.
2. **Minimize:** remove irrelevant steps and data until the smallest scenario still fails; every remaining element must contribute.
3. **Fix:** change the code.
4. **Retest:** confirm the reproduction command no longer fails and remove every temporary diagnostic message.
5. **If blocked:** when reproduction or repair is impossible, report what was tried and request the original error text or screenshot. Do not make blind changes without a reproduction.

## Relationship to ExecPlans

- Work that fits within 30 minutes uses this workflow plus root TASKS.md.
- Multi-hour or multi-day work uses an ExecPlan plus `docs/exec-plans/active/<slug>-tasks.md`.
- ExecPlans own milestones and approved scope; this document owns execution actions within that scope.
- Move completed ExecPlans to `completed/`, update both indexes, and record cross-task debt in `tech-debt-tracker.md`.
