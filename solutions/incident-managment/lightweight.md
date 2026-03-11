---
title: Incident Management Flow
---
flowchart TD
    %% ── Detection ──
    D["🔍 <b>DETECTION</b><br/><i>Target: &lt; 5 min</i>"]
    D1["Automated alert fires<br/>(APM / Infra / Synthetic)"]
    D2["User / stakeholder<br/>reports issue"]
    D3["Health-check or<br/>heartbeat fails"]

    D1 --> D
    D2 --> D
    D3 --> D

    %% ── Triage ──
    D --> T["⚖️ <b>TRIAGE &amp; CLASSIFY</b><br/><i>Target: &lt; 10 min</i>"]
    T --> T1["Confirm incident is real"]
    T1 --> T2["Assign priority<br/>P1 → P4"]
    T2 --> T3["Assign Incident Commander"]
    T3 --> FORK{"🔀 <b>What type<br/>of incident?</b><br/><i>System down or<br/>behaving wrong?</i>"}

    %% ══════════════════════════════════
    %% INFRA TRACK (left)
    %% ══════════════════════════════════
    FORK -->|"System is <b>DOWN</b><br/>or unreachable"| IC["🛡️ <b>CONTAINMENT</b><br/><i>Target: &lt; 30 min</i>"]

    IC --> IC1["Failover to healthy<br/>region / replica"]
    IC --> IC2["Roll back infra change<br/>(deploy / config)"]
    IC --> IC3["Restart crashed<br/>services / pods"]
    IC --> IC4["Enable maintenance page<br/>/ circuit breakers"]

    IC1 --> IR["🔧 <b>RESOLUTION &amp; RECOVERY</b><br/><i>Target: varies</i>"]
    IC2 --> IR
    IC3 --> IR
    IC4 --> IR

    IR --> IR1["Apply durable fix"]
    IR --> IR2["Verify health checks green"]
    IR --> IR3["Monitor ≥ 15 min<br/>for regressions"]

    IR1 --> MERGE["✅ <b>SERVICE RESTORED</b>"]
    IR2 --> MERGE
    IR3 --> MERGE

    %% ══════════════════════════════════
    %% APP / LOGIC TRACK (right)
    %% ══════════════════════════════════
    FORK -->|"System is <b>UP</b> but<br/>behaving wrong"| AA["🔬 <b>IMPACT ASSESSMENT</b><br/><i>Target: &lt; 1 hr</i>"]

    AA --> AA1["Reproduce the<br/>incorrect behavior"]
    AA --> AA2["RCA: code bug,<br/>config, or data issue"]
    AA --> AA3["Quantify data &amp;<br/>financial impact"]

    AA1 --> AF["🩹 <b>FIX &amp; VALIDATE</b><br/><i>Target: hours → days</i>"]
    AA2 --> AF
    AA3 --> AF

    AF --> AF1["Develop fix +<br/>unit / integration tests"]
    AF --> AF2["Code review with<br/>extra scrutiny"]
    AF --> AF3["QA validates in staging"]
    AF --> AF4["Deploy &amp; verify<br/>in production"]

    AF1 --> DATAQ{"🗃️ <b>Bad data<br/>written?</b>"}
    AF2 --> DATAQ
    AF3 --> DATAQ
    AF4 --> DATAQ

    DATAQ -->|"Yes"| DR["🗃️ <b>DATA REMEDIATION</b>"]
    DR --> DR1["Run correction scripts<br/>(backup first!)"]
    DR --> DR2["Recalculate reports<br/>/ invoices / balances"]
    DR --> DR3["Notify affected<br/>customers"]
    DR1 --> MERGE
    DR2 --> MERGE
    DR3 --> MERGE

    DATAQ -->|"No"| MERGE

    %% ══════════════════════════════════
    %% SHARED — POST-RESOLUTION
    %% ══════════════════════════════════
    MERGE --> PIR["📝 <b>RCA — ROOT CAUSE ANALYSIS</b><br/><i>Within 48 hours</i>"]
    PIR --> PIR1["Blameless RCA meeting"]
    PIR --> PIR2["Build detailed timeline"]
    PIR --> PIR3["Identify root cause &amp;<br/>contributing factors"]
    PIR --> PIR4["Define action items<br/>with owners &amp; dates"]
    PIR --> PIR5["Update runbooks &amp;<br/>monitoring"]

    PIR1 --> DONE["🏁 <b>INCIDENT CLOSED</b><br/><i>RCA published · Actions tracked in backlog</i>"]
    PIR2 --> DONE
    PIR3 --> DONE
    PIR4 --> DONE
    PIR5 --> DONE

    %% ══════════════════════════════════
    %% COMMUNICATION — parallel swim lane
    %% ══════════════════════════════════
    COMMS["📢 <b>COMMUNICATION</b><br/><i>Runs parallel — all phases</i>"]
    COMMS -.- |"P1: every 30 min<br/>P2: every 1 hr"| T
    COMMS -.- |"Status page<br/>updates"| IC
    COMMS -.- |"Customer<br/>notification"| AA
    COMMS -.- |"All-clear<br/>message"| MERGE

    %% ══════════════════════════════════
    %% SEVERITY LEGEND (as a subgraph)
    %% ══════════════════════════════════
    subgraph SEV ["📊 Priority Matrix"]
        direction LR
        S1["<b>P1</b> Critical<br/>Full outage / data breach<br/><i>All hands 24/7</i>"]
        S2["<b>P2</b> Major<br/>Significant degradation<br/><i>On-call + escalation</i>"]
        S3["<b>P3</b> Minor<br/>Partial impact<br/><i>Business hours</i>"]
        S4["<b>P4</b> Low<br/>Cosmetic issue<br/><i>Next business day</i>"]
    end

    %% ══════════════════════════════════
    %% STYLES
    %% ══════════════════════════════════

    classDef shared fill:#2D2B55,stroke:#6366F1,stroke-width:2px,color:#E8E6FF,rx:10
    classDef fork fill:#1E1B3A,stroke:#A78BFA,stroke-width:2.5px,color:#DDD6FE,rx:4
    classDef infra fill:#3B1518,stroke:#E8453C,stroke-width:2px,color:#FEC8C5,rx:10
    classDef infraStep fill:#2A1012,stroke:#E8453C55,stroke-width:1px,color:#F5A8A3,rx:6
    classDef app fill:#3B2A08,stroke:#D97706,stroke-width:2px,color:#FDE68A,rx:10
    classDef appStep fill:#2A1E06,stroke:#D9770655,stroke-width:1px,color:#FCD480,rx:6
    classDef mergeNode fill:#0C2E1A,stroke:#10B981,stroke-width:2.5px,color:#A7F3D0,rx:10
    classDef review fill:#1A1040,stroke:#8B5CF6,stroke-width:2px,color:#DDD6FE,rx:10
    classDef done fill:#052E16,stroke:#22C55E,stroke-width:2.5px,color:#BBF7D0,rx:12
    classDef comms fill:#0C2340,stroke:#0EA5E9,stroke-width:2px,color:#BAE6FD,rx:10
    classDef detect fill:#1E1B3A,stroke:#6366F1,stroke-width:1px,color:#C4B5FD,rx:6
    classDef sev1 fill:#450A0A,stroke:#EF4444,stroke-width:1.5px,color:#FCA5A5,rx:6
    classDef sev2 fill:#451A03,stroke:#F59E0B,stroke-width:1.5px,color:#FCD34D,rx:6
    classDef sev3 fill:#0C2340,stroke:#3B82F6,stroke-width:1.5px,color:#93C5FD,rx:6
    classDef sev4 fill:#052E16,stroke:#10B981,stroke-width:1.5px,color:#6EE7B7,rx:6
    classDef dataQ fill:#2A1E06,stroke:#FBBF24,stroke-width:2.5px,color:#FDE68A,rx:4

    class D,T shared
    class FORK fork
    class D1,D2,D3,T1,T2,T3 detect
    class IC,IR infra
    class IC1,IC2,IC3,IC4,IR1,IR2,IR3 infraStep
    class AA,AF app
    class AA1,AA2,AA3,AF1,AF2,AF3,AF4 appStep
    class DATAQ dataQ
    class DR app
    class DR1,DR2,DR3 appStep
    class MERGE mergeNode
    class PIR review
    class PIR1,PIR2,PIR3,PIR4,PIR5 detect
    class DONE done
    class COMMS comms
    class S1 sev1
    class S2 sev2
    class S3 sev3
    class S4 sev4