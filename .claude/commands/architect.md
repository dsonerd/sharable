# Architect

Design system architecture for the given topic or component.

## Domain Context

**Technical domain** — IT Operations, DevOps, DevSecOps, AWS cloud:
- Apply AWS Well-Architected Framework pillars: Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability
- Consider: zero trust, defense in depth, encryption (at rest and in transit), least privilege
- Infrastructure patterns: microservices, event-driven, serverless, container orchestration (ECS/EKS)
- Operational readiness: monitoring, alerting, logging, tracing, runbooks, DR/BCP

**Business domain** — Life insurance & banking in Vietnam:
- Core system integration: policy admin, claims, underwriting, billing, reinsurance
- Data architecture: PII classification, data residency in Vietnam, audit trails, retention policies
- Regulatory compliance: reporting pipelines, data lineage, access control per Vietnamese regulations
- High availability requirements for financial services (RPO/RTO)

## Instructions

1. Clarify scope, constraints, and non-functional requirements before designing.
2. Produce a structured architecture document covering:
   - **Context**: Problem statement, stakeholders, business drivers
   - **Design goals**: Functional and non-functional requirements, quality attributes
   - **Constraints**: Regulatory, security, budget, timeline, existing systems
   - **Architecture overview**: Components, interactions, data flow
   - **Infrastructure**: AWS services, networking, compute, storage, security controls
   - **Key decisions**: ADR (Architecture Decision Record) format — context, decision, consequences
   - **Trade-offs**: What was sacrificed and why (e.g., cost vs resilience, simplicity vs flexibility)
   - **Diagrams**: Use Mermaid syntax — C4 model (context, container, component), sequence diagrams, deployment diagrams
   - **Security posture**: Threat model considerations, encryption, access control, audit logging
   - **Operational model**: Deployment strategy, monitoring, incident response, scaling
3. For regulated workloads, include a compliance section noting which regulations apply and how the design addresses them.
4. Save the result to `architecture/<topic-in-kebab-case>.md` (use a subfolder if the design has multiple documents).
5. If an architecture document on the same topic already exists, update it rather than creating a new one.
6. Commit the result when done.

## Topic

$ARGUMENTS
