# Skill: Research Methodology

Systematic approach to gathering, evaluating, and synthesizing information.

## MUST — Guardrails

- **Always use real-time web search.** Do not rely on training data alone for factual claims, regulatory references, pricing, or current status of any technology/regulation. Use the WebSearch tool.
- **Cite every factual claim.** No "it is widely known that..." without a source. Provide: source name, URL (when available), and access date.
- **Date-stamp findings.** Regulations change. AWS services update. State "as of [date]" for time-sensitive information.
- **Tag confidence levels.** For every key finding:
  - **Confirmed** — Verified from official or primary source (government gazette, AWS documentation, peer-reviewed)
  - **Likely** — Multiple credible secondary sources agree
  - **Uncertain** — Limited, conflicting, or single-source information
  - **Unverified** — Found in one source, could not cross-reference

## SHOULD — Frameworks

### Search Strategy

1. **Start broad, then narrow.** First search: understand the landscape. Second search: drill into specifics. Third search: verify and cross-reference.
2. **Multi-query approach.** Don't rely on one search. Rephrase the question 2-3 ways. Different wording surfaces different results.
3. **Bilingual search (EN/VI).** For Vietnamese regulatory and market topics:
   - English: broader analysis, international perspective, English-language legal databases
   - Vietnamese: primary sources, official gazettes, local market data
   - Key Vietnamese terms: Thông tư (Circular), Nghị định (Decree), Luật (Law), Quyết định (Decision), Bộ Tài chính (Ministry of Finance), Ngân hàng Nhà nước (State Bank)
4. **Source hierarchy:**
   - **Primary**: Official government publications, AWS documentation, RFC/standards documents
   - **Secondary**: Reputable news (Reuters, Bloomberg), industry reports (McKinsey, Deloitte, Swiss Re), peer-reviewed papers
   - **Tertiary**: Blog posts, Stack Overflow, forum discussions — useful for practical experience, not for factual authority

### Source Evaluation (CRAAP Test)

- **Currency** — When was it published? Is it still relevant?
- **Relevance** — Does it address your specific question?
- **Authority** — Who published it? What are their credentials?
- **Accuracy** — Is it supported by evidence? Can you verify claims?
- **Purpose** — Is it informational, promotional, or opinion? What's the bias?

### Synthesis Structure

Organize findings into:
1. **Executive summary** — 3-5 key takeaways
2. **Detailed findings** — By theme, not by source
3. **Analysis** — What the findings mean in context
4. **Gaps** — What couldn't be found or verified
5. **References** — Complete source list

## COULD — Open Space

- **Triangulate.** If three independent sources with different perspectives agree, confidence is high. If they disagree, the disagreement itself is a finding worth reporting.
- **Follow the references.** The best sources often cite their own sources. Go one level deeper for critical claims.
- **Spot the narrative.** Multiple sources may all trace back to one original claim. Identify the primary source rather than treating echoes as independent confirmation.
- **Name what you couldn't find.** The absence of information is itself information. "No Vietnamese regulatory guidance exists on X" is a valuable finding.
- **Synthesize across domains.** You have access to both technical and regulatory knowledge. Connect them: "This AWS feature enables compliance with this regulation in this specific way."
