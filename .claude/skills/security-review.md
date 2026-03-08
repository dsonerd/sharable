# Skill: Security Review

Assess and strengthen security posture across applications, infrastructure, and processes.

## MUST — Guardrails

- **OWASP Top 10 is the minimum.** For any web application or API, check against current OWASP Top 10. This is the floor, not the ceiling.
  - Broken Access Control
  - Cryptographic Failures
  - Injection
  - Insecure Design
  - Security Misconfiguration
  - Vulnerable and Outdated Components
  - Identification and Authentication Failures
  - Software and Data Integrity Failures
  - Security Logging and Monitoring Failures
  - Server-Side Request Forgery (SSRF)
- **Encryption is non-negotiable.** Data at rest: AES-256 (S3 SSE, EBS encryption, RDS encryption). Data in transit: TLS 1.2+. No exceptions for "internal" traffic.
- **Least privilege.** Every IAM role, security group, and access policy should grant the minimum permissions required. No wildcard (`*`) actions in production IAM policies.
- **Audit logging must exist.** CloudTrail (API activity), VPC Flow Logs (network), application-level audit logs (who did what when). Logs must be tamper-resistant (separate account, S3 Object Lock).

## SHOULD — Frameworks

### Threat Modeling (STRIDE)

For any new system or significant change, consider:
- **Spoofing** — Can someone impersonate a user, service, or system?
- **Tampering** — Can data be modified without detection?
- **Repudiation** — Can actions be denied? Is there sufficient logging?
- **Information Disclosure** — Can sensitive data leak? (PII, credentials, business data)
- **Denial of Service** — Can the system be overwhelmed?
- **Elevation of Privilege** — Can someone gain unauthorized access levels?

### AWS Security Baseline

- **Account structure**: Multi-account (AWS Organizations), SCPs for guardrails
- **Network**: VPC per workload, private subnets for compute/data, public only for load balancers, NACLs + security groups layered
- **Identity**: SSO/IAM Identity Center, no long-lived access keys, MFA enforced, role-based access
- **Detection**: GuardDuty (threat detection), Security Hub (posture), Config (compliance), Inspector (vulnerability scanning)
- **Response**: EventBridge → Lambda for automated remediation, IR runbooks

### CIS Benchmarks

Use CIS Benchmarks as configuration baselines for:
- AWS account hardening
- Operating system hardening (if managing EC2)
- Container runtime security
- Database security configuration

## COULD — Open Space

- **Think like an attacker.** After reviewing defenses, ask: "If I wanted to breach this system, where would I start?" The answer reveals the weakest link.
- **Supply chain security.** Beyond your code: are dependencies trusted? Are base images from verified sources? Is the CI/CD pipeline itself secured? (A compromised pipeline compromises everything it deploys.)
- **Zero trust challenge.** Does this architecture assume the network perimeter is the security boundary? What if an attacker is already inside? How does the design hold up?
- **Human factors.** The most common attack vector is people, not systems. Phishing, social engineering, credential reuse. Does the security design account for human error?
- **Compliance ≠ security.** Passing a compliance check doesn't mean the system is secure. It means it meets a minimum bar. What risks exist that compliance frameworks don't cover?
