# Skill: AWS Cloud Patterns

Architecture patterns, service selection, and operational practices for AWS.

## MUST — Guardrails

- **Don't recommend services you can't justify.** If suggesting an AWS service, state why it fits better than alternatives. No cargo-cult architecture.
- **Region matters.** For Vietnam-based workloads, consider: ap-southeast-1 (Singapore) is the nearest region. Data residency requirements may mandate specific architectural choices.
- **Cost is a first-class concern.** Every architectural recommendation must consider cost implications. "Serverless" isn't free. "Managed service" has a premium. State the trade-off.
- **Security is not optional.** Every architecture must address: encryption (at rest + in transit), IAM (least privilege), network isolation (VPC, security groups, NACLs), logging (CloudTrail, VPC Flow Logs).

## SHOULD — Frameworks

### AWS Well-Architected Framework (6 Pillars)

Apply as a checklist lens, not a rigid template:

1. **Operational Excellence** — Automation, IaC, observability, incident response, continuous improvement
2. **Security** — IAM, detective controls, infrastructure protection, data protection, incident response
3. **Reliability** — Fault isolation, auto-scaling, backup/restore, DR strategy (pilot light, warm standby, multi-region active)
4. **Performance Efficiency** — Right compute type, caching strategy, database selection, CDN usage
5. **Cost Optimization** — Right-sizing, savings plans/reserved instances, spot for fault-tolerant workloads, storage tiering
6. **Sustainability** — Resource efficiency, managed services over self-managed, right-size to reduce waste

### Common Architecture Patterns

- **Three-tier web**: ALB → ECS/EKS/EC2 → RDS/Aurora. Bread and butter for most applications.
- **Serverless**: API Gateway → Lambda → DynamoDB/Aurora Serverless. Good for: event-driven, spiky traffic, low-maintenance.
- **Event-driven**: SQS/SNS/EventBridge → Lambda/ECS. Good for: decoupling, async processing, integration.
- **Data pipeline**: S3 → Glue/EMR → Redshift/Athena → QuickSight. Good for: analytics, reporting, data lake.
- **Hybrid/migration**: Direct Connect + VPN, AWS Migration Hub, DMS for database migration.

### Service Selection Heuristics

- **Compute**: Fargate (default for containers) → ECS/EC2 (need control) → Lambda (event-driven, short-lived) → EKS (need K8s ecosystem)
- **Database**: Aurora (relational default) → DynamoDB (key-value/document, massive scale) → ElastiCache (caching) → RDS (specific engine need)
- **Storage**: S3 (object, default) → EBS (block, EC2-attached) → EFS (shared file) → FSx (specialized)
- **Messaging**: SQS (queue default) → SNS (pub/sub fan-out) → EventBridge (event routing) → Kinesis (streaming, high-volume)

## COULD — Open Space

- **Challenge the AWS-only assumption.** Is there a simpler solution using a SaaS product? Not everything needs to be built on primitives.
- **Emerging services.** AWS releases new services constantly. Is there a newer service that simplifies this architecture? (But also: is it mature enough for production?)
- **Multi-account strategy.** For regulated workloads, consider: separate accounts for prod/non-prod, security tooling, logging. AWS Organizations + SCPs for governance.
- **Unconventional combinations.** Step Functions for orchestration, AppSync for real-time GraphQL, IoT Core for device telemetry — services designed for one use case often solve unexpected problems elegantly.
- **Exit strategy.** What's the lock-in level? If using DynamoDB, you're locked in. If using RDS PostgreSQL, you're portable. Make lock-in a conscious choice, not an accident.
