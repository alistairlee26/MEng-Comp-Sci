from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import constants
constants.BLOCK_LIMIT = 12


if __name__ == '__main__':
    runpy.run_path(str(ROOT / 'client.py'), run_name='__main__')
