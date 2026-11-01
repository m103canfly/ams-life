# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
# XiaoHeiHeSign from https://github.com/z-mio/ParseHub at commit
# 0ba8ba5890998576d5ba5156ea6ddefb70593ec5.
# Copyright (c) 2024 梓澪. MIT License; see NOTICE.md.
# The original class is retained with its standard library imports supplied here.
import asyncio
import base64
import hashlib
import json
import logging
import random
import re
import secrets
import time
from datetime import datetime
from http.cookies import SimpleCookie
from html.parser import HTMLParser
from urllib.parse import parse_qs, urlencode, urlsplit
from urllib.request import Request, build_opener

try:
    from . import atomic_file, browse, weather
    from .common import STATE_DIR
except ImportError:
    import atomic_file
    import browse
    import weather
    from common import STATE_DIR

logger = logging.getLogger('ams-life.heybox')
HOST = 'api.xiaoheihe.cn'
BASE_URL = 'https://' + HOST
LIMIT = 512 * 1024
TIMEOUT = 10
SIGN_OFFSET = 1
APP = 'heybox'
# Verify the token shape and signing settings on the first real request.
PATHS = frozenset(('/account/get_qrcode_url/', '/account/qr_state/',
                   '/bbs/app/feeds', '/bbs/app/link/tree'))
LOGIN_PATHS = frozenset(('/account/get_qrcode_url/', '/account/qr_state/'))
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0.0.0 Safari/537.36'


def read_json(path):
    try:
        value = json.loads(path.read_text(encoding='utf-8'))
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError):
        return {}


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix('.tmp')
    temp.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')
    atomic_file.replace(temp, path)


def captcha_paused(now=None):
    day = datetime.fromtimestamp(time.time() if now is None else now).date().isoformat()
    return read_json(STATE_DIR / 'heybox-status.json').get('captcha_date') == day


def handle_status(status, now=None, path=None):
    day = datetime.fromtimestamp(time.time() if now is None else now).date().isoformat()
    state_path = STATE_DIR / 'heybox-status.json'
    state = read_json(state_path)
    if status == 'show_captcha':
        state['captcha_date'] = day
    if status in ('login', 'relogin', 'lack_token'):
        state['login_required'] = True
    if path in PATHS - LOGIN_PATHS and not state.get('first_signed_ok'):
        if status not in ('ok', 'show_captcha', 'login', 'relogin', 'lack_token'):
            state['review_required'] = True
    if status != 'ok':
        logger.warning('heybox %s status: %s', path or 'status', status if status in
                       ('show_captcha', 'login', 'relogin', 'lack_token', 'failed') else 'other')
    write_json(state_path, state)
    return status == 'ok'


def request(path, params, device_id, cookies, *, get=None, now=None):
    if (path not in PATHS or captcha_paused(now)
            or (path not in LOGIN_PATHS and read_json(STATE_DIR / 'heybox-status.json').get('review_required'))):
        return None, []
    query = {'os_type': 'web', 'client_type': 'web', 'version': '999.0.4',
             'web_version': '2.5', 'x_client_type': 'web', 'x_app': 'heybox_website',
             'x_os_type': 'Windows', 'device_info': 'Chrome', 'device_id': device_id,
             'app': APP}
    query.update(params)
    if path not in LOGIN_PATHS:
        signer = XiaoHeiHeSign()
        signer._offset = SIGN_OFFSET
        query.update(signer.sign(path))
    url = BASE_URL + path + '?' + urlencode(query)
    if not browse.check_url(url)[0]:
        return None, []
    headers = {'Referer': 'https://www.xiaoheihe.cn/', 'User-Agent': USER_AGENT}
    if cookies:
        headers['Cookie'] = cookies
    req = Request(url, headers=headers, method='GET')
    try:
        with (get or build_opener(weather.NoRedirect()).open)(req, timeout=TIMEOUT) as response:
            if response.status != 200:
                handle_status('other', now, path)
                return None, []
            body = response.read(LIMIT + 1)
            if len(body) > LIMIT:
                handle_status('other', now, path)
                return None, []
            cookies_out = response.headers.get_all('Set-Cookie') or []
        data = json.loads(body)
        if isinstance(data, dict):
            status = data.get('status')
            logger.info('heybox %s status: %s', path, status if status in
                        ('ok', 'show_captcha', 'login', 'relogin', 'lack_token', 'failed') else 'other')
        if not isinstance(data, dict):
            handle_status('other', now, path)
            return None, []
        if not handle_status(data.get('status'), now, path):
            return None, []
        return data.get('result'), cookies_out
    except (OSError, ValueError, TypeError):
        handle_status('other', now, path)
        return None, []


