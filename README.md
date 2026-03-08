# Sharable

A shared workspace for brainstorming, architecture, solution design, knowledge exploration, and prototyping — focused on life insurance, banking, and IT operations in Vietnam.

## Quick Start

Open this project in Claude Code and use slash commands:

```
/brainstorm digital distribution channels for life insurance
/architect core policy admin system migration to AWS
/solve incident management process for production systems
/research new circular on bancassurance regulations
/prototype trivy container scanning in github actions
/review architecture/payment-gateway-design.md
```

## Commands

| Command | What it does | Output folder |
|---|---|---|
| `/brainstorm <topic>` | Structured ideation with decomposition and trade-off analysis | `brainstorming/` |
| `/architect <topic>` | System architecture with ADRs, Mermaid diagrams, and full Well-Architected review | `architecture/` |
| `/solve <problem>` | Solution design with root cause analysis, alternatives, and implementation plan | `solutions/` |
| `/research <topic>` | Real-time web research with source evaluation and confidence tagging | `knowledge/` |
| `/prototype <idea>` | Quick PoC with security guardrails and a README | `prototypes/` |
| `/review <file>` | Multi-lens review with severity-rated findings | In-place |

## Skills System

Commands don't work alone — they compose **skills**, reusable reasoning modules that ensure consistent quality while leaving room for creative thinking.

### How skills are structured

Each skill has three tiers:

| Tier | Purpose | Example |
|---|---|---|
| **MUST** | Guardrails. Never skip. Ensures consistency. | "Never fabricate regulatory references" |
| **SHOULD** | Frameworks. Suggested tools — use them or bring your own. | "Consider 5 Whys, Fishbone, or your own method" |
| **COULD** | Open space. Invitation to innovate and challenge. | "What cross-domain analogy applies here?" |

### Skill catalog

**Analytical Frameworks** — *how to think*

| Skill | What it ensures |
|---|---|
| `structured-decomposition` | Breaks problems into parts before solving. Prevents "first idea" anchoring. |
| `trade-off-analysis` | Compares options with explicit criteria. Forces reasoning about what's sacrificed. |
| `risk-assessment` | Identifies risks and mitigations. Prevents happy-path-only thinking. |

**Domain Knowledge** — *what to know*

| Skill | What it provides |
|---|---|
| `vietnam-insurance-regulatory` | Regulatory framework for life insurance in Vietnam (MoF, ISA, Insurance Business Law). |
| `vietnam-banking-regulatory` | SBV/NHNN directives, Basel adoption, AML/KYC, payment regulations. |
| `insurance-domain-model` | Core business concepts — products, underwriting, claims, policy admin, reinsurance. |
| `aws-cloud-patterns` | Architecture patterns, service selection, Well-Architected Framework. |
| `devsecops-practices` | CI/CD pipelines, IaC, security-as-code, container security, observability. |

**Quality Gates** — *how to validate*

| Skill | What it checks |
|---|---|
| `security-review` | OWASP Top 10, STRIDE threat model, encryption, least privilege, audit logging. |
| `compliance-check` | Data residency, PII handling, regulatory reporting, audit trails. |
| `operational-readiness` | Monitoring, alerting, DR/BCP, runbooks, SLO/SLI/SLA. |
| `cost-analysis` | TCO, AWS pricing models, build-vs-buy, cost optimization levers. |

**Research & Meta** — *how to gather and challenge*

| Skill | What it does |
|---|---|
| `research-methodology` | Real-time web search, bilingual (EN/VI), source evaluation (CRAAP), confidence tagging. |
| `creative-challenge` | The meta-skill. Challenges assumptions, finds cross-domain connections, names the elephant. |

### How commands compose skills

Every command loads skills automatically. Three domain skills are **always on** because this workspace operates in a regulated industry:

- `vietnam-insurance-regulatory`
- `vietnam-banking-regulatory`
- `insurance-domain-model`

Other skills are loaded based on the command type. Example composition:

```
/architect migrate policy admin to AWS

  Always-on:    vietnam-insurance-regulatory
                vietnam-banking-regulatory
                insurance-domain-model
                compliance-check

  Command:      aws-cloud-patterns
                security-review
                operational-readiness
                cost-analysis
                risk-assessment
                trade-off-analysis
                creative-challenge
```

The agent reads each skill file, applies MUST guardrails for consistency, uses SHOULD frameworks as tools, and explores COULD open space for creative insight.

## Project Structure

```
brainstorming/        # Ideas, mind maps, rough explorations
architecture/         # System design, diagrams, ADRs, component layouts
solutions/            # Solution designs, technical proposals, PoCs
knowledge/            # Research, references, learnings, how-tos
prototypes/           # Quick code experiments, spike solutions
assets/               # Shared images, diagrams, media files
.claude/
  commands/           # Slash commands (the "what")
  skills/             # Reusable reasoning modules (the "how")
```

## Conventions

- **Language**: English for code, comments, and documentation
- **File format**: Markdown for documents, kebab-case for names (e.g., `payment-gateway-design.md`)
- **Secrets**: Never committed. Use `.local/credentials.env` (gitignored)
- **Git**: Always commit after completing a task. Never push unless explicitly asked.
