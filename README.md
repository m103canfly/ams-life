# ams-life

小爱（《鸣潮》爱弥斯设定）的“生命层”，以 AstrBot 插件运行。

目标是三件事：

- **只有一个她**：所有群和私聊共用一个身体（心情、几种冲动）和一份记忆；
- **记忆带出处**：她什么都记得，但私下听来的不在别处讲；没有人能用聊天里的话让她忘记，只有维护者能在面板里删，删了就真删、以后不再记；
- **她自己挑地方**：一个注意力循环决定这会儿去哪个群看、在哪开口。

> **状态：第 0 步（准备），还不能部署。** 现在仓库里的行为还和 BioCore v1.2.99 完全一样：
> 改了插件名、数据目录和链接，把一万行的 `main.py` 原样拆成了几个模块，并用录下来的对话轨迹测试保证拆分前后一字不差。

## 来源与许可

ams-life 是 [BioCore](https://github.com/Johnhmzm/astrbot_plugin_biocore)（Copyright (C) 2026 Johnhmzm）的衍生作品，
同样按 **GNU AGPL-3.0** 发布，完整条款见 [LICENSE](LICENSE)。改了什么记在 [NOTICE.md](NOTICE.md)。

AGPL 要求：把 ams-life 部署给别人用（包括群友通过 QQ 和她聊天），要能向他们提供对应的完整源码。本仓库公开就是为了满足这一点。

BioCore 原来的说明、更新日志放在 `docs/upstream/`，没有改动。

## 目录

| 路径 | 是什么 |
| --- | --- |
| `main.py` | AstrBot 插件入口：插件类、`__init__`、收消息和请求/回复钩子（没有聊天指令） |
| `common.py` | 公共部分：导入、数据目录、常量、工具函数 |
| `body.py` `homeostasis.py` | 电子幽灵的身体：心情三轴、压力、想说话、好奇、无聊、想被看见、说多了、周围热闹不热闹；只有数字，不存任何原话 |
| `mixin_phone.py` | 她的手机：每个群、每个私聊一个窗口，存这个窗口里所有人的消息和她的回复（都只留 24 小时，过期的定期从硬盘上删掉）、待办 |
| `discretion.py` `mixin_discretion.py` | 出处和分寸表：什么能在哪说；按人、按消息真删（只从面板） |
| `forget_registry.py` | 遗忘登记：谁、哪条消息她不能再记（旧账号被要求忘记的，和维护者在面板里删的），写之前都先查；面板加载整份备份时不覆盖它，恢复完按它再删一遍 |
| `atomic_file.py` | 她换文件（先写临时文件，再换过去）时，文件正被别的程序开着就等几毫秒再试，不丢这一次的写 |
| `vector_store.py` | 记忆的向量单独存一个 SQLite，按记忆 id，不再塞在记忆库的 JSON 里 |
| `redline.py` | 红线词表 |
| `impressions.py` `mixin_impressions.py` | 群友印象：每晚给每个群当天常说话的人更新称呼、说话的样子、常聊什么（不存原话，每群每晚最多调 1 次模型，默认关闭）；回话时按分寸表放进“认识的人”一行；称呼也进匿名名单（删印象、旧称呼被挤掉都还留着，删人才删）；面板里能看、能删 |
| `stickers.py` `tools/import_stickers.py` | 她的表情包（第 2 步丙块）的纯逻辑：认图片格式和大小、只从 QQ 图片服务器取、认出 QQ 标成“表情”的图、看一眼图要回的那几样和存不存、她的表情包库（30 天不用就删、最多 300 张，主人给的不删不占数、删人连他发的图一起删）、回话时挑几张候选、发成 QQ 表情时只许发到这条消息的会话、看过的图的描述记上是谁发的；导入旧小爱 118 张的工具（写进暂存文件夹）；还没接进插件 |
| `mixin_memory.py` | 向量、记忆的存储、打分、召回、巩固 |
| `mixin_events.py` | 事件档案：总结、值不值得记、去重、洞察 |
| `mixin_people.py` | 她的本子（只由她自己写，每晚写一次，每条带出处）、每个人的记录和关系 |
| `mixin_autonomy.py` | 私聊里的主动开口 |
| `mixin_llm.py` `mixin_settings.py` `mixin_media.py` `mixin_pages.py` | 模型调用、设置、图片语音、面板 |
| `brain_graph.py` `mixin_brain.py` | “她的脑子”页面的只读接口：把记忆、事件、人、窗口、本子、印象画成星和线（图里不带原话、名字、QQ 号，点开才取），每条都过遗忘登记；每次回话想起了什么（只记 id，最近 200 轮） |
| `memory_list.py` | 面板里“她记住了什么”那一页：同一份快照列成表（记忆、事件、本子、群友印象），按种类、地方、公开私下、日期、字筛，一页最多 50 条；号码先藏着，点一下才给；只读，只有记忆能删（走原来的删除接口，先确认） |
| `interpretation.py` | 回复时给模型看的几行描述（她现在怎样、她想起来的、她的本子、主人定的规矩……；不带“该怎么回”。她自己写的几行不带数字；想起来的照存下的原样，号码也在，别处来的去掉名字和号码），各种提示词 |
| `memory_meta.py` `relationship_meta.py` | BioCore 原有模块 |
| `pages/dashboard/` | 状态面板（AstrBot WebUI 里打开）；AstrBot 侧栏只进按名字排第一的页，所以它要排第一 |
| `.astrbot-plugin/i18n/` | 两页在 AstrBot 里显示的名字（“ams-life 面板”“她的脑子（单独一页）”） |
| `pages/starmap/` `tools/brain/` | “她的脑子”：她的记忆画成一个能转的星球（只读；见 `docs/brain-viz.md`）。面板里也有这一项（`pages/dashboard/brain/` 是同一份，由 `tools/brain/build.mjs` 写，`brain_frame.js` 嵌进去） |
| `tests/` | 离线测试，不连 AstrBot、不联网、不调用模型 |
| `tools/` | 离线工具：导入旧数据、回放旧聊天记录、查漏；只写到仓库外的新文件夹 |
| `docs/` | 改造计划、上游原文档 |

## 跑测试

```bash
python3 -m unittest discover -s tests
```

测试用 `tests/stubs/` 里的假 AstrBot 接口，在任何装了 Python 3.10+ 的机器上都能跑。

## 数据

插件数据在 AstrBot 的 `data/plugin_data/astrbot_plugin_ams_life/`，不在代码目录，也不进仓库。
里面有聊天整理出的记忆和对群友的印象，不要外传。
