# Document Validation Standard

This is the canonical source for document validation. `SKILL.md` and other workflow documents link here instead of duplicating validation details.

## Contents

- [When to Validate](#when-to-validate)
- [Validation Checklist](#validation-checklist)
- [Severity Levels](#severity-levels)
- [Simplified and Mature AGENTS.md](#simplified-and-mature-agentsmd)
- [Test and Validation Quality](#test-and-validation-quality)
- [Commands](#commands)

---

## When to Validate

| Timing | Scope | Minimum Severity |
|--------|-------|------------------|
| After establishing constraints | Core documents: AGENTS.md + WORKFLOW.md + architecture information + completion gates + scripts/validate_agents_docs.py; TASKS.md optional | WARN |
| Before ending every conversation | TASKS.md progress consistency | WARN |
| During project recovery | Document completeness + knowledge freshness | ERROR + WARN |
| Before committing | Full check | INFO |

## Validation Checklist

### Core Documents (Must Pass)

| File | Check | Requirement |
|------|-------|-------------|
| `AGENTS.md` | Exists | Required at project root |
| `AGENTS.md` | Complete sections | Root and child files follow their selected standard |
| `AGENTS.md` | Line count | Simplified ≤150; mature ≤140 |
| `AGENTS.md` | Quick Entry has no dead links | Every referenced document exists |
| `WORKFLOW.md` | Exists, or AGENTS.md contains a lightweight alternative | Default project workflow |
| `scripts/validate_agents_docs.py` | Exists | Core validator required for every project |
| `TASKS.md` | When present, standard sections (`In Progress`, `To Do`, `Completed`) and `✅` validation on every task | Absence is allowed after all tasks finish |
| `tasks.md` | Legacy-name compatibility | When present, request renaming to root `TASKS.md` |
| `docs/ARCHITECTURE.md` | Required for multi-file projects; CLI/single-file alternative is an AGENTS.md `Architecture` section | Describes architecture |
| `docs/ARCHITECTURE.md` | Overview, module/code map, key files, constraints/invariants | Missing concepts produce WARN |
| `docs/EXECUTION_GATES.md` | Required for multi-file projects; CLI/single-file alternative is a gate summary in AGENTS.md | Defines validation, risk, and closeout |
| Root `AGENTS.md` | `Constraint Mechanism` exists | Project metadata is declared at root only |
| Root `AGENTS.md` | `Constraint Mechanism.Mode` valid | `agents-only` or `linter+agents` |
| Root `AGENTS.md` | `Constraint Mechanism.Configuration` valid | `N/A` for agents-only; real path for linter+agents |
| Root `AGENTS.md` | Verbatim workflow and active-ExecPlan hard constraints exist | Must contain `MUST NOT skip documentation...`, `Lightweight path ONLY...`, `Formal coding starts only after...`, and `Treat the active ExecPlan as the execution source of truth...`; see `document-templates.md` |

Child/module AGENTS.md inherits the root Constraint Mechanism. It may repeat it for readability, but validation does not require that repetition.

### Conditional Documents (Validate When Present)

| File | Check | Requirement |
|------|-------|-------------|
| `docs/exec-plans/` | Subdirectory structure | Check `active/` and `completed/` when the directory exists |
| `docs/product-specs/` | Index and Spec structure | Check goals, non-goals, and acceptance criteria |
| `docs/DESIGN.md` | Section structure | Check when present |
| `docs/QUALITY_SCORE.md` | Score-table format | Check when present |
| `docs/SECURITY.md` | Security constraints | Check when present |
| Constraint configuration declared by AGENTS.md | File exists | Required in `linter+agents` mode |

### Knowledge Freshness

| Check | Requirement | Severity |
|-------|-------------|----------|
| Quick Entry links | Every path exists | WARN |
| TASKS.md progress | Completed work checked; new work recorded | WARN |
| ARCHITECTURE.md module map | Matches current code structure | WARN |

## Severity Levels

| Level | Meaning | Response |
|-------|---------|----------|
| **ERROR** | Must fix | Cannot enter the next phase until resolved |
| **WARN** | Review required | Resolve it, or record the acceptance reason and residual risk before proceeding or claiming completion |
| **INFO** | Status | No action required |

`--level` controls which findings are displayed. Every ERROR blocks progress. A WARN keeps the validator's exit status nonzero until resolved; the workflow may proceed only when the WARN is either resolved or explicitly accepted with its reason and residual risk. Use `--level WARN` at completion gates so both actionable levels remain visible.

### ERROR Conditions

- Missing core documents: AGENTS.md; WORKFLOW.md without an AGENTS.md lightweight alternative; architecture information; or completion-gate information.
- Missing `scripts/validate_agents_docs.py`.
- Missing required section.
- Root AGENTS.md lacks `Constraint Mechanism` or Mode.
- `Mode=agents-only` with Configuration other than `N/A`.
- `Mode=linter+agents` without a real existing configuration path.
- Root AGENTS.md lacks either hard workflow phrase or the active ExecPlan gate, or softens them to generic wording such as "Follow the workflow."
- TASKS.md exists but task state cannot be recognized.
- TASKS.md lacks `In Progress`, `To Do`, or `Completed`.
- A TASKS.md item lacks a `✅` validation condition.

### WARN Conditions

- Legacy root `tasks.md` must be renamed to `TASKS.md`.
- Line-count limit exceeded.
- Dead Quick Entry link.
- ARCHITECTURE.md lacks any concept group: overview, module/code map, key files, or architecture constraints/invariants.

### INFO Conditions

- File line counts.
- TASKS.md task counts.
- AGENTS.md version detection.

## Simplified and Mature AGENTS.md

### Version Detection

| Condition | Version |
|-----------|---------|
| Contains `## Scope` | Mature |
| Does not contain `## Scope` | Simplified |

### Simplified Standard

**Use for:** three or fewer modules, beginner projects, one developer.

Required root sections:

- Quick Entry
- Core Beliefs
- Development Workflow
- Common Commands
- Architecture, for CLI/single-file projects only
- Constraint Mechanism, at root only

**Limit:** 150 lines.

### Mature Standard

**Use for:** more than three modules, multiple collaborators, or multiple AI tools.

Required root sections:

- Scope
- Do
- Avoid
- Constraint Mechanism
- Commands
- Tests
- Related Skills

**Limit:** 140 lines.

### Root and Child Rules

- Root AGENTS.md declares the project Constraint Mechanism.
- Child/module AGENTS.md inherits it and need not repeat it.
- Child/module AGENTS.md still satisfies every other required section of its selected template.

## Test and Validation Quality

When writing tests or validators for a project:

- **Test behavior, not implementation:** use public entry points such as page behavior, API responses, or command output. A refactor should not break tests merely because internals changed.
- **Use independent expected values:** compare against a known literal, specification, or hand-calculated example. Do not compute expected output with the same logic as the implementation.
- **One loop at a time:** one check → one implementation increment → the next check. A batch of speculative tests validates imagined behavior rather than observed behavior.
- **Reproduce before fixing bugs:** follow the reproduction-loop discipline in `ai-coding-workflow.md` under Bugs During Execution.

## Commands

### Basic

```bash
python scripts/validate_agents_docs.py
```

### Severity Filter

```bash
# ERROR only
python scripts/validate_agents_docs.py --level ERROR

# ERROR + WARN
python scripts/validate_agents_docs.py --level WARN

# Everything (default)
python scripts/validate_agents_docs.py --level INFO
```

### Target Project

```bash
python scripts/validate_agents_docs.py --project /path/to/project
```

When run from inside the target project, a deleted local validator prevents the command itself from starting. When this skill's copy validates another project through `--project`, it must still report that missing file.

### Example Output

```
[INFO] AGENTS.md: simplified, 45 lines
[INFO] TASKS.md: 5 pending, 3 completed
[INFO] docs/ARCHITECTURE.md: 32 lines
[INFO] docs/exec-plans/: directory absent (generated only when needed)
[WARN] AGENTS.md: dead Quick Entry link: docs/DESIGN.md

Validation requires review: 0 errors, 1 warning
```

## Embedding Validation in the Workflow

### After Constraints

After generating core and conditional documents and recording a valid root Constraint Mechanism:

```
Complete Phase 5 → Run validation → Resolve every ERROR → Resolve or explicitly accept each WARN → Enter Phase 6
```

### End of Conversation

After updating TASKS.md:

```
End work → Update TASKS.md when present → Run --level WARN → Resolve findings or record accepted WARNs and residual risk
```

### Recovery

Attempt validation before summarizing. If the project lacks the script, use this skill's copy with `--project` or record the omission without blocking orientation:

```
Read AGENTS.md → Attempt --level WARN → Record unresolved ERRORs as blockers and WARNs as resolved or accepted risks → Present recovery summary and wait
```

## Summary

The validator prioritizes **structural completeness** over **verbatim content** because project content changes with user needs. The root AGENTS.md workflow and active ExecPlan hard constraints remain marker-checked so they cannot be softened over time.
