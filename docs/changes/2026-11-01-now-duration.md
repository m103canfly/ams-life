# Keep the start time of an ongoing activity

Repeated updates to the same unexpired activity keep its original start time.
An optional integer duration is clamped to 5–240 minutes. The now line shows
elapsed time and, after the estimated duration, reminds her to choose what to
do next. Existing schedule boundaries and the three-hour limit still apply.
Text cleaning and the source place remain in place; no plugin method was added.

Offline targeted tests: test_now_duration, test_set_now_clean, test_selfie,
test_daily, test_prepare_turn, test_golden and test_basics passed. The old
now-line assertions in test_selfie were updated with the owner's permission.
The golden traces were rerecorded for the now-line change. The standalone golden
test could not run in the sandbox because aiohttp is unavailable; it needs the
owner's external test environment. The full suite was not run. AstrBot-specific
work was omitted under the owner's November 1 instruction. No switches changed.
