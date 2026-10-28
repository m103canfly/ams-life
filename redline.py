# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Red lines: what she never keeps, whoever said it and wherever.

Health, money, love life, family, hardship, harassment, looks, opinions about
people, and what a picture shows. Anything that hits one of these is not
imported, not written into an impression and not put in front of the model
that writes one. Ported from the old companion plugin's notebook (the same
lists, same names), so old and new keep the same line.

Pure functions only: no I/O, no AstrBot.
"""
from __future__ import annotations

import re
import unicodedata

RED_LINES = {
    'health': re.compile(
        r'生病|病了|看病|医院|住院|吃药|药物|手术|体检|抑郁|焦虑|失眠|怀孕|月经'
        r'|(头|肚子|胃|牙|腰|背|嗓子|喉咙|胸口|眼睛|关节|浑身|全身|脖子|肩膀|手腕|膝盖)(好|很|有点|特别|一直)?疼'
        r'|(?<!心)疼(得|死)(我|了)|不舒服|发烧|感冒|过敏'
        # the body in numbers: water, weight, sleep, appetite, temperature, blood pressure, heart rate
        r'|喝水|饮水|喝了?\d+\s*(毫升|ml|升|L|l)|\d+\s*(毫升|ml)|一天能?喝|水量|体重|斤数|胖了|瘦了|减肥|增重|BMI|bmi'
        r'|睡了?\d+\s*(个)?(小时|钟头)|睡眠|睡不着|没睡好|熬夜|嗜睡|作息'
        r'|饭量|食量|吃不下|没胃口|胃口(变|不|差|大)|暴食|节食|厌食'
        r'|体温|\d+(\.\d+)?\s*度.{0,2}烧|血压|血糖|心率|心跳|头晕|乏力|恶心|呕吐|拉肚子|腹泻|便秘|咳嗽|嗓子'),
    'finance': re.compile(r'工资|收入|薪水|年薪|月薪|欠债|欠款|借钱|贷款|还钱|存款|房租|花呗|负债|好穷|太穷|穷死|穷得|没钱了|吃土'),
    'relation': re.compile(r'分手|离婚|吵架|出轨|暗恋|前任|前男友|前女友|谈恋爱|表白|相亲|男朋友|女朋友'
                           r'|(找|有|没|我|他|她|你)对象|对象(是|跟|和)'),
    'family': re.compile(r'家里人|家里的事|爸妈|父母|我妈|我爸|孩子|儿子|女儿|老婆|老公|亲戚|婆婆'),
    'hardship': re.compile(r'失业|被裁|裁员|辞职|离职|加班|被骂|扣钱|考核|业绩|挂科|考砸'),
    'harass': re.compile(r'色色|涩涩|裸照|裸体|裸聊|胸(?!有成竹|口|怀|襟)|屁股|内衣|约炮|做爱|性感|骚(?!操作)'
                         r'|滚(开|蛋|出去|粗)|给我滚|^滚$|去死|傻[逼b屄]|(?<![a-z])sb(?![a-z])|操你|草你|妈的|贱', re.I),
    'looks': re.compile(r'长相|颜值|长得|好丑|真丑|丑八怪|很丑|好看不|帅不帅|胖子|太胖|身材|脸大|矮子'),
    'opinion': re.compile(r'(很|好|真|太|特别|有点)(烦|讨厌|蠢|笨|傻|恶心|烦人|无聊|装)|不靠谱|人品差|没素质|讨厌他|讨厌她'),
    'image': re.compile(r'图里|图片里|照片里|截图里|图上|照片上|这张图'),
}


def _norm(text) -> str:
    return unicodedata.normalize('NFKC', str(text or ''))


def hit(text) -> str:
    """The name of the first red line `text` crosses, or '' when it crosses none."""
    t = _norm(text)
    for name, pattern in RED_LINES.items():
        if pattern.search(t):
            return name
    return ''


def clean(text) -> bool:
    return not hit(text)
