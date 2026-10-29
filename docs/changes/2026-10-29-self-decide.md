# 2026-10-29 self-decide: she decides herself whether to answer (step 2, 甲)

The setting `self_decide` is off by default. With it off nothing changes: AstrBot decides as before, and the goldens are unchanged. The plan is the design card's sections 2–4 and 7, with the owner's decisions 1–4 and 27, and 熟不熟 (by the dealings; the owner always the closest).

## What

- **`attention.py`** (pure functions):
  - Called: an @ of her, a quote, her name; every private message; and someone taking up what she just said (she spoke in this window within 3 minutes, to him).
  - Night (01:00–08:25): called once, she sleeps on. Called 3 times within 10 minutes, she is woken and answers until nobody calls her for 20 minutes. She never speaks up herself at night.
  - Familiarity, 0..1, by the dealings: days they talked (the last 30 weigh most), times he called her, a private chat. The owner (`owner_qq`) is always 1.
  - Score of a message she was not called by. It goes up with the topic (cosine with what she keeps), people she knows and how long she has been quiet here. It goes down with how much she said here lately and with a quarrel. The three levels' thresholds: less 0.55, normal 0.45, more 0.35.
  - Safety nets:
    - about 30 of her messages an hour in one group;
    - the money of the day: 10 yuan; from 8 yuan only the owner's private chat; over 10 nothing.
  - Cost of a call from its tokens; prices are in the config (yuan a million tokens).
  - What she sends: `【不说】`, QQ faces (`[表情:名字]`, a short list of names), several messages split at `【下一条】` (at most 5; what is beyond goes into the last), and a typing pause of 1–3 seconds.
- **`mixin_attention.py`**, the plugin around those rules:
  - **`on_message_decide`** (new handler in `main.py`, after `on_message` has kept the message):
    1. called?
    2. at night;
    3. wait a few seconds (group 6, called 2, private 3): when more comes in meanwhile, this one is not judged (it was kept all the same); the last one carries "called" on;
    4. the safety nets;
    5. then:
       - called: AstrBot answers as before, or, when the last message did not wake AstrBot, the plugin asks for a reply (`request_llm` in the current conversation: her persona and the history, saved back);
       - not called: a score over the level's threshold asks too.
  - Reply prompt: one more line `[她可以]` says what she may pick. It describes; it does not order.
  - **`on_llm_response`**:
    - `【不说】`: nothing sent, nothing kept.
    - Several messages: the first is sent by AstrBot (a face alone as a chain); the rest go to the same chat by `context.send_message`, with a pause before each. What she keeps is the messages, one a line.
    - Her messages of the hour are counted per group.
  - Money: every reply, every second try of the send check, and every model call the plugin makes itself (wrapped where the provider is picked) goes into `states/spend.json` by kind, in yuan. Tokens come from DeepSeek's own cache numbers when the raw answer has them, else AstrBot's; with neither, every input token counts as not cached.
  - The dealings in `states/ties.json`; each window's night calls and her messages of the hour in `states/attention.json`. Numbers only.
- **Panel**: "今天调模型花了约 … 元，还剩 … 元", shown only with the switch on.
- **Settings**: `self_decide`, `attention_level`, `owner_qq` (only on this computer), `day_budget_yuan`, `day_budget_soft_yuan`, `price_input_miss` / `price_input_hit` / `price_output` (deepseek-flash at its peak price, 7.2 yuan a dollar: 2.2 / 0.05 / 8.7; to be checked against DeepSeek's page on install), `group_hour_max`, `night_start`, `night_end`.
- **`tools/replay.py --judge-only`**: no model at all.
  - Every message is judged as `self_decide` would: a stretch by its last message, called or not, and the score against the three levels.
  - Her old replies go into her phone as she said them.
  - `judge.json`: per window and day, and each group's average a day — the numbers the owner picks a level by.

## Not here (乙, its own PR)

These come in 乙's PR:
- what she hears moving her mood;
- being praised, told off, woken up, a quarrel, someone taking up her words;
- being left unanswered, by familiarity;
- `body_brief`'s new words;
- the threshold moving with her mood.

`_woken_at` is noted here for it.

## New modules (for the README's table)

| File | What |
| --- | --- |
| `attention.py` `mixin_attention.py` | 第 2 步甲块（`self_decide` 打开时）：她自己判断回不回——叫到她一定问模型、没叫她的程序打分过门槛才问；先等几秒只看最后一条；夜里一直叫才醒；一个群一小时约 30 句、每天花费上限两道安全网；她可以不说、回 QQ 小表情、分几条发；每次调模型记花费，面板上能看 |

## Files

`attention.py` (new), `mixin_attention.py` (new), `main.py`, `mixin_llm.py` (counting the plugin's own calls), `mixin_send_check.py` (the second try counted), `mixin_pages.py`, `pages/dashboard/index.html`, `pages/dashboard/app.js`, `_conf_schema.json`, `tools/replay.py`, `tests/test_attention.py`, `tests/attention_cases.py` (new), `tests/test_replay_tools.py` (`JudgeOnly`), `tests/test_basics.py`, `tests/stubs/astrbot/api/message_components.py` (`Face`).
