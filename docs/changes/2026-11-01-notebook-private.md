# Private notebook sittings

Private notebook prompts request lessons and feelings without names, group names or private details. Private materials accept only digest or model summaries; fallback and unknown sources are excluded, and model-event titles can fall back to raw text. Private writes anonymize names from the chat and known person records and remove long numbers. Origins remain private. Group names have no table and rely on the prompt. Group sittings retain their previous behavior.

No new switch or plugin method was added. AstrBot-specific work was omitted per the owner's November 1 instruction.

`tests/discretion_cases.py` marks the events in the notebook, notebook_full and notebook_many fixture and the notebook_readonly fixture as `digest`; no old assertions were changed. This lets those synthetic summaries enter the private sitting.

Validation, one file at a time: `tests.test_notebook_private` (4), `tests.test_body_heart` (41), `tests.test_digest` (27), `tests.test_discretion` (84), `tests.test_her_days` (7), `tests.test_golden` (2) and `tests.test_basics` (11) passed. The full suite and `tests.test_golden_standalone` were not run here, per the owner's instructions.
