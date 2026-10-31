# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""One NapCat (OneBot 11) message becomes an ``events.Incoming``, and it agrees with AstrBot's split.

Every number, name and link here is made up (10001, 10003, 20002, 900001). The last class builds the
AstrBot event by hand the way AstrBot 4.29.3 builds it, and compares the two Incoming objects field
by field, so moving to our own QQ layer does not change what she hears.
"""
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE / 'stubs'))

import events  # noqa: E402
import adapter_astrbot  # noqa: E402
import harness  # noqa: E402
from adapter_onebot import from_onebot  # noqa: E402
from astrbot.api.message_components import At, Face, Image, Plain, Record, Reply  # noqa: E402

ME = '20002'        # her own account, made up
GROUP = '900001'    # a group, made up
HIM = '10001'       # someone in the group, made up
OTHER = '10003'     # someone else, made up
CARD = '柠檬'
NICK = '柠檬草'


# The AstrBot component classes only a class name is read from: a forward, and the parts events.py
# keeps as "other". They stand in for AstrBot's own classes.
class _Stand:
    """A stand-in for one AstrBot component class."""

    def __init__(self, **fields):
        for key, value in fields.items():
            setattr(self, key, value)


class Forward(_Stand):
    pass


class Video(_Stand):
    pass


class File(_Stand):
    pass


class RPS(_Stand):
    pass


class Dice(_Stand):
    pass


class Shake(_Stand):
    pass


class Share(_Stand):
    pass


class Contact(_Stand):
    pass


class Location(_Stand):
    pass


class Music(_Stand):
    pass


class Poke(_Stand):
    pass


class Node(_Stand):
    pass


class Nodes(_Stand):
    pass


class Json(_Stand):
    pass


# OneBot 11 part -> the AstrBot class it keeps, as the table of the card says.
_OTHER_CLASS = {'video': Video, 'file': File, 'rps': RPS, 'dice': Dice, 'shake': Shake,
                'share': Share, 'contact': Contact, 'location': Location, 'music': Music,
                'poke': Poke, 'node': Node, 'nodes': Nodes, 'json': Json}


# The parts of a message, as NapCat sends them.

def part(kind, **data):
    """One part of an array-format OneBot 11 message."""
    return {'type': kind, 'data': dict(data)}


def message(*parts, group=GROUP, user=HIM, card=CARD, nickname=NICK, self_id=ME,
            message_id='m-7001', post_type='message'):
    """One NapCat message event as JSON: a group message, or a private one when group is None.

    group_id and user_id are numbers, as NapCat sends them; the names are made up.
    """
    sender = {'nickname': nickname, 'card': card}
    payload = {'post_type': post_type, 'message': list(parts), 'time': 1793000000, 'sender': sender}
    if group is None:
        payload['message_type'] = 'private'
    else:
        payload['message_type'] = 'group'
        payload['group_id'] = int(group)
    if self_id is not None:
        payload['self_id'] = int(self_id)
    if message_id is not None:
        payload['message_id'] = message_id
    if user is not None:
        sender['user_id'] = int(user)
        payload['user_id'] = int(user)
    return payload


def quoted_from(user):
    """What get_msg gives for the quoted message: its sender's id."""
    return {'message_type': 'group', 'sender': {'user_id': int(user)}}


# The AstrBot side, built by hand.

def _at_name(qq, names):
    """The name AstrBot finds for an @: "全体成员" for all, else the group member's name."""
    if qq == 'all':
        return '全体成员'
    return str((names or {}).get(qq, ''))


def _quoted_sender(quoted):
    """The sender of the quoted message, as AstrBot gets it from get_msg."""
    sender = (quoted or {}).get('sender') if isinstance(quoted, dict) else None
    return str((sender or {}).get('user_id', ''))


