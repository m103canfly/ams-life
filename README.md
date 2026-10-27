# ams-life

小爱（《鸣潮》爱弥斯设定）的“生命层”，以 AstrBot 插件运行。

目标是三件事：

- **只有一个她**：所有群和私聊共用一个身体（心情、几种冲动）和一份记忆；
- **记忆带出处**：她什么都记得，但私下听来的不在别处讲，群友说“忘记我”就真删；
- **她自己挑地方**：一个注意力循环决定这会儿去哪个群看、在哪开口。

> **状态：第 0 步（准备），还不能部署。** 现在仓库里基本还是 BioCore v1.2.99 的原样代码，
> 只改了插件名、数据目录和链接。改造计划见 `docs/plan.md`。

## 来源与许可

ams-life 是 [BioCore](https://github.com/Johnhmzm/astrbot_plugin_biocore)（Copyright (C) 2026 Johnhmzm）的衍生作品，
同样按 **GNU AGPL-3.0** 发布，完整条款见 [LICENSE](LICENSE)。改了什么记在 [NOTICE.md](NOTICE.md)。

AGPL 要求：把 ams-life 部署给别人用（包括群友通过 QQ 和她聊天），要能向他们提供对应的完整源码。本仓库公开就是为了满足这一点。

BioCore 原来的说明、更新日志放在 `docs/upstream/`，没有改动。

## 目录

| 路径 | 是什么 |
| --- | --- |
| `main.py` | AstrBot 插件入口（BioCore 原有，正在拆分） |
| `interpretation.py` `homeostasis.py` `memory_meta.py` `relationship_meta.py` | BioCore 原有模块 |
| `pages/dashboard/` | 状态面板（AstrBot WebUI 里打开） |
| `tests/` | 离线测试，不连 AstrBot、不联网、不调用模型 |
| `docs/` | 改造计划、上游原文档 |

## 跑测试

```bash
python3 -m unittest discover -s tests
```

测试用 `tests/stubs/` 里的假 AstrBot 接口，在任何装了 Python 3.10+ 的机器上都能跑。

## 数据

插件数据在 AstrBot 的 `data/plugin_data/astrbot_plugin_ams_life/`，不在代码目录，也不进仓库。
里面有聊天整理出的记忆和对群友的印象，不要外传。
