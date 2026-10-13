# Methodology and source mapping
## Sources
- Article: https://aishippingblog.com/p/ai-native-development-specifications
- Reference repository: https://github.com/alexeygrigorev/retroloop
- Detailed issue example: https://github.com/alexeygrigorev/retroloop/issues/17

The orchestrator retrieved the article and example issue before delegating product specifications. The article establishes brainstorming, Markdown product/architecture/process documents, role instructions, scoped task specifications, orchestrator delegation and QA feedback. The reference repository instructions inspected include `AGENTS.md`, `_docs/process.md` and `_docs/outdated/plan.md`. The reference issue uses `Goal`, `Acceptance criteria`, `Out of scope`, `Constraints`; StudyFlow issues preserve those exact sections while adding task-specific user story, data, routes and testing under them.

The article's canonical `_docs/team/{pm,software-engineer,qa-engineer}.md` structure is present. `AGENT.md`, root `process.md` and `roles/` compatibility files satisfy the assignment's named examples without replacing the canonical files. `AGENTS.md` and `CLAUDE.md` guide agents toward the same scope.

## Limits and evidence
The embedded video at https://www.youtube-nocookie.com/embed/VUJxJGpaDEs could not be inspected because the player required JavaScript; no transcript was inspected. Do not claim video review. `chat-brainstorm.md` records AI decisions from this execution, not fabricated user dialogue. `_docs/tasks.md` tracks local specification and actual remote status separately. QA evidence must be written after execution. Actual GitHub issue timestamps and publication commits are recorded in `publication.md`. The user later supplied a deadline of 1.5–2 hours from approximately 12:00 Asia/Qyzylorda on 2026-10-13; 13:30 is used as the conservative inferred cutoff. Local implementation preceded GitHub issue creation; specifications and issues preceded the staged implementation publication commits.