def astrbot_parts(payload, *, names=None, quoted=None):
    """The components AstrBot 4.29.3 builds from the same message, by hand.

    The rules, from astrbot/core/platform/sources/aiocqhttp/aiocqhttp_platform_adapter.py (198-425):
    a row of text parts is joined and the joined words are stripped, and a row that is empty once
    stripped adds no Plain; At carries the name looked up in the group's members (here: names);
    Reply carries the quoted id and the quoted message's sender (here: quoted, from get_msg);
    mface is skipped; a markdown is one Plain with its words as they are, not stripped and not
    joined with the text parts beside it; video, file, rps, dice, shake, share, contact, location,
    music, poke, node, nodes and json each keep their class; a part AstrBot does not know is left out.
    """
    out, run = [], []

    def flush():
        if run:
            words = ''.join(run).strip()
            run.clear()
            if words:
                out.append(Plain(words))

    for raw in payload.get('message') or []:
        if not isinstance(raw, dict) or not isinstance(raw.get('data'), dict):
            continue
        data, kind = raw['data'], raw.get('type')
        if kind == 'text':
            run.append(str(data.get('text') or ''))
            continue
        flush()
        if kind == 'at':
            qq = str(data.get('qq'))
            out.append(At(qq=qq, name=_at_name(qq, names)))
        elif kind == 'reply':
            out.append(Reply(id=str(data.get('id')), sender_id=_quoted_sender(quoted)))
        elif kind == 'image':
            out.append(Image(url=str(data.get('url') or ''), file=str(data.get('file') or '')))
        elif kind == 'record':
            out.append(Record(url=str(data.get('url') or ''), file=str(data.get('file') or '')))
        elif kind == 'face':
            out.append(Face(id=str(data.get('id'))))
        elif kind == 'forward':
            out.append(Forward(id=str(data.get('id'))))
        elif kind == 'markdown':
            out.append(Plain(str(data.get('markdown') or data.get('content') or '')))
        elif kind in _OTHER_CLASS:
            out.append(_OTHER_CLASS[kind]())
    flush()
    return out


def astrbot_message_str(payload, names):
    """AstrBot 4.29.3 aiocqhttp_platform_adapter.py 231-422 and waking_check/stage.py 79-81."""
    from itertools import groupby

    parts = [p for p in payload.get('message', [])
             if isinstance(p, dict) and isinstance(p.get('data'), dict)]
    words = ''
    for kind, group in groupby(parts, key=lambda p: p.get('type')):
        data = [p['data'] for p in group]
        if kind == 'text':
            words += ''.join(str(d.get('text') or '') for d in data).strip()
        elif kind == 'at':
            seen_self = False
            for d in data:
                qq = str(d.get('qq') or '')
                if qq == 'all':
                    continue
                if qq == str(payload.get('self_id') or '') and not seen_self:
                    seen_self = True
                else:
                    words += ' @%s(%s) ' % (_at_name(qq, names), qq)
        elif kind == 'markdown':
            words += ''.join(str(d.get('markdown') or d.get('content') or '') for d in data)
    return words.strip()


def astrbot_event(payload, *, names=None, quoted=None):
    """A harness.FakeEvent holding the same message, with AstrBot's own parts."""
    sender = payload.get('sender') if isinstance(payload.get('sender'), dict) else {}
    group = payload.get('group_id')
    user = str(sender.get('user_id', ''))
    name = str(sender.get('card') or sender.get('nickname') or '')
    ev = harness.FakeEvent('', sender=user, name=name, group=group,
                           self_id=str(payload.get('self_id', '')))
    ev.message_str = astrbot_message_str(payload, names)
    ev.unified_msg_origin = ('default:GroupMessage:%s' % group if group is not None
                             else 'default:FriendMessage:%s' % user)
    ev.message_obj = type('Obj', (), {
        'self_id': str(payload.get('self_id', '')),
        'message_id': str(payload.get('message_id', '')),
        'sender': type('Sender', (), {'user_id': user,
                                      'nickname': str(sender.get('nickname', '')),
                                      'card': str(sender.get('card') or '')})(),
    })()
    ev.is_at_or_wake_command = False   # the platform's wake check, which NapCat's event has not
    ev.get_messages = lambda: astrbot_parts(payload, names=names, quoted=quoted)
    return ev


