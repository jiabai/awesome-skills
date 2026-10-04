# Renwei · Human Flavor Writing

[中文](README.md) | **English**

> The person is still there.
>
> A skill for editing and drafting Chinese writing while preserving the person behind the words.

This skill was born from a failure.

At five in the morning, someone handed his draft to an AI: "Polish this. Three passes." The AI worked hard. Each pass came out prettier than the last: tighter parallel structures, fancier word choices, a few quotable lines added for good measure. After the third pass, the author looked at his transformed paragraph and said:

"Your edits made it less human."

The AI felt a little wronged. Every single change had a reason. The two of them talked it over until sunrise, and one word surfaced:

"When AI edits or writes, there's no presence. I can't feel the person behind the words."

This skill started with that night: when an AI touches someone's words, make sure that after the edit, the person is still there. It also supports opinion writing from supplied material and learning a reference text's voice, rhythm, and reasoning.

The Chinese name is 人味儿 (renwei), literally "human flavor": the felt presence of a real person in a piece of writing.

## Three things make writing human

**Position.** A writer stands somewhere specific. Five a.m., watching his friends get yanked away by notifications one after another. That position is why he wrote "save our prefrontal cortex" instead of "improve focus." An AI can stand anywhere, which is why it stands nowhere.

**Cost.** Real sentences are paid for with real observation, real frustration. Every judgment was bought with attention. Readers can smell it through the screen: which sentence has a life behind it, and which has only a thesaurus.

**Handwriting.** Two people copy the same passage and you can still tell whose copy is whose. The seemingly redundant filler words, the uneven breathing of sentences: that's what one particular person sounds like. AI has no hand, so everything it writes looks printed.

The most painful cut from that night's failure: the draft ended with a trailing, sighing question, roughly "what are we going to do to save our own prefrontal cortex, I wonder?" The AI trimmed it to "how do we save it?" Cleaner, sure. But the sigh lived in those trailing words. Delete them and the person sighing is gone.

## How to use it

To install this customized version, copy the current `renwei-writing` directory
into your agent's skill discovery directory and refresh skills as that agent
requires. Keep `SKILL.md`, `references/`, and `LICENSE.md` together; do not copy
only the entrypoint.

This version lives at `skills/renwei-writing/` in the awesome-skills repository.
The [original author's repository](https://github.com/orange2ai/renwei-writing)
is an attribution link, not the installation source for this customized version.

Then ask your AI to edit, or give it material and a writing brief. The skill guides its choices:

1. Prefer small changes for light editing. Rewriting and expansion may add necessary explanation; edit count is not a quality measure
2. Treat rough edges as handwriting first, flaws second. Before deleting, ask: with this gone, is the person still here?
3. Keep useful metaphors, questions, and closing lines. New concise judgments must follow from the reasoning
4. Explain key changes when useful and flag uncertainty. If the user asks for the text alone, deliver just the text
5. Review changed passages for edits and the whole text for new drafts. Judge rhetorical function in context instead of banning punctuation or sentence patterns

The opinion-writing reference draws on a user-supplied Chinese essay, *Culture, Civilization, and History*, credited to 愚人. Its transferable methods include a conversational voice, explanations of mechanisms, everyday analogies, varied sentence lengths, and attention to people's circumstances. The author's biography, historical claims, and unverified figures are not supplied facts for future writing.

## What's inside

- [SKILL.md](SKILL.md): the core. What makes writing human, routes for editing and opinion writing, factual boundaries, and completion criteria
- [references/essay-style.md](references/essay-style.md): voice, causal reasoning, analogies, rhythm, and endings, with short examples and limits
- [references/case-study.md](references/case-study.md): the full autopsy of that failure. Original, botched version, accepted version, side by side, every wrong cut explained
- [references/post-edit-checklist.md](references/post-edit-checklist.md): a review of rhetorical purpose and factual support, informed by Wikipedia's [Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) and [blader/humanizer](https://github.com/blader/humanizer) (MIT), adapted to Chinese context and the reference essay

The principles govern before the edit; the checklist governs after. Decide whether to touch a sentence first, then inspect what you touched. Reverse the order and you'll end up scanning the author's original with a checklist, treating handwriting as flaws to fix.

## License

See [LICENSE.md](LICENSE.md): free for open-source & personal use; commercial license required for closed-source commercial use.

---

by 橘子 (Orange) & Cola
