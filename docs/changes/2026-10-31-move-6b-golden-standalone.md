# Move 6b: standalone golden comparison

## Purpose and changes

Share the scripted conversation and snapshots with a standalone scenario. Compare all three routes by leaf path against the reviewed differences. No plugin or golden file was changed.

The scenario now supports three paths: AstrBot with self-decision, standalone without history, and standalone with history. The report compares the golden trace to AstrBot, AstrBot to standalone without history, and standalone without history to standalone with history. It groups differing paths and leaves unknown causes open for investigation.

All three paths import the panel and aiohttp before the harness seeds unseeded random generators, so import order cannot shift the body's test seed. The AstrBot fixture now includes an At segment when a scripted turn wakes her, as a real AstrBot chain does.

The fake reply model drains background tasks before answering, matching the time available during a real network request for event archival.

## Allowed differences

The table below groups repeated list positions; the test lists the individual paths from the three-step report. Spend paths match the date format used at runtime.

- Golden to A, `asked_uncalled`: A records uncalled model requests.
- Golden to A, `sent`: the golden trace has no send record.
- Golden to A, `turns[*].inject[0]`: A adds self-decision guidance and addressed text.
- Golden to A, `files.states/attention.json.private:10001`: A records attention state.
- Golden to A, `files.states/ties.json` per person, call day, seen day, last and private: A records familiarity.
- Golden to A, `files.states/spend.json` calls, event_summary, reply, persona_compile and tom_probe: A counts enabled model calls.
- Golden to A, `page_status.data.spend` hard, left, level, soft, spent and state: A exposes spending state.
- Golden to A, each phone `recent[*].text`: A includes the At segment.
- Golden to A, archive and panel events' `appraisal.goal_relevance`, `event`, `big_summary`, `small_summary`, `source_check.length_ratio` and specific `source_texts` entries: addressed text changes event sources and their derived values.
- A to B0, `turns[*].session`: AstrBot sessions and neutral places differ.
- A to B0, each `sent` place, segment type and text: standalone records delivery.
- A to B0, each phone `umo`: only AstrBot keeps its session string.
- A to B0, `files.api_config.json.embedding` api_key, base_url, model and source: standalone configures the fake embedding provider.
- A to B0, `page_status.data.api_config.embedding` enabled, provider_id and source: the panel reports the selected provider.
- A to B0, `page_status.data.astrbot_embedding` base_url, has_key, model and provider_id: only AstrBot exposes that provider.
- A to B0, `page_status.data.llm_providers[0]` id, model and type: only AstrBot exposes its chat provider.
- A to B0, `log[0..23][1]`: AstrBot's phone-tools warning corresponds to standalone's missing speech-provider context warning; the test checks both exact messages.
- A to B0, `log[24][0..1]`: standalone reports its missing knowledge-base manager; the test checks the exact message.
- B0 to B, `files.history.sqlite3.history` each row and column: only B writes conversation history.

## Test results

- Outside the sandbox, before the date-matching test was added: `tests.test_golden` 2 OK (unchanged), `tests.test_golden_standalone` 4 OK, `tests.test_turn_runner` 9 OK, `tests.test_app` 11 OK, and `tests.test_basics` 11 OK (505 methods).
- In the sandbox after the change: `tests.test_golden` 2 OK and `PathMatching.test_spend_date_placeholder` 1 OK.

The full suite and the card's spot checks run once blocks 5 and 6 are written (the owner's rule, 10-31).

## Appendix: difference report

The three-step report records 85, 139 and 480 differing paths in basic, and 132, 139 and 480 in full. The allowed table follows those paths.