class OneMessage(unittest.TestCase):
    """What the fields are, one case at a time."""

    def test_a_plain_message_in_a_group(self):
        one = from_onebot(message(part('text', text='你好')))
        self.assertEqual(one.place, 'group:' + GROUP)
        self.assertEqual((one.sender_id, one.sender_name), (HIM, CARD))
        self.assertEqual((one.self_id, one.message_id), (ME, 'm-7001'))
        self.assertEqual(one.segments, (events.Segment('text', {'text': '你好'}),))
        self.assertEqual(events.plain_text(one), '你好')
        self.assertFalse(one.is_private)
        self.assertFalse(one.is_self)
        self.assertEqual((one.reply_to, one.image_refs, one.at_me), ('', (), False))
        self.assertGreater(one.ts, 0)

    def test_the_card_falls_back_to_the_nickname(self):
        self.assertEqual(from_onebot(message(part('text', text='你好'), card='')).sender_name, NICK)
        payload = message(part('text', text='你好'))
        del payload['sender']['card']
        self.assertEqual(from_onebot(payload).sender_name, NICK)
        del payload['sender']['nickname']
        self.assertEqual(from_onebot(payload).sender_name, '')

    def test_a_message_in_a_private_chat(self):
        one = from_onebot(message(part('text', text='在吗'), group=None))
        self.assertEqual(one.place, 'private:' + HIM)   # AstrBot's session is the sender
        self.assertTrue(one.is_private)

    def test_an_at_of_her_wakes_her_and_the_words_lose_the_space(self):
        one = from_onebot(message(part('at', qq=ME), part('text', text=' 你好')), names={ME: '小爱'})
        self.assertTrue(one.at_me)
        self.assertEqual(events.plain_text(one), '你好')
        self.assertEqual(one.segments[0], events.Segment('at', {'qq': ME, 'name': '小爱'}))
        self.assertEqual([seg.type for seg in one.segments], ['at', 'text'])

    def test_an_at_of_someone_else_is_not_her(self):
        one = from_onebot(message(part('at', qq=OTHER), part('text', text=' 在吗')),
                          names={OTHER: '阿星'})
        self.assertFalse(one.at_me)
        self.assertEqual(one.segments[0].data, {'qq': OTHER, 'name': '阿星'})
        self.assertEqual(from_onebot(message(part('at', qq=OTHER))).segments[0].data,
                         {'qq': OTHER, 'name': ''})   # nobody looked the name up
        # the segment says a string, a member table says a number: both are the same number
        self.assertEqual(from_onebot(message(part('at', qq=OTHER)),
                                     names={int(OTHER): '阿星'}).segments[0].data['name'], '阿星')

    def test_an_at_of_all_is_everyone_and_not_her(self):
        one = from_onebot(message(part('at', qq='all'), part('text', text=' 集合')))
        self.assertFalse(one.at_me)
        self.assertEqual(one.segments[0].data, {'qq': 'all', 'name': '全体成员'})

    def test_a_row_of_texts_becomes_one(self):
        one = from_onebot(message(part('text', text='a '), part('text', text=' b'),
                                  part('text', text='')))
        self.assertEqual(one.segments, (events.Segment('text', {'text': 'a  b'}),))

    def test_a_row_of_blanks_is_no_text(self):
        self.assertEqual(from_onebot(message(part('text', text=' '), part('text', text='  ')))
                         .segments, ())

    def test_a_text_on_each_side_of_a_part_stays_two(self):
        one = from_onebot(message(part('text', text='看'), part('at', qq=OTHER),
                                  part('text', text=' 这个')))
        self.assertEqual([seg.type for seg in one.segments], ['text', 'at', 'text'])
        self.assertEqual(events.plain_text(one), '看这个')

    def test_a_quote_of_her_wakes_her(self):
        one = from_onebot(message(part('reply', id='m-7101'), part('text', text=' 嗯')),
                          quoted=quoted_from(ME))
        self.assertTrue(one.at_me)
        self.assertEqual(one.reply_to, 'm-7101')
        self.assertEqual(one.segments[0], events.Segment('reply', {'id': 'm-7101', 'sender_id': ME}))

    def test_a_quote_of_someone_else_is_not_her(self):
        one = from_onebot(message(part('reply', id='m-7102'), part('text', text=' 嗯')),
                          quoted=quoted_from(OTHER))
        self.assertFalse(one.at_me)
        self.assertEqual(one.segments[0].data, {'id': 'm-7102', 'sender_id': OTHER})

    def test_a_quote_without_the_quoted_message_keeps_the_id_only(self):
        one = from_onebot(message(part('reply', id='m-7103'), part('text', text=' 嗯')))
        self.assertFalse(one.at_me)
        self.assertEqual(one.reply_to, 'm-7103')
        self.assertEqual(one.segments[0].data, {'id': 'm-7103', 'sender_id': ''})

    def test_a_long_quoted_id_is_cut_to_eighty(self):
        one = from_onebot(message(part('reply', id='x' * 100), part('text', text=' 嗯')))
        self.assertEqual(one.reply_to, 'x' * 80)

    def test_the_images_in_order(self):
        one = from_onebot(message(part('image', url='http://img.test/a.png'), part('text', text='和'),
                                  part('image', file='b.png')))
        self.assertEqual(one.image_refs, ('http://img.test/a.png', 'b.png'))
        self.assertEqual([seg.type for seg in one.segments], ['image', 'text', 'image'])

    def test_an_image_with_a_url_and_a_file_takes_the_url(self):
        one = from_onebot(message(part('image', url='http://img.test/both.png', file='both.png')))
        self.assertEqual(one.image_refs, ('http://img.test/both.png',))

    def test_an_image_with_only_a_file_takes_the_file(self):
        self.assertEqual(from_onebot(message(part('image', file='c.png'))).image_refs, ('c.png',))

    def test_an_image_with_neither_is_no_reference(self):
        self.assertEqual(from_onebot(message(part('image'))).image_refs, ())

    def test_the_parts_of_the_plugin(self):
        one = from_onebot(message(part('face', id='14'), part('record', url='http://v.test/a.amr'),
                                  part('forward', id='m-7201'),
                                  part('markdown', markdown=' # 标题 '), part('mface'),
                                  part('video'), part('poke'), part('lightapp')))
        self.assertEqual([seg.type for seg in one.segments],
                         ['face', 'record', 'forward', 'text', 'other', 'other'])
        self.assertEqual(one.segments[0].data, {'id': '14'})
        self.assertEqual(one.segments[1].data, {'url': 'http://v.test/a.amr', 'file': ''})
        self.assertEqual(one.segments[2].data, {'id': 'm-7201'})
        self.assertEqual(one.segments[3].data, {'text': ' # 标题 '})   # as it is: no strip, no join
        self.assertEqual(one.segments[4].data, {'kind': 'Video'})
        self.assertEqual(one.segments[5].data, {'kind': 'Poke'})

    def test_a_markdown_falls_back_to_its_content(self):
        one = from_onebot(message(part('markdown', content='[一张卡片]'), part('markdown')))
        self.assertEqual([seg.data for seg in one.segments], [{'text': '[一张卡片]'}, {'text': ''}])

    def test_every_part_that_is_another(self):
        kinds = list(_OTHER_CLASS)
        one = from_onebot(message(*[part(kind) for kind in kinds]))
        self.assertEqual([seg.type for seg in one.segments], ['other'] * len(kinds))
        self.assertEqual([seg.data['kind'] for seg in one.segments],
                         [cls.__name__ for cls in _OTHER_CLASS.values()])

    def test_her_own_message_sent_by_her(self):
        one = from_onebot(message(part('text', text='好'), user=ME, card='小爱',
                                  post_type='message_sent'))
        self.assertEqual((one.sender_id, one.self_id), (ME, ME))
        self.assertTrue(one.is_self)
        self.assertFalse(from_onebot(message(part('text', text='好'),
                                             post_type='message_sent')).is_self)


