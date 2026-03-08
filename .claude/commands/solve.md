# Solve

Create a solution design or technical proposal for the given problem.

## Skills

Before proceeding, read and apply the following skills from `.claude/skills/`:

**Always apply:**
1. **structured-decomposition** — Decompose the problem before proposing solutions
2. **risk-assessment** — Identify risks, failure modes, rollback scenarios
3. **trade-off-analysis** — Compare alternatives explicitly
4. **creative-challenge** — Challenge your own solution, find simpler paths, surface unasked questions

**Apply when relevant:**
- **aws-cloud-patterns** — If solution involves AWS infrastructure
- **devsecops-practices** — If solution involves CI/CD, automation, or security tooling
- **security-review** — If solution affects security posture
- **compliance-check** — If solution affects regulated processes or data
- **operational-readiness** — If solution changes how systems are operated
- **cost-analysis** — If solution has significant cost implications
- **vietnam-insurance-regulatory** / **vietnam-banking-regulatory** — If problem exists in regulated space
- **insurance-domain-model** — If problem involves insurance business processes
- **research-methodology** — If the problem requires investigation of external information

## Instructions

1. Read all applicable skill files listed above.
2. Understand the problem — ask clarifying questions if needed.
3. **Decompose** the problem (`structured-decomposition`) — don't jump to solutions.
4. Assess impact and urgency:
   - Who is affected? What's the blast radius if unsolved?
   - Are there regulatory deadlines or compliance implications?
5. Produce a solution document:
   - **Problem statement**: Clear description with evidence/symptoms, root cause analysis
   - **Proposed solution**: Detailed approach with rationale
   - **Alternatives considered**: At least 2 alternatives (`trade-off-analysis`)
   - **Implementation plan**: Phases, milestones, dependencies
   - **Security & compliance impact**: If applicable (`security-review`, `compliance-check`)
   - **Risks and mitigations**: (`risk-assessment`)
   - **Rollback plan**: How to revert
   - **Success criteria**: How to know the problem is solved
   - **Creative challenges**: (`creative-challenge`) — assumptions questioned, simpler alternatives, unasked questions
6. Save to `solutions/<topic-in-kebab-case>/` (subfolder with index for multi-part).
7. If a solution on the same topic already exists, update it.
8. Commit the result when done.

## Topic

$ARGUMENTS
