# 2026-10-30 cx-lookback: pictures just before a reply

## Why

During a group test, the owner sent a picture and addressed her a few seconds later; the reply could not see the picture. The review found that ordinary group pictures required trigger words and only pictures embedded in replies were considered.

## What changed

- Addressed group messages use their own and quoted pictures; direct chats keep the same behavior. A quote containing only an ID is fetched with `get_msg`, and only image segments are used. Fetch failures are ignored.
- Incoming pictures from other people are kept in memory by place, sender, message, address and time. A reply with no current or quoted image can look back at unseen pictures from the same sender and place. Captions identify their age, and successful looks are marked and removed from the group browsing queue and pending batches. Forgetting a person or message removes the corresponding entries.
- The existing image lock, caption cache, permission and reply accounting remain in use. The image recognition and caption switches still apply; sticker handling remains separate. `image_trigger_words` remains accepted but is no longer used to decide whether to look.
- Review fix: quoted pictures now pass the forget registry using the quoted sender and message ID, whether embedded or fetched; the deletion test now calls `_forget`.
- Constants: `RECENT_IMAGE_SECONDS = 120` limits the lookback to a recent exchange; `RECENT_IMAGE_LIMIT = 10` bounds memory per place; `RECENT_IMAGE_LOOK_LIMIT = 3` bounds work per reply.
- No changes outside the card. Golden files did not change: the recorded conversations contain no group message that addresses her while carrying a picture.

## Tests

Added offline tests `test_group_addressed_image_and_empty_trigger_words`, `test_unaddressed_group_image_is_not_seen`, `test_embedded_quoted_image`, `test_quote_id_fetches_only_images`, `test_recent_image_has_age_and_is_removed_from_pending`, `test_other_sender_and_other_place_are_isolated`, `test_expired_image_is_not_seen`, `test_forget_person_and_message_remove_images`, `test_disabled_caption_preserves_unseen_image`, `test_private_success_is_not_repeated_and_failure_can_retry`, `test_recent_images_are_bounded_and_newest_first`, `test_quote_fetch_failure_is_ignored`, and `test_lookback_increments_reply_counter`. The review added `test_embedded_quote_checks_forgotten_sender_and_message`, `test_fetched_quote_checks_forgotten_sender_and_message`, `test_quote_unknown_sender_still_checks_message_registry`, and `test_unreadable_registry_rejects_quoted_images`.

For the original change, the external full suite passed all 781 tests. Two external mutation checks (removing the same-sender condition and restoring the group trigger-word condition) both caused tests to fail. After the review fixes the full suite passed all 785 tests; removing the forget-registry check on quoted pictures failed four tests, and removing the `_forget_recent_images` call from `_forget` failed `test_forget_person_and_message_remove_images`. Whether the local NapCat quote carries the picture itself has not been checked on the machine yet; both shapes are handled and tested with fake events.
