# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Everyday words. A name that is one of these (or a single character) is only taken for
someone's name where it plainly means a person: after an @, or as the one who says
something ("周末说", "周末：") -- never inside ordinary talk (discretion.anonymize,
impressions.masker, forget_registry.names_in)."""

WORDS = frozenset("""
今天 明天 昨天 后天 周末 早上 上午 中午 下午 晚上 半夜 现在 刚才 以后 以前 马上 一会 一起 大家 我们
你们 他们 她们 自己 别人 有人 某人 朋友 同学 老师 老板 宝贝 宝宝 哥哥 姐姐 弟弟 妹妹 小哥 小姐 兄弟
姐妹 大佬 群主 管理 哈哈 哈哈哈 嘿嘿 嘻嘻 呵呵 嗯嗯 好的 可以 不行 没有 就是 然后 所以 因为 但是
还是 知道 觉得 真的 其实 什么 这个 那个 这样 那样 怎么 为什么 你好 晚安 早安 谢谢 不客气 对不起 没事
加油 辛苦 厉害 可爱 好看 开心 快乐 难过 无聊 游戏 副本 抽卡 吃饭 睡觉 上班 下班 上学 放学 作业 考试
音乐 电影 手机 电脑 天气 下雨 晴天 春天 夏天 秋天 冬天
""".split())