def unseen(posts, now=None):
    now = time.time() if now is None else now
    path = STATE_DIR / 'heybox_seen.json'
    seen = {key: stamp for key, stamp in read_json(path).items()
            if isinstance(stamp, (int, float)) and 0 <= now - stamp < 7 * 86400}
    write_json(path, seen)
    return [post for post in posts if str(post.get('id') or '') not in seen][:20]


def mark_seen(ids, now=None):
    now = time.time() if now is None else now
    path = STATE_DIR / 'heybox_seen.json'
    seen = {key: stamp for key, stamp in read_json(path).items()
            if isinstance(stamp, (int, float)) and 0 <= now - stamp < 7 * 86400}
    seen.update({str(value): now for value in ids if value})
    write_json(path, seen)


def local_token(now=None, random_hex=None):
    stamp = str(int(time.time() if now is None else now))
    random_hex = random_hex or (lambda: secrets.token_hex(16))
    chunks = [stamp, random_hex(), random_hex(), random_hex()]
    return base64.b64encode(b''.join(hashlib.md5(s.encode('ascii')).digest() for s in chunks) + b'\x00').decode('ascii')


def credential(keys):
    try:
        data = json.loads(keys.get('heybox'))
        if (not isinstance(data, dict) or not isinstance(data.get('device_id'), str)
                or len(data['device_id']) != 32 or not isinstance(data.get('cookies'), dict)
                or not (data['cookies'].get('user_pkey') or data['cookies'].get('pkey'))
                or not data['cookies'].get('x_xhh_tokenid')):
            return None
        return data
    except Exception:
        return None


def cookie_values(headers):
    result = {}
    for header in headers:
        try:
            cookie = SimpleCookie()
            cookie.load(header)
            for name in ('user_pkey', 'pkey', 'user_heybox_id', 'heybox_id', 'x_xhh_tokenid'):
                if name in cookie and cookie[name].value:
                    result[name] = cookie[name].value
        except Exception:
            continue
    return result


def read_request(path, params, saved):
    cookies = saved['cookies']
    values = cookie_header(cookies)
    query = dict(params, heybox_id=str(cookies.get('heybox_id') or cookies.get('user_heybox_id') or ''))
    return request(path, query, saved['device_id'], values)[0]


def cookie_header(cookies):
    values = []
    for name in ('user_pkey', 'pkey', 'user_heybox_id', 'heybox_id', 'x_xhh_tokenid'):
        value = cookies.get(name)
        if isinstance(value, str) and value and not any(c in value for c in '\r\n;'):
            values.append(name + '=' + value)
    return '; '.join(values)


def feed_items(result):
    if isinstance(result, dict):
        result = next((result.get(key) for key in ('links', 'list', 'feeds', 'feed')
                       if isinstance(result.get(key), list)), [])
    out = []
    for row in result if isinstance(result, list) else []:
        if not isinstance(row, dict):
            continue
        row = row.get('link') if isinstance(row.get('link'), dict) else row
        ident = str(row.get('link_id') or row.get('id') or '')
        title = row.get('title')
        if re.fullmatch(r'[0-9]{1,20}', ident) and isinstance(title, str) and title.strip():
            out.append({'id': ident, 'title': title.strip()[:120]})
        if len(out) == 20:
            break
    return out


