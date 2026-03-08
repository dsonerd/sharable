# Solve

Create a solution design or technical proposal for the given problem.

## Domain Context

**Technical domain** — IT Operations, DevOps, DevSecOps, AWS cloud:
- Incident resolution, root cause analysis, post-mortems
- Security vulnerability remediation, compliance gap closure
- Infrastructure migration, modernization, optimization
- CI/CD pipeline design, automation, toolchain selection
- Cost reduction, performance tuning, reliability improvement

**Business domain** — Life insurance & banking in Vietnam:
- Regulatory compliance solutions (Ministry of Finance circulars, SBV directives, Insurance Business Law)
- System integration: core insurance ↔ banking ↔ payment ↔ regulatory reporting
- Business process optimization: underwriting, claims, policy servicing
- Digital channel enablement, customer onboarding, e-KYC

## Instructions

1. Understand the problem — ask clarifying questions if needed.
2. Assess impact and urgency:
   - Who is affected? (customers, operations, regulators, security posture)
   - What is the blast radius if unsolved?
   - Are there regulatory deadlines or compliance implications?
3. Produce a solution document covering:
   - **Problem statement**: Clear description with evidence/symptoms
   - **Root cause analysis**: Why does this problem exist? (use 5 Whys or Fishbone if appropriate)
   - **Proposed solution**: Detailed approach with rationale
   - **Alternatives considered**: At least 2 alternatives with pros/cons comparison
   - **Implementation plan**: Phases, milestones, dependencies, ownership
   - **Security & compliance impact**: How does this solution affect security posture and regulatory compliance?
   - **Risks and mitigations**: What could go wrong and how to handle it
   - **Rollback plan**: How to revert if the solution causes issues
   - **Success criteria**: How do we know the problem is solved?
4. For solutions in regulated environments, include:
   - Regulatory references (specific circular/decree numbers where applicable)
   - Approval requirements (who needs to sign off)
   - Audit trail considerations
5. Save the result to `solutions/<topic-in-kebab-case>/` — use a subfolder with an index file for multi-part solutions.
6. If a solution on the same topic already exists, update it rather than creating a new one.
7. Commit the result when done.

## Topic

$ARGUMENTS
