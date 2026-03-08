# Skill: Operational Readiness

Ensure systems can be operated, monitored, and recovered in production.

## MUST — Guardrails

- **If you can't monitor it, don't ship it.** Every production system must have: health checks, key metrics, alerting on failure conditions, and log aggregation. No exceptions.
- **Runbooks must exist for critical systems.** Documented procedures for: common failures, escalation paths, rollback steps, and emergency contacts. A system without runbooks is a system that fails at 3 AM with no recovery path.
- **DR/BCP must be defined.** State explicitly: RPO (how much data can you lose?), RTO (how long can you be down?), and the recovery strategy that achieves them. For financial services, these are regulatory requirements, not nice-to-haves.
- **Deployment must be automated and reversible.** Manual deployment to production is a risk. Every deployment must have a documented rollback procedure that's been tested.

## SHOULD — Frameworks

### Operational Readiness Checklist

Before going to production, verify:

**Monitoring & Observability:**
- [ ] Health check endpoints defined and monitored
- [ ] Key business metrics instrumented (transactions/sec, error rate, latency)
- [ ] Infrastructure metrics monitored (CPU, memory, disk, network)
- [ ] Logs structured (JSON), centralized, and searchable
- [ ] Distributed tracing enabled for multi-service architectures
- [ ] Dashboards created for operational and business visibility

**Alerting:**
- [ ] Alerts defined for critical failure conditions
- [ ] Alert thresholds tuned (no alert fatigue, no silent failures)
- [ ] Escalation paths defined (L1 → L2 → L3, with timeouts)
- [ ] On-call rotation established and documented

**Resilience:**
- [ ] Single points of failure identified and mitigated (or accepted)
- [ ] Auto-scaling configured with appropriate min/max
- [ ] Circuit breakers / retry logic for external dependencies
- [ ] Graceful degradation path defined (what works when dependency X is down?)

**Deployment:**
- [ ] Deployment automated (CI/CD pipeline)
- [ ] Rollback tested and documented
- [ ] Blue/green or canary deployment for high-risk changes
- [ ] Database migration strategy (backward compatible, rollback-safe)

**Disaster Recovery:**
- [ ] RPO and RTO defined and agreed with business
- [ ] Backup strategy implemented and tested
- [ ] DR environment provisioned (pilot light / warm standby / multi-region)
- [ ] DR drill scheduled and results documented

### SLO/SLI/SLA Framework

- **SLI (Service Level Indicator)** — The metric you measure (e.g., request latency p99)
- **SLO (Service Level Objective)** — The target (e.g., p99 latency < 500ms, 99.9% availability)
- **SLA (Service Level Agreement)** — The contract with consequences (e.g., SLA breach → credits/penalties)
- **Error budget** — The acceptable amount of unreliability. When budget is exhausted, freeze features and fix reliability.

## COULD — Open Space

- **Challenge the RTO/RPO.** Are the stated recovery targets actually tested? An untested DR plan is a wish, not a plan. When was the last DR drill?
- **Toil analysis.** What operational work is repetitive and automatable? Every hour spent on toil is an hour not spent on improvement. Track and reduce it.
- **Game day / chaos engineering.** Once operationally mature: intentionally inject failures. Kill an instance, block a dependency, saturate a queue. Does the system recover as designed?
- **Operational cost of complexity.** Every new component adds operational overhead: another thing to monitor, patch, scale, debug. Is the architectural complexity justified by the operational burden it creates?
