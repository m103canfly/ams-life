# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
import json
import uuid
from urllib.parse import urlsplit

SEARCH_URL = "https://api.deepseek.com/v1/tools/search"
FETCH_URL = "https://api.deepseek.com/v1/tools/fetch"
TIMEOUT_SECONDS = 30
MAX_RESPONSE_BYTES = 8 * 1024 * 1024


class DeepSeekTools:
    def __init__(self, *, api_key, session_factory=None, timeout=TIMEOUT_SECONDS):
        if not api_key:
            raise ValueError("no key")
        self._api_key = api_key
        self._session_factory = session_factory
        self._timeout = timeout

    def __repr__(self):
        return "DeepSeekTools()"

    def _session(self):
        if self._session_factory is not None:
            return self._session_factory()
        import aiohttp
        return aiohttp.ClientSession(trust_env=False, timeout=aiohttp.ClientTimeout(total=self._timeout))

    async def _post(self, url, payload, failure):
        headers = {"Authorization": "Bearer " + self._api_key, "Content-Type": "application/json"}
        async with self._session() as session:
            async with session.post(url, json=payload, headers=headers, allow_redirects=False) as response:
                if response.status != 200:
                    raise RuntimeError(f"{failure}, status: {response.status}")
                body = bytearray()
                async for chunk in response.content.iter_chunked(65536):
                    body.extend(chunk)
                    if len(body) > MAX_RESPONSE_BYTES:
                        raise RuntimeError("DeepSeek response too large")
                return json.loads(body)

    async def search(self, query, count=10, ori_question=None, need_content=False) -> str:
        if not isinstance(query, str) or not query.strip() or len(query) > 128:
            return "Error: Invalid query."
        if type(count) is not int or not 1 <= count <= 50:
            return "Error: Invalid count."
        if ori_question is not None and (not isinstance(ori_question, str) or not 1 <= len(ori_question) <= 128):
            return "Error: Invalid ori_question."
        if not isinstance(need_content, bool):
            return "Error: Invalid need_content."
        payload = {"query": query, "count": count, "need_content": need_content}
        if ori_question is not None:
            payload["ori_question"] = ori_question
        data = await self._post(SEARCH_URL, payload, "DeepSeek web search failed")
        results = data.get("results") or []
        if not results:
            return "Error: DeepSeek web search does not return any results."
        prefix = str(uuid.uuid4())[:4]
        output = []
        for index, result in enumerate(results, 1):
            snippet = result.get("summary") or result.get("snippet") or ""
            if need_content and result.get("content"):
                snippet += "\n\n" + result["content"]
            output.append({"title": result.get("title", ""), "url": result.get("url", ""),
                           "snippet": snippet, "index": f"{prefix}.{index}"})
        return json.dumps({"results": output}, ensure_ascii=False)

    async def fetch(self, url) -> str:
        if not isinstance(url, str) or not 1 <= len(url) <= 8192 or any(c.isspace() for c in url):
            return "Error: Invalid URL."
        try:
            parts = urlsplit(url)
            valid = parts.scheme in ("http", "https") and parts.hostname and parts.username is None and parts.password is None
            parts.port
        except ValueError:
            valid = False
        if not valid:
            return "Error: Invalid URL."
        data = await self._post(FETCH_URL, {"url": url}, "DeepSeek fetch failed")
        content = data.get("content")
        if not content:
            return "Error: DeepSeek fetch does not return any content."
        return f"URL: {url}\nTitle: {data.get('title', '')}\nContent: {content}"


class BuiltinToolStandIn:
    """Stand in for the builtin tool's call(context, **kwargs) interface."""

    def __init__(self, tools, kind):
        if kind not in ("search", "read"):
            raise ValueError("invalid tool kind")
        self._tools = tools
        self._kind = kind

    async def call(self, context, **kwargs) -> str:
        if self._kind == "search":
            return await self._tools.search(**{k: kwargs[k] for k in ("query", "count", "ori_question", "need_content")
                                               if k in kwargs})
        return await self._tools.fetch(url=kwargs.get("url"))
