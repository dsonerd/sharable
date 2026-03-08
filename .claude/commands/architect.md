# Architect

Design system architecture for the given topic or component.

## Skills

Before proceeding, read and apply the following skills from `.claude/skills/`:

**Always apply:**
1. **aws-cloud-patterns** — Service selection, Well-Architected pillars, architecture patterns
2. **security-review** — Threat model, encryption, access control, audit logging
3. **operational-readiness** — Monitoring, alerting, DR/BCP, deployment strategy
4. **cost-analysis** — TCO, pricing models, cost optimization levers
5. **risk-assessment** — Architectural risks, failure modes, mitigations
6. **trade-off-analysis** — Explicit trade-offs for every key decision
7. **creative-challenge** — Challenge the design, find simpler alternatives, surface assumptions

**Apply when relevant:**
- **compliance-check** — If handling PII, financial data, or regulatory reporting
- **devsecops-practices** — If architecture includes CI/CD, IaC, or deployment automation
- **vietnam-insurance-regulatory** / **vietnam-banking-regulatory** — If the system operates in regulated space
- **insurance-domain-model** — If the system handles insurance business processes

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
   - **Compliance**: Regulatory alignment if applicable (`compliance-check`)
   - **Creative challenges**: Assumptions challenged, simpler alternatives considered (`creative-challenge`)
4. Save to `architecture/<topic-in-kebab-case>.md` (subfolder if multi-document).
5. If an architecture document on the same topic already exists, update it.
6. Commit the result when done.

## Topic

$ARGUMENTS
