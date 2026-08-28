# Extended Document Templates (Phase 4, Conditional)

This document defines templates for conditional `docs/` documents, CONTEXT.md, and ADRs. See `document-templates.md` for the core set (AGENTS.md, WORKFLOW.md, TASKS.md, and validator) and `deployment-spec.md` for the complete deployment template and guidance rules.

## docs/EXECUTION_GATES.md

Defines when work may be called complete. **Generate for:** multi-file projects, Web/API/desktop projects, or any project needing test, release, or delivery standards.

```markdown
# Execution Gates

## Purpose

This document defines the checks required before a task is complete. Validation must be proportional to risk and visible in the final delivery.

## Hard Gates

- Affected code paths or documentary sources of truth were inspected.
- The minimum effective tests or checks for affected areas passed.
- Document structure validation completed with `python scripts/validate_agents_docs.py --level WARN`.
- Every ERROR was resolved; every WARN was resolved or explicitly accepted with its reason and residual risk. Accepted WARNs are listed in delivery and are not described as a clean pass.
- Progress, Decision Log, and validation records are current in every touched active ExecPlan.
- Active ExecPlan scope, sequence, acceptance, and validation are current; approved deviations are recorded.
- Non-trivial work completed two independent reviews: the Spec axis (faithfulness to source intent) and Standards axis (compliance with project standards). Findings were fixed or recorded as technical debt.
- Changes to architecture, security, workflow, runtime contracts, or operations were synchronized to durable documentation.

## Soft Gates

- Broader regression testing.
- Manual runtime checks.
- Dependency or security scans.
- Coverage reports.

When a relevant soft gate is skipped, record the reason and residual risk in the final delivery or active ExecPlan.

## Definition Of Done

1. Requested behavior is implemented or fixed, or explicitly recorded as out of scope.
2. Hard gates pass for every affected area.
3. Relevant Specs, design documents, references, AGENTS maps, and ExecPlans are synchronized.
4. New technical debt is recorded in the active plan or `docs/exec-plans/tech-debt-tracker.md`.
5. Final delivery lists Passed, Not run, and Residual risk. Non-trivial work also includes separate Spec review and Standards review lines.
```

## CONTEXT.md

A project glossary at the root beside AGENTS.md. It keeps users and AI on the same language; Spec titles, task names, test names, and code identifiers all use canonical terminology.

**Generate when:** Phase 1.5 clarified at least three project-specific terms. See `requirements-elicitation.md`. Otherwise, put essential concepts in AGENTS.md core beliefs.

**AGENTS.md integration:** after generation, add `- Glossary: see CONTEXT.md` to Quick Entry. Do not list it when absent.

```markdown
# {Project Name} Glossary

This document defines canonical names for key project concepts. AI-generated Specs, tasks, tests, and code identifiers must use the canonical term, not aliases listed under Avoid.

## Language

**{Canonical Term}**:
{One or two sentences defining what it is.}
_Avoid_: {alias 1}, {alias 2}
```

Define what each term is in one or two sentences. Include only project-specific concepts. Choose one canonical term when several names refer to the same concept and list the others under Avoid. Every term must come from actual elicitation.

## docs/ARCHITECTURE.md

An architecture map answering "Where is X?" and "What does this code do?" **Every project must provide architecture information:**

- **Multi-file project:** generate `docs/ARCHITECTURE.md` with 50–150 lines. Include an overview, code map (modules and relationships), architecture invariants, layer boundaries, cross-cutting concerns, and key files.
- **CLI/single-file project:** do not generate `docs/`. Put an overview, key files, and 2–3 invariants in the AGENTS.md Architecture section (≤20 lines). Create the document when the project grows into multiple files.

Write only stable content. Refer to symbols rather than links.

## docs/DESIGN.md

Design standards. **Generate when:** the project has a UI or API. Cover UI component rules, API design rules, or code style. If omitted, put 2–3 essential design constraints in AGENTS.md core beliefs.

## docs/QUALITY_SCORE.md

A per-module quality score updated at milestones. **Generate when:** the project has more than three modules. Do not generate at launch for a smaller project.

```
| Module | Maintainability | Test Coverage | Documentation | Overall |
|--------|-----------------|---------------|---------------|---------|
| src/ui | 🟢 | 🟡 | 🟢 | 🟢 |
| src/service | 🟢 | 🟢 | 🟡 | 🟢 |
```

## docs/SECURITY.md

Security standards. **Generate when:** the project makes network requests, stores data, or uses API keys. Cover sensitive-data storage, input validation, and dependency-scan frequency. If omitted, put essential security constraints such as "Never hard-code API keys; use environment variables" in AGENTS.md core beliefs.

## docs/DEPLOYMENT.md

Deployment specification. **Generate when:** the project is a Web/API/long-running server project and the user wants cloud-server deployment. See `deployment-spec.md` for the complete self-contained template. Omit for local CLI or serverless projects; create later when needed and update AGENTS.md Quick Entry.

## docs/design-docs/core-beliefs.md

Expanded core beliefs. **Generate when:** more than three core beliefs require explanation. Otherwise, keep up to five core beliefs directly in AGENTS.md.

## Architecture Decision Record (ADR)

A lightweight record of why a decision was made. Store in `docs/design-docs/` as `NNNN-<slug>.md`, numbered from `0001`.

Create an ADR only when all three conditions hold:

1. **Hard to reverse** — changing the decision later has a noticeable cost, such as database or framework choice.
2. **Confusing without context** — a future reader, including an AI agent, would ask why this approach was chosen.
3. **Real tradeoff** — a credible alternative existed and was rejected for a concrete reason.

Task-specific choices belong in the ExecPlan Decision Log. Only cross-task, long-lived decisions become ADRs. Do not record the same decision twice.

```markdown
# {Short Decision Title}

{One to three sentences describing the context, decision, and reason.}
```

Add optional Alternatives only when rejected options are worth preserving, and Consequences only when downstream impact is not obvious. Use the next number after the current maximum, update `docs/design-docs/index.md`, and never pre-generate empty ADRs.