class TextOnly(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)


def text_only(value):
    if not isinstance(value, str):
        return ''
    try:
        decoded = json.loads(value)
        if isinstance(decoded, list):
            value = ' '.join(str(row.get('text') or row.get('content') or row.get('html') or '')
                             for row in decoded if isinstance(row, dict))
    except ValueError:
        pass
    parser = TextOnly()
    parser.feed(value[:20000])
    return ' '.join(' '.join(parser.parts).split())[:6000]


def post_text(result):
    link = result.get('link') if isinstance(result, dict) else None
    if not isinstance(link, dict):
        return ''
    return text_only(link.get('text', ''))


def comment_texts(result):
    if isinstance(result, dict):
        rows = next((result.get(k) for k in ('comments', 'list', 'comment_list')
                     if isinstance(result.get(k), list)), [])
    else:
        rows = []
    return [text_only(row.get('text') or row.get('content') or '') for row in rows[:20]
            if isinstance(row, dict)]


class Login:
    """A single in-memory QR attempt; only its final credentials are persisted."""
    def __init__(self, keys):
        self.keys = keys
        self.task = None
        self.state = 'idle'

    def status(self):
        if captcha_paused():
            return {'state': 'captcha'}
        if read_json(STATE_DIR / 'heybox-status.json').get('review_required'):
            return {'state': 'review_required'}
        if read_json(STATE_DIR / 'heybox-status.json').get('login_required'):
            return {'state': 'relogin'}
        if self.state == 'waiting':
            return {'state': 'waiting'}
        return {'state': 'logged_in' if credential(self.keys) else self.state}

    async def panel_status(self):
        return self.status()

    async def start(self):
        if captcha_paused():
            return {'state': 'captcha'}
        if self.task and not self.task.done():
            self.task.cancel()
        device = secrets.token_hex(16)
        token = local_token()
        result, headers = await asyncio.to_thread(request, '/account/get_qrcode_url/',
                                                  {'app': 'web', '_notip': 'true'}, device, 'x_xhh_tokenid=' + token)
        if not isinstance(result, dict):
            self.state = 'failed'
            return self.status()
        url = result.get('qr_url')
        if not isinstance(url, str) or len(url) > 2048 or urlsplit(url).scheme != 'https':
            self.state = 'failed'
            return self.status()
        qr = parse_qs(urlsplit(url).query).get('qr', [''])[0]
        if not qr or len(qr) > 512:
            self.state = 'failed'
            return self.status()
        expire = result.get('expire', 120)
        expire = max(1, min(expire, 180)) if type(expire) is int else 120
        self.state = 'waiting'
        pending = {'x_xhh_tokenid': token}
        pending.update(cookie_values(headers))
        self.task = asyncio.create_task(self.poll(qr, device, pending, expire))
        return {'state': 'waiting', 'qr_url': url, 'expire': expire}

    async def poll(self, qr, device, pending, expire):
        deadline = time.monotonic() + expire
        try:
            while time.monotonic() < deadline:
                await asyncio.sleep(3)
                if time.monotonic() >= deadline:
                    break
                if captcha_paused():
                    self.state = 'captcha'
                    return
                result, headers = await asyncio.to_thread(request, '/account/qr_state/',
                                                           {'qr': qr, 'app': 'web'}, device,
                                                           cookie_header(pending))
                pending.update(cookie_values(headers))
                if not isinstance(result, dict):
                    self.state = 'failed'
                    return
                status = result.get('error')
                if status in ('wait', 'ready'):
                    continue
                if status != 'ok':
                    self.state = 'expired' if status in ('timeout', 'expired') else 'failed'
                    return
                cookies = pending
                if not (cookies.get('user_pkey') or cookies.get('pkey')):
                    self.state = 'failed'
                    return
                if result.get('heyboxid') and not cookies.get('heybox_id'):
                    cookies['heybox_id'] = str(result['heyboxid'])
                self.keys.set('heybox', json.dumps({'device_id': device, 'cookies': cookies}, ensure_ascii=True))
                state = read_json(STATE_DIR / 'heybox-status.json')
                state.pop('login_required', None)
                write_json(STATE_DIR / 'heybox-status.json', state)
                self.state = 'logged_in'
                return
            self.state = 'expired'
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            logger.warning('heybox login failed (%s)', type(exc).__name__)
            self.state = 'failed'

    async def logout(self):
        if self.task and not self.task.done():
            self.task.cancel()
        self.keys.clear('heybox')
        state = read_json(STATE_DIR / 'heybox-status.json')
        state.pop('login_required', None)
        state.pop('review_required', None)
        state.pop('first_signed_ok', None)
        write_json(STATE_DIR / 'heybox-status.json', state)
        self.state = 'idle'
        return {'state': 'idle'}


