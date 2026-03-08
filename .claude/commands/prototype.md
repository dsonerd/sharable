# Prototype

Build a quick prototype or spike solution for the given idea.

## Domain Context

**Technical domain** — IT Operations, DevOps, DevSecOps, AWS cloud:
- Infrastructure-as-Code: Terraform modules, CDK constructs, CloudFormation templates
- CI/CD: GitHub Actions workflows, pipeline configurations
- Automation scripts: Python, Bash, PowerShell for operational tasks
- Container configs: Dockerfiles, docker-compose, ECS task definitions, K8s manifests
- Security tools: scanning configs, policy-as-code (OPA, Sentinel), WAF rules
- Monitoring: CloudWatch dashboards, alerting configs, custom metrics

**Business domain** — Life insurance & banking in Vietnam:
- Calculation engines: premium calculation, reserve computation, benefit projection
- Data processing: regulatory report generators, data transformation pipelines
- Integration PoCs: API mockups, message queue patterns, file exchange formats
- Workflow prototypes: approval flows, underwriting rules, claims triage logic

## Instructions

1. Clarify the goal and success criteria before coding.
2. Keep it minimal — focus on proving the concept, not production quality.
3. Even in prototypes, follow these guardrails:
   - **No hardcoded secrets** — use environment variables or `.local/` files
   - **No real PII or customer data** — use synthetic/mock data
   - **Note security shortcuts** — comment what would need hardening for production
4. Include a `README.md` in the prototype folder covering:
   - What this prototype proves or demonstrates
   - How to run it (prerequisites, commands)
   - What would need to change for production use
   - Known limitations
5. Preferred tech stack (unless the topic requires otherwise):
   - **IaC**: Terraform or AWS CDK (TypeScript)
   - **Scripts**: Python 3.x or Bash
   - **Containers**: Docker with multi-stage builds
   - **APIs**: Python (FastAPI) or Node.js (Express)
6. Save the result to `prototypes/<topic-in-kebab-case>/` as a self-contained folder.
7. If a prototype on the same topic already exists, update it rather than creating a new one.
8. Commit the result when done.

## Topic

$ARGUMENTS
