# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
import importlib.util
import json
import re
import unittest
from pathlib import Path
from unittest.mock import patch

import browse
import deepseek_tools as ds

KEY = 'made-up-key'


class Response:
    def __init__(self, data=None, status=200, body=None):
        self.status = status
        self.body = body if body is not None else json.dumps(data or {}).encode()
        self.content = self

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    async def iter_chunked(self, size):
        for i in range(0, len(self.body), size):
            yield self.body[i:i + size]


class Session:
    def __init__(self, response):
        self.response = response
        self.calls = []

    async def __aenter__(self):
        return self

    async def __aexit__(self, *args):
        pass

    def post(self, url, **kwargs):
        self.calls.append((url, kwargs))
        return self.response


class DeepSeekToolsTest(unittest.IsolatedAsyncioTestCase):
    def make_tools(self, data=None, status=200, body=None):
        session = Session(Response(data, status, body))
        return ds.DeepSeekTools(api_key=KEY, session_factory=lambda: session), session

    async def test_key_and_repr(self):
        with self.assertRaisesRegex(ValueError, '^no key$'):
            ds.DeepSeekTools(api_key='')
        tools, _ = self.make_tools()
        self.assertNotIn(KEY, repr(tools))

    async def test_search_validation(self):
        tools, session = self.make_tools()
        cases = [dict(query='  '), dict(query='x' * 129), dict(query='x', count=0),
                 dict(query='x', count=51), dict(query='x', count=True), dict(query='x', count='3'),
                 dict(query='x', ori_question=''), dict(query='x', ori_question='x' * 129),
                 dict(query='x', need_content='yes')]
        for case in cases:
            with self.subTest(case=case):
                self.assertTrue((await tools.search(**case)).startswith('Error: '))
        self.assertEqual(session.calls, [])

    async def test_search_request(self):
        tools, session = self.make_tools({'results': []})
        await tools.search('query', 5)
        url, options = session.calls[0]
        self.assertEqual(url, ds.SEARCH_URL)
        self.assertEqual(options['headers'], {'Authorization': 'Bearer ' + KEY, 'Content-Type': 'application/json'})
        self.assertEqual(options['json'], {'query': 'query', 'count': 5, 'need_content': False})
        await tools.search('query', ori_question='question', need_content=True)
        self.assertEqual(session.calls[1][1]['json']['ori_question'], 'question')
        self.assertTrue(session.calls[1][1]['json']['need_content'])

    async def test_search_results_and_empty(self):
        data = {'results': [{'title': 'A', 'url': 'https://example.org/a', 'summary': 'short', 'content': 'full'},
                            {'title': 'B', 'url': 'https://example.org/b', 'snippet': 'other'},
                            {'title': 'C', 'url': 'https://example.org/c'}]}
        tools, _ = self.make_tools(data)
        results = json.loads(await tools.search('x', need_content=True))['results']
        self.assertEqual([set(x) for x in results], [{'title', 'url', 'snippet', 'index'}] * 3)
        self.assertEqual([x['snippet'] for x in results], ['short\n\nfull', 'other', ''])
        prefix = results[0]['index'][:4]
        self.assertRegex(prefix, r'^[0-9a-f]{4}$')
        self.assertEqual([x['index'] for x in results], [f'{prefix}.{n}' for n in (1, 2, 3)])
        empty, _ = self.make_tools({'results': []})
        self.assertEqual(await empty.search('x'), 'Error: DeepSeek web search does not return any results.')

    async def test_browse_parser_compatibility(self):
        data = {'results': [{'title': 'A', 'url': 'https://example.org/a', 'summary': 'short'}]}
        tools, _ = self.make_tools(data)
        actual = json.loads(await tools.search('x'))['results']
        expected = json.loads(json.dumps({'results': [{'title': 'A', 'url': 'https://example.org/a',
                                                       'snippet': 'short', 'index': 'abcd.1'}]}))['results']
        self.assertEqual(browse.search_results(actual), browse.search_results(expected))

    async def test_fetch_validation_and_result(self):
        tools, session = self.make_tools({'title': 'A', 'content': 'text'})
        for url in ('ftp://example.org', 'http://user:pw@x', 'https://example.org/a b',
                    'https://example.org:bad', 'x' * 8193):
            with self.subTest(url=url[:40]):
                self.assertTrue((await tools.fetch(url)).startswith('Error: '))
        self.assertEqual(session.calls, [])
        url = 'https://example.org/a'
        self.assertEqual(await tools.fetch(url), f'URL: {url}\nTitle: A\nContent: text')
        self.assertEqual(session.calls[0][0], ds.FETCH_URL)
        self.assertEqual(session.calls[0][1]['json'], {'url': url})
        self.assertEqual(session.calls[0][1]['headers']['Authorization'], 'Bearer ' + KEY)
        empty, _ = self.make_tools({'title': 'A'})
        self.assertEqual(await empty.fetch(url), 'Error: DeepSeek fetch does not return any content.')

    async def test_status_hides_body_and_key(self):
        for kind in ('search', 'fetch'):
            tools, _ = self.make_tools(status=500, body=b'secret response')
            with self.subTest(kind=kind), self.assertRaises(RuntimeError) as caught:
                await (tools.search('x') if kind == 'search' else tools.fetch('https://example.org'))
            message = str(caught.exception)
            self.assertIn('500', message)
            self.assertNotIn('secret response', message)
            self.assertNotIn(KEY, message)

    async def test_response_size_limit(self):
        tools, _ = self.make_tools(body=b'x' * (ds.MAX_RESPONSE_BYTES + 1))
        with self.assertRaises(RuntimeError):
            await tools.search('x')
        with self.assertRaises(RuntimeError):
            await tools.fetch('https://example.org')

    async def test_stand_in_filters_arguments(self):
        tools, _ = self.make_tools({'results': [{'title': 'A', 'url': 'https://example.org', 'snippet': 'x'}]})
        with patch.object(ds.uuid, 'uuid4', return_value='abcd-fixed'):
            self.assertEqual(await ds.BuiltinToolStandIn(tools, 'search').call(None, query='x', count=5, extra=1),
                             await tools.search('x', 5))
        tools, _ = self.make_tools({'title': 'A', 'content': 'text'})
        self.assertEqual(await ds.BuiltinToolStandIn(tools, 'read').call(None, url='https://example.org', extra=1),
                         await tools.fetch('https://example.org'))

    @unittest.skipUnless(importlib.util.find_spec('aiohttp'), 'aiohttp unavailable')
    async def test_default_session_does_not_trust_environment(self):
        import aiohttp
        real_factory = aiohttp.ClientSession
        seen = []
        fake = Session(Response({'results': []}))

        def factory(**kwargs):
            real = real_factory(**kwargs)
            seen.append(real.trust_env)
            return real

        with patch.object(aiohttp, 'ClientSession', side_effect=factory):
            tools = ds.DeepSeekTools(api_key=KEY)
            # Create the real session but replace post before any request can be sent.
            async with tools._session() as session:
                self.assertFalse(session.trust_env)
        self.assertEqual(seen, [False])

    def test_source_has_fixed_urls_and_no_astrbot_or_logging(self):
        source = Path(ds.__file__).read_text(encoding='utf-8')
        self.assertIn('https://api.deepseek.com/v1/tools/search', source)
        self.assertIn('https://api.deepseek.com/v1/tools/fetch', source)
        self.assertNotRegex(source, r'(?m)^\s*(?:from|import)\s+(?:astrbot|logging)\b')
