# Architect

Design system architecture for the given topic or component.

## Skills

Before proceeding, read and apply the following skills from `.claude/skills/`:

**Always apply:**
1. **vietnam-insurance-regulatory** — Regulatory context for life insurance in Vietnam
2. **vietnam-banking-regulatory** — Banking regulatory context (SBV, AML/KYC, payments)
3. **insurance-domain-model** — Core business concepts, processes, terminology
4. **compliance-check** — Data residency, PII handling, regulatory reporting
5. **aws-cloud-patterns** — Service selection, Well-Architected pillars, architecture patterns
6. **security-review** — Threat model, encryption, access control, audit logging
7. **operational-readiness** — Monitoring, alerting, DR/BCP, deployment strategy
8. **cost-analysis** — TCO, pricing models, cost optimization levers
9. **risk-assessment** — Architectural risks, failure modes, mitigations
10. **trade-off-analysis** — Explicit trade-offs for every key decision
11. **creative-challenge** — Challenge the design, find simpler alternatives, surface assumptions

**Apply when relevant:**
- **devsecops-practices** — If architecture includes CI/CD, IaC, or deployment automation

## Instructions

1. Read all applicable skill files listed above.
2. Clarify scope, constraints, and non-functional requirements before designing.
3. Produce a structured architecture document:
   - **Context**: Problem statement, stakeholders, business drivers
   - **Requirements**: Functional, non-functional, constraints (apply domain skills for completeness)
   - **Architecture**: Components, interactions, data flow — use Mermaid diagrams (C4, sequence, deployment)
   - **Key decisions**: ADR format per decision — context, options considered (`trade-off-analysis`), decision, consequences
   - **Security**: Threat model, controls, encryption, access (`security-review`)
   - **Operations**: Monitoring, alerting, DR/BCP, deployment (`operational-readiness`)
   - **Cost**: Estimated cost profile, optimization opportunities (`cost-analysis`)
   - **Risks**: Architectural risks and mitigations (`risk-assessment`)
   - **Compliance**: Regulatory alignment (`compliance-check`)
   - **Creative challenges**: Assumptions challenged, simpler alternatives considered (`creative-challenge`)
4. Save to `architecture/<topic-in-kebab-case>.md` (subfolder if multi-document).
5. If an architecture document on the same topic already exists, update it.
6. Commit the result when done.

## Topic

$ARGUMENTS
