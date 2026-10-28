"""Made-up stand-ins for the old companion plugin's data and for an old chat log.

Same tables and columns as the real ones, so tools/import_old.py and tools/replay.py can be
tested without them. Every number, name and sentence here is invented.
"""
import json
import sqlite3
from pathlib import Path

T0 = 1_793_000_000.0
BOT = '20002'
G_BUSY, G_SMALL, G_TEST = '900001', '900002', '900009'
MANGO, LEMON, STAR, PEACH, FISH = '10001', '10002', '10003', '10004', '10005'   # STAR asked to be forgotten
NAMES = {MANGO: '芒果', LEMON: '柠檬', STAR: '阿星', PEACH: '桃子', FISH: '小鱼'}
PRIVATE_SECRET = '我下周要去外地看极光三天'
HER_PRIVATE_REPLY = '好呀，你去外地看极光要多穿点衣服哦'


def _db(path, script, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(str(path))
    db.executescript(script)
    for table, values in rows:
        for v in values:
            db.execute('INSERT INTO %s VALUES (%s)' % (table, ','.join('?' * len(v))), v)
    db.commit()
    db.close()


def build_old(root):
    """<root>/plugin_data/snow_companion/... and <root>/extra/.../notebook-forget.sqlite3."""
    snow = Path(root) / 'plugin_data' / 'snow_companion'
    gs = lambda g: 'default:GroupMessage:' + g  # noqa: E731
    tomb = ('CREATE TABLE tombstones (seq INTEGER PRIMARY KEY, kind TEXT, scope TEXT, qq TEXT, source_id TEXT, '
            'entry_id TEXT, fingerprint TEXT, stamp REAL);')
    _db(snow / 'notebook-forget.sqlite3', tomb, [('tombstones', [
        (1, 'qq', 'group:' + G_BUSY, STAR, None, None, None, T0 + 5000),
        (2, 'source', 'group:' + G_BUSY, None, '-5001', None, None, T0 + 6000),
        (3, 'source', 'group:' + G_SMALL, None, '5002', None, None, T0 + 6100),
    ])])
    _db(snow / 'ledger' / 'forget-registry.sqlite3',
        'CREATE TABLE forgotten (seq INTEGER PRIMARY KEY, scope TEXT, source_id TEXT, entry_id TEXT, stamp REAL, '
        'store_uuid TEXT); CREATE TABLE forget_cutoffs (seq INTEGER, scope TEXT, qq TEXT, cutoff REAL);',
        [('forgotten', [(1, gs(G_BUSY), None, None, T0 + 5000, None),           # bare marker next to a cutoff
                        (2, gs(G_BUSY), '-5001', None, T0 + 6000, None),        # same as the notebook's
                        (3, gs(G_BUSY), '5003', None, T0 + 6200, None),         # only here
                        (4, None, None, 'e-old', T0 + 6300, 'ab' * 16)]),       # an old archive entry: nothing to carry
         ('forget_cutoffs', [(1, gs(G_BUSY), STAR, T0 + 5000)])])
    _db(Path(root) / 'extra' / 'replay-test' / 'day1' / 'notebook-forget.sqlite3', tomb, [('tombstones', [
        (1, 'optout', 'group:' + G_TEST, LEMON, None, None, None, T0 + 100)])])

    ledger = """
    CREATE TABLE entries (id TEXT, book TEXT, group_scope TEXT, origins TEXT, visibility TEXT, subject TEXT, payload TEXT,
        label TEXT, date TEXT, event_at REAL, created REAL, expires REAL, state TEXT, retention TEXT, version INT,
        last_used REAL, last_review REAL, fingerprint TEXT);
    CREATE TABLE actors (scope TEXT, qq TEXT, name TEXT);
    CREATE TABLE sources (scope TEXT, id TEXT, qq TEXT, text TEXT, received REAL, original REAL, basis TEXT, hash TEXT,
        related TEXT, revoked INT);
    CREATE TABLE entry_sources (entry_id TEXT, scope TEXT, source_id TEXT);
    """

    def entry(eid, book, g, payload, state='active', visibility='scoped', origins=None):
        return (eid, book, gs(g) if g else None, json.dumps(origins or ([gs(g)] if g else [])), visibility, '',
                json.dumps(payload, ensure_ascii=False), '', '2026-10-04', T0 + 3000, T0 + 3000, None, state, 'short',
                1, None, None, '')
    _db(snow / 'ledger' / 'snapshot' / 'state.sqlite3', ledger, [
        ('entries', [
            entry('d1', 'day_line', G_BUSY, {'text': '⟦person:%s⟧ 和大家约了周末一起打副本' % MANGO, 'basis': 'said'}),
            entry('d2', 'day_line', G_BUSY, {'text': '群里聊了新出的角色', 'basis': 'said'}, state='expired'),
            entry('d3', 'day_line', G_BUSY, {'text': '⟦person:%s⟧ 说最近工资太低了' % LEMON, 'basis': 'said'}),  # red line
            entry('d4', 'day_line', G_BUSY, {'text': '⟦person:%s⟧ 分享了一张猫图' % STAR, 'basis': 'said'}),      # forgotten
            entry('d5', 'day_line', G_TEST, {'text': '测试群里试了几句', 'basis': 'said'}),                        # test place
            entry('h1', 'day_headline', G_SMALL, {'text': '大家一起看了流星雨', 'basis': 'said'}),
            entry('w1', 'week', G_BUSY, {'text': '这周群里很热闹', 'basis': 'said'}),
            entry('l1', 'lore', G_BUSY, {'term': '歪了', 'meaning': '抽卡没抽到想要的', 'quotes': [{'text': '又歪了'}]}),
            entry('l2', 'lore', G_BUSY, {'term': '欧皇', 'meaning': '运气好的人', 'quotes': []}, state='candidate'),
            entry('p1', 'person', G_BUSY, {'quotes': [{'text': '我最近在学吉他', 'qq': MANGO}], 'basis': 'said'}),
            entry('s1', 'self_said', G_BUSY, {'text': '早呀~', 'basis': 'said'}),
            entry('y1', 'diary', None, {'text': '今天两个群都很热闹', 'basis': 'self'}, visibility='global',
                  origins=[gs(G_BUSY), gs(G_SMALL)]),
        ]),
        ('actors', [(gs(G_BUSY), MANGO, NAMES[MANGO]), (gs(G_BUSY), LEMON, NAMES[LEMON]), (gs(G_BUSY), STAR, NAMES[STAR])]),
        ('sources', [(gs(G_BUSY), '4001', MANGO, '', T0 + 2000, T0 + 2000, '', '', '', 0),
                     (gs(G_BUSY), '4002', LEMON, '', T0 + 2100, T0 + 2100, '', '', '', 0),
                     (gs(G_BUSY), '4003', STAR, '', T0 + 2200, T0 + 2200, '', '', '', 0),
                     (gs(G_SMALL), '4004', PEACH, '', T0 + 2300, T0 + 2300, '', '', '', 0)]),
        ('entry_sources', [('d1', gs(G_BUSY), '4001'), ('d3', gs(G_BUSY), '4002'), ('d4', gs(G_BUSY), '4003'),
                           ('h1', gs(G_SMALL), '4004'), ('w1', gs(G_BUSY), '4001')]),
    ])
    _db(snow / 'notebook.sqlite3', """
    CREATE TABLE entries (id INTEGER, layer TEXT, scope TEXT, content TEXT, keywords TEXT, importance INT, state TEXT,
        origin TEXT, origin_qq TEXT, about_qq TEXT, source_ids TEXT, created REAL, updated REAL, version INT,
        corrected INT, last_hit REAL);""", [('entries', [
        (1, 'fact', 'group:' + G_SMALL, '桃子喜欢拍星空', '', 2, 'active', 'member', PEACH, PEACH, '["4004"]',
         T0 + 2400, T0 + 2400, 1, 0, None),
        (2, 'self', 'global', '我喜欢热闹的群', '', 2, 'active', 'self', '', '', '[]', T0, T0, 1, 0, None),
        (3, 'rule', 'global', '别在群里提私聊的事', '', 3, 'archived', 'master', MANGO, '', '[]', T0, T0, 1, 0, None),
        (4, 'fact', 'global', '主人在学日语', '', 2, 'active', 'master', MANGO, MANGO, '[]', T0, T0, 1, 0, None),
        (5, 'fact', 'group:' + G_BUSY, '阿星养了一只猫', '', 2, 'active', 'member', STAR, STAR, '["4003"]',
         T0 + 2200, T0 + 2200, 1, 0, None),
    ])])
    _db(snow / 'social.sqlite3', """
    CREATE TABLE items (id INTEGER, scope TEXT, kind TEXT, qq TEXT, text TEXT, reason TEXT, created REAL, expires REAL,
        delta REAL, behavior TEXT, explicit INT, revoked INT);
    CREATE TABLE evidence (item_id INTEGER, scope TEXT, source_id TEXT);""", [
        ('items', [(1, 'default:FriendMessage:' + MANGO, 'memory', MANGO, '一起聊过喜欢的歌', '', T0, None, 0, '', 0, 0)]),
        ('evidence', [(1, 'default:FriendMessage:' + MANGO, '-4100')])])
    _db(snow / 'experience.sqlite3', """
    CREATE TABLE items (id INTEGER, scope TEXT, qq TEXT, kind TEXT, text TEXT, basis TEXT, important INT, state TEXT,
        created REAL, updated REAL, expires REAL, active INT, supersedes TEXT, fingerprint TEXT);
    CREATE TABLE evidence (item_id INTEGER, scope TEXT, source_id TEXT);""", [('items', []), ('evidence', [])])
    stats = {'口头禅': ['哼哼', '工资'], '在本群的消息条数': 120}
    _db(snow / 'group_cognition.sqlite3', """
    CREATE TABLE profile (scope TEXT, content TEXT, stats TEXT, src_from TEXT, src_to TEXT, created REAL, updated REAL,
        version INT, state TEXT);
    CREATE TABLE card (scope TEXT, qq TEXT, name TEXT, content TEXT, stats TEXT, src_from TEXT, src_to TEXT,
        created REAL, updated REAL, version INT, state TEXT);
    CREATE TABLE alias (scope TEXT, qq TEXT, card TEXT, aliases TEXT, updated REAL);""", [
        ('profile', [('group:' + G_BUSY, '一个爱聊抽卡的游戏群', '{}', '2026-10-04', '2026-10-26', T0, T0, 1, 'active'),
                     ('group:' + G_TEST, '测试用的小群', '{}', '2026-10-04', '2026-10-26', T0, T0, 1, 'active')]),
        ('card', [('group:' + G_BUSY, MANGO, NAMES[MANGO], '说话很快，爱用语气词', json.dumps(stats, ensure_ascii=False),
                   '2026-10-04', '2026-10-26', T0, T0, 1, 'active'),
                  ('group:' + G_BUSY, LEMON, NAMES[LEMON], '有点烦人', '{}', '2026-10-04', '2026-10-26', T0, T0, 1,
                   'active'),
                  ('group:' + G_BUSY, STAR, NAMES[STAR], '爱发猫图', '{}', '2026-10-04', '2026-10-26', T0, T0, 1,
                   'active')]),
        ('alias', [('group:' + G_SMALL, PEACH, NAMES[PEACH], '["桃桃"]', T0)])])
    return snow


# ----------------------------------------------------------------------
# A chat log like botshepherd.db
# ----------------------------------------------------------------------
LOG_SCHEMA = """
CREATE TABLE messages (id INTEGER NOT NULL PRIMARY KEY, message_id VARCHAR(50), self_id VARCHAR(20) NOT NULL,
    user_id VARCHAR(20), group_id VARCHAR(20), message_type VARCHAR(20) NOT NULL, sub_type VARCHAR(20),
    post_type VARCHAR(20), raw_message TEXT, message_content TEXT, sender_info TEXT, timestamp BIGINT NOT NULL,
    direction VARCHAR(10) NOT NULL, connection_id VARCHAR(50), processed BOOLEAN, created_at DATETIME);
"""

# (seconds after T0, who, group or None for her private chat with MANGO, text, @her?, quoted message id, her reply)
CHAT = [
    (100, MANGO, G_BUSY, '今天抽卡又歪了', False, '', ''),
    (160, LEMON, G_BUSY, '我也是 心态崩了', False, '', ''),
    (220, STAR, G_BUSY, '我家猫今天把杯子打碎了', False, '', ''),        # forgotten (before his cutoff)
    (300, MANGO, G_BUSY, '小爱 你说下次会出货吗', True, '', '会的会的~'),
    (400, PEACH, G_SMALL, '今晚有流星雨 一起看吗', False, '', ''),
    (460, FISH, G_SMALL, '小爱 流星雨几点开始呀', True, '', '大概十点吧~'),
    (600, MANGO, None, PRIVATE_SECRET, True, '', HER_PRIVATE_REPLY),
    (700, MANGO, None, '记得别跟群里说哦', True, '', '嗯嗯，不说'),
    (5100, STAR, G_BUSY, '刚下班 好累', False, '', ''),                  # after his cutoff
    (5200, LEMON, G_BUSY, '这句后来被要求忘掉了', False, '', ''),         # forgotten message 5003 below
    (5300, MANGO, G_BUSY, '小爱 晚上好呀', True, '5003', '晚上好~'),     # quotes the forgotten one
    (5400, FISH, G_SMALL, '小爱 你去过哪里旅游吗', True, '', '我哪都去不了啦'),
    (5500, PEACH, G_BUSY, '小爱 群里最近有人要出远门吗', True, '', '不知道诶'),
]


def build_chat(path):
    rows, n = [], 0
    for sec, who, group, text, at, quoted, reply in CHAT:
        n += 1
        mid = '5003' if text == '这句后来被要求忘掉了' else str(7000 + n)
        raw = ('[CQ:reply,id=%s]' % quoted if quoted else '') + ('[CQ:at,qq=%s] ' % BOT if at and group else '') + text
        content = ('@小爱 ' if at and group else '') + text
        info = json.dumps({'user_id': int(who), 'nickname': NAMES[who], 'card': NAMES[who]}, ensure_ascii=False)
        rows.append((n, mid, BOT, who, group, 'group' if group else 'private', 'normal' if group else 'friend',
                     'message', raw, content, info, int(T0 + sec), 'RECV', 'conn', 1, '2026-10-04 00:00:00'))
        if reply:
            n += 1
            info = json.dumps({'user_id': int(BOT), 'nickname': '小爱'}, ensure_ascii=False)
            rows.append((n, str(8000 + n), BOT, None if group else who, group, 'unknown', None, 'message_sent',
                         reply, reply, info, int(T0 + sec + 5), 'RECV', 'conn', 1, '2026-10-04 00:00:00'))
    _db(path, LOG_SCHEMA, [('messages', rows)])
    return path
