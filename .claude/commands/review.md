# Review

Review and improve an existing document or piece of work in this workspace.

## Skills

Before proceeding, read and apply the following skills from `.claude/skills/`:

**Always apply:**
1. **vietnam-insurance-regulatory** — Regulatory context for life insurance in Vietnam
2. **vietnam-banking-regulatory** — Banking regulatory context (SBV, AML/KYC, payments)
3. **insurance-domain-model** — Core business concepts, processes, terminology
4. **compliance-check** — Data residency, PII handling, regulatory reporting
5. **creative-challenge** — After structured review, challenge assumptions and surface what's missing

**Apply based on content type:**
- **security-review** — For architecture docs, infrastructure configs, code
- **operational-readiness** — For architecture docs, deployment configs, runbooks
- **cost-analysis** — For architecture docs, infrastructure proposals
- **risk-assessment** — For solution designs, proposals, architecture docs
- **aws-cloud-patterns** — For AWS architecture documents
- **devsecops-practices** — For CI/CD configs, Dockerfiles, IaC code
- **research-methodology** — For research documents (verify sources, check confidence tags)

## Instructions

1. Read the target file(s) thoroughly.
2. Identify which review skills apply based on content type — read those skill files.
3. Apply each applicable skill as a review lens. For each lens, assess:
   - What's done well (acknowledge strengths)
   - What's missing or incomplete
   - What's incorrect or risky
4. Categorize every finding by severity:
   - **Critical**: Must fix — security risk, regulatory issue, factual error, data exposure
   - **Important**: Should fix — significant gap, misleading content, missing consideration
   - **Suggestion**: Nice to have — clarity improvement, structural polish, additional perspective
5. Apply `creative-challenge` last:
   - What assumptions does this document make that might be wrong?
   - What question should the author have asked but didn't?
   - Is there a simpler approach to the same goal?
6. Present findings as a structured review:
   - Summary (overall assessment in 2-3 sentences)
   - Findings by severity (Critical → Important → Suggestion)
   - Specific recommendations with rationale
7. Apply improvements directly to the file (with user agreement on Critical/Important changes).
8. Commit the result when done.

## Target

$ARGUMENTS
