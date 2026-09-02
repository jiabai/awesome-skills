# Requirements Elicitation Method (Phase 1.5)

This document defines how Phase 1.5—after learning about the user but before recommending a tech stack—turns a one-sentence idea into requirements suitable for a spec. See `workflow-governance.md` for the Spec template and `phase-guidance.md` for interaction language.

## Contents

- [Purpose and Outputs](#purpose-and-outputs)
- [Domain Adaptation](#domain-adaptation)
- [Elicitation Depth](#elicitation-depth)
- [Three Elicitation Techniques](#three-elicitation-techniques)
- [User-Story List](#user-story-list)
- [Glossary (CONTEXT.md)](#glossary-contextmd)
- [Tone](#tone)
- [Completion Criteria](#completion-criteria)
- [Common Mistakes](#common-mistakes)

---

## Purpose and Outputs

Phase 1 establishes what the user is building, which languages they know, and which OS they use. Phase 1.5 answers: **What exactly should this project do, and what would make it good enough?** Without this step, Phase 7 can only synthesize a spec from vague conversational memory.

| Output | Formed | Persisted |
|--------|--------|-----------|
| User-story list | Confirmed one item at a time in conversation | Written to the Product Spec's User Stories section in Phase 7 |
| Glossary of clarified domain concepts | Captured throughout the conversation | Written to root `CONTEXT.md` in Phase 4 when warranted |
| Definition of success | Confirmed in conversation | Written to the Product Spec's Acceptance Criteria section in Phase 7 |

The project directory may not exist during Phase 1.5. Hold these outputs in the conversation until Phase 4 and Phase 7 persist them.

## Domain Adaptation

Use the generic elicitation framework to generate domain-specific questions dynamically. The framework determines how to ask; the project context determines what to ask.

Before the first elicitation round:

1. Identify the likely domain and business model from the user's words. State the inference briefly and invite correction.
2. Build a temporary domain map covering actors and permissions, core entities, lifecycle and state transitions, business rules, integrations, failure and recovery, and security, compliance, or deployment risks.
3. Rank unanswered questions by their impact on scope, architecture, and risk. Ask only the next 1–3 highest-value questions, then wait for the user's answers.
4. Use the user's domain language. If the user cannot answer, offer concrete alternatives or a real-life scenario; treat every model-generated option as a suggestion until the user confirms it.
5. Track each item as **confirmed**, **open**, or **assumption**. Never promote an assumption into a user story, acceptance criterion, or implementation decision without confirmation.
6. Rebuild or refine the domain map after every answer and use it to select the next questions. For legal, tax, payment, privacy, or other regulated boundaries, identify the jurisdiction and flag the rule for authoritative verification before implementation.

For example, after "I want an e-commerce independent site," derive a map around customers, administrators, products and variants, inventory, carts, orders, payments, shipments, refunds, and notifications. Then ask about the product type and target market before asking about page layout or technology.

## Elicitation Depth

| Project Size | Signals | Intensity |
|--------------|---------|-----------|
| Small | Explainable in one sentence, one user, no payments/permissions/roles | Lightweight: 3–5 core questions and one confirmation round |
| Medium | Two or more user types, state transitions, accumulating data | Standard: user stories + terminology + scenario stress tests |
| Large | Multiple roles or clients, payments, collaboration, or external integrations | Full: standard flow + prototypes for disputed boundaries |

When scope or risk is uncertain, ask targeted follow-ups before choosing a shallower depth. Use a shallow path only for a clearly small project or when the user explicitly prioritizes speed. If the user cannot answer, offer a binary choice or disposable prototype, then confirm the decision.

## Three Elicitation Techniques

### 1. Sharpen Terminology

When the user uses an ambiguous or overloaded word, propose precise canonical terms immediately:

```text
User: "I want to record every transaction."
Follow-up: "Does a transaction mean money you spent, or also money someone owes you? We can call these 'expense' and 'receivable' from here on. Does that distinction work?"
```

Rules:

- Clarify immediately when one word is used for two meanings or two words are mixed for one meaning.
- Add the result to a working glossary: **canonical term + one- or two-sentence definition + aliases to avoid**.
- Include only concepts specific to this project. Generic programming terms such as timeout and cache do not belong.

### 2. Stress-Test Scenarios

Invent edge cases to reveal conceptual boundaries. Users may struggle to state requirements along a happy path but immediately correct a counterexample:

```text
"Suppose you record an expense and later notice the amount is wrong. Should you edit it, or delete it and create a new one? Those choices affect the monthly report differently."
"Two family members each record an expense on the same day. Should the monthly report combine them or show them separately?"
```

Rules:

- Ask 1–3 scenarios per round, then wait for an answer.
- Prefer scenarios that should fail or actions that should not be allowed; they expose boundary gaps quickly.
- "I haven't thought about that" is normal. Offer a binary choice and record the decision.

### 3. Prototype Validation

When requirements remain unclear or the user cannot answer abstract questions, generate a **disposable single-file HTML prototype** that opens directly with no framework, build, or installation.

**Logic prototype** (validates state transitions or business rules):

- State the question the prototype is answering at the top of the page.
- Label controls and states in domain language ("Record an expense," not "Call addExpense()").
- Show the complete current state after every action.
- Put business logic in independent pure functions or modules so validated decisions can later move into real code.

**UI variant prototype** (validates visual structure):

- Include three **structurally different** options in one file: different layouts or information hierarchies, not just different colors.
- Add a switcher at the bottom with arrows and an always-visible current variant name.

Prototype rules:

- Disposable: no persistence, tests, or error handling. Its mission ends when it answers the question.
- Write it to the current working directory as `prototype-<topic>.html`; after capturing the decision, tell the user it can be deleted.
- When the user says, "Wait, that should not be allowed," immediately update the working user stories or glossary before continuing.
- Feedback such as "use A's layout with B's input method" is an ideal result. Record it verbatim instead of choosing for the user.

## User-Story List

This is the primary elicitation output. Format:

```text
As a <role>, I want <capability> so that <benefit>.

1. As a person tracking expenses, I want to categorize each transaction so that I know where my money went at the end of the month.
2. As a person tracking expenses, I want monthly summaries so that I can compare spending across months.
```

Rules:

- Use a concrete person as the role ("person tracking expenses," "parent reviewing reports"), not an empty word such as "user."
- Cover every confirmed scenario, including stories derived from edge cases.
- Aim for 3–8 stories. More than 10 suggests the project may be too large; ask whether the first release should be narrowed.
- Obtain user confirmation for every story. Do not invent stories on the user's behalf.

## Glossary (CONTEXT.md)

Persistence decision, applied in Phase 4:

| Condition | Action |
|-----------|--------|
| Three or more project-specific terms were clarified | Generate root `CONTEXT.md` using the template in `docs-templates.md` |
| Fewer than three terms, with no significant ambiguity | Do not generate it; put essential concepts in `AGENTS.md` core beliefs |

After generating `CONTEXT.md`, add `- Glossary: see CONTEXT.md` to the root `AGENTS.md` Quick Entry section.

Every later artifact—Spec titles, task names, test names, and code identifiers—must use canonical terms from `CONTEXT.md`, never aliases marked Avoid.

## Tone

**Be relentless with the idea and compassionate with the person.**

- Challenge conceptual boundaries and scenario gaps, not the user's competence. Ask "How should these two cases differ?" instead of "You did not explain this clearly."
- Ask only 1–3 questions per round, then stop.
- When the user says "I don't know" or "I haven't thought about it," switch to a real-life analogy, a binary choice, or a prototype. Do not repeat the same abstract question in different words.
- Let the user change their mind. A changed decision means elicitation is working, not that someone made a mistake.

## Coverage Check

Before completion, inspect the applicable categories: happy path, edge and negative cases, actors and permissions, data lifecycle, failure and recovery, integrations, and security or deployment. Ask a follow-up for each unaddressed category; mark a category N/A only after the user confirms it.

## Completion Criteria

Phase 1.5 is complete only when all of the following are true:

1. The user-story list contains at least three stories, each confirmed by the user.
2. Every ambiguous key term has been clarified and captured in the working glossary.
3. One paragraph can explain what users will do with the finished project and what counts as success.
4. The user explicitly confirms that requirements are complete.
5. The domain map has been confirmed by the user or its remaining items are explicitly marked as assumptions.
6. All applicable coverage categories are answered or marked N/A, and unresolved assumptions are explicit.

Summarize the elicitation—the number of user stories, number of terms, and a one-sentence draft of acceptance—then obtain confirmation before entering Phase 2 tech stack recommendations.

## Common Mistakes

| Mistake | Consequence | Correct Approach |
|---------|-------------|------------------|
| Recommend a tech stack before elicitation | Phase 7 invents a Spec from impressions, causing rework | Meet the elicitation completion criteria first |
| Interrogate the user with a long question chain | Non-technical users become overwhelmed and invent answers | Ask 1–3 questions per round; switch to a prototype when needed |
| Choose shallow depth because scope is uncertain | Material assumptions survive into implementation | Ask targeted follow-ups and complete the applicable coverage check |
| Invent user stories | The Spec reflects the agent's imagination | Confirm every story with the user |
| Generate CONTEXT.md for every project | Empty documents are more dangerous than missing ones | Generate only with at least three terms |
| Polish the prototype | Time is spent on appearance instead of answering the question | Keep it disposable and stop once the question is answered |
| Fail to record prototype findings | Newly discovered boundaries are lost | Update working outputs after every "that's not right" moment |
