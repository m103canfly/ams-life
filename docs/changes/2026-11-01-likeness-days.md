# Likeness: two days

Weekly likeness selections now include up to two recorded days, chosen with a week-specific seed. Current weeks fill missing days; saved past weeks remain unchanged. Reply selections still contain up to 20 samples. Day ratings use the existing endpoint.

Day entries retain related user IDs privately so forgetting a person removes their entries from saved selections. The panel strips those IDs, masks numbers, and anonymizes known names in details and feelings. Names absent from the existing name index cannot be identified from the day record alone. There is no new setting, route, or plugin method.

Only the Python half is included. The AstrBot-specific work is omitted under the November 1 instruction; no pages or golden files were changed.

Validation: `tests.test_likeness` (18 run, one skipped), `tests.test_her_days` (7 passed), `tests.test_golden` (2 passed), and `tests.test_basics` (11 passed). The full suite and `tests.test_golden_standalone` were not run as instructed.
