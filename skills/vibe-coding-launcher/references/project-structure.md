# Project Structure Standard

## Contents

- [Core Set](#core-set-phase-3)
- [Extended Set](#extended-set-generated-when-needed)
- [Document Generation Rules](#document-generation-rules)
- [Adjustments by Project Type](#adjustments-by-project-type)

---

## Core Set (Phase 3)

Generate the mandatory items in Phase 3 and add conditional items only when their conditions are met:

```
project-name/
├── AGENTS.md                    # Agent entry-point map (~150 lines, including initial constraint mechanism)
├── WORKFLOW.md                  # Default workflow and non-trivial-work gates
├── TASKS.md                     # Conditional: present only while execution tasks exist
├── README.md                    # Project overview
├── scripts/
│   └── validate_agents_docs.py  # Copied verbatim from this skill
└── docs/
    ├── ARCHITECTURE.md          # Architecture map (omitted for CLI/single-file projects)
    └── EXECUTION_GATES.md       # Validation, risk, and completion gates
```

> **CLI/single-file exception:** Generate AGENTS.md + WORKFLOW.md + README.md + scripts/validate_agents_docs.py; add TASKS.md while execution tasks exist. Do not generate `docs/`. Put the architecture overview, key files, 2–3 invariants, completion-gate summary, and initial `Constraint Mechanism` in AGENTS.md.

The root `AGENTS.md` must contain a valid `Constraint Mechanism` during the core-set phase. Simple projects default to `Mode=agents-only` and `Configuration=N/A`. If a complex project chooses `linter+agents`, generate the real configuration file and record its path at the same time so document validation does not fail later.

## Extended Set (Generated When Needed)

Complete in Phase 4:

```
project-name/
├── CONTEXT.md                  # Project glossary (when 3+ terms were clarified)
├── docs/
│   ├── DESIGN.md               # Design standards
│   ├── QUALITY_SCORE.md        # Quality score tracking
│   ├── SECURITY.md             # Security standards
│   ├── DEPLOYMENT.md           # Deployment specification for deployable server projects
│   ├── design-docs/
│   │   ├── index.md            # Design-document index
│   │   ├── core-beliefs.md     # Core beliefs and principles
│   │   └── *.md                # Other design documents
│   ├── exec-plans/
│   │   ├── active/             # Plans in progress
│   │   ├── completed/          # Completed or superseded plans
│   │   └── tech-debt-tracker.md
│   ├── product-specs/
│   │   ├── index.md
│   │   └── *.md
│   ├── references/
│   │   ├── *.txt               # LLM-friendly technical references
│   │   └── *.md                # API documentation and similar material
│   └── generated/
│       └── db-schema.md
├── src/
└── .gitignore
```

## Document Generation Rules

This table covers conditional core documents (`WORKFLOW.md`, `docs/EXECUTION_GATES.md`) and every extended document, including what replaces a document when it is omitted.

| File / Directory | Generate When | If Omitted |
|------------------|---------------|------------|
| `WORKFLOW.md` | By default for every project; a tiny one-off script may inline it into AGENTS.md | Describe the lightweight workflow in AGENTS.md |
| `TASKS.md` | Concrete execution tasks exist | Create it when execution starts; delete it after all tasks complete |
| `CONTEXT.md` | Phase 1.5 clarified at least three project-specific terms | Put essential concepts in AGENTS.md core beliefs |
| `docs/EXECUTION_GATES.md` | Multi-file project or any project needing test/release/delivery standards | Put minimum validation and final-delivery format in AGENTS.md |
| `docs/DESIGN.md` | Project has a UI or API | Put 2–3 key design constraints in AGENTS.md core beliefs |
| `docs/QUALITY_SCORE.md` | Project has more than three modules | Create later if the module count grows |
| `docs/SECURITY.md` | Project makes network requests, stores data, or uses API keys | Put key security constraints in AGENTS.md core beliefs |
| `docs/DEPLOYMENT.md` | Web/API/long-running server project and the user wants cloud-server deployment; see `deployment-spec.md` | Omit for local CLI/serverless projects; create when deployment becomes necessary |
| `docs/design-docs/` | At least three core beliefs need fuller treatment | Keep core beliefs in AGENTS.md |
| `docs/exec-plans/` | Project needs multi-step development plans; see `task-management.md` | Track active small tasks in root TASKS.md |
| `docs/product-specs/` | Multiple features require specifications | Create after feature scope becomes clear |
| `docs/references/` | Project depends on external APIs or complex technology | Create when reference material becomes necessary |
| `docs/generated/` | Project uses a database | Omit |
| `src/` | Project has more than one source file | Keep a single-file project at root |

Prefer fewer documents. At launch, generate only the core set and extended documents whose conditions are met. Never pre-generate empty documents; an empty document is more dangerous than no document.

Keep `AGENTS.md` as an entry-point map. Put process detail in `WORKFLOW.md`, completion standards in `docs/EXECUTION_GATES.md`, feature intent in `docs/product-specs/`, and implementation history in `docs/exec-plans/`. Do not combine them into an oversized `AGENTS.md`.

## Adjustments by Project Type

- **Web app:** add `templates/` and `static/`; layer `src/` as `ui/`, `service/`, and `repo/`.
- **API service:** layer `src/` as `routes/`, `models/`, and `services/`.
- **CLI:** a single file is acceptable. Generate AGENTS.md + WORKFLOW.md + README.md + scripts/validate_agents_docs.py, add TASKS.md while work is active, and omit `docs/`.
- **AI application:** add `config.py` for API-key configuration and put API documentation in `docs/references/`.
