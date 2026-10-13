# Using the delivery archive

The delivery zip contains a `studyflow/` source directory and `studyflow-history.bundle` beside it. Extract both. Run the application directly from the source directory using README instructions; Git is not required to use the application.

To restore the genuine local Git history, run from the extracted parent directory:

```bash
git clone studyflow-history.bundle restored-studyflow
cd restored-studyflow
```

The bundle contains real local development commits; it does not establish GitHub publication or issue activity. The bundled source excludes `.git`, installed environments and private/local runtime database files.

The publication helper requires a Git checkout and authenticated `gh`. Restore the bundle first when publishing an extracted deliverable. Follow the README helper instructions, inspect dry-run output and use actual capabilities to publish. Repository and issue links are valid only after the remote operations succeed. Do not claim issue creation preceded this local implementation or backdate any event. No deadline was supplied.
