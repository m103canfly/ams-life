# Photo wait before reply

The owner said: “现在不会等照片出来了再回复，缺少了等待” and asked for the reply and photo to arrive together.

When a reply queues a photo, the reply waits for the cleared photo to be made before sending. This can delay the reply by up to 150 seconds. If the photo times out, fails, or is unavailable, the words are sent alone and the photo is not sent later. Silent and held replies do not start a photo. Voice and screenshots keep their existing timing. There are no new switches or plugin methods.

AstrBot 4.29.3's OnLLMResponseEvent is called by astr_agent_hooks.on_agent_done through context_utils.call_event_hook, which directly awaits the handler without wait_for or timeout. The agent runner, internal.py, astr_main_agent.py, and scheduler.py do not wrap it in a timeout, so there is no timeout shorter than 150 seconds. This is based on the owner's source review.

The sandbox checks passed for test_photo_wait, test_selfie, test_selfie_ports, test_send_neutral, test_turn_tools, test_golden, and test_basics. The full suite was not run as instructed; the owner will run test_golden_standalone outside the sandbox. No files outside the card were intentionally changed.
