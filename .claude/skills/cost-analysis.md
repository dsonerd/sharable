# Skill: Cost Analysis

Evaluate and optimize cost implications of technical and business decisions.

## MUST — Guardrails

- **Never ignore cost.** Every architecture, tool selection, or infrastructure decision has cost implications. State them, even if approximate.
- **Compare total cost of ownership (TCO), not just unit price.** Include: compute, storage, data transfer, licensing, operational overhead (people), migration cost, and opportunity cost.
- **Distinguish one-time vs recurring costs.** Migration has a one-time cost. Infrastructure has a recurring cost. Don't compare them directly without time-horizon context.
- **Account for data transfer costs.** AWS data transfer is the hidden cost that surprises everyone. Cross-AZ, cross-region, internet egress — model them explicitly.

## SHOULD — Frameworks

### AWS Cost Optimization Levers

In order of impact:

1. **Right architecture** — Serverless vs containers vs EC2. The biggest cost lever is the architecture pattern itself.
2. **Right-sizing** — Match instance types to actual workload. Use AWS Compute Optimizer, CloudWatch metrics for CPU/memory utilization.
3. **Pricing models** — On-demand (flexibility) → Savings Plans (1-3yr commitment, ~30-70% savings) → Spot (fault-tolerant, ~60-90% savings). Reserved Instances for RDS/ElastiCache.
4. **Storage tiering** — S3 Intelligent-Tiering, lifecycle policies (Standard → IA → Glacier). EBS volume type optimization (gp3 vs gp2).
5. **Waste elimination** — Unused resources (idle EC2, unattached EBS, old snapshots, unused Elastic IPs). Tag everything, audit monthly.
6. **Data transfer optimization** — VPC endpoints (avoid NAT Gateway costs), CloudFront for egress, same-AZ placement where possible.

### Build vs Buy vs SaaS Analysis

| Factor | Build | Buy (License) | SaaS |
|---|---|---|---|
| Upfront cost | High (dev time) | Medium (license) | Low (subscription) |
| Ongoing cost | Maintenance burden | License renewal + ops | Subscription (scales with usage) |
| Customization | Full control | Configurable | Limited |
| Time to value | Slow | Medium | Fast |
| Operational burden | You own everything | You operate, vendor patches | Vendor operates |
| Lock-in risk | Low (you own code) | Medium (vendor dependency) | High (data + integration) |
| Exit cost | Low | Medium | High (migration) |

### Cost Estimation Approach

1. **Identify cost components** — Compute, storage, network, licensing, people
2. **Estimate usage patterns** — Steady-state, peak, growth trajectory
3. **Model 3 scenarios** — Conservative, expected, optimistic
4. **Use AWS Pricing Calculator** for infrastructure estimates
5. **Add operational overhead** — People cost to build, operate, and maintain
6. **Calculate payback period** — When does the investment break even?

## COULD — Open Space

- **FinOps culture.** Cost optimization isn't a one-time exercise — it's a discipline. Should there be cost visibility dashboards, budget alerts, team-level accountability?
- **Cost of delay.** Sometimes the cheapest option is the slowest. What's the business cost of delayed delivery? A faster, more expensive approach may have higher ROI.
- **Hidden costs of "free."** Open-source is free to license but not free to operate. "Serverless" eliminates server cost but may increase debugging and observability cost. Name the hidden costs.
- **Revenue perspective.** Cost optimization is defense. Revenue enablement is offense. Sometimes spending more on infrastructure to launch a product faster generates more value than the savings from optimization.
