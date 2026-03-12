# IT Incident Management — Swimlane Flow

> Lean incident management process. Shows who does what at each stage.
> Designed for 1–2 slide presentation.
>
> Related: [`incident-triage-guideline.md`](incident-triage-guideline.md) · [`lightweight.md`](lightweight.md) · [`severity-triage.md`](severity-triage.md) · [`incident-knowledge-base.md`](incident-knowledge-base.md)

---

## Incident Classification

| Type | Definition | Owner | Examples |
|------|-----------|-------|---------|
| **Infrastructure Incident** | Platform layer is broken — servers, network, DB, cloud services. Application cannot run. | Infra / DevOps | Server crash, network outage, DB down, cloud service disruption, certificate expired |
| **Application Incident** | Infrastructure is healthy. Problem is at the application layer — crash, wrong output, logic error, design flaw. | Dev / BA team | App OOM, wrong calculation, missing info display, design flaw affecting all customers, data corruption |

**Key question**: Is infrastructure healthy? NO → Infra Incident. YES → Application Incident.

Both can be **any priority**. A silent design flaw miscalculating premiums for all customers = P1 Application Incident.

---

## Priority Matrix

| Priority | Name | Definition | Response Time | Resolution Target | Who's Involved |
|----------|------|-----------|---------------|-------------------|----------------|
| **P1** | Critical | Full outage, data breach, or financial data affected | Immediate | < 1 hour | All hands: IC + Tech + Mgmt + Comms |
| **P2** | Major | Significant degradation, key function unavailable | < 15 min | < 4 hours | IC + On-call team + Mgmt notified |
| **P3** | Minor | Partial impact, workaround available | < 1 hour | < 1 business day | On-call / assigned team |
| **P4** | Low | Cosmetic, minimal impact | Next business day | < 5 business days | Assigned developer |

---

## Swimlane Flow — Who Does What

### Slide Layout (5 Stages × 6 Roles)

