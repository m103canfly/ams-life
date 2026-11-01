# Sticker relook

Older imported and self-kept stickers can lack the newer semantic look. When the
standalone program uses stickers, an enabled background worker looks at old
stickers first, then self-kept stickers. Owner stickers are not relooked.
Sticker and image-caption settings both control the worker.

Each successful look updates the look fields and schedules a vector update;
usage, origin and saved timestamps stay intact. Pictures remain even when the
new look says not to keep them. Personal and group-meme flags prevent offering
those pictures. Failed looks leave the row unchanged; three consecutive failures
stop the worker until restart. The worker waits 20 seconds after success and
five minutes between failures.

Fresh vision requests bypass caption cache reads while retaining accounting,
cache writes and the shared vision lock. Other requests keep their existing
cache behavior. The AstrBot path is not included in the relook worker, per the
November 1 instruction.

Validation: the new relook tests, sticker vectors, sticker look v2, sticker
wiring, vision channel, golden, basics and vision neutral passed individually.
Group browse had five errors because its PictureDummy lacks _window_places;
testing stopped under the instruction for unrelated old-test failures. Real
browser and LLM-from-panel tests remain unrun. The standalone golden is run
outside the sandbox by the owner. No full suite was run. Only the files named
on the revised card were changed.
