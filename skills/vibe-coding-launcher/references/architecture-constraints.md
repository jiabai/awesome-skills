# Architecture Constraint Standard

## Layered Architectures

Choose layers by project type:

| Project Type | Layers |
|--------------|--------|
| Web app | UI → Runtime → Service → Repo → Config → Types |
| API service | Routes → Service → Repo → Config → Types |
| CLI | CLI → Service → Config → Types |
| TUI | EventLoop → View → State → Command → Service → Config → Types |
| AI application | Interface → Agent → Service → Config → Types |
| Single file / script | No layers; state in AGENTS.md core beliefs: "Keep one file until it exceeds 200 lines" |
| Desktop app | UI (frontend SPA) → IPC (bridge) → Native → Worker (subprocess/external service) → Config → Types |
| Rust systems project (cross-crate workspace) | Interface → Core → Service → Infra → Config → Types |

Dependencies flow only forward/downward. Mechanically prohibit cross-layer reverse dependencies.

These are conceptual layers and need not map one-to-one to directories. For example, Runtime is orchestration in a Web app and may live inside Service in a simple project. See `project-structure.md`.

Special-architecture essentials:

- **Desktop:** UI is an embedded WebView SPA with no SSR. IPC is the frontend/native protocol boundary and must use a typed contract such as JSON Schema or TypeScript interfaces. Native owns files, processes, and system APIs. An optional Worker communicates with Native over stdio or HTTP.
- **TUI:** EventLoop dispatches events and schedules rendering. View renders layout and ANSI output without mutating State. State owns the state tree. Command translates input into state changes or service calls. Target a render frame under 16 ms.
- **Rust workspace:** Interface crates are entry points and depend only on Core's public API. Core never depends on an Interface crate. Service crates may depend on Core but not each other. Infra supports upper layers. Prevent Core bloat by creating a separate crate for non-core features.

See `architecture-special-cases.md` for detailed responsibilities, scenarios, and extended validation.

## Module Design Baseline

Use these criteria when choosing module boundaries, writing `docs/ARCHITECTURE.md`, and reviewing module shape:

- **Small interface, deep implementation:** minimize what callers must learn while hiding substantial complexity. Ask whether there can be fewer methods, simpler parameters, or more hidden complexity.
- **Deletion test:** imagine deleting the module. If complexity disappears, the module is only forwarding and should be removed. If complexity spreads into callers, the module performs real work and should remain.
- **Accept dependencies; do not create them internally:** pass collaborators as parameters instead of constructing database connections or external clients inside the module. This is the source of testability.
- **Return results; avoid hidden mutation:** computational functions return new values instead of modifying input objects in place.

These rules apply to functions, classes, files, and directories. Record critical deep modules as architecture invariants in `docs/ARCHITECTURE.md` or the AGENTS.md Architecture section.

## Applying Constraints

### Decision Flow

1. Simple project (≤3 modules, one developer) → root AGENTS.md declares `Mode=agents-only`, `Configuration=N/A`; put constraints directly in AGENTS.md.
2. Complex project (>3 modules or multiple layers) → declare `Mode=linter+agents`; choose a real configuration file from the mapping table and record it in AGENTS.md.
3. When layer-direction enforcement is required, enable the advanced configuration. Constraints a linter cannot enforce always belong in root AGENTS.md core beliefs.
4. Whenever a constraint is added or changed, synchronize its summary to root AGENTS.md core beliefs.

Core rules:

- **Error messages are agent-readable guidance:** a linter error is more effective than prose because it mechanically enforces the rule.
- **Write-back rule:** AGENTS.md is the default entry point and constraint summary. Summarize every project-level constraint source—linter configuration or child document—at the root. See `ai-coding-workflow.md` for write-back triggers.
- **Explicit mode wins:** the validator reads the root AGENTS.md declaration instead of inferring complexity from directory structure.

### Hard-Constraint Configuration Mapping

Group by language ecosystem, aligned with `tech-stack-recommendations.md`:

| Ecosystem | Default Configuration | Advanced Configuration | Mechanically Enforced | Declarative in Root AGENTS.md |
|-----------|-----------------------|------------------------|-----------------------|-------------------------------|
| **Python** | `ruff.toml` or `[tool.ruff]` in `pyproject.toml` | `[tool.importlinter]` in `pyproject.toml` | Style, import order, unused imports, line length | Layer direction without import-linter; architecture invariants |
| **JS / TS** | `eslint.config.js` flat config | Same file + `eslint-plugin-import` | Style, restricted imports, layer direction | Design principles and technology choices |
| **Vue / Svelte** | `eslint.config.js` with framework plugin | Same as JS/TS | JS/TS rules plus framework rules | Same as JS/TS |
| **Dart** | `analysis_options.yaml` | — | Lints and type-checking strictness | Architecture invariants and layer direction |
| **Rust** | `rustfmt.toml` + `clippy.toml` | `cargo audit` and similar tools | Style, lints, type safety, `cargo check` | Architecture invariants, FFI boundaries, memory-safety rules, IPC contracts, cross-crate direction |