```
 STAGE ▸       ① DETECT         ② TRIAGE            ②b COLLABORATE       ③ RESPOND & FIX      ④ VERIFY          ⑤ CLOSE
               (< 5 min)        (< 15 min)          (App, no KB match)   (Priority-dependent)  (< 30 min)        (P1/P2: < 48 hrs)
─────────────┬────────────────┬───────────────────┬────────────────────┬──────────────────────┬─────────────────┬──────────────────
             │                │                   │                    │                      │                 │
 ANYONE      │ Report issue   │                   │                    │                      │                 │
 (User /     │ via channel    │                   │                    │                      │                 │
  Alert)     │ or alert fires │                   │                    │                      │                 │
             │                │                   │                    │                      │                 │
─────────────┼────────────────┼───────────────────┼────────────────────┼──────────────────────┼─────────────────┼──────────────────
             │                │                   │                    │                      │                 │
 L1/L2 ITO   │ Receive &      │ Confirm real?     │ Loop in Tech Team  │                      │                 │
 (On-call /  │ acknowledge    │ Check infra       │ + BA within 30 min │                      │                 │
  Help Desk) │                │ health            │ Share prelim P     │                      │                 │
             │                │ Classify: Infra   │ Confirm / adjust P │                      │                 │
             │                │ or Application?   │                    │                      │                 │
             │                │                   │                    │                      │                 │
             │                │ Check Knowledge   │                    │                      │                 │
             │                │ Base for known    │                    │                      │                 │
             │                │ scenarios         │                    │                      │                 │
             │                │                   │                    │                      │                 │
             │                │ KB MATCH:         │                    │                      │                 │
             │                │ → Assign P from   │                    │                      │                 │
             │                │   KB immediately  │                    │                      │                 │
             │                │ → Execute first   │                    │                      │                 │
             │                │   response        │                    │                      │                 │
             │                │ → App: notify     │                    │                      │                 │
             │                │   tech team       │                    │                      │                 │
             │                │   (don't wait)    │                    │                      │                 │
             │                │                   │                    │                      │                 │
             │                │ KB NO MATCH:      │                    │                      │                 │
             │                │ → Infra: assign P │                    │                      │                 │
             │                │   by scope        │                    │                      │                 │
             │                │ → App: assign     │                    │                      │                 │
             │                │   preliminary P   │                    │                      │                 │
             │                │                   │                    │                      │                 │
─────────────┼────────────────┼───────────────────┼────────────────────┼──────────────────────┼─────────────────┼──────────────────
             │                │                   │                    │                      │                 │
 INCIDENT    │                │ Assigned as IC    │                    │ Coordinate team      │ Confirm service │ Lead RCA
 COMMANDER   │                │ (P1/P2 only)      │                    │ Manage comms         │ restored        │ Publish report
 (IC)        │                │                   │                    │ Decide: rollback?    │                 │ Track actions
             │                │                   │                    │   escalate? war room?│                 │ Update Knowledge
             │                │                   │                    │ Status updates       │                 │ Base
             │                │                   │                    │ (P1: 30m · P2: 1hr)  │                 │
             │                │                   │                    │                      │                 │
─────────────┼────────────────┼───────────────────┼────────────────────┼──────────────────────┼─────────────────┼──────────────────
             │                │                   │                    │                      │                 │
 TECH TEAM   │                │                   │ App Incident:      │ INFRA INCIDENT:      │ Monitor 15 min  │ Contribute to
 (Dev /      │                │                   │ Assess blast       │  → Rollback/restart/ │ for regression  │ RCA findings
  Infra /    │                │                   │ radius with L1     │    failover          │                 │
  BA / DBA)  │                │                   │ Confirm or         │  → Apply infra fix   │                 │
             │                │                   │ adjust P           │                      │                 │
             │                │                   │                    │ APP INCIDENT:        │                 │
             │                │                   │                    │  → Root cause        │                 │
             │                │                   │                    │  → Develop & test fix│                 │
             │                │                   │                    │  → Deploy via CI/CD  │                 │
             │                │                   │                    │  → Remediate bad data│                 │
             │                │                   │                    │                      │                 │
─────────────┼────────────────┼───────────────────┼────────────────────┼──────────────────────┼─────────────────┼──────────────────
             │                │                   │                    │                      │                 │
 QA          │                │                   │                    │ Validate fix in      │                 │
             │                │                   │                    │ staging before deploy│                 │
             │                │                   │                    │ (App Incident only)  │                 │
             │                │                   │                    │                      │                 │
─────────────┼────────────────┼───────────────────┼────────────────────┼──────────────────────┼─────────────────┼──────────────────
             │                │                   │                    │                      │                 │
 MANAGEMENT  │                │ Notified          │                    │ Receive status       │ Notified of     │ Review RCA
 (IT Mgr /   │                │ (P1/P2)           │                    │ updates              │ restoration     │ Sign off
  CTO)       │                │ Approve           │                    │ (P1: every 30 min,   │                 │ action items
             │                │ escalation        │                    │  P2: every 1 hr)     │                 │
             │                │                   │                    │                      │                 │
─────────────┴────────────────┴───────────────────┴────────────────────┴──────────────────────┴─────────────────┴──────────────────
```

> **P3/P4 note:** No Incident Commander assigned. Team lead coordinates directly. Simplified post-incident review instead of full RCA — escalate to full RCA only if financial or data impact.

---

## RACI Matrix

| Stage | L1/L2 ITO | Incident Commander | Tech Team | QA | Management |
|-------|-----------|-------------------|-----------|-----|------------|
| ① Detect | **R** | I | I | — | — |
| ② Triage | **R/A** | **A** (P1/P2) | **C** | — | **I** (P1/P2) |
| ②b Collaborate (App, no KB match) | **R** | I | **R/A** | — | — |
| ③ Respond & Fix | I | **A** (P1/P2) | **R** | **R** (App Incident) | **I** |
| ④ Verify | I | **A** | **R** | — | **I** |
| ⑤ Close (RCA) | — | **R** | **C** | — | **A** |

