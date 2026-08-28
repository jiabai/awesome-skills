# Vibe Coding Launcher

> A project scaffolding tool—establish an AI-friendly development framework, then step aside.

---

## What Problem Does This Skill Solve?

When you want AI to help build a project, the biggest friction is often not writing code. It is that:

- The AI does not understand your project structure or conventions.
- You must explain the tech stack and architecture again in every conversation.
- The AI skips steps, forgets validation, or fails to update documentation.
- As the project grows, its context becomes confusing and output quality declines.

Vibe Coding Launcher addresses these problems at the source. It establishes an AI-friendly governance system for your project so future AI collaboration follows clear rules.

---

## What Can It Do?

### 1. Launch a New Project

Starting from scratch, it guides you phase by phase through:

- **Project scaffold**: directory structure, configuration files, and initial code.
- **Governance documents**: an `AGENTS.md` + `WORKFLOW.md` + `docs/` system that teaches AI your conventions and workflow.
- **Architecture constraints**: tech stack choices, code boundaries, and a security baseline.
- **First plan**: an executable Spec and ExecPlan derived from the larger goal.

### 2. Recover an Existing Project

After a pause, it restores context quickly:

- Reads `AGENTS.md` to understand the project.
- Reads `TASKS.md` to locate the last stopping point.
- Inspects code to confirm the current state.
- Continues from that point without repeating completed work.

---

## When to Use It

| Scenario | Use It? |
|----------|---------|
| Starting a new project from scratch | ✅ **Yes** |
| Recovering context and continuing an existing project | ✅ **Yes** |
| The project scaffold exists and routine iteration has begun | ❌ **No** |
| Fixing a bug, adding a small feature, or refactoring code | ❌ **No** |

### Exit Signals

The skill has completed its mission once the project reaches these milestones:

- `AGENTS.md` has been generated and stabilized.
- `WORKFLOW.md` defines how tasks move forward.
- The `docs/` structure is established.
- Workflow governance rules are in place.
- The first Spec / ExecPlan has been created.

Afterward, routine development should rely on the governance documents stored inside the project instead of loading this skill again.

---

## How Routine Development Works

Once the project enters its iteration phase, an AI agent follows this flow:

```
Read AGENTS.md → Inspect code → Classify the task → Execute → Validate → Sync documentation
```

**Lightweight tasks** (fix a typo, adjust styling, change one function):
implement directly → run relevant tests → finish.

**Non-trivial tasks** (new features, cross-module changes, architecture changes):
write a Spec → write an ExecPlan → break down tasks → implement incrementally → satisfy completion gates → archive the plan.

See [`references/ai-coding-workflow.md`](references/ai-coding-workflow.md) and [`references/workflow-governance.md`](references/workflow-governance.md) for details.

---

## Core Principle

**Humans steer. Agents execute.**

- Humans decide direction and goals.
- AI handles execution and details.
- Direction-setting gates—requirements, stack, document set, Spec, and ExecPlan—wait for human confirmation; approved execution continues through meaningful milestones.
- Validation is never skipped, and planning is never merged with execution.

---

## Maintaining the Skill

This section is for maintainers. It is not part of the runtime instructions in `SKILL.md`; do not copy it into `SKILL.md` or `references/`.

### Rule Ownership

Change rule details only in their owning file. Runtime files should contain only necessary cross-references so the same rule does not drift across multiple locations.

| Rule Type | Owning Location |
|-----------|-----------------|
| Invocation and exclusion boundaries | `SKILL.md` frontmatter `description` |
| Phase order and recovery hard gates | `SKILL.md` |
| Phase confirmation language, terminology, and pitfalls | `references/phase-guidance.md` |
| Requirements elicitation methodology (Phase 1.5) | `references/requirements-elicitation.md` |
| Tech stack recommendations | `references/tech-stack-recommendations.md` |
| Project file structure | `references/project-structure.md` |
| Core document templates (AGENTS/WORKFLOW/TASKS/validator) | `references/document-templates.md` |
| Extended document templates (`docs/`, CONTEXT.md, ADR) | `references/docs-templates.md` |
| Document validation standards | `references/validation-standards.md` |
| Architecture constraints and linter modes | `references/architecture-constraints.md` |
| Special architectures (desktop/TUI/Rust workspace/cross-codebase) | `references/architecture-special-cases.md` |
| Spec / ExecPlan / lightweight-path / completion-gate decisions | `references/workflow-governance.md` |
| `TASKS.md` format and lifecycle | `references/task-management.md` |
| ExecPlan document format | `references/execplan-format.md` |
| Routine execution, document synchronization, and progressive validation | `references/ai-coding-workflow.md` |
| Deployment specification generation and guidance | `references/deployment-spec.md` |

---

## Skill File Structure

```
vibe-coding-launcher/
├── SKILL.md                          # Skill entry point (read by AI agents)
├── README.md                         # This file (user guide)
├── references/
│   ├── ai-coding-workflow.md         # Routine development execution workflow
│   ├── architecture-constraints.md   # Architecture constraint configuration
│   ├── architecture-special-cases.md # Desktop/TUI/Rust workspace details
│   ├── deployment-spec.md            # Deployment specification and guidance
│   ├── docs-templates.md             # Extended document templates (Phase 4)
│   ├── document-templates.md         # Core document templates (Phase 3)
│   ├── execplan-format.md            # ExecPlan format
│   ├── phase-guidance.md             # Phase interaction guidance
│   ├── project-structure.md          # Project structure recommendations
│   ├── requirements-elicitation.md   # Requirements elicitation (Phase 1.5)
│   ├── task-management.md            # Task management standards
│   ├── tech-stack-recommendations.md # Tech stack recommendations
│   ├── validation-standards.md        # Validation standards
│   └── workflow-governance.md        # Workflow governance and completion gates
└── scripts/
    └── validate_agents_docs.py       # Documentation structure validator
```

---

## Key Concepts

| Concept | One-Sentence Explanation |
|---------|--------------------------|
| `AGENTS.md` | The project entry-point map and default source of context for AI agents. |
| `WORKFLOW.md` | How the project advances work, including the default process and lightweight path. |
| `docs/` | Detailed rules kept outside `AGENTS.md` so the entry point stays concise. |
| Spec | A product specification answering what to build, what not to build, and how it will be accepted. |
| ExecPlan | An implementation plan answering how to build it, in what order, and how to validate it. |
| Completion gates | Proof that code was inspected, validation passed, and documentation was synchronized. |
| Lightweight path | A fast execution path for low-risk, small-scope work with no new boundary. |

---

## In One Sentence

> Vibe Coding Launcher is **scaffolding**, not a **daily tool**. Once the structure is built, routine development runs on the project's own `AGENTS.md`, `WORKFLOW.md`, and `docs/` system.
