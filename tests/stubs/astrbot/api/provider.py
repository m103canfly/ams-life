"""astrbot.api.provider stand-in."""


class ProviderRequest:
    def __init__(self, prompt='', system_prompt='', contexts=None):
        self.prompt = prompt
        self.system_prompt = system_prompt
        self.contexts = list(contexts or [])
        self.extra_user_content_parts = []


class LLMResponse:
    def __init__(self, completion_text='', result_chain=None):
        self.completion_text = completion_text
        self.result_chain = result_chain
