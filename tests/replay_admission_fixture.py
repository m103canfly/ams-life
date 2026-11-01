"""Run the replay with the fictional owner and group used by the nightly test."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / 'tests'))

from tools import replay  # noqa: E402
import fake_old_data as fake  # noqa: E402
import harness  # noqa: E402

prepare = harness.prepare


def prepare_with_admission(*args, **kwargs):
    clock = prepare(*args, **kwargs)
    import main
    original_init = main.BioCorePlugin.__init__

    def init_with_admission(self, context, config=None):
        config = dict(config or {})
        config.update(owner_qq=fake.ORANGE, reply_groups=[fake.G_SMALL])
        original_init(self, context, config=config)

    main.BioCorePlugin.__init__ = init_with_admission
    return clock


harness.prepare = prepare_with_admission
replay.main()
