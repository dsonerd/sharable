# Research

Research a topic and compile findings into a knowledge document.

## Skills

Before proceeding, read and apply the following skills from `.claude/skills/`:

**Always apply:**
1. **research-methodology** — Search strategy, source evaluation, confidence tagging, citation standards
2. **creative-challenge** — After gathering findings, synthesize across domains, spot what's missing, challenge narratives

**Apply when relevant:**
- **vietnam-insurance-regulatory** / **vietnam-banking-regulatory** — If researching regulatory topics
- **insurance-domain-model** — If researching insurance business topics
- **aws-cloud-patterns** — If researching AWS services or cloud architecture
- **devsecops-practices** — If researching DevOps/security tooling
- **security-review** — If researching security topics
- **cost-analysis** — If research involves pricing, TCO, or financial comparison

## Instructions

1. Read all applicable skill files listed above.
2. **Plan the search** (`research-methodology`):
   - Formulate 3-5 search queries from different angles
   - Use bilingual search (EN/VI) for Vietnamese regulatory or market topics
   - Identify primary, secondary, and tertiary sources to target
3. **Execute web searches** — Use the WebSearch tool. Do not skip this step.
4. **Evaluate sources** — Apply CRAAP test from `research-methodology`. Discard unreliable sources.
5. **Synthesize findings** into a structured document:
   - **Executive summary**: 3-5 key takeaways
   - **Background / context**: Why this topic matters
   - **Key findings**: Organized by theme (not by source), with confidence tags
   - **Comparisons / evaluations**: Tables or matrices where applicable
   - **Vietnam-specific considerations**: When relevant
   - **Implications**: What does this mean for our work?
   - **Open questions**: What remains unclear or needs investigation?
   - **References**: Full source list with URLs and access dates
6. **Apply creative challenge** (`creative-challenge`):
   - What narrative are the sources collectively pushing? Is it accurate?
   - What's missing from the available information?
   - What cross-domain connections exist?
7. Save to `knowledge/<topic-in-kebab-case>.md` (subfolder for multi-part).
8. If a knowledge document on the same topic already exists, update it.
9. Commit the result when done.

## Topic

$ARGUMENTS
