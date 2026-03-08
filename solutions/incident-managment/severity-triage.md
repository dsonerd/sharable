---
title: Severity Triage Decision Tree
---
flowchart TD
    START["🚨 <b>INCIDENT REPORTED</b><br/><i>Start here</i>"]

    START --> Q1{"🔐 <b>Data breach<br/>or security event?</b>"}

    Q1 -->|"Yes"| SEV1_SEC["🔴 <b>SEV1 — CRITICAL</b><br/>Security incident"]
    SEV1_SEC --> A_SEC["Invoke security<br/>incident playbook"]
    A_SEC --> A_SEC1["Isolate affected systems"]
    A_SEC --> A_SEC2["Notify CISO + Legal"]
    A_SEC --> A_SEC3["Assess regulatory<br/>reporting obligation<br/><i>(PDPD / MoF / ISA)</i>"]

    Q1 -->|"No"| Q2{"💰 <b>Financial transactions<br/>affected?</b><br/><i>Premiums, claims,<br/>policy values, payouts</i>"}

    Q2 -->|"Yes — data<br/>may be wrong"| SEV1_FIN["🔴 <b>SEV1 — CRITICAL</b><br/>Financial integrity"]
    SEV1_FIN --> A_FIN["Stop writes to<br/>affected system"]
    A_FIN --> A_FIN1["Identify blast radius<br/>(policies / amount)"]
    A_FIN --> A_FIN2["Notify Finance + Actuarial"]
    A_FIN --> A_FIN3["Prepare data<br/>remediation plan"]

    Q2 -->|"Yes — delayed<br/>but correct"| Q3
    Q2 -->|"No"| Q3{"👥 <b>How many users<br/>are affected?</b>"}

    Q3 -->|"All users /<br/>full outage"| SEV1_OUT["🔴 <b>SEV1 — CRITICAL</b><br/>Full outage"]
    SEV1_OUT --> A_OUT["All-hands response"]
    A_OUT --> A_OUT1["Activate Incident<br/>Commander"]
    A_OUT --> A_OUT2["Status page update<br/>every 30 min"]
    A_OUT --> A_OUT3["Exec notification<br/>within 15 min"]

    Q3 -->|"Many users /<br/>major feature down"| Q4{"⏰ <b>During peak<br/>business hours?</b><br/><i>Mon-Sat 8AM-6PM</i>"}

    Q4 -->|"Yes"| SEV2_PEAK["🟠 <b>SEV2 — MAJOR</b><br/>Peak-hour degradation"]
    SEV2_PEAK --> A_PEAK["On-call + escalation"]
    A_PEAK --> A_PEAK1["Notify affected<br/>business units"]
    A_PEAK --> A_PEAK2["Status update<br/>every 1 hour"]
    A_PEAK --> A_PEAK3["Workaround<br/>if available"]

    Q4 -->|"No"| SEV3_OFF["🟡 <b>SEV3 — MINOR</b><br/>Off-peak degradation"]
    SEV3_OFF --> A_OFF["On-call handles"]
    A_OFF --> A_OFF1["Fix during next<br/>business day if stable"]

    Q3 -->|"Few users /<br/>partial impact"| SEV3_PART["🟡 <b>SEV3 — MINOR</b><br/>Partial impact"]
    SEV3_PART --> A_PART["Assigned engineer"]
    A_PART --> A_PART1["Best-effort during<br/>business hours"]

    Q3 -->|"Cosmetic /<br/>no user impact"| SEV4["🟢 <b>SEV4 — LOW</b><br/>Cosmetic / minor"]
    SEV4 --> A_LOW["Backlog ticket"]
    A_LOW --> A_LOW1["Fix in next<br/>sprint"]

    %% ══════════════════════════════════
    %% ESCALATION RULES
    %% ══════════════════════════════════
    subgraph ESC ["📞 Escalation Rules"]
        direction LR
        E1["<b>SEV1</b><br/>IC + all engineers<br/>CTO within 15 min<br/>CEO within 1 hr"]
        E2["<b>SEV2</b><br/>On-call + backup<br/>IT Manager within 30 min"]
        E3["<b>SEV3</b><br/>Assigned engineer<br/>Team lead if no progress 2 hrs"]
        E4["<b>SEV4</b><br/>Sprint backlog<br/>No escalation"]
    end

    %% ══════════════════════════════════
    %% REGULATORY TRIGGERS
    %% ══════════════════════════════════
    subgraph REG ["⚖️ Regulatory Reporting Triggers"]
        direction LR
        R1["Personal data<br/>of policyholders<br/>exposed or lost"]
        R2["Financial transactions<br/>incorrectly processed<br/>above threshold"]
        R3["Core systems<br/>unavailable > 4 hrs<br/>during business hours"]
        R4["Any event affecting<br/>policyholder rights<br/>or benefits"]
    end

    %% ══════════════════════════════════
    %% STYLES
    %% ══════════════════════════════════
    classDef start fill:#1E1B3A,stroke:#6366F1,stroke-width:2.5px,color:#E8E6FF,rx:10
    classDef question fill:#1E1B3A,stroke:#A78BFA,stroke-width:2px,color:#DDD6FE,rx:4
    classDef sev1 fill:#450A0A,stroke:#EF4444,stroke-width:2.5px,color:#FCA5A5,rx:10
    classDef sev2 fill:#451A03,stroke:#F59E0B,stroke-width:2px,color:#FCD34D,rx:10
    classDef sev3 fill:#0C2340,stroke:#3B82F6,stroke-width:2px,color:#93C5FD,rx:10
    classDef sev4 fill:#052E16,stroke:#10B981,stroke-width:2px,color:#6EE7B7,rx:10
    classDef action fill:#1A1040,stroke:#8B5CF655,stroke-width:1px,color:#C4B5FD,rx:6
    classDef escBox fill:#0C2340,stroke:#0EA5E9,stroke-width:1.5px,color:#BAE6FD,rx:6
    classDef regBox fill:#2A1E06,stroke:#FBBF24,stroke-width:1.5px,color:#FDE68A,rx:6

    class START start
    class Q1,Q2,Q3,Q4 question
    class SEV1_SEC,SEV1_FIN,SEV1_OUT sev1
    class SEV2_PEAK sev2
    class SEV3_OFF,SEV3_PART sev3
    class SEV4 sev4
    class A_SEC,A_SEC1,A_SEC2,A_SEC3 action
    class A_FIN,A_FIN1,A_FIN2,A_FIN3 action
    class A_OUT,A_OUT1,A_OUT2,A_OUT3 action
    class A_PEAK,A_PEAK1,A_PEAK2,A_PEAK3 action
    class A_OFF,A_OFF1 action
    class A_PART,A_PART1 action
    class A_LOW,A_LOW1 action
    class E1,E2,E3,E4 escBox
    class R1,R2,R3,R4 regBox