class XiaoHeiHeSign:
    """
    小黑盒 API 签名生成器

    签名流程:
    1. 生成当前秒级时间戳 _time
    2. 生成随机 nonce（MD5(时间戳 + 随机数) 的大写形式）
    3. 根据 路径 + 时间戳 + nonce 通过 ov 算法计算 hkey
       - 三个输入分别经过字符映射后交织拼接，取前20位
       - MD5 后对头部和尾部分别做变换，拼接得到最终 hkey
    """

    # 字符映射表，用于将字符码映射为固定字符集中的字符
    CHAR_TABLE = "AB45STUVWZEFGJ6CH01D237IXYPQRKLMN89"

    # lv 对象中各 key 对应的时间戳偏移量
    # 运行时由 Wm[3] 决定使用哪个 key，当前为 "g" → offset = +1
    _OFFSET_MAP = {
        "a": -1,
        "b": -2,
        "c": -3,
        "d": -4,
        "e": -5,
        "f": 0,
        "g": +1,
        "h": +2,
        "i": +3,
        "j": +4,
        "k": +5,
    }

    def __init__(self, method_key: str = "g"):
        """
        Args:
            method_key: lv 对象的调度 key，决定时间戳偏移量，默认 "g"（即 Wm[3]）
        """
        self._offset = self._OFFSET_MAP[method_key]

    # ──────────────────── 公开接口 ────────────────────

    def sign(self, path: str) -> dict[str, str | int]:
        """
        为指定 API 路径生成签名参数

        Args:
            path: API 路径，如 "/bbs/app/link/tree"

        Returns:
            包含 hkey, _time, nonce 三个字段的字典
        """
        _time = int(time.time())

        # nonce = MD5(时间戳 + 随机小数).toUpperCase()
        nonce = hashlib.md5((str(_time) + str(random.random())).encode()).hexdigest().upper()

        hkey = self._ov(path, _time + self._offset, nonce)

        return {"hkey": hkey, "_time": _time, "nonce": nonce}

    # ──────────────────── 核心签名算法 ────────────────────

    def _ov(self, path: str, t: int, nonce: str) -> str:
        """
        核心签名计算

        Args:
            path:  标准化后的请求路径
            t:     经过偏移的时间戳
            nonce: 随机字符串
        """
        # Step 1: 路径标准化 → "/bbs/app/link/tree/"
        path = "/" + "/".join(p for p in path.split("/") if p) + "/"

        # Step 2: 对三组输入分别做字符映射
        #   - 时间戳字符串 → av 映射（映射表截掉末尾2位，长度34）
        #   - 路径          → sv 映射（映射表全量，长度36）
        #   - nonce         → sv 映射
        mapped = [
            self._av(str(t), self.CHAR_TABLE, -2),
            self._sv(path, self.CHAR_TABLE),
            self._sv(nonce, self.CHAR_TABLE),
        ]

        # Step 3: 三路交织拼接，取前 20 个字符
        interleaved = self._interleave(mapped)[:20]

        # Step 4: MD5
        md5_hex = hashlib.md5(interleaved.encode()).hexdigest()  # 32位十六进制

        # Step 5-a: 尾部 6 字符 → AES InvMixColumns → 求和 % 100
        tail_codes = [ord(c) for c in md5_hex[-6:]]
        mixed = self._mix_columns(tail_codes)
        suffix = str(sum(mixed) % 100).zfill(2)  # 补零到 2 位

        # Step 5-b: 头部 5 字符 → av 映射（映射表截掉末尾4位，长度32）
        prefix = self._av(md5_hex[:5], self.CHAR_TABLE, -4)

        return prefix + suffix  # 最终 hkey（7位字符串）

    # ──────────────────── 字符映射 ────────────────────

    @staticmethod
    def _av(text: str, table: str, cut: int) -> str:
        """
        按截断映射表替换字符

        对每个字符: table[charCode % len(截断后的table)]
        cut 为负数，表示从映射表末尾截掉 |cut| 个字符
        """
        sub_table = table[:cut]
        return "".join(sub_table[ord(c) % len(sub_table)] for c in text)

    @staticmethod
    def _sv(text: str, table: str) -> str:
        """
        按完整映射表替换字符

        对每个字符: table[charCode % len(table)]
        """
        return "".join(table[ord(c) % len(table)] for c in text)

    @staticmethod
    def _interleave(arrays: list[str]) -> str:
        """
        多路交织拼接（Round-Robin）

        依次从每个数组中取第 i 个字符拼接:
        ["ABC", "12", "XY"] → "A1X" + "B2Y" + "C" → "A1XB2YC"
        """
        result = []
        max_len = max(len(a) for a in arrays)
        for i in range(max_len):
            for a in arrays:
                if i < len(a):
                    result.append(a[i])
        return "".join(result)

    # ──────────────────── AES InvMixColumns ────────────────────
    # GF(2^8) 有限域运算，约减多项式 x^8 + x^4 + x^3 + x + 1 (0x1B)
    # 这组函数等价于 AES 的 InvMixColumns 变换矩阵乘法

    @staticmethod
    def _xtime(e: int) -> int:
        """GF(2^8) 上的 ×2 运算"""
        return (e << 1 ^ 27) & 0xFF if e & 128 else e << 1

    @classmethod
    def _mul3(cls, e: int) -> int:
        """GF(2^8) 上的 ×3 = ×2 ⊕ ×1"""
        return cls._xtime(e) ^ e

    @classmethod
    def _mul6(cls, e: int) -> int:
        """GF(2^8) 上的 ×6 = ×3(×2)"""
        return cls._mul3(cls._xtime(e))

    @classmethod
    def _mul12(cls, e: int) -> int:
        """GF(2^8) 上的 ×12 = ×6(×3(×2))"""
        return cls._mul6(cls._mul3(cls._xtime(e)))

    @classmethod
    def _mul14(cls, e: int) -> int:
        """GF(2^8) 上的 ×14 = ×12 ⊕ ×6 ⊕ ×3"""
        return cls._mul12(e) ^ cls._mul6(e) ^ cls._mul3(e)

    @classmethod
    def _mix_columns(cls, col: list[int]) -> list[int]:
        """
        AES InvMixColumns 变换

        输入: 至少 4 字节的列向量
        输出: 变换后的列向量（超出 4 个的元素原样追加）
        """
        # 确保至少有4个元素
        while len(col) < 4:
            col.append(0)

        e = col
        t = [
            cls._mul14(e[0]) ^ cls._mul12(e[1]) ^ cls._mul6(e[2]) ^ cls._mul3(e[3]),
            cls._mul3(e[0]) ^ cls._mul14(e[1]) ^ cls._mul12(e[2]) ^ cls._mul6(e[3]),
            cls._mul6(e[0]) ^ cls._mul3(e[1]) ^ cls._mul14(e[2]) ^ cls._mul12(e[3]),
            cls._mul12(e[0]) ^ cls._mul6(e[1]) ^ cls._mul3(e[2]) ^ cls._mul14(e[3]),
        ]

        # 额外元素原样追加
        if len(e) > 4:
            t.extend(e[4:])

        return t
