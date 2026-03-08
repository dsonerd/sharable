# Review

Review and improve an existing document or piece of work in this workspace.

## Domain Context

Apply review lenses appropriate to the content:

**Technical lens** — IT Operations, DevOps, DevSecOps, AWS:
- Security: OWASP Top 10, CIS benchmarks, AWS security best practices, least privilege
- Operational readiness: monitoring, alerting, runbooks, DR/BCP, scaling
- Cost: right-sizing, reserved vs on-demand, data transfer costs, storage tiers
- Reliability: single points of failure, blast radius, failure modes, graceful degradation
- IaC quality: modularity, state management, drift detection, idempotency

**Business lens** — Life insurance & banking in Vietnam:
- Regulatory compliance: Does this align with current Vietnamese regulations?
- PII handling: Is customer data classified and protected appropriately?
- Audit trail: Are decisions and changes traceable?
- Business accuracy: Are domain terms, calculations, and processes correct?
- Completeness: Are edge cases in insurance/banking workflows covered?

## Instructions

1. Read the target file(s) thoroughly.
2. Identify which review lenses apply based on the content type.
3. Provide structured feedback across applicable dimensions:
   - **Clarity & structure**: Is it well-organized and easy to follow?
   - **Completeness**: Are there gaps, missing considerations, or unstated assumptions?
   - **Accuracy**: Are there factual errors, outdated information, or questionable assumptions?
   - **Security & compliance**: Are there security risks or compliance gaps? (for technical/regulated content)
   - **Actionability**: Can someone act on this? Are next steps clear?
   - **Consistency**: Does it align with other documents in this workspace?
4. For each finding, categorize severity:
   - **Critical**: Must fix — security risk, regulatory issue, factual error
   - **Important**: Should fix — significant gap or improvement
   - **Suggestion**: Nice to have — polish, clarity, minor improvement
5. Apply improvements directly to the file (with user agreement on critical/important changes).
6. Summarize changes made and remaining recommendations.
7. Commit the result when done.

## Target

$ARGUMENTS
