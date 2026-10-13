# Delivery checklist — actual progress

Updated from available implementation and independent QA evidence. Local success does not establish remote publication.

- [x] Article and example issue analyzed; methodology mapping in `methodology.md`.
- [x] Original application selected and honest decision log written in `../chat-brainstorm.md`.
- [x] Product plan, architecture, process, roles and six detailed issue specifications prepared before implementation.
- [x] Issue 01 bootstrap independently accepted after fix commit `cb4c14c`; `qa/01.md` records 6 passing tests and resolved validation defects.
- [x] Issue 02 courses independently accepted after Unicode uniqueness fix `af0ca1f`; `qa/02.md` records 18 passing tests.
- [x] Issue 03 task CRUD independently accepted at `897e327`; `qa/03.md` records 35 passing tests and request/database/restart checks.
- [x] Issue 04 search and filters independently accepted at `eb14ba0`; `qa/04.md` records 45 passing tests and independent combined-filter/Unicode-search checks.
- [x] Issue 05 dashboard: independent functional and actual Chromium 150 browser checks PASS at desktop 1440×1000 and mobile 390×844; `qa/05.md` records complete evidence.
- [x] Issue 06 CSV and final delivery independently accepted at `f92ad8d`; QA commit `934bd46` records 99 passing tests, 195 control-prefix checks and 65 real CSV rows.
- [x] Full final regression: 99 tests passed in 0.87s; complete desktop/mobile browser workflows passed.
- [x] Final README and independently verified demo, backup and publication dry-run instructions.
- [x] Public GitHub repository created and source published: https://github.com/Usmanovkairat/studyflow.
- [x] Six actual GitHub issues created, linked to feature-publication commits and QA PASS comments, and closed as completed after acceptance.
- [x] Submission repository URL and published files verified.

## Publication and deadline evidence
The user authorized browser repository creation and completed sign-in. Six real GitHub issues were created with current timestamps; six feature-publication commits reference them. Fresh public clone and clean virtual environment both pass 99 tests. See `publication.md` for actual event data and the conservative inferred deadline (13:30 local on 2026-10-13). All six issues closed at 12:22–12:23 local, before the conservative inferred 13:30 cutoff; states and timestamps were re-fetched and verified. The embedded video was unavailable; no video review is claimed.

## Evidence links
See [task ledger](tasks.md), [bootstrap QA](qa/01.md), [course QA](qa/02.md), [task QA](qa/03.md), [filter QA](qa/04.md), [methodology](methodology.md) and the Git history for actual local progress. Final test totals must be updated from the final executed run, not accumulated from earlier stage counts.

## Methodology sequencing limitation
Specifications were completed before local implementation, and PM/engineer/independent QA stages are evidenced. Actual GitHub issues were not created before implementation. Publishing after completion cannot retrospectively satisfy the article/assignment create-before-implement remote issue sequence or fabricate an earlier issue history. Remote publication is now real and verified. Issue closure and deadline comparison are recorded from actual re-fetched GitHub states. GitHub Actions Tests run 2 succeeded.

- [x] Actual GitHub Actions run 38362143761 completed successfully; dependency installation and pytest job succeeded.
