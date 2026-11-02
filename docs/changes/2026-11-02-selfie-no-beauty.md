# 2026-11-02 · selfie-no-beauty

Files: `mixin_selfie.py` (`SELFIE_PROMPT` only), `tests/test_her_look.py` (the one
assertion on the reference line), `tests/test_photo_prompts.py` (new prompt checks),
and this file.

Mango said the selfie look was still not real enough: “现在的小爱形象照还需要更真实化，现在的形象照片还不够真实”
(roughly: the xiao-ai portrait photo still needs to be more real, it is not real enough yet).

`SELFIE_PROMPT` in `mixin_selfie.py` gained one line right after the opening one. It
asks for no beauty mode, no skin smoothing and no filter, with pores and tiny skin
texture. The hair must look like real hair: frizz, loose strands and uneven
brightness. No hair ornament on the head, and no strand sticking up at the top. The
word for that stray strand is not written out, so the old guard test still passes.

The reference image no longer controls hair colour. He picked a new reference image
that already shows the dyed pink hair, so the prompt now says the hair colour is dyed
pink instead of claiming it is her original colour. Later A1 will let the hair
change. The reference still fixes the face shape, the amber eyes and their
expression, and height and build. Nothing else in `SELFIE_PROMPT` changed;
`SNAP_PROMPT` and `PHOTO_GUIDE` are untouched. The assertion for the old reference
line in `tests/test_her_look.py` was updated to the new line. New checks live in
`tests/test_photo_prompts.py`.

The change is limited to the files named on the card.

Sandbox validation: in `tests/test_photo_prompts.py` the three new prompt checks
passed, and so did the existing prompt tests. The photo path test errored only
because the sandbox denied writing to the temp folder. `tests/test_her_look.py`,
`tests/test_selfie.py` and both golden tests could not run for the same reason
(PermissionError on temp and state folders). The golden traces hold no selfie
prompt text, so they should not change. The full suite was not run.
