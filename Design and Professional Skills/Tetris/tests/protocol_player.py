import atexit
import json
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import constants
constants.BLOCK_LIMIT = 12
import player


def report(instance):
    print(json.dumps({
        'searches': instance.search_decisions,
        'fallback': instance.fallback_decisions,
        'failures': instance.planning_failures,
    }), file=sys.stderr)


class ObservedPlayer(player.HeuristicPlayer):
    def __init__(self):
        super().__init__(block_limit=12)
        atexit.register(report, self)


if __name__ == '__main__':
    player.SelectedPlayer = ObservedPlayer
    runpy.run_path(str(ROOT / 'server.py'), run_name='__main__')