class Nothing(unittest.TestCase):
    """Anything that is not one NapCat message event gives None."""

    def test_not_a_dict(self):
        for payload in (None, '你好', [], 0, ('text',)):
            self.assertIsNone(from_onebot(payload), payload)

    def test_another_post_type(self):
        for post in ('notice', 'request', 'meta_event', ''):
            self.assertIsNone(from_onebot(message(part('text', text='你好'), post_type=post)), post)
        payload = message(part('text', text='你好'))
        del payload['post_type']
        self.assertIsNone(from_onebot(payload))

    def test_another_message_type(self):
        for kind in ('guild', 'other', ''):
            payload = message(part('text', text='你好'))
            payload['message_type'] = kind
            self.assertIsNone(from_onebot(payload), kind)

    def test_a_string_message(self):
        # the string format is not read, as AstrBot does not read it either
        payload = message(part('text', text='你好'))
        payload['message'] = '你好'
        self.assertIsNone(from_onebot(payload))
        payload['message'] = {'type': 'text', 'data': {'text': '你好'}}
        self.assertIsNone(from_onebot(payload))
        del payload['message']
        self.assertIsNone(from_onebot(payload))


class Broken(unittest.TestCase):
    """A part that cannot be read is left out; nothing is raised."""

    def test_a_part_that_cannot_be_read_is_left_out(self):
        one = from_onebot(message('不是字典', {'type': 'text'}, {'type': 'text', 'data': '不是字典'},
                                  {'data': {'text': '你好'}}, part('text', text='你好')))
        self.assertEqual(one.segments, (events.Segment('text', {'text': '你好'}),))

    def test_a_broken_sender_does_not_raise(self):
        payload = message(part('text', text='在吗'), group=None)
        payload['sender'] = int(HIM)   # a number, not a sender object
        one = from_onebot(payload)
        self.assertEqual((one.sender_id, one.sender_name), (HIM, ''))   # the event's own user_id
        self.assertEqual(one.place, 'private:' + HIM)

    def test_an_event_with_nothing_readable(self):
        one = from_onebot({'post_type': 'message', 'message_type': 'group',
                           'message': [None, 1, {}, {'type': 'at'}]})
        self.assertIsNotNone(one)
        self.assertEqual((one.place, one.sender_id, one.sender_name, one.self_id, one.message_id),
                         ('group:', '', '', '', ''))
        self.assertEqual((one.segments, one.reply_to, one.image_refs, one.at_me), ((), '', (), False))
        self.assertFalse(one.is_private)
        self.assertFalse(one.is_self)


