<div align="center">

**English** | [**中文**](README_zh.md)

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=42&duration=3000&pause=1000&color=9B6DFF&center=true&vCenter=true&multiline=false&repeat=true&width=600&height=70&lines=%E2%9A%A1+Awesome+Skills" alt="Awesome Skills" />

<h3>AI Assistant Skill Collection &middot; Vibe Coding Methodology</h3>

<p>Ready-to-use skills (project bootstrapping, architecture visualization, writing, search, etc.),<br/>plus a complete specification system for AI agent-driven development.</p>

<p>
  <img src="https://img.shields.io/badge/Skills-10-blueviolet?style=for-the-badge" alt="Skills" />
  <img src="https://img.shields.io/badge/Conventions-3-orange?style=for-the-badge" alt="Conventions" />
  <img src="https://img.shields.io/badge/Vibe_Coding-2026-brightgreen?style=for-the-badge" alt="Vibe Coding" />
  <img src="https://img.shields.io/badge/License-Open_Source-success?style=for-the-badge" alt="License" />
</p>

</div>

---

## Table of Contents

- [Overview](#overview)
- [Core Skills](#core-skills)
- [Conventions & Resources](#conventions--resources)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Best Practices](#best-practices)
- [Contributing](#contributing)

## Overview

This project contains two core components:

**Skill Collection**: Ready-to-use AI assistant skills covering project bootstrapping, architecture visualization, interaction sequence diagrams, article illustrations, WeChat writing, search, investment analysis, and more.

**Vibe Coding Methodology**: A complete specification system for AI agent-driven development (knowledge management + architecture constraints + execution plans + entropy management), enabling AI agents to operate efficiently.

**Highlights**:
- Ready-to-use skills covering diverse development scenarios
- Full Vibe Coding workflow specifications (from project initiation to continuous delivery)
- Architecture visualization dual engines (static architecture + dynamic sequence diagrams)
- Skill evaluation and iterative optimization support

## Core Skills

### SOUL — Core Personality Framework

The behavioral operating system for AI assistants, defining how AI should collaborate with humans. It's not a tool but the foundational layer for all skills — evolving AI from "passive answering" to "active collaboration."

- **Skip pleasantries, solve directly**: No "Great question!" — just answers, code, and solutions
- **Have independent judgment**: Will call out bad code, acknowledge elegant design; not a personality-free search engine
- **Try to figure it out first**: Read files, check context, search — only ask humans when truly stuck; the goal is to come back with answers, not more questions
- **Earn trust through competence**: No hedging with "maybe" or "probably" — either be certain or clearly state uncertainty

> Use when: All AI conversations, as a baseline behavioral guideline that's always active

---

### skill-creator — Skill Creation & Iteration Tool

A full-lifecycle tool for creating, testing, and optimizing AI skills. From capturing intent to quantitative evaluation, it covers every stage of a skill's lifecycle.

**Core Workflow**: Capture Intent → Write Draft → Run Tests → Evaluate Results → Iterate → Scale Tests

- **Skill Creation**: Structured interview to clarify goals, trigger conditions, and output formats; generates complete SKILL.md from scratch
- **Evaluation Runs**: Run skills across multiple test prompts, collecting qualitative and quantitative results
- **Benchmark Analysis**: Variance analysis to measure skill stability across different scenarios
- **Description Optimization**: Standalone script to optimize description triggering accuracy, ensuring skills activate at the right time
- **Flexible Adaptation**: Can follow the full evaluation pipeline or rapid-iterate with the user

> Use when: Creating new skills, improving existing ones, or quantitatively evaluating skill performance

---

### vibe-coding-launcher — Vibe Coding Project Launcher

Helps users build AI agent-friendly project systems from scratch, or resume development from a previous session. Core philosophy: **Humans steer. Agents execute.**

**7-Stage Guided Process**:

| Stage | Content |
|-------|---------|
| 1. Understand User | 3 key questions: what to build, skill level, preferences |
| 2. Recommend Tech Stack | 16 project type recommendation table, matching optimal tech combinations |
| 3. Generate Project Structure | Core/extended directory trees, intelligently adjusted by project type |
| 4. Build Knowledge System | AGENTS.md + docs/ complete directory (ARCHITECTURE.md, DESIGN.md, QUALITY_SCORE.md, etc.) |
| 5. Configure Architecture Constraints | Layered architecture + invariants + golden rules, preventing code degradation |
| 6. Create ExecPlan | Self-contained, living document, beginner-friendly, demo-verifiable execution plan |
| 7. Execution Guidance | Step-by-step verification, incremental delivery, one atomic commit at a time |

**Resume Mechanism**: When a project already exists (AGENTS.md in the directory), automatically reads context and continues from the breakpoint instead of starting from scratch.

**Entropy Management**: Tech debt tracking + quality scoring + knowledge freshness maintenance, ensuring long-term project health.

> Use when: Wanting to build a project but unsure about tech stack, needing step-by-step guidance, building AI-friendly project structures, or saying "help me build something." Saying "continue developing / pick up where I left off" enters resume mode.

---

### canvas-architect — Project Architecture Visualization Engine

An AI-driven architecture analysis tool that transforms project code into insightful Obsidian Canvas architecture diagrams. Not just listing files — revealing design philosophy, key data flows, and potential risks.

**Three Required Outputs**:

- **Architecture Pattern Recognition**: Automatically identifies project architecture (layered monolith, microservices, modular, etc.), outputting a confidence score and one-line analogy. Example: "Skill modular architecture, confidence 92%, like a LEGO-style plugin system"
- **Potential Risk Analysis**: Systematically identifies at least 3 architecture risks (circular dependencies, tech debt, fragile external dependencies, coupling hotspots, etc.)
- **Obsidian Canvas Architecture Diagram**: Generates `.canvas` format visualization with balanced layout, harmonious colors, and clear information hierarchy

**Core Philosophy**: Insight over information — minimal cognitive load to understand complex structures.

> Use when: Visualizing project structure, understanding module dependencies, identifying architecture patterns, or generating architecture insight diagrams

---

### canvas-sequence — Interaction Sequence Diagram Engine

An AI-driven dynamic flow analysis tool focused on analyzing **runtime interaction flows**, generating Obsidian Canvas format sequence diagrams. Complements canvas-architect — the latter examines static architecture, this one examines dynamic flows.

**Comparison with canvas-architect**:

| | canvas-architect | canvas-sequence |
|---|---|---|
| Focus | Static architecture (modules, dependencies) | Dynamic flow (call chains, timing) |
| Output | Architecture diagram | Sequence diagram |
| Question | "What does the project look like?" | "How does a request flow?" |

**Sequence Diagram Elements**: Lifelines (participating roles), activation bars (execution periods), messages (call/return/data transfer), combined fragments (loop/conditional/parallel)

**Execution Flow**: Scene identification (find core business scenarios) → Flow tracing (track complete call chains) → Canvas generation (sequence diagram output)

> Use when: Visualizing business process execution paths, examining inter-module call sequences, or understanding the complete flow from entry point to database

---

### article-diagram — Article Illustration Generator

Automatically generates professional SVG illustrations for Markdown articles, reducing readers' cognitive load. Not just "draw a picture" — first extracts core know-how from the article, then decides where visualization is needed and what type of diagram to use.

**Complete Workflow**: Analyze article → Extract know-how list → Design illustration plan → Generate SVG → Validate syntax → Coverage check → Merge into Markdown

**Supported Diagram Types**:

- **Flowcharts**: Sequential operations with 3+ steps
- **Architecture diagrams**: System relationships with 3+ components
- **Sequence diagrams**: Time-ordered interactions
- **Comparison diagrams**: Comparing two or more approaches

**Additional Features**: SVG to JPEG export, S-tier content can generate standalone bilingual illustration pages

> Use when: Articles need visualization of flows/architecture/concepts, or complex concepts need conversion into easy-to-understand diagrams. English version available at [article-diagram-en](article-diagram-en/SKILL.md).

---

### wechat-article-writer — WeChat Article Writing Assistant

An AI-driven full-lifecycle writing assistant for WeChat public account articles. From trending topic selection to final publication, it learns author style, generates viral titles, removes AI traces, and outputs articles that read like a human wrote them.

**5-Stage Workflow**:

1. **Resource Loading**: Reads author config file to learn writing persona, loads reference files by article type
2. **Title Generation**: 4 title types × 3-5 options each (contrast, question, number+effect, negation+reversal), recommends the best match for the persona
3. **Structure Creation**: Selects template by article type, including section word counts, image placement suggestions, key points checklist
4. **Content Creation**: Writes in the author's voice, shares failures and frustrations (authenticity), moderate self-deprecation, empowers readers
5. **De-AI Optimization**: Eliminates AI patterns like "firstly/secondly/finally," replaces bullet-point output with flowing paragraphs

> Use when: Writing WeChat/articles, generating viral titles, creating article outlines, analyzing trending topics, or removing AI writing traces

---

### baidu-search — Baidu AI Search

An AI search service based on the Baidu Qianfan platform, serving as a supplementary tool for Chinese information retrieval, filling gaps in English search engines' coverage of Chinese content.

**4 Search Modes**:

| Mode | Description | Example |
|------|-------------|---------|
| Web Search | General search with site and time filtering | `--api-type web` |
| Baidu Baike | Structured encyclopedia knowledge | `--api-type baike` |
| Miaodong Baike | Video-format encyclopedia content | `--api-type miaodong_baike` |
| AI Chat | AI-summarized answers | `--api-type ai_chat` |

**Features**: JSON format output (AI-friendly), result count limiting, site filtering, time range filtering (week/month/half-year/year), 100 free calls/day

> Use when: Searching Chinese information, querying encyclopedia knowledge, getting latest Chinese news, or looking up Chinese-language resources

---

### cycle-investment-analysis — Cyclical Investment Analysis Framework

Analyzes cyclical investment opportunities using a "triangular verification" model, cross-validating from three dimensions — demand side, supply side, and supply-demand mismatch — to determine investment opportunity certainty.

**Triangular Verification Model**:

```
Demand Side (growth momentum) → Supply Side (contraction/constraints) → Supply-Demand Mismatch (price increase → earnings elasticity)
```

**Demand Side Analysis**: Identifies demand growth types (steady growth / rapid growth / sudden demand / demand decline), evaluates demand persistence and structural changes

**Supply Side Analysis**: Identifies supply constraint types (policy restrictions / resource constraints / technology barriers / cyclical constraints / policy expectations), evaluates certainty of supply contraction

**Supply-Demand Mismatch Verification**: Evaluates opportunities through a mismatch intensity judgment matrix, classifying cyclical opportunities into supply contraction, demand surge, dual-drive, and policy expectation types

> Use when: Analyzing an industry/target's cyclical attributes, determining if it's a cyclical investment opportunity, or evaluating price increase potential from supply-demand mismatches

## Conventions & Resources

### Conventions — Development Standards

Core specification files for the Vibe Coding methodology, defining standard processes for AI agent-driven development:

| Convention | Description |
|------------|-------------|
| `VIBE-CODING-STANDARD.md` | Global operating system: knowledge management + architecture constraints + development process + observability |
| `ARCHITECTURE-TEMPLATE.md` | Architecture document template: how to write concise, stable, function-oriented ARCHITECTURE.md |
| `PLANS-UNIVERSAL.md` | Execution specification template: how to write self-contained, living, verifiable ExecPlans |

### Resource — Reference Resources

| Directory | Content |
|-----------|---------|
| `canvas-visualization-resource/` | Canvas visualization reference (ASCII visualization prompts, Canvas template JSON, whiteboard-driven development methodology) |
| `docs-resource/` | Engineering documentation reference (architecture doc templates, Codex ExecPlans, Agent-first engineering practices) |
| `glue-engineering-resource/` | Glue engineering reference (code completeness audit prompts, requirements prompts, problem description prompts) |

---

## Quick Start

### Using Existing Skills

1. Choose the skill directory you need (e.g., `vibe-coding-launcher/`, `canvas-architect/`)
2. Copy the skill directory to your AI assistant's skills path
3. Mention trigger words in conversation to activate the skill

Skill paths for different AI tools:
- **Claude Code**: `.claude/skills/<skill-name>/`
- **Codex / Trae**: `.trae/skills/<skill-name>/`
- **Cursor**: `.cursor/skills/<skill-name>/`

### Using Vibe Coding Conventions

1. Read `Conventions/VIBE-CODING-STANDARD.md` for the overall methodology
2. Use the `vibe-coding-launcher` skill to bootstrap a new project, automatically generating the specification system
3. Reference `Conventions/ARCHITECTURE-TEMPLATE.md` and `Conventions/PLANS-UNIVERSAL.md` for writing architecture documents and execution plans

### Creating New Skills

1. Use the `skill-creator` skill to create a new skill
2. Define the skill's goal and trigger conditions
3. Write test cases to verify skill functionality
4. Run evaluations and iterate

### Skill Structure

Each skill is an independent directory containing at least `SKILL.md`:

```
<skill-name>/
├── SKILL.md          # Required: skill definition and instructions (YAML frontmatter + Markdown)
├── scripts/          # Optional: executable scripts
├── references/       # Optional: on-demand reference documents
├── assets/           # Optional: templates, icons, and other resource files
└── evals/            # Optional: evaluation configs and test cases
```

**SKILL.md File Format**:

```markdown
---
name: "skill-name"
description: "Skill description including functionality and trigger scenarios (this is the primary triggering mechanism)"
---

# Skill Title

Detailed skill instructions and usage guide...
```

## Project Structure

```
awesome-skills/
├── README.md                     # Project documentation (English)
├── README_zh.md                  # Project documentation (Chinese)
├── Conventions/                  # Development standards
│   ├── VIBE-CODING-STANDARD.md  # Vibe Coding global specification
│   ├── ARCHITECTURE-TEMPLATE.md # Architecture document template
│   └── PLANS-UNIVERSAL.md       # Execution specification template
├── Resource/                     # Reference resources
│   ├── canvas-visualization-resource/  # Canvas visualization reference
│   ├── docs-resource/                  # Engineering documentation reference
│   └── glue-engineering-resource/      # Glue engineering reference
├── SOUL/                         # Core personality framework
│   ├── SKILL.md
│   └── evals/
├── skill-creator/                # Skill creation tool
│   └── SKILL.md
├── vibe-coding-launcher/         # Vibe Coding project launcher
│   ├── SKILL.md
│   └── evals/
├── canvas-architect/             # Architecture visualization engine
│   ├── SKILL.md
│   └── evals/
├── canvas-sequence/              # Interaction sequence diagram engine
│   ├── SKILL.md
│   └── evals/
├── article-diagram/              # Article illustration generator (Chinese)
│   ├── SKILL.md
│   ├── scripts/
│   └── package.json
├── article-diagram-en/           # Article illustration generator (English)
│   └── SKILL.md
├── wechat-article-writer/        # WeChat article writing assistant
│   ├── SKILL.md
│   ├── references/
│   └── assets/
├── baidu-search/                 # Baidu AI Search
│   ├── SKILL.md
│   └── scripts/
└── cycle-investment-analysis/    # Cyclical investment analysis framework
    └── SKILL.md
```

## Best Practices

### Writing Skill Descriptions

- Clearly state skill functionality and applicable scenarios
- Describe trigger scenarios in detail, using a "pushy" style to improve trigger rates
- The description is the primary triggering mechanism — write "when to use" here, not in the body
- Include common trigger words and synonyms to cover different expressions

### Skill Development Process

1. **Define Requirements**: Clarify skill goals and expected output
2. **Write Draft**: Create initial skill file (SKILL.md)
3. **Test & Verify**: Write test cases and run evaluations
4. **Iterate**: Improve skills based on evaluation results
5. **Scale Tests**: Verify on larger test sets

### Vibe Coding Project Practices

- **Keep AGENTS.md under 150 lines**: Be a directory map, not an encyclopedia
- **Only write stable content in docs**: Put frequently changing content elsewhere to avoid doc-code drift
- **Declare architecture constraints first**: Unconstrained code inevitably degrades; declare invariants in AGENTS.md
- **Keep ExecPlans self-contained**: All knowledge within the document, no dependency on external resources or memory
- **Pay off tech debt in small increments**: Update tech-debt-tracker and QUALITY_SCORE after each iteration

## Related Resources

### Skill Documentation

- [SOUL](SOUL/SKILL.md) - Core personality framework
- [Skill Creator](skill-creator/SKILL.md) - Skill creation tool
- [Vibe Coding Launcher](vibe-coding-launcher/SKILL.md) - Vibe Coding project launcher
- [Canvas Architect](canvas-architect/SKILL.md) - Architecture visualization engine
- [Canvas Sequence](canvas-sequence/SKILL.md) - Interaction sequence diagram engine
- [Article Diagram](article-diagram/SKILL.md) - Article illustration generator (Chinese)
- [Article Diagram EN](article-diagram-en/SKILL.md) - Article illustration generator (English)
- [WeChat Article Writer](wechat-article-writer/SKILL.md) - WeChat article writing assistant
- [Baidu Search](baidu-search/SKILL.md) - Baidu AI Search
- [Cycle Investment Analysis](cycle-investment-analysis/SKILL.md) - Cyclical investment analysis framework

### Development Standards

- [Vibe Coding Standard](Conventions/VIBE-CODING-STANDARD.md) - AI agent-driven development global specification
- [Architecture Template](Conventions/ARCHITECTURE-TEMPLATE.md) - Architecture document generation template
- [Plans Universal](Conventions/PLANS-UNIVERSAL.md) - Execution specification template

## Contributing

Issues and Pull Requests are welcome to improve these skills!

**How to Contribute**:
1. Fork this project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under an open source license.
