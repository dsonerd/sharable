# Research

Research a topic and compile findings into a knowledge document.

## Domain Context

**Technical domain** — IT Operations, DevOps, DevSecOps, AWS cloud:
- AWS service evaluations, pricing comparisons, feature matrices
- DevSecOps toolchain assessments (SAST, DAST, SCA, container scanning)
- Security advisories, CVE analysis, CIS benchmarks, NIST frameworks
- Industry best practices, case studies, reference architectures

**Business domain** — Life insurance & banking in Vietnam:
- Vietnamese regulations: Ministry of Finance circulars, SBV/NHNN directives, decrees, amendments
- Insurance Business Law (Luật Kinh doanh bảo hiểm) — latest version and amendments
- IAIS (International Association of Insurance Supervisors) standards
- Basel framework adaptations for Vietnam banking
- AML/KYC/CFT regulations, data privacy laws
- Market reports, industry benchmarks, competitor analysis

## Instructions

1. **Always use real-time web search** (WebSearch tool) to gather current information. Do not rely solely on training data — regulations and cloud services change frequently.
2. Search strategy:
   - Use multiple search queries from different angles
   - For Vietnamese regulations: search in both English and Vietnamese (e.g., "Thông tư", "Nghị định", "Luật kinh doanh bảo hiểm")
   - For AWS/DevOps: check official documentation, AWS blogs, re:Invent talks, community benchmarks
   - Cross-reference findings from multiple sources
3. Synthesize findings into a well-structured document covering:
   - **Executive summary**: Key takeaways in 3-5 bullet points
   - **Background / context**: Why this topic matters
   - **Key findings**: Organized by theme, with evidence and sources
   - **Comparisons / evaluations**: Tables or matrices where applicable
   - **Vietnam-specific considerations**: Regulatory, market, or operational factors unique to Vietnam (when relevant)
   - **Implications**: What does this mean for our work?
   - **Open questions**: What remains unclear or needs further investigation?
   - **References**: Full list of sources with URLs and access dates
4. Be objective — clearly distinguish facts from opinions. Flag uncertainty levels:
   - **Confirmed**: Verified from official/authoritative sources
   - **Likely**: Multiple credible sources agree
   - **Uncertain**: Limited or conflicting information
5. For regulatory research, always note:
   - Effective date of the regulation
   - Which entities it applies to
   - Key requirements and deadlines
   - Penalties for non-compliance (if stated)
6. Save the result to `knowledge/<topic-in-kebab-case>.md` (use a subfolder for multi-part research).
7. If a knowledge document on the same topic already exists, update it rather than creating a new one.
8. Commit the result when done.

## Topic

$ARGUMENTS
