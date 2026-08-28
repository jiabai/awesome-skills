# Special Architecture Constraints

This document expands constraints and examples for desktop apps, TUIs, Rust workspaces, cross-codebase systems, and compiled build systems. See `architecture-constraints.md` for general layering, module design, and constraint decisions. Read this file only when the project uses one of these architectures.

## Desktop Applications

Layers: UI (frontend SPA) → IPC (bridge) → Native → Worker (subprocess/external service) → Config → Types.

- **UI:** usually a React/Vue SPA embedded in a WebView, with no SSR requirement.
- **IPC:** the frontend/native protocol boundary (Tauri commands or Electron IPC), defined with typed contracts such as JSON Schema or TypeScript interfaces.
- **Native:** Rust/Tauri code that manages files, processes, and system APIs.
- **Worker:** an optional subprocess or external service, such as a Python AI worker, communicating with Native over stdio or HTTP.

## TUI Applications

Layers: EventLoop → View → State → Command → Service → Config → Types.

- **EventLoop:** the main loop, responsible for event dispatch and render scheduling.
- **View:** terminal rendering—layout, ANSI output, scrolling regions—typically using ratatui `Widget` and `Layout` traits. It never mutates state directly.
- **State:** the application state tree, including sessions, buffers, and cursor positions. Changes go through Command.
- **Command:** translates keyboard or mouse events into state changes or service calls.
- Performance: render each frame in under 16 ms (60 fps); support xterm, kitty, and Warp.

## Rust Workspace (Cross-Crate)

Layers: Interface → Core → Service → Infra → Config → Types. Outer crates depend only on public APIs of inner crates.

Using Codex-style names as an example:

- **Interface** crates such as `codex-cli` and `codex-tui` are entry points and depend only on Core's public API.
- **Core** such as `codex-core` contains business essentials and never depends on Interface crates.
- **Service** crates such as `codex-exec` and `codex-skills` provide independent services. They may depend on Core but not on each other.
- **Infra** crates such as `codex-config`, `codex-protocol`, and `codex-secrets` provide lower-level facilities consumed by upper layers.

Critical constraint: prevent Core bloat. Create a new crate for new non-core functionality instead of adding it to Core.

## Cross-Codebase Coordination

When several independent codebases form one product, such as a desktop frontend + native layer + worker + server:

| Constraint | Meaning | Enforcement |
|------------|---------|-------------|
| **Contract-first IPC** | Define cross-process/language communication with typed contracts (`.d.ts`, JSON Schema, Protobuf); version changes | Declarative core belief + separate contract review |
| **One-way dependencies** | Frontend depends only on the IPC contract; Worker depends on contracts, never UI | `no-restricted-imports` + declarative rule |
| **Replayable protocol** | Every message serializes and deserializes; no closures, generators, or non-serializable objects | Declarative rule + integration tests |
| **Codebase ownership** | `app/` owns UI, `app/src-tauri/` Native, `worker/` AI, `server/` accounts/quotas; no cross-boundary imports | Declarative rule + review gate |
| **Contract synchronization** | Every consumer updates with a contract change; CI checks consistency | CI script + integration tests |

Example: a Tauri frontend calls Rust with `invoke('command_name', payload)`. Input and output types live in a shared `.d.ts` file or `contracts/` JSON; frontend and native implementations remain separate but share the contract.

## Compiled Build Systems

For Bazel, Cargo workspaces, Gradle, and similar systems:

| Constraint | Meaning | Enforcement |
|------------|---------|-------------|
| **Primary/secondary build relationship** | Declare the production build system and keep its BUILD files synchronized with sources | AGENTS.md core belief + CI build |
| **Dependency consistency** | Use the same dependency version in primary and secondary systems | Update script + lockfile diff |
| **Cross-crate visibility** | Rust `pub mod` controls visibility; do not re-export internals as public API | `clippy::restricted_public_levels` + review |
| **Prevent Core bloat** | New non-core functionality gets a separate crate | Declarative rule + PR gate |
| **Compile first** | Every Rust change passes `cargo check` or the relevant Bazel target | CI + pre-commit hook |
| **Synchronize BUILD files** | New sources or dependencies update Bazel BUILD targets | Declarative rule + CI Bazel build |
| **Feature flags** | Document every Cargo feature; prohibit implicit activation | Declarative rule + `cargo tree --features` |

Example: a project uses Bazel for production/CI and Cargo for local development. After Rust changes, run `cargo check`, then `just fix` (rustfmt + clippy) and `just test`. CI runs the full `bazel test` suite to verify BUILD/source consistency.

## Multi-Codebase Configuration Examples

For `app/` + `worker/` + `server/`, list each primary linter in root `Constraint Mechanism.Configuration`:

```markdown
- Mode: `linter+agents`
- Configuration: `eslint.config.js` (frontend), `ruff.toml` (worker), `rustfmt.toml` (native Rust)
```

For a Rust workspace:

```markdown
- Mode: `linter+agents`
- Configuration: `rustfmt.toml` (workspace), `clippy.toml` (workspace), `deny.toml` (dependency audit)
```

## Extended Validation

In addition to general checks from `architecture-constraints.md`:

| Validation | Project | Method | Example |
|------------|---------|--------|---------|
| **TUI rendering** | TUI | Compare terminal snapshots | Start app → capture ANSI snapshot → diff against expected output |
| **Desktop build** | Desktop | Full package + installer test | `npm run tauri build` creates an installable package that launches |
| **Process lifecycle** | Desktop with Worker | Start/stop/crash recovery | Start Worker → force-kill it → verify watchdog recovery |
| **IPC contract** | Cross-codebase | End-to-end serialization test | Send complete message → Native receives/returns → frontend parses |
| **Platform signing** | Distributed desktop app | Signature/notarization checks | macOS: `codesign --verify` + `spctl --assess`; Windows: `signtool verify` |
