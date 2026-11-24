import argparse
import os
from pathlib import Path
import runpy
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import constants


def main():
    parser = argparse.ArgumentParser(description='Play or watch the basic Tetris player')
    parser.add_argument('--interface', choices=('pygame', 'tkinter', 'terminal'),
                        default='pygame')
    parser.add_argument('--seed', type=int, help='Choose the local piece sequence')
    parser.add_argument('--manual', action='store_true')
    args = parser.parse_args()
    if args.seed is not None:
        constants.DEFAULT_SEED = args.seed
    entry_points = {
        'pygame': 'visual-pygame.py',
        'tkinter': 'visual.py',
        'terminal': 'cmdline.py',
    }
    entry = ROOT / entry_points[args.interface]
    sys.argv = [str(entry)]
    if args.manual:
        sys.argv.append('-m')
    os.chdir(str(ROOT))
    runpy.run_path(str(entry), run_name='__main__')


if __name__ == '__main__':
    main()
