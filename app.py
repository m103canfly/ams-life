# -*- coding: utf-8 -*-
# ams-life (AGPL-3.0); see NOTICE.md.
"""Standalone entry point for her OneBot connection and local panel."""
import argparse
import asyncio
import importlib
import logging
from logging.handlers import RotatingFileHandler
import os
import sys
from pathlib import Path

logger = logging.getLogger('ams-life.app')
ROOT = Path(__file__).resolve().parent


def ensure_astrbot(import_module=importlib.import_module):
    """Put compat/ first on sys.path when AstrBot itself cannot be imported."""
    try:
        import_module('astrbot')
    except ImportError:
        path = str(ROOT / 'compat')
        if path in sys.path:
            sys.path.remove(path)
        sys.path.insert(0, path)


class DataDirectoryError(ValueError):
    """The data folder is live, or not the one the plugin modules already use."""


def prepare_data(path):
    """Check the data folder and set AMS_LIFE_DATA_DIR before the plugin modules are imported."""
    from tools._guard import live_reason
    path = Path(path).resolve()
    if live_reason(path):
        raise DataDirectoryError('AstrBot data directory is not allowed')
    loaded = sys.modules.get('common')
    if loaded is not None and Path(loaded.DATA_DIR).resolve() != path:
        raise DataDirectoryError('data directory differs from the loaded data directory')
    os.environ['AMS_LIFE_DATA_DIR'] = str(path)
    ensure_astrbot()
    import common
    if Path(common.DATA_DIR).resolve() != path:
        raise DataDirectoryError('data directory differs from the loaded data directory')
    return path


def panel_llm_config(api_config):
    """Return the complete, safe panel LLM settings, if selected."""
    from deepseek_client import deepseek_url_ok
    llm = api_config.get('llm') if isinstance(api_config, dict) else None
    if not isinstance(llm, dict) or llm.get('source') != 'custom':
        return None
    base_url, model = llm.get('base_url'), llm.get('model')
    if not base_url or not model:
        return None
    if not deepseek_url_ok(base_url):
        logger.warning('[ams-life] panel LLM address is not DeepSeek; using --model')
        return None
    return base_url, model


