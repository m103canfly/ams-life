# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Offline weather retrieval, scheduling and turn checks."""
import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_basics  # noqa: E402,F401

import app_config
import harness
import her
import mixin_autonomy
import mixin_turn
import turn
import weather


def payload():
    return {'daily': {'time': [datetime.now(weather.ZONE).date().isoformat()],
                      'weather_code': [61], 'temperature_2m_max': [22],
                      'temperature_2m_min': [15], 'precipitation_probability_max': [20]}}


def response(data, status=200):
    reply = Mock()
    reply.status = status
    reply.read.return_value = data
    reply.__enter__ = Mock(return_value=reply)
    reply.__exit__ = Mock(return_value=False)
    return reply


class FetchTests(unittest.TestCase):
    def test_fetch_request_and_daily_values(self):
        reply = response(json.dumps(payload()).encode())
        get = Mock(return_value=reply)
        result = weather.fetch(0.0, 0.0, get=get)
        request = get.call_args.args[0]
        url = urlparse(request.full_url)
        self.assertEqual((url.scheme, url.netloc, url.path), ('https', 'api.open-meteo.com', '/v1/forecast'))
        self.assertEqual(request.get_method(), 'GET')
        self.assertEqual(get.call_args.kwargs, {'timeout': 5})
        self.assertEqual(parse_qs(url.query)['forecast_days'], ['1'])
        self.assertEqual(parse_qs(url.query)['timezone'], ['Asia/Shanghai'])
        self.assertEqual(reply.read.call_args.args, (65536,))
        self.assertEqual({k: result[k] for k in ('code', 'max', 'min', 'rain')},
                         {'code': 61, 'max': 22, 'min': 15, 'rain': 20})

    def test_fetch_failures_and_redirect(self):
        for reply in (response(b'bad'), response(b'{}'), response(b'x' * 65537), response(b'{}', 503)):
            with self.subTest(reply=reply), self.assertRaises((ValueError, KeyError)):
                weather.fetch(0, 0, get=Mock(return_value=reply))
        with self.assertRaises(TimeoutError):
            weather.fetch(0, 0, get=Mock(side_effect=TimeoutError))
        self.assertIsNone(weather.NoRedirect().redirect_request(None, None, 302, '', {}, 'https://example.invalid'))

    def test_describe_and_line(self):
        self.assertEqual([weather.describe(x) for x in (85, 86)], ['阵雪', '阵雪'])
        self.assertEqual([weather.describe(x) for x in (0, 61, 95, 999)], ['晴', '小雨', '雷雨', ''])
        self.assertEqual(weather.line({'code': 61, 'min': 15, 'max': 22, 'rain': 20}, '示例城'),
                         '天气：示例城 小雨 15–22℃，降水 20%')


class WeatherTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.path = self.root / 'weather.json'
        self.config = {'weather_lat': 0.0, 'weather_lon': 0.0, 'weather_place': '示例城'}
        self.logger = Mock()
        self.now = datetime.now(weather.ZONE).replace(hour=1, minute=0, second=0, microsecond=0)

    async def test_default_config_round_trip_and_float_validation(self):
        schema = app_config.load_schema()
        config = app_config.defaults(schema)
        path = self.root / 'config.json'
        app_config.save(path, config, schema)
        loaded, problems = app_config.load(path, schema)
        self.assertEqual(problems, [])
        self.assertEqual(loaded, config)
        self.assertIsNone(loaded['weather_lat'])
        self.assertIsNone(loaded['weather_lon'])
        config['weather_lat'] = 0
        app_config.save(path, config, schema)
        self.assertEqual(app_config.load(path, schema)[0]['weather_lat'], 0.0)
        config['phone_photo_price'] = None
        with self.assertRaises(app_config.ConfigError):
            app_config.save(path, config, schema)

    async def test_empty_configuration_never_fetches(self):
        fetcher = Mock()
        for config in ({}, {'weather_lat': 0.0}, {'weather_lon': 0.0}):
            await weather.tick(config, self.path, self.logger, now=self.now, fetcher=fetcher)
        fetcher.assert_not_called()
        self.assertFalse(self.path.exists())

    async def test_today_yesterday_and_private_cache(self):
        data = {'date': self.now.date().isoformat(), 'code': 0, 'max': 22, 'min': 15, 'rain': 20}
        fetcher = Mock(return_value=data)
        weather.write(self.path, data)
        await weather.tick(self.config, self.path, self.logger, now=self.now, fetcher=fetcher)
        fetcher.assert_not_called()
        weather.write(self.path, dict(data, date=(self.now - timedelta(days=1)).date().isoformat()))
        await weather.tick(self.config, self.path, self.logger, now=self.now, fetcher=fetcher)
        self.assertEqual(fetcher.call_count, 1)
        self.assertEqual(set(weather.read(self.path)), {'date', 'fetched', 'code', 'max', 'min', 'rain'})
        self.assertNotIn('示例城', self.path.read_text(encoding='utf-8'))

    async def test_failure_retry_cap_and_restart(self):
        fetcher = Mock(side_effect=TimeoutError('private detail'))
        for hours in (0, 1, 3, 6, 9):
            await weather.tick(self.config, self.path, self.logger, now=self.now + timedelta(hours=hours), fetcher=fetcher)
        self.assertEqual(fetcher.call_count, 3)
        self.assertEqual(self.logger.warning.call_count, 3)
        self.assertEqual(self.logger.warning.call_args.args[-1], 'TimeoutError')
        self.assertFalse(self.path.exists())
        self.assertEqual(set(weather.read(self.root / 'weather-attempts.json')), {'date', 'count', 'last'})

    async def test_enabled_background_loop_runs_without_other_switches(self):
        plugin = her.Her(harness.FakeContext(), config=dict(self.config, photo_enabled=False))
        test_basics.PLUGINS.append(plugin)
        self.assertIsNotNone(plugin._autonomy_task)
        plugin._autonomy_task.cancel()
        plugin.proactive_autonomy = False
        plugin.autonomy_loop_enabled = False
        calls = 0

        async def sleep(_seconds):
            nonlocal calls
            calls += 1
            if calls == 2:
                plugin.enabled = False

        with patch.object(mixin_autonomy.asyncio, 'sleep', side_effect=sleep), \
             patch.object(weather, 'tick', new_callable=AsyncMock) as tick:
            await plugin._autonomy_loop()
        tick.assert_awaited_once()
        self.assertEqual(tick.await_args.args[0]['weather_lat'], 0.0)

    async def test_weather_failure_does_not_stop_loop(self):
        plugin = her.Her(harness.FakeContext(), config=dict(self.config))
        test_basics.PLUGINS.append(plugin)
        plugin._autonomy_task.cancel()
        calls = 0

        async def sleep(_seconds):
            nonlocal calls
            calls += 1
            if calls == 3:
                plugin.enabled = False

        with patch.object(mixin_autonomy.asyncio, 'sleep', side_effect=sleep), \
             patch.object(weather, 'tick', new_callable=AsyncMock, side_effect=RuntimeError('detail')) as tick, \
             patch.object(mixin_autonomy.logger, 'warning') as warning:
            await plugin._autonomy_loop()
        self.assertEqual(tick.await_count, 2)
        self.assertEqual(warning.call_args_list[0].args, ('[ams-life] weather tick failed: %s', 'RuntimeError'))

    async def test_prepare_turn_offline_with_and_without_photo(self):
        config = dict(self.config, photo_enabled=False)
        plugin = her.Her(harness.FakeContext(), config=config)
        test_basics.PLUGINS.append(plugin)
        plugin._image_context = AsyncMock(return_value='')
        data = {'date': datetime.now(weather.ZONE).date().isoformat(), 'code': 0, 'max': 22, 'min': 15, 'rain': 20}
        weather.write(self.path, data)
        with patch.object(mixin_turn, 'STATE_DIR', self.root), patch.object(weather, 'fetch', side_effect=AssertionError('network')) as fetcher, patch('urllib.request.urlopen', side_effect=AssertionError('network')), patch.object(weather, 'build_opener', side_effect=AssertionError('network')):
            for photo in (False, True):
                plugin.config['photo_enabled'] = photo
                request = turn.TurnRequest(prompt='hello')
                await plugin._prepare_turn(harness.FakeEvent('hello'), request)
                prompt = '\n'.join(part.get('text', '') for part in request.extra_user_content_parts)
                self.assertIn('天气：示例城 晴', prompt)
                self.assertEqual('[她今天]' in prompt, photo)
            plugin.config.pop('weather_lat')
            request = turn.TurnRequest(prompt='hello')
            await plugin._prepare_turn(harness.FakeEvent('hello'), request)
            self.assertNotIn('天气：', str(request.extra_user_content_parts))
            fetcher.assert_not_called()
