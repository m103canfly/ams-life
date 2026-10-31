# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""A DeepSeek chat client using the OpenAI SDK."""
from urllib.parse import urlsplit

try:
    from . import browse, model_client
except ImportError:
    import browse
    import model_client


BASE_URL = 'https://api.deepseek.com'
TIMEOUT_SECONDS = 60
MAX_RETRIES = 1


class DeepSeekModel(model_client.ModelClient):
    def __init__(self, *, api_key, model, client=None, base_url=BASE_URL,
                 timeout=TIMEOUT_SECONDS, max_retries=MAX_RETRIES):
        if not api_key:
            raise ValueError('no key')
        try:
            url = urlsplit(base_url)
            valid = (url.scheme == 'https' and url.netloc == 'api.deepseek.com'
                     and not url.query and not url.fragment)
        except (ValueError, TypeError):
            valid = False
        if not valid:
            raise ValueError('invalid DeepSeek base URL')
        self.model = model
        self.base_url = base_url
        if client is None:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=api_key, base_url=base_url, timeout=timeout,
                                 max_retries=max_retries)
        self._client = client

    def __repr__(self):
        return f'DeepSeekModel(model={self.model!r}, base_url={self.base_url!r})'

    async def chat(self, *, prompt=None, system=None, messages=None, images=None, tools=None):
        if images:
            raise ValueError('DeepSeek chat does not take images')
        sent = []
        if system is not None:
            sent.append({'role': 'system', 'content': system})
        sent.extend(dict(message) for message in (messages or ()))
        if prompt is not None:
            sent.append({'role': 'user', 'content': prompt})
        options = {}
        if tools:
            options['tools'] = [{'type': 'function', 'function': {
                'name': tool.name, 'description': tool.description, 'parameters': tool.parameters}}
                for tool in tools]
        response = await self._client.chat.completions.create(model=self.model, messages=sent,
                                                               **options)
        choices = getattr(response, 'choices', None) or ()
        message = getattr(choices[0], 'message', None) if choices else None
        text = getattr(message, 'content', None) or ''
        calls = []
        for index, call in enumerate(getattr(message, 'tool_calls', None) or ()):
            function = getattr(call, 'function', None)
            name = getattr(function, 'name', None)
            if name:
                calls.append(model_client.ToolCall(getattr(call, 'id', None) or f'call_{index}',
                                                   name, model_client.arguments_of(
                                                       getattr(function, 'arguments', None))))
        extra = getattr(message, 'model_extra', None) or {}
        reasoning = getattr(message, 'reasoning_content', None) or extra.get('reasoning_content') or ''
        usage = getattr(response, 'usage', None)
        if usage is not None:
            dump = getattr(usage, 'model_dump', None)
            if callable(dump):
                usage = dump()
            elif not isinstance(usage, dict):
                keys = ('input_other', 'input_cached', 'output', 'prompt_tokens',
                        'completion_tokens', 'prompt_cache_hit_tokens', 'prompt_cache_miss_tokens',
                        'cached_tokens')
                usage = {key: getattr(usage, key, None) for key in keys}
        return model_client.ModelReply(text=text, tool_calls=tuple(calls),
                                       usage=browse.usage_of(usage), reasoning=reasoning)
