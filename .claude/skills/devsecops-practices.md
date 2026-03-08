# Skill: DevSecOps Practices

CI/CD pipeline patterns, security-as-code, infrastructure automation, and operational tooling.

## MUST — Guardrails

- **Secrets never in code.** No hardcoded credentials, API keys, tokens, or passwords — not in source, not in Dockerfiles, not in CI configs. Use secrets managers (AWS Secrets Manager, Parameter Store) or environment injection.
- **IaC is the default.** Infrastructure should be defined in code, version-controlled, and reproducible. Manual console changes are acceptable only for emergencies, then must be codified.
- **Security shifts left.** Security scanning happens in the pipeline, not after deployment. SAST, SCA, and container scanning are pipeline stages, not afterthoughts.
- **Immutable artifacts.** Build once, deploy many. The artifact deployed to production must be the same one tested in staging. No "rebuild for prod."

## SHOULD — Frameworks

### CI/CD Pipeline Pattern

Standard pipeline stages (adapt, don't blindly follow):

```
Source → Build → Unit Test → SAST/SCA → Container Build →
Container Scan → Integration Test → Deploy Staging →
Smoke Test → Deploy Production → Post-deploy Verification
```

Key practices:
- **Trunk-based development** or short-lived feature branches (< 2 days)
- **Automated testing** at every stage — fail fast, fail loud
- **Deployment strategies**: Blue/green, canary, rolling — choose based on risk tolerance and rollback speed
- **Pipeline as code** — Jenkinsfile, GitHub Actions workflow, GitLab CI — versioned alongside application code

### Infrastructure as Code

- **Terraform**: Multi-cloud, state management, module ecosystem. Good for: infrastructure provisioning, multi-account setups.
- **AWS CDK**: AWS-native, imperative (TypeScript/Python), synthesizes to CloudFormation. Good for: teams that prefer programming over config.
- **CloudFormation**: AWS-native, declarative. Good for: simple stacks, AWS-managed integrations.
- **State management**: Remote state (S3 + DynamoDB lock for Terraform), never local state in shared environments.
- **Module design**: Small, composable, single-responsibility. Pin versions. Test modules independently.

### Security Tooling in Pipeline

- **SAST** (Static Analysis): SonarQube, Semgrep, Checkmarx — find code vulnerabilities
- **SCA** (Software Composition Analysis): Snyk, Dependabot, Trivy — find dependency vulnerabilities
- **Container scanning**: Trivy, Grype, ECR native scanning — find image vulnerabilities
- **IaC scanning**: tfsec, Checkov, cfn-lint — find infrastructure misconfigurations
- **Secrets detection**: GitLeaks, TruffleHog — prevent secret commits

### Observability Stack

- **Metrics**: CloudWatch Metrics, Prometheus + Grafana
- **Logs**: CloudWatch Logs, ELK/OpenSearch, Loki
- **Traces**: X-Ray, Jaeger, OpenTelemetry
- **Alerting**: CloudWatch Alarms, PagerDuty, OpsGenie
- **Dashboards**: CloudWatch Dashboards, Grafana — operational visibility for on-call

## COULD — Open Space

- **Challenge the tool choice.** The "industry standard" tool isn't always the right one. A simpler tool that the team actually uses beats a powerful tool that's shelfware.
- **GitOps and progressive delivery.** ArgoCD, Flux, Flagger — pull-based deployment models and canary analysis. Worth considering for Kubernetes workloads.
- **Platform engineering.** Instead of every team building pipelines from scratch, should there be an internal developer platform (IDP)? Golden paths, self-service templates, paved roads.
- **Policy as code.** OPA/Rego, AWS SCPs, Sentinel — encode governance rules so they're automatically enforced, not manually checked.
- **Chaos engineering.** AWS Fault Injection Simulator, Litmus — intentionally break things to find weaknesses. Only for mature operations, but powerful when ready.