class App:
    """Her, her history, the OneBot server and the panel, started and stopped together."""

    def __init__(self, args, model=None):
        self.args, self.model = args, model
        self.her = self.history = self.onebot = self.panel = None
        self._stopped = asyncio.Event()
        self._log_handler = None
        self._log_level = None

    async def start(self):
        """Start everything; {'onebot': port or None, 'panel': port}. A failure stops what started."""
        log_path = getattr(self.args, 'log', None)
        if log_path and self._log_handler is None:
            path = Path(log_path)
            path.parent.mkdir(parents=True, exist_ok=True)
            handler = RotatingFileHandler(path, maxBytes=2 * 1024 * 1024, backupCount=5, encoding='utf-8')
            handler.setLevel(logging.INFO)
            handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s: %(message)s'))
            root_logger = logging.getLogger()
            self._log_level = root_logger.level
            if root_logger.level > logging.INFO:
                root_logger.setLevel(logging.INFO)
            root_logger.addHandler(handler)
            self._log_handler = handler
        try:
            root = prepare_data(self.args.data)
        except DataDirectoryError as error:
            if self._log_handler is not None:
                logger.info('%s', error)
            await self.stop()
            raise
        except BaseException:
            await self.stop()
            raise
        import app_config
        import persona_file
        import panel_api
        from her import Her
        from history_store import HistoryStore
        from key_store import KeyStore, KeyStoreError
        from panel_server import PanelServer

        try:
            keys = KeyStore(root / 'keys.dat')
            values = {}
            for name in ('deepseek', 'napcat', 'vision'):
                if keys.has(name):
                    try:
                        values[name] = keys.get(name)
                    except KeyStoreError:
                        logger.warning('[ams-life] %s cannot decrypt; please refill it in the panel', name)
            deepseek = values.get('deepseek', '')
            napcat = values.get('napcat', '')
            schema = app_config.load_schema()
            config_path = root / 'config.json'
            config, problems = app_config.load(config_path, schema)
            for problem in problems:
                logger.warning('[ams-life] config problem: %s', problem)
            try:
                persona = persona_file.load(root / persona_file.NAME).text
            except persona_file.PersonaError as error:
                logger.warning('[ams-life] persona error: %s', type(error).__name__)
                persona = ''
            self.history = HistoryStore(root / 'history.sqlite3')
            collector = panel_api.RouteCollector()
            self.her = Her(collector, config)
            self.her.self_decide = True
            if self.model is not None:
                self.her._neutral_model = self.model
            elif deepseek:
                from deepseek_client import DeepSeekModel
                panel_llm = panel_llm_config(self.her.api_config)
                if panel_llm:
                    try:
                        self.her._neutral_model = DeepSeekModel(api_key=deepseek, model=panel_llm[1],
                                                               base_url=panel_llm[0])
                    except ValueError:
                        panel_llm = None
                if not panel_llm:
                    self.her._neutral_model = DeepSeekModel(api_key=deepseek, model=self.args.model)
                logger.info('[ams-life] chat model: %s', panel_llm[1] if panel_llm else self.args.model)
            self.her._key_store = keys
            self.her._history = self.history
            self.history.gate = self.her._history_gate
            self.her._neutral_persona = persona
            self.her._config_path = config_path
            self.her._config_schema = schema
            onebot_port = None
            if deepseek and napcat:
                from onebot_server import OneBotServer
                self.onebot = OneBotServer(token=napcat, on_event=self.on_event,
                                           host='127.0.0.1', port=self.args.onebot_port)
                self.her._neutral_messenger = self.onebot.messenger(roots=[root])
                onebot_port = await self.onebot.start()
            else:
                print('Please fill in the keys in the panel.')
                if self._log_handler is not None:
                    logger.info('Please fill in the keys in the panel.')
            panel_api.install_request_shim()
            self.panel = PanelServer(root=ROOT / 'pages', keys=keys,
                                     key_names=('deepseek', 'vision', 'napcat'),
                                     host='127.0.0.1', port=self.args.panel_port,
                                     api_routes=panel_api.aiohttp_routes(collector.routes),
                                     start_page='dashboard/')
            panel_port = await self.panel.start()
            print('OneBot port: %s; panel port: %s' % (onebot_port, panel_port))
            if self._log_handler is not None:
                logger.info('OneBot port: %s; panel port: %s', onebot_port, panel_port)
            return {'onebot': onebot_port, 'panel': panel_port}
        except BaseException:
            await self.stop()
            raise

    async def _lookup(self, action, params):
        """The data of one OneBot call, or None when it failed."""
        try:
            result = await self.onebot.call_api(action, params)
            if isinstance(result, dict) and result.get('status') == 'ok' and isinstance(result.get('data'), dict):
                return result['data']
        except Exception:
            pass
        return None

    async def on_event(self, frame):
        """One OneBot frame: a message from someone else becomes one turn; errors are logged by kind."""
        try:
            if not isinstance(frame, dict) or frame.get('post_type') != 'message':
                return
            from adapter_onebot import from_onebot
            from turn import TurnEvent
            import turn_runner

            quoted, names = None, {}
            parts = frame.get('message')
            for part in parts if isinstance(parts, list) else ():
                if not isinstance(part, dict) or not isinstance(part.get('data'), dict):
                    continue
                data = part['data']
                if part.get('type') == 'reply':
                    quoted = await self._lookup('get_msg', {'message_id': data.get('id')})
                elif part.get('type') == 'at' and frame.get('message_type') == 'group':
                    qq = str(data.get('qq') or '')
                    if qq and qq != 'all' and qq not in names:
                        member = await self._lookup('get_group_member_info',
                                                    {'group_id': frame.get('group_id'), 'user_id': data.get('qq')})
                        if member:
                            name = member.get('card') or member.get('nickname')
                            if name:
                                names[qq] = name
            incoming = from_onebot(frame, quoted=quoted, names=names)
            if incoming is not None and not incoming.is_self:
                await turn_runner.run_turn(self.her, TurnEvent(incoming), history_limit=self.args.history)
        except Exception as error:
            logger.error('[ams-life] event error: %s', type(error).__name__)

    async def stop(self):
        """Stop the 5-minute loop, the OneBot server, the history and the panel; safe to call twice."""
        self._stopped.set()
        try:
            task = getattr(self.her, '_autonomy_task', None)
            if task is not None and not task.done():
                task.cancel()
                await asyncio.gather(task, return_exceptions=True)
            if self.onebot is not None:
                server, self.onebot = self.onebot, None
                await server.stop()
            if self.history is not None:
                history, self.history = self.history, None
                history.close()
            if self.panel is not None:
                panel, self.panel = self.panel, None
                await panel.stop()
        finally:
            if self._log_handler is not None:
                root_logger = logging.getLogger()
                root_logger.removeHandler(self._log_handler)
                self._log_handler.close()
                self._log_handler = None
                root_logger.setLevel(self._log_level)
                self._log_level = None


async def run(args, model=None):
    """Start, wait until stopped, then stop; 2 for a refused data folder."""
    instance = App(args, model=model)
    try:
        await instance.start()
        await instance._stopped.wait()
    except DataDirectoryError as error:
        print(str(error))
        return 2
    finally:
        await instance.stop()
    return 0


def main(argv=None):
    """The command line: python app.py --data <folder> [options]."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True)
    parser.add_argument('--onebot-port', type=int, default=6199)
    parser.add_argument('--panel-port', type=int, default=0)
    parser.add_argument('--model', default='deepseek-chat')
    parser.add_argument('--history', type=int, default=20)
    parser.add_argument('--log')
    return asyncio.run(run(parser.parse_args(argv)))


if __name__ == '__main__':
    sys.exit(main())
