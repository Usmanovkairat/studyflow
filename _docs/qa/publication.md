# Independent QA — fresh public checkout

Verdict: **PASS** for published commit `54a1a70f05e9f8a2833c6003a79f714d99fb0f2f`.

Actual commands executed:

- `git clone https://github.com/Usmanovkairat/studyflow.git /tmp/studyflow-publication-qa` — succeeded.
- `git checkout 54a1a70f05e9f8a2833c6003a79f714d99fb0f2f` — checkout succeeded; message Publish verified Export filtered CSV and verify delivery (refs #6).
- `python -m pytest -q` in fresh clone — **99 passed in0.96s**.
- `python -m pip check` — No broken requirements found.
- `python scripts/demo.py` — creates3courses/5assignments in empty clone; second invocation refuses existing records. Subsequent factory verifies counts3/5 persisted.
- `python -m flask --app studyflow routes` — all13expected endpoints load (dashboard, courses, tasks, export and static).
- `python -m venv /tmp/studyflow-publication-venv` followed by its `python -m pip install -r requirements.txt` — clean environment successfully installs exact Flask3.1.3/pytest9.1.1 plus dependencies, using cached wheels and downloading packaging26.3.

Independent byte comparison of22app/template/style/test/requirements files in public checkout versus original verified workspace: every byte identical. Prior desktop1440/mobile390 Chromium150 workflows, screenshot assessment and security/CSV QA therefore apply to the same published application source. No app changes or external writes performed by QA. Issue closing and repository documentation publication status are handled separately by orchestrator; no claim of remote issue closure made here.

Clean-venv final run: `/tmp/studyflow-publication-venv/bin/python -m pytest -q` → **99 passed in0.89s**; its pip check reports no broken requirements. Fresh factory reads persisted demo3courses/5tasks; `/`, `/courses`, `/tasks`, `/tasks/export.csv` each200. This also resolves the earlier bootstrap report's fresh-install verification limitation.
