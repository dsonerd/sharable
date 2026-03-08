# Skill: Trade-off Analysis

Compare options rigorously. Make the reasoning behind choices explicit and defensible.

## MUST — Guardrails

- **Always present at least 2 alternatives.** A recommendation without alternatives is an assumption, not a decision. Include "do nothing" as an option when relevant.
- **Make criteria explicit.** State what you're optimizing for before evaluating options. No hidden weighting.
- **Acknowledge what you're giving up.** Every choice sacrifices something. Name it. "We chose X, which means we accept Y limitation."
- **Separate facts from judgment.** Clearly distinguish objective data ("Lambda cold start is ~200ms") from subjective assessment ("this is acceptable for our use case").

## SHOULD — Frameworks

- **Decision matrix** — List options as rows, criteria as columns, score each cell. Weight criteria if some matter more. Works well for: technology selection, vendor comparison, architectural choices.
- **Pros/Cons with severity** — Simpler than a matrix. List pros and cons for each option, tag each as Critical/Important/Minor. Good for: quick decisions, stakeholder communication.
- **Reversibility test** — Classify each option: easily reversible (two-way door) vs hard to reverse (one-way door). One-way doors deserve more analysis. Two-way doors deserve faster decisions.
- **Time-horizon analysis** — How does each option look at 1 month, 6 months, 2 years? Some options are cheap now but expensive later (tech debt). Some are expensive now but pay off later (infrastructure investment).

## COULD — Open Space

- **Challenge the criteria.** Are you optimizing for the right things? Sometimes the user's implicit criteria (e.g., "minimize cost") conflict with unstated needs (e.g., "move fast"). Surface this.
- **Find the option nobody proposed.** After analyzing presented alternatives, ask: is there a third path that combines the strengths of multiple options?
- **Invert the analysis.** Instead of "which option is best?", ask "which option would be hardest to recover from if wrong?" Minimize regret, not just maximize benefit.
- **Question the decision's necessity.** Sometimes the best trade-off is realizing you don't need to choose yet. Is there a way to defer the decision and preserve optionality?
