"""Which provider looks at pictures (step 2, 丙: the owner, 10-29: "用deepseek-flash"). AstrBot
marks what a provider takes in its config (modalities: text, image, tool_use); a chat model that
takes pictures is one that sees them. The old guess by name stays as a fallback. All ids are
made up; no network, no model.
"""
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE / 'stubs'))
import mixin_llm  # noqa: E402


class Provider:
    def __init__(self, pid, model='', modalities=None):
        self.provider_config = {'id': pid, 'model': model}
        if modalities is not None:
            self.provider_config['modalities'] = modalities


class Context:
    def __init__(self, providers, using=None, default_image=''):
        self.providers = {p.provider_config['id']: p for p in providers}
        self.using = using
        self.default_image = default_image

    def get_provider_by_id(self, pid):
        return self.providers.get(pid)

    def get_using_provider(self, umo=None):
        return self.using

    def get_config(self, umo=None):
        return {'provider_settings': {'default_image_caption_provider_id': self.default_image}}


def holder(context, override=''):
    h = type('P', (mixin_llm.LLMMixin,), {})()
    h.context = context
    h.llm_functions = {'image_caption': {'enabled': True, 'provider': override or 'follow_llm'}}
    return h


FLASH = Provider('deepseek/deepseek-flash', 'deepseek-flash', ['text', 'image', 'tool_use'])
TEXT_ONLY = Provider('some/text-model', 'text-model', ['text', 'tool_use'])
BY_NAME = Provider('my-vision', 'qwen-vl')


class SeesImages(unittest.TestCase):
    def test_modalities_decide(self):
        h = holder(Context([]))
        self.assertTrue(h._sees_images(FLASH))
        self.assertFalse(h._sees_images(TEXT_ONLY))
        self.assertTrue(h._sees_images(BY_NAME))          # the old guess by name, as a fallback

    def test_a_chat_model_that_sees_images_is_still_a_chat_model(self):
        self.assertEqual(holder(Context([]))._provider_kind(FLASH), 'chat')


class WhichOne(unittest.TestCase):
    def test_the_one_set_for_the_function(self):
        h = holder(Context([FLASH, TEXT_ONLY], using=TEXT_ONLY), override='deepseek/deepseek-flash')
        self.assertIs(h._vision_provider_for(), FLASH)

    def test_one_set_that_cannot_see_is_not_used(self):
        h = holder(Context([FLASH, TEXT_ONLY], using=TEXT_ONLY), override='some/text-model')
        self.assertIsNone(h._vision_provider_for())

    def test_astrbots_default_image_provider(self):
        h = holder(Context([FLASH, TEXT_ONLY], using=TEXT_ONLY, default_image='deepseek/deepseek-flash'))
        self.assertIs(h._vision_provider_for(), FLASH)

    def test_nothing_set_the_chat_model_when_it_sees_images(self):
        self.assertIs(holder(Context([FLASH], using=FLASH))._vision_provider_for(), FLASH)
        self.assertIsNone(holder(Context([TEXT_ONLY], using=TEXT_ONLY))._vision_provider_for())


if __name__ == '__main__':
    unittest.main()
