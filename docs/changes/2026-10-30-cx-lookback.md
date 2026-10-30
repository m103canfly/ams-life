# 2026-10-30 cx-lookback: pictures just before a reply

## Why

During a group test, the owner sent a picture and addressed her a few seconds later; the reply could not see the picture. The review found that ordinary group pictures required trigger words and only pictures embedded in replies were considered.

## What changed

- Addressed group messages use their own and quoted pictures; direct chats keep the same behavior. A quote containing only an ID is fetched with `get_msg`, and only image segments are used. Fetch failures are ignored.
- Incoming pictures from other people are kept in memory by place, sender, message, address and time. A reply with no current or quoted image can look back at unseen pictures from the same sender and place. Captions identify their age, and successful looks are marked and removed from the group browsing queue and pending batches. Forgetting a person or message removes the corresponding entries.
- The existing image lock, caption cache, permission and reply accounting remain in use. The image recognition and caption switches still apply; sticker handling remains separate. `image_trigger_words` remains accepted but is no longer used to decide whether to look.
- Constants: `RECENT_IMAGE_SECONDS = 120` limits the lookback to a recent exchange; `RECENT_IMAGE_LIMIT = 10` bounds memory per place; `RECENT_IMAGE_LOOK_LIMIT = 3` bounds work per reply.
- No changes outside the card. Golden files were not updated; group-image prompts can change when an addressed message contains an image, so affected goldens may need re-recording.

## Tests

Added offline tests `test_group_addressed_image_and_empty_trigger_words`, `test_unaddressed_group_image_is_not_seen`, `test_embedded_quoted_image`, `test_quote_id_fetches_only_images`, `test_recent_image_has_age_and_is_removed_from_pending`, `test_other_sender_and_other_place_are_isolated`, `test_expired_image_is_not_seen`, `test_forget_person_and_message_remove_images`, `test_disabled_caption_preserves_unseen_image`, `test_private_success_is_not_repeated_and_failure_can_retry`, `test_recent_images_are_bounded_and_newest_first`, and `test_quote_fetch_failure_is_ignored`, and `test_lookback_increments_reply_counter`.

Python tests and mutation checks were not run in this environment. The actual local adapter quote format was not inspected under the task constraints.
