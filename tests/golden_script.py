# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Shared scripted conversation and deterministic snapshots."""
import json

GROUP_A, GROUP_B = '900001', '900002'
TAG_JOY = '<bc>{"e":"joy","i":0.6}</bc>'
TAG_SAD = '<bc>{"e":"sadness","i":0.4,"n":"be_heard"}</bc>'

# (seconds since previous turn, event, model reply)
SCRIPT = [
    (0, dict(text='小爱早呀，今天想听你唱歌', sender='10001', name='芒果'), '早呀~ 想听哪首？' + TAG_JOY),
    (90, dict(text='就唱上次那首吧', sender='10001', name='芒果'), '好嘞，哼哼' + TAG_JOY),
    (600, dict(text='小爱 你说今天抽卡会不会歪', sender='10002', name='柠檬', group=GROUP_A), '别灰心嘛'),
    (40, dict(text='我已经歪了三次了 心态崩了', sender='10003', name='阿星', group=GROUP_A), '抱抱，下次一定出' + TAG_SAD),
    (20, dict(text='我也歪了 哈哈', sender='10005', name='路人', group=GROUP_A), None),  # does not wake her
    (40, dict(text='小爱帮我们算算保底还差多少', sender='10002', name='柠檬', group=GROUP_A), '我算算哦' + TAG_JOY),
    (3600, dict(text='小爱 晚上好', sender='10004', name='桃子', group=GROUP_B), '晚上好~'),
    (120, dict(text='最近工作好累啊', sender='10004', name='桃子', group=GROUP_B), '辛苦啦，快去歇会儿' + TAG_SAD),
    (30, dict(text='早点睡吧', sender='10006', name='小鱼', group=GROUP_B), None),  # does not wake her
    (7200, dict(text='明天要考试了 好紧张', sender='10001', name='芒果'), '你可以的！' + TAG_JOY),
    (30, dict(text='你还记得我早上让你唱什么吗', sender='10001', name='芒果'), '上次那首嘛~'),
    (86400, dict(text='小爱 我考完了', sender='10001', name='芒果'), '考得怎么样？' + TAG_JOY),
    (300, dict(text='小爱 今天群里好安静', sender='10002', name='柠檬', group=GROUP_A), '是诶，大家都去哪了'),
    (60, dict(text='小爱 你是AI吗', sender='10005', name='路人', group=GROUP_A), '是呀，按爱弥斯的设定在聊~'),
    (172800, dict(text='好久不见小爱', sender='10004', name='桃子', group=GROUP_B), '好久不见！' + TAG_JOY),
    (20, dict(text='我换工作了 现在轻松多了', sender='10004', name='桃子', group=GROUP_B), '太好了！' + TAG_JOY),
    # strong feelings: should push the core over the archive thresholds. Her replies
    # carry words of feeling too (step 1-2: the state tags are cut out and not used)
    (30, dict(text='太开心了！！！我终于抽到了！！！', sender='10002', name='柠檬', group=GROUP_A),
     '恭喜恭喜！我也好开心<bc>{"e":"joy","i":0.95}</bc>'),
    (20, dict(text='啊啊啊啊 好激动 小爱快夸我', sender='10002', name='柠檬', group=GROUP_A),
     '超厉害的！好高兴<bc>{"e":"joy","i":0.9,"x":"open"}</bc>'),
    (400, dict(text='小爱 我好难过 想哭', sender='10001', name='芒果'),
     '我在呢，听着也好难过<bc>{"e":"sadness","i":0.9,"n":"be_heard"}</bc>'),
    (20, dict(text='今天被骂了 真的很委屈', sender='10001', name='芒果'), '抱抱你，好委屈啊<bc>{"e":"sadness","i":0.85}</bc>'),
    (20, dict(text='气死我了！！！他凭什么这样说我', sender='10001', name='芒果'), '太过分了，我也生气<bc>{"e":"anger","i":0.8}</bc>'),
    (30, dict(text='真的受够了！！！气死了！！！', sender='10001', name='芒果'), '先别气坏自己<bc>{"e":"anger","i":0.9}</bc>'),
    (620, dict(text='我还是好生气！！！凭什么啊！！！', sender='10001', name='芒果'), '我陪着你，真让人生气<bc>{"e":"anger","i":0.9}</bc>'),
    (400, dict(text='小爱 我们约好下周一起打副本吧', sender='10003', name='阿星', group=GROUP_A), '好呀，说定了~'),
    (30, dict(text='记得提醒我明天交报告', sender='10003', name='阿星', group=GROUP_A), '记下啦'),
    (3600, dict(text='小爱 报告我交了', sender='10003', name='阿星', group=GROUP_A), '太好了~' + TAG_JOY),
]

FULL_CONFIG = {'llm_only_reply_summary': False, 'safety_enabled': True, 'we_memory_enabled': True,
               'proactive_autonomy': True, 'autonomy_loop_enabled': True, 'noise_seed': 7,
               'memory_worthiness_enabled': False}


def sqlite_snapshot(path):
    """A SQLite file as rows (its bytes are not stable): the memory vectors (rounded), the forget registry."""
    import sqlite3
    from array import array
    db = sqlite3.connect(str(path))
    out = {}
    for (table,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"):
        rows = []
        for row in db.execute('SELECT * FROM "%s" ORDER BY 1' % table):
            cells = []
            for cell in row:
                if isinstance(cell, bytes):
                    a = array('d')
                    a.frombytes(cell)
                    cell = [round(x, 6) for x in a]
                cells.append(cell)
            rows.append(cells)
        out[table] = rows
    db.close()
    return out


def files_snapshot(root):
    out = {}
    for path in sorted(p for p in root.rglob('*') if p.is_file()):
        rel = path.relative_to(root).as_posix()
        if path.suffix == '.sqlite3':
            out[rel] = sqlite_snapshot(path)
            continue
        text = path.read_text('utf-8', errors='replace')
        if path.suffix == '.json':
            try:
                out[rel] = json.loads(text)
                continue
            except ValueError:
                pass
        if path.suffix == '.jsonl':
            out[rel] = [json.loads(line) if line.strip().startswith('{') else line for line in text.splitlines()]
            continue
        out[rel] = text
    return out

