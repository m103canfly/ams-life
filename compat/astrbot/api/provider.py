# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Standalone stand-in; use AstrBot itself when installed."""


class ProviderRequest:
    def __init__(self, prompt='', system_prompt='', contexts=None):
        self.prompt = prompt
        self.system_prompt = system_prompt
        self.contexts = list(contexts or [])
        self.extra_user_content_parts = []


class LLMResponse:
    """As AstrBot 4.29.3 has it (provider/entities.py 447-462): with a result_chain, the text is
    read from the chain, and setting it replaces the chain's words."""

    def __init__(self, completion_text='', result_chain=None):
        self.result_chain = result_chain
        self._completion_text = completion_text

    @property
    def completion_text(self):
        if self.result_chain:
            return self.result_chain.get_plain_text()
        return self._completion_text

    @completion_text.setter
    def completion_text(self, value):
        if self.result_chain:
            from .message_components import Plain
            self.result_chain.chain = [c for c in self.result_chain.chain if not isinstance(c, Plain)]
            self.result_chain.chain.insert(0, Plain(value))
        else:
            self._completion_text = value
