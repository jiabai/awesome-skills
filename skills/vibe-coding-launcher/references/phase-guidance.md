# Phase Interaction Guide

`SKILL.md` contains only entry points and the phase overview. This document contains confirmation language, step templates, terminology, pitfalls, and examples. See `validation-standards.md`, `task-management.md`, and `architecture-constraints.md` for their respective rules.

## Human-Gate Confirmation

Use this format at a direction-setting gate: requirements, stack, generated document set, Product Spec, or ExecPlan.

```text
{Phase Name} is complete:
- {Completed item 1}
- {Completed item 2}

Confirm whether to continue to the next phase. Reply with:
- "Continue" or "OK" — enter the next phase
- "Issue: xxx" — resolve the issue first
- "Pause" — end this conversation and recover next time
```

- Wait for a reply at these gates.
- After the user approves an ExecPlan or lightweight task, continue autonomously through meaningful milestones. Pause again only for the exceptions defined in `SKILL.md`.

## Applicability Check

After invocation, verify that the request is genuinely a project launch or project-recovery orientation.

| Request | Response |
|---------|----------|
| New project / uncertain tech stack / needs AI-friendly project system | Continue the phase workflow |
| Existing project; user says continue, resume, or previous project | Enter recovery mode: read context, attempt validation, summarize |
| Isolated function, snippet, or programming question | Exit launch workflow and answer or implement directly |
| Bug, debugging, routine small feature, or refactor | Exit launch workflow; if AGENTS.md exists, read it only as project context |
| Routine iteration after governance exists | Exit launch workflow and follow the project's AGENTS.md / WORKFLOW.md |

When exiting, explain why in one sentence. Do not generate project structure, Specs, ExecPlans, or docs.

## Recovery Confirmation

The first recovery round performs orientation only. Even when the user says "continue," present a recovery summary and wait for a second confirmation before advancing.

If the project's validator is missing, do not generate or repair governance documents automatically. Prefer this skill's `scripts/validate_agents_docs.py --project <project-root>`. If that cannot run, record "validator missing / not validated" as an uncertainty and still complete the summary.

Format:

```text
Context recovered:
- Sources: AGENTS.md, TASKS.md, docs/exec-plans/active/...
- Current phase/stopping point: ...
- Completed: ...
- Candidate next step: ...
- Uncertainties: ...

Continue from "..."?
```

Only after the user replies "continue," "confirmed," or "start here" may the agent create a plan, update tasks, or execute code.

## Phase 8 Milestone Update

```text
## Milestone N: {Milestone Name}
- Result: {observable outcome}
- Validation: {check and result}
- Next: {next approved milestone}
```

- Continue after the update when the next milestone is already approved.
- Pause when authorization, a new decision, changed scope or risk, or an unresolved error requires user input.

## Handling Problems

When the user reports a problem:

1. Ask for the exact error, preferably a screenshot or original text.
2. Provide a targeted resolution.
3. Resume only after the problem is resolved; do not skip the step.

## Deployment Guidance After Delivery

After Phase 8 completion gates pass, check whether the project is deployable: it has `docs/DEPLOYMENT.md` or is a Web/API/server project.

For a deployable project, append:

```text
Development is complete. To deploy to a cloud server, reply "Deploy."
I will guide you through docs/DEPLOYMENT.md one step at a time—you run commands in your SSH terminal, and I validate the results.
```

- Use deployment pacing: one command → user runs it → user reports success or exact error → validate before the next command.
- The agent never runs remote commands directly or requests server passwords. See `deployment-spec.md`.
- Do not offer deployment for local CLI or serverless projects, or when the user does not want it.

## Language Style

- Concise: one sentence, one purpose.
- Concrete: provide an exact command or action.
- Friendly: let users say "I don't understand" and explain patiently.
- For beginners, use real-life analogies rather than explaining jargon with more jargon.

## Common Terms

| Concept | Plain-Language Explanation |
|---------|----------------------------|
| Terminal / command line | A program where you type commands for the computer to run |
| Editor | A tool for writing code, such as VS Code |
| Dependency / library | Code written by someone else that the project can reuse |
| API | An interface exposed by a website or service |
| AGENTS.md | The entry-point map that tells AI agents how the project is organized |
| User story | "As a <role>, I want <capability> so that <benefit>" |
| CONTEXT.md | A project glossary of canonical terms and aliases to avoid |
| TASKS.md | A temporary checklist of work and its validation |
| ExecPlan | A step-by-step implementation plan for an AI agent |
| Architecture constraint | A rule that prevents code structure from degrading |

## Common Pitfalls

| Claim | Reality | Correct Response |
|-------|---------|------------------|
| The user already described the project, so no questions are needed | Language familiarity and OS are often missing | Ask only for missing items, but complete all three Phase 1 questions |
| Recommend a stack immediately after hearing the idea | Without elicitation, Phase 7 invents the Spec | Perform requirements elicitation between Phases 1 and 2 |
| Elicitation should be exhaustive questioning | Non-technical users become overwhelmed and invent answers | Ask 1–3 questions per round; use a prototype or binary choice |
| A simple project is faster if code starts immediately | Without governance, later work slows down | Establish the core set first |
| An isolated function or bug should enter all eight phases | It is a task, not a project launch | Handle directly; read existing AGENTS.md only as context |
| Recovery is too slow; start coding | Skipping AGENTS.md loses architecture context | Recover first, then enter the current phase |
| "Continue" authorizes immediate action | There may be uncertainty or unfinished work | Summarize state and wait for confirmation |
| A CLI should get `docs/` just in case | Empty documents are more dangerous than missing ones | Do not generate `docs/` for CLI/single-file projects |
| An approved Phase 8 plan still needs confirmation after every task | Excess pauses fragment execution without adding a decision | Continue through approved milestones; pause only at human gates |
| Development ends without deployment guidance | Projects with DEPLOYMENT.md stop before the last mile | Offer guided deployment in the final report |
| Add constraints later | Architecture degrades naturally | Establish constraints in Phase 5 |
| TASKS.md needs checkboxes but no validation | Completion cannot be proven | Every task includes a `✅` condition |

## Scenarios

| Scenario | User Input | Recommended Response |
|----------|------------|----------------------|
| Beginner project | "I want a small expense-tracking web page" | Ask three questions → elicit user stories and terms → recommend the simplest stack → generate core structure |
| CLI tool | "I want a tool that sends email automatically" | Recommend Python → identify CLI → build core set first |
| AI application | "Build me a chatbot" | Recommend the simplest viable approach → follow the complex-project workflow |
| Recovery | "Continue the project from last time" | Read AGENTS.md + TASKS.md → summarize current state → wait for confirmation |