> **R** = Responsible · **A** = Accountable · **C** = Consulted · **I** = Informed
>
> For P3/P4: team lead assumes IC accountability. No formal IC role assigned.

---

## Quick Reference — Infrastructure vs Application Incident

| | Infrastructure Incident | Application Incident |
|---|---|---|
| **Infra health** | Broken | Healthy |
| **Problem layer** | Server, network, DB, cloud | App code, logic, design, config, data |
| **Priority assignment** | KB match → assign P from KB. No match → assign by scope. | KB match → assign P from KB, act immediately, notify tech team. No match → preliminary P → Tech Team confirms within 30 min. |
| **Response** | Restore immediately (rollback, restart, failover) | Assess blast radius → fix correctly → remediate data |
| **Owner** | Infra / DevOps | Dev / BA team |
| **Detection** | Loud — monitoring catches it | Often quiet — detected by people, not alerts |
| **RCA trigger** | Always for P1/P2 | Always for P1/P2 + if financial/data impact |

---

## Mermaid Diagrams

### Main Flow — Incident Management Process

```mermaid
flowchart TD
    %% ═══════════════════════════════════════
    %% STAGE 1: DETECT
    %% ═══════════════════════════════════════
    subgraph S1["① DETECT  •  < 5 min"]
        direction TB
        A1["Monitoring alert fires"]
        A2["User / stakeholder reports"]
        A3["Health check fails"]
    end

    %% ═══════════════════════════════════════
    %% STAGE 2: TRIAGE
    %% ═══════════════════════════════════════
    subgraph S2["② TRIAGE  •  < 15 min"]
        direction TB
        B1["<b>L1/L2 ITO</b><br/>Confirm incident is real"]
        B2["<b>L1/L2 ITO</b><br/>Classify: Is infra healthy?"]
        B1 --> B2
    end

    A1 --> B1
    A2 --> B1
    A3 --> B1

    B2 --> FORK{"Infra healthy?"}

    %% ═══════════════════════════════════════
    %% INFRA INCIDENT PATH
    %% ═══════════════════════════════════════
    FORK -->|"NO — infra broken"| KB_I{"Check KB<br/>Match found?"}

    subgraph S3A["③ RESPOND — Infrastructure Incident"]
        direction TB
        C0["<b>L1</b> assigns P from KB<br/>Execute documented response"]
        C0N["<b>L1</b> assigns P by scope"]
        C1["<b>IC</b> · P1/P2 only<br/>Coordinate · Status updates<br/>(P1: 30 min · P2: 1 hr)"]
        C2["<b>Infra / DevOps</b><br/>Rollback / Restart / Failover"]
        C3["<b>Infra / DevOps</b><br/>Apply infrastructure fix"]
        C0 --> C1
        C0N --> C1
        C1 --> C2 --> C3
    end

    KB_I -->|"YES"| C0
    KB_I -->|"NO"| C0N

    %% ═══════════════════════════════════════
    %% APPLICATION INCIDENT PATH
    %% ═══════════════════════════════════════
    FORK -->|"YES — infra healthy"| KB_A{"Check KB<br/>Match found?"}

    subgraph S3B["②b + ③ — Application Incident"]
        direction TB
        D0K["<b>L1</b> assigns P from KB<br/>Execute documented response<br/>Notify tech team (don't wait)"]
        D0["<b>L1</b> assigns preliminary P"]
        D0B["<b>L1 + Tech Team + BA</b><br/>Collaborate within 30 min<br/>Assess blast radius · Confirm / adjust P"]
        D1["<b>IC</b> · P1/P2 only<br/>Coordinate · Status updates"]
        D2["<b>Dev Team</b><br/>Root cause & develop fix"]
        D3["<b>QA</b><br/>Validate fix in staging"]
        D4["<b>Dev / DBA</b><br/>Deploy & remediate data"]
        D0K --> D1
        D0 --> D0B --> D1
        D1 --> D2 --> D3 --> D4
    end

    KB_A -->|"YES"| D0K
    KB_A -->|"NO"| D0

    %% ═══════════════════════════════════════
    %% STAGE 4: VERIFY
    %% ═══════════════════════════════════════
    subgraph S4["④ VERIFY  •  < 30 min"]
        direction TB
        E1["<b>Tech Team</b><br/>Monitor 15 min for regression"]
        E3["<b>IC / Team Lead</b><br/>Confirm service restored"]
        E1 --> E3
    end

    C3 --> E1
    D4 --> E1

    %% ═══════════════════════════════════════
    %% STAGE 5: CLOSE
    %% ═══════════════════════════════════════
    subgraph S5["⑤ CLOSE  •  Within 48 hrs"]
        direction TB
        F1["<b>IC / Team Lead</b><br/>Lead blameless RCA"]
        F2["<b>Tech Team</b><br/>Identify root cause"]
        F3["<b>IC / Team Lead</b><br/>Define action items<br/>Update Knowledge Base"]
        F5["<b>Management</b><br/>Review & sign off"]
        F6["<b>INCIDENT CLOSED</b><br/>RCA published · Actions in backlog<br/>Knowledge Base updated"]
        F1 --> F2 --> F3 --> F5 --> F6
    end

    E3 --> F1

    %% ═══════════════════════════════════════
    %% MANAGEMENT — parallel track
    %% ═══════════════════════════════════════
    MGT["<b>Management</b><br/>Notified P1/P2<br/>Status updates"]

    C1 -. "P1/P2<br/>notify + updates" .-> MGT
    D1 -. "P1/P2<br/>notify + updates" .-> MGT
    E3 -. "all-clear" .-> MGT

    %% ═══════════════════════════════════════
    %% STYLES
    %% ═══════════════════════════════════════
    classDef stageDetect fill:#1E293B,stroke:#6366F1,stroke-width:2px,color:#E2E8F0
    classDef stageTriage fill:#1E293B,stroke:#8B5CF6,stroke-width:2px,color:#E2E8F0
    classDef stageInfra fill:#1C1917,stroke:#EF4444,stroke-width:2px,color:#FCA5A5
    classDef stageApp fill:#1C1917,stroke:#F59E0B,stroke-width:2px,color:#FDE68A
    classDef stageVerify fill:#1E293B,stroke:#10B981,stroke-width:2px,color:#A7F3D0
    classDef stageClose fill:#1E293B,stroke:#0EA5E9,stroke-width:2px,color:#BAE6FD
    classDef forkNode fill:#1E1B3A,stroke:#A78BFA,stroke-width:2.5px,color:#DDD6FE
    classDef mgtNode fill:#0C2340,stroke:#0EA5E9,stroke-width:1.5px,color:#BAE6FD,rx:8
    classDef doneNode fill:#052E16,stroke:#22C55E,stroke-width:2.5px,color:#BBF7D0,rx:12

    class S1 stageDetect
    class S2 stageTriage
    class S3A stageInfra
    class S3B stageApp
    class S4 stageVerify
    class S5 stageClose
    class FORK,KB_I,KB_A forkNode
    class MGT mgtNode
    class F6 doneNode
```

