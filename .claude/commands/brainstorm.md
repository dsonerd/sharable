# Brainstorm

Start a structured brainstorming session on the given topic.

## Skills

Before proceeding, read and apply the following skills from `.claude/skills/`:

1. **vietnam-insurance-regulatory** — Regulatory context for life insurance in Vietnam
2. **vietnam-banking-regulatory** — Banking regulatory context (SBV, AML/KYC, payments)
3. **insurance-domain-model** — Core business concepts, processes, terminology
4. **structured-decomposition** — Decompose the topic before ideating. Don't anchor on the first idea.
5. **trade-off-analysis** — For each promising idea, surface trade-offs explicitly.
6. **risk-assessment** — Flag risks for top candidates (don't kill ideas, but be honest).
7. **creative-challenge** — After structured brainstorming, challenge your own output and look for non-obvious angles.

**Apply when topic involves infrastructure or technical operations:**
- **aws-cloud-patterns** / **devsecops-practices**

## Instructions

1. Read all applicable skill files listed above.
2. Identify which domain(s) the topic touches. If ambiguous, ask.
3. **Decompose** the topic into sub-areas using `structured-decomposition`.
4. For each sub-area, generate multiple ideas — aim for breadth before depth.
5. Evaluate top candidates with `trade-off-analysis` and `risk-assessment`.
6. Apply `creative-challenge` — challenge assumptions, find cross-domain connections, surface unasked questions.
7. Structure output:
   - Topic decomposition
   - Ideas per sub-area (with brief feasibility notes)
   - Top 3-5 candidates with trade-off summary
   - Creative challenges and non-obvious angles
8. Save to `brainstorming/<topic-in-kebab-case>.md`.
9. If a file on the same topic already exists, update it rather than creating a new one.
10. Commit the result when done.

## Topic

$ARGUMENTS
