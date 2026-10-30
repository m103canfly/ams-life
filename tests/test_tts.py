"""Her voice: what of a reply is spoken aloud, and what is asked of the local service.

No GPU, no service, no network here: only the text and the request body."""
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import tts  # noqa: E402


class Speakable(unittest.TestCase):
    def test_stickers_and_next_message_are_not_read_aloud(self):
        self.assertEqual(tts.speakable('[表情包:挥手] 你好【下一条】晚安'), '你好 晚安')

    def test_qq_face_is_not_read_aloud(self):
        self.assertEqual(tts.speakable('[表情:微笑] 我在呢'), '我在呢')

    def test_unknown_face_name_still_goes(self):
        self.assertIn('在', tts.speakable('[表情:这个她不会] 在'))

    def test_links_are_dropped(self):
        said = tts.speakable('看这个 https://example.com/a?b=1 好看')
        self.assertNotIn('http', said)
        self.assertIn('好看', said)

    def test_markdown_marks_are_dropped(self):
        self.assertEqual(tts.speakable('**真的**吗 # 嗯'), '真的吗 嗯')

    def test_carried_things_are_dropped(self):
        self.assertEqual(tts.speakable('[图片] 看见了'), '看见了')

    def test_lines_are_kept(self):
        self.assertEqual(tts.speakable('第一行\n\n第二行'), '第一行\n第二行')

    def test_max_chars(self):
        self.assertLessEqual(len(tts.speakable('好' * 200, 50)), 50)

    def test_cut_back_to_a_sentence_end(self):
        said = tts.speakable('啊' * 45 + '。' + '啊' * 100, 50)
        self.assertTrue(said.endswith('。'))
        self.assertLessEqual(len(said), 50)

    def test_nothing_to_say(self):
        self.assertEqual(tts.speakable(''), '')
        self.assertEqual(tts.speakable('   \n  '), '')
        self.assertEqual(tts.speakable('[表情:微笑]'), '')

    def test_none(self):
        self.assertEqual(tts.speakable(None), '')


class Payload(unittest.TestCase):
    def test_fields_the_service_reads(self):
        body = tts.payload('你好', r'G:\ref\a.wav', prompt_text='参考', prompt_lang='zh',
                           text_lang='zh', speed=0.9)
        self.assertEqual(body['text'], '你好')
        self.assertEqual(body['ref_audio_path'], r'G:\ref\a.wav')
        self.assertEqual(body['prompt_text'], '参考')
        self.assertEqual(body['prompt_lang'], 'zh')
        self.assertEqual(body['text_lang'], 'zh')
        self.assertEqual(body['speed_factor'], 0.9)
        self.assertEqual(body['media_type'], 'wav')
        self.assertFalse(body['streaming_mode'])

    def test_speed_follows_the_setting(self):
        self.assertEqual(tts.payload('a', 'r', speed=1.2)['speed_factor'], 1.2)
        self.assertEqual(tts.payload('a', 'r', speed=0)['speed_factor'], 1.0)


if __name__ == '__main__':
    unittest.main()