class SameAsAstrBot(unittest.TestCase):
    """The same message, split by us and by AstrBot 4.29.3: the same Incoming."""

    def check(self, payload, names=None, quoted=None, case=''):
        one = from_onebot(payload, names=names, quoted=quoted)
        self.assertIsNotNone(one, case)
        other = adapter_astrbot.from_astrbot(astrbot_event(payload, names=names, quoted=quoted))
        for field in ('place', 'sender_id', 'sender_name', 'message_id', 'self_id', 'at_me',
                      'reply_to', 'image_refs', 'text'):
            self.assertEqual(getattr(one, field), getattr(other, field), '%s: %s' % (case, field))
        self.assertEqual(events.plain_text(one), events.plain_text(other), case)
        self.assertEqual([seg.type for seg in one.segments],
                         [seg.type for seg in other.segments], case)

    def test_a_plain_message(self):
        self.check(message(part('text', text='你好')), case='plain')
        self.check(message(part('text', text='在吗'), group=None), case='private')

    def test_ats(self):
        self.check(message(part('at', qq=ME), part('text', text=' 你好')),
                   names={ME: '小爱'}, case='at her')
        self.check(message(part('at', qq=OTHER), part('text', text=' 在吗')),
                   names={OTHER: '阿星'}, case='at someone')
        self.check(message(part('at', qq='all'), part('text', text=' 集合')), case='at all')

    def test_quotes(self):
        self.check(message(part('reply', id='m-7101'), part('text', text=' 嗯')),
                   quoted=quoted_from(ME), case='quote of her')
        self.check(message(part('reply', id='m-7102'), part('text', text=' 嗯')),
                   quoted=quoted_from(OTHER), case='quote of someone')
        self.check(message(part('reply', id='m-7103'), part('text', text=' 嗯')), case='no quoted')
        self.check(message(part('reply', id='x' * 100), part('text', text=' 嗯')),
                   quoted=quoted_from(OTHER), case='long id')

    def test_images(self):
        self.check(message(part('image', url='http://img.test/a.png'), part('text', text='和'),
                           part('image', file='b.png')), case='two')
        self.check(message(part('image', url='http://img.test/both.png', file='both.png')),
                   case='url and file')
        self.check(message(part('image', file='c.png')), case='file only')

    def test_the_parts_of_the_plugin(self):
        self.check(message(part('face', id='14'), part('record', url='http://v.test/a.amr'),
                           part('forward', id='m-7201'), part('markdown', markdown=' # 标题 '),
                           part('mface'), part('video'), part('poke'), part('lightapp')),
                   case='the table')


class Standalone(unittest.TestCase):
    """The new module stands alone: it does not import AstrBot."""

    def test_no_astrbot_import(self):
        source = (ROOT / 'adapter_onebot.py').read_text('utf-8')
        for n, line in enumerate(source.splitlines(), 1):
            words = line.strip()
            if words.startswith(('import ', 'from ')):
                self.assertNotIn('astrbot', words.lower(), 'adapter_onebot.py:%d' % n)


if __name__ == '__main__':
    unittest.main()
