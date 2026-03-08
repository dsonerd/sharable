# Skill: Structured Decomposition

Break complex problems into manageable parts before attempting solutions.

## MUST — Guardrails

- **Never jump to solutions.** Decompose first, solve second. If you catch yourself proposing a solution before understanding the problem structure, stop and decompose.
- **Name the parts.** Every decomposition must produce explicitly named sub-problems or components. No vague "there are several aspects to consider."
- **Verify completeness.** After decomposing, ask: "Is there a part I'm missing?" If the parts don't reassemble into the whole, the decomposition is wrong.

## SHOULD — Frameworks

Reach for the tool that fits. Don't force a framework where it doesn't belong.

- **5 Whys** — When the problem is a symptom and the root cause is hidden. Ask "why?" repeatedly until you reach something actionable. Watch for: stopping too early (surface cause) or too late (cosmic cause).
- **Fishbone / Ishikawa** — When the problem has multiple possible cause categories. Classic categories: People, Process, Technology, Environment, Policy, Measurement. Adapt categories to the domain.
- **Issue Trees / MECE** — When you need exhaustive, non-overlapping coverage. Mutually Exclusive, Collectively Exhaustive. Good for: scoping exercises, gap analysis, stakeholder mapping.
- **Functional decomposition** — When dealing with systems. Break by function, then by sub-function. Useful for architecture and process design.
- **Temporal decomposition** — When sequence matters. Break by phase: before, during, after. Or: initiation, execution, closure.

If none of these fit, **invent your own decomposition logic** and state it explicitly. The method matters less than the discipline of decomposing.

## COULD — Open Space

- **Reframe the problem.** Is the stated problem the real problem? Sometimes decomposition reveals the question itself is wrong. Say so.
- **Find the leverage point.** After decomposing, which sub-problem, if solved, would make the others easier or irrelevant? Focus there.
- **Cross-domain decomposition.** How would a different discipline break this problem? (A doctor diagnosing? An engineer debugging? An economist modeling?)
- **Challenge the boundaries.** The user's framing implicitly scopes the problem. What are they excluding that might matter?