### Incident Classification Decision

```mermaid
flowchart LR
    START["Incident<br/>Reported"] --> Q1{"Is infrastructure<br/>healthy?"}

    Q1 -->|"NO — server, network,<br/>DB, or cloud broken"| II["<b>Infrastructure<br/>Incident</b>"]
    Q1 -->|"YES — infra healthy,<br/>problem is in the app"| AI["<b>Application<br/>Incident</b>"]

    II --> II_KB{"KB match?"}
    II_KB -->|"YES"| II_P1["Assign P from KB<br/>Execute response"]
    II_KB -->|"NO"| II_P2["Assign P by scope"]
    II --> II_OWNER["<b>Owner:</b><br/>Infra / DevOps"]
    II --> II_ACTION["<b>Actions:</b><br/>Failover · Restart<br/>Rollback · Fix infra"]

    AI --> AI_KB{"KB match?"}
    AI_KB -->|"YES"| AI_P1["Assign P from KB<br/>Act immediately<br/>Notify tech team"]
    AI_KB -->|"NO"| AI_P2["Assign preliminary P<br/>→ Collaborate with<br/>Tech Team within 30 min"]
    AI --> AI_OWNER["<b>Owner:</b><br/>Dev / BA team"]
    AI --> AI_ACTION["<b>Actions:</b><br/>Assess blast radius<br/>Root cause · Fix & test<br/>Deploy · Remediate data"]

    classDef start fill:#1E1B3A,stroke:#6366F1,stroke-width:2px,color:#E8E6FF,rx:10
    classDef question fill:#1E1B3A,stroke:#A78BFA,stroke-width:2px,color:#DDD6FE
    classDef infra fill:#450A0A,stroke:#EF4444,stroke-width:2.5px,color:#FCA5A5,rx:10
    classDef app fill:#451A03,stroke:#F59E0B,stroke-width:2.5px,color:#FCD34D,rx:10
    classDef detail fill:#1E293B,stroke:#475569,stroke-width:1px,color:#CBD5E1,rx:6

    class START start
    class Q1 question
    classDef kbNode fill:#1E1B3A,stroke:#A78BFA,stroke-width:2px,color:#DDD6FE

    class II infra
    class AI app
    class II_KB,AI_KB kbNode
    class II_P1,II_P2,II_OWNER,II_ACTION,AI_P1,AI_P2,AI_OWNER,AI_ACTION detail
```

