# Prototype

Build a quick prototype or spike solution for the given idea.

## Skills

Before proceeding, read and apply the following skills from `.claude/skills/`:

**Always apply:**
1. **devsecops-practices** — Pipeline patterns, IaC conventions, security-in-code basics
2. **security-review** — Even in prototypes: no hardcoded secrets, no real PII, flag what needs hardening

**Apply when relevant:**
- **aws-cloud-patterns** — If prototype involves AWS services
- **insurance-domain-model** — If prototype involves insurance business logic
- **cost-analysis** — If prototype tests something with cost implications (estimate expected cost)
- **creative-challenge** — If the prototype goal is ambiguous, challenge scope before building

## Instructions

1. Read all applicable skill files listed above.
2. Clarify the goal and success criteria before coding.
3. Keep it minimal — prove the concept, not production quality.
4. Apply security guardrails from `security-review` (MUST tier only):
   - No hardcoded secrets — use env vars or `.local/` files
   - No real PII or customer data — use synthetic/mock data
   - Comment what would need hardening for production
5. Follow `devsecops-practices` conventions:
   - IaC: Terraform or AWS CDK (TypeScript) preferred
   - Scripts: Python 3.x or Bash preferred
   - Containers: Docker with multi-stage builds
   - APIs: Python (FastAPI) or Node.js preferred
6. Include a `README.md` in the prototype folder:
   - What this prototype proves or demonstrates
   - How to run it (prerequisites, commands)
   - What would need to change for production
   - Known limitations and shortcuts taken
7. Save to `prototypes/<topic-in-kebab-case>/` as a self-contained folder.
8. If a prototype on the same topic already exists, update it.
9. Commit the result when done.

## Topic

$ARGUMENTS
