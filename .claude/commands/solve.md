# Solve

Create a solution design or technical proposal for the given problem.

## Skills

Before proceeding, read and apply the following skills from `.claude/skills/`:

**Always apply:**
1. **vietnam-insurance-regulatory** — Regulatory context for life insurance in Vietnam
2. **vietnam-banking-regulatory** — Banking regulatory context (SBV, AML/KYC, payments)
3. **insurance-domain-model** — Core business concepts, processes, terminology
4. **compliance-check** — Data residency, PII handling, regulatory reporting
5. **structured-decomposition** — Decompose the problem before proposing solutions
6. **risk-assessment** — Identify risks, failure modes, rollback scenarios
7. **trade-off-analysis** — Compare alternatives explicitly
8. **creative-challenge** — Challenge your own solution, find simpler paths, surface unasked questions

**Apply when relevant:**
- **aws-cloud-patterns** — If solution involves AWS infrastructure
- **devsecops-practices** — If solution involves CI/CD, automation, or security tooling
- **security-review** — If solution affects security posture
- **operational-readiness** — If solution changes how systems are operated
- **cost-analysis** — If solution has significant cost implications
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
   - **Security & compliance impact**: (`security-review`, `compliance-check`)
   - **Risks and mitigations**: (`risk-assessment`)
   - **Rollback plan**: How to revert
   - **Success criteria**: How to know the problem is solved
   - **Creative challenges**: (`creative-challenge`) — assumptions questioned, simpler alternatives, unasked questions
6. Save to `solutions/<topic-in-kebab-case>/` (subfolder with index for multi-part).
7. If a solution on the same topic already exists, update it.
8. Commit the result when done.

## Topic

$ARGUMENTS