### Priority Levels

```mermaid
flowchart LR
    subgraph PRI["Priority Matrix"]
        direction TB
        S1["P1 — Critical<br/>Full outage · Data breach · Financial data affected<br/><i>Respond: Immediate · Resolve: < 1 hr</i><br/>All hands + IC + Management"]
        S2["P2 — Major<br/>Significant degradation · Key function down<br/><i>Respond: < 15 min · Resolve: < 4 hrs</i><br/>IC + On-call + Mgmt notified"]
        S3["P3 — Minor<br/>Partial impact · Workaround exists<br/><i>Respond: < 1 hr · Resolve: < 1 day</i><br/>On-call / assigned engineer"]
        S4["P4 — Low<br/>Cosmetic · Minimal impact<br/><i>Respond: Next day · Resolve: < 5 days</i><br/>Assigned developer"]
        S1 ~~~ S2 ~~~ S3 ~~~ S4
    end

    classDef sev1 fill:#450A0A,stroke:#EF4444,stroke-width:2px,color:#FCA5A5,rx:8
    classDef sev2 fill:#451A03,stroke:#F59E0B,stroke-width:2px,color:#FCD34D,rx:8
    classDef sev3 fill:#0C2340,stroke:#3B82F6,stroke-width:2px,color:#93C5FD,rx:8
    classDef sev4 fill:#052E16,stroke:#10B981,stroke-width:2px,color:#6EE7B7,rx:8

    class S1 sev1
    class S2 sev2
    class S3 sev3
    class S4 sev4
```

---

## PPT Design Notes

- **Slide 1**: Swimlane flow. Horizontal lanes per role, left-to-right stages. Infra Incident path (red) vs Application Incident path (amber). Note the collaboration step (②b) in the App path.
- **Slide 2**: Priority matrix (color-coded) + RACI grid + Quick Reference comparison.
- **Colors**: P1 = Red, P2 = Orange, P3 = Blue, P4 = Green.
- **Font**: 14pt minimum for readability.