Language notes:

- **Python:** Ruff cannot restrict import paths. Use `import-linter` for mechanical layer direction; otherwise keep it declarative.
- **Rust:** Cargo has no built-in layer-direction tool. Use `pub mod` visibility, review, and declarative constraints. See the workspace guidance above.
- **Multi-codebase projects** such as `app/` + `worker/` + `server/`: list each codebase's primary linter in `Constraint Mechanism.Configuration`, for example `` `eslint.config.js` (frontend), `ruff.toml` (worker), `rustfmt.toml` (native Rust) ``.

### Cross-Codebase and Compiled-Build Constraints

Multi-codebase coordination and compiled build systems such as Bazel, Cargo workspaces, and Gradle require additional constraints. See `architecture-special-cases.md` for the full table. Essentials:

- **Contract-first IPC:** define cross-process and cross-language communication with typed contracts such as JSON Schema, `.d.ts`, or Protobuf. Version contract changes and update every consumer; CI checks consistency.
- **One-way dependencies:** the frontend depends only on IPC contracts and never imports Native or Worker code directly.
- **Replayable protocol:** IPC messages must serialize and deserialize. Never pass closures, generators, or other non-serializable objects.
- **Clear ownership:** `app/` owns UI, `app/src-tauri/` owns native behavior, `worker/` owns AI processing, and `server/` owns accounts. Prohibit cross-boundary imports.
- **Primary/secondary build consistency:** keep primary build files in sync with sources and use the same dependency versions across primary and secondary systems.
- **Prevent Core bloat:** add new functionality in a separate crate instead of the Core crate.
- **Compile early:** Rust changes pass `cargo check` or the corresponding Bazel target before broader validation.
- **Document feature flags:** never activate `[features]` in Cargo.toml implicitly.

### Mechanically Enforced vs. Declarative

| Constraint Type | Test | Location | Example |
|-----------------|------|----------|---------|
| **Mechanically enforceable** | A linter can detect and report it | Linter configuration | `no-console`, `unused-imports` |
| **Declarative** | Requires human judgment | Root AGENTS.md core beliefs | "The data layer does not depend on the presentation layer" |

### Constraint Mechanism Declaration

The root AGENTS.md must retain this machine-readable section:

```markdown
## Constraint Mechanism

- Mode: `agents-only` or `linter+agents`
- Configuration: `N/A` or a real configuration-file path
```

In `agents-only`, Configuration must be `N/A`. In `linter+agents`, it must be a real path. CLI/single-file and simple multi-file projects default to `agents-only`; complex and multi-codebase projects use `linter+agents`. This lets agents understand enforcement without guessing and lets the validator require real files based on an explicit mode.

## Golden Principles

Candidate architecture principles for AGENTS.md core beliefs:

| Principle | Reason |
|-----------|--------|
| Shared toolkit over hand-written helpers | Centralizes invariants and avoids duplication |
| Validate boundaries instead of guessing | Agents must not guess data shapes |
| Boring technology over novelty | Broad training coverage and stable APIs |
| Transparent in-house logic over opaque libraries | Agents can understand, modify, and test it |
| Local-first over cloud-first | Desktop apps work offline, preserve privacy, and remain controllable |
| Keep Core crates lean | Separate crates prevent the core library becoming a dumping ground |

## Validation Capabilities

Agent autonomy depends on self-validation. Configure by project complexity:

| Validation Type | Projects | Example |
|-----------------|----------|---------|
| **Endpoint** | Web/API | `curl localhost:5000/health` returns 200 |
| **Page** | Web | Browser opens `localhost:3000` and displays the result |
| **Output** | CLI/script | `python main.py` prints expected output |
| **Tests** | All, recommended | `pytest` passes |
| **Types** | Typed languages | `mypy src/` or `tsc --noEmit` reports no errors |
| **Compile** | Rust/C++/Go | `cargo check` or `bazel build //...` passes |
| **Formatting** | All | `cargo fmt --check` or `ruff check` passes |

See `architecture-special-cases.md` for TUI snapshots, desktop packaging, process lifecycle, IPC contract, and platform-signing validation.

Every ExecPlan's Validation section must contain at least one executable check. Commands must be directly runnable; do not write vague steps such as "check manually."
