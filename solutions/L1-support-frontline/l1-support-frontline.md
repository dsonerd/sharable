``` mermaid
flowchart LR
    %% Main L1 Support Flow
    Sale((Sale)) --> iProtek[iProtek\nSale Portal]
    iProtek --> Tori([Tori\nAI Assistant])

    %% Tori's knowledge base
    ekyc[eKYC] -.-> Tori
    Payment[Payment] -.-> Tori
    System[System] -.-> Tori

    %% Tori outcomes
    Tori -->|Answer| Sale
    Tori -->|Cannot Answer| LogTicket[Log a Ticket]

    %% Ticket flow
    LogTicket -->|L1| JSM[JSM\nJira Service Management]
    LogTicket -->|Call Hotline| IT_DO_DA[IT / DO / DA]

    %% JSM actions
    JSM -->|Request| Change[Change]
    JSM -->|Escalate| L2_L3

    %% Jira ticket tracking
    JSM -.->|Jira Ticket:\n2 NS, Logsheet| JiraNote[ ]

    %% Cannot Answer from support
    IT_DO_DA -->|Cannot Answer| LogTicket
    JSM -->|Cannot Answer| LogTicket

    %% Have Answer returns to Sale
    LogTicket -->|Have Answer| Sale

    %% === Bottom Flow: Sale Process ===
    Sale2((Sale)) --> Submit[Submit]
    Submit --> GhiCan[Ghi Cận]
    GhiCan --> eKYC2[eKYC]
    eKYC2 --> PaymentStep[Payment]

    %% === Action Items ===
    subgraph Action Items
        direction TB
        A1["①  Operational Document + FAQs for\n     - iProtek\n     - Care\n     - Customer Portal"]
        A2["②  L2/L3 Contact Point"]
        A3["③  SLA+"]
    end

    %% Styling
    classDef ai fill:#4A90D9,stroke:#2C5F8A,color:#fff
    classDef portal fill:#5CB85C,stroke:#3D7A3D,color:#fff
    classDef process fill:#F0AD4E,stroke:#C78C3E,color:#fff
    classDef sale fill:#D9534F,stroke:#A33B38,color:#fff
    classDef action fill:#fff3cd,stroke:#856404,color:#333

    class Tori ai
    class iProtek portal
    class LogTicket,JSM process
    class Sale,Sale2 sale
    class A1,A2,A3 action