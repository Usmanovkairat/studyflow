# AI-native development process
1. **Brainstorm:** orchestrator compares feasible ideas and records genuine decisions in `chat-brainstorm.md`.
2. **Specify:** delegate to PM. PM writes the product plan, architecture context and detailed feature tasks before implementation. The user has already authorized reasonable independent decisions.
3. **Prepare issues:** preserve four-section specifications: Goal, Acceptance criteria, Out of scope, Constraints. Create actual GitHub issues when a repository and write capabilities exist. Record actual IDs; never substitute local filenames for remote issues.
4. **Implement:** delegate one scoped task to software engineer, read acceptance criteria and dependencies, implement and run relevant checks. Work sequentially through the six tasks. Changes should map to their specification.
5. **Review and QA:** delegate acceptance verification to QA with fresh evidence. QA checks user workflows, edge cases, persistence and security; reports findings to orchestrator. Engineer fixes defects, QA reruns affected checks.
6. **Document and close:** update actual test evidence and README. Commit reviewed work. Close actual remote issues only after acceptance and publication are verified. If publication is blocked, retain pending remote status and prepare reviewable delivery files.
7. **Deliver:** report real links, tests and limitations, distinguishing locally implemented tasks from actual GitHub activity.

The article describes orchestrator delegation to PM, software engineer and QA, with `_docs` documents guiding execution. This project uses those boundaries. Do not fabricate historical interactions or silently treat inaccessible video content as reviewed.
