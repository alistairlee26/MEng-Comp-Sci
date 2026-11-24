# Compare players on repeatable piece sequences without a graphical view.

import argparse
from contextlib import redirect_stdout
import io
import json
from pathlib import Path
from statistics import median
import sys
import os
from time import perf_counter, process_time
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from adversary import RandomAdversary
from board import Board
from constants import BOARD_HEIGHT, BOARD_WIDTH, BLOCK_LIMIT
from exceptions import BlockLimitException
from player import RandomPlayer, SelectedPlayer


def peak_memory_bytes():
    # This is the process lifetime peak, so a reused benchmark worker can
    # conservatively include memory from its previous games too.
    if os.name == 'nt':
        import ctypes
        from ctypes import wintypes

        class MemoryCounters(ctypes.Structure):
            _fields_ = [
                ('size', wintypes.DWORD), ('page_faults', wintypes.DWORD),
                ('peak_working_set', ctypes.c_size_t),
                ('working_set', ctypes.c_size_t),
                ('peak_paged_pool', ctypes.c_size_t),
                ('paged_pool', ctypes.c_size_t),
                ('peak_nonpaged_pool', ctypes.c_size_t),
                ('nonpaged_pool', ctypes.c_size_t),
                ('pagefile', ctypes.c_size_t), ('peak_pagefile', ctypes.c_size_t),
            ]

        counters = MemoryCounters()
        counters.size = ctypes.sizeof(counters)
        kernel = ctypes.WinDLL('kernel32', use_last_error=True)
        process_api = ctypes.WinDLL('psapi', use_last_error=True)
        kernel.GetCurrentProcess.argtypes = []
        kernel.GetCurrentProcess.restype = wintypes.HANDLE
        process_api.GetProcessMemoryInfo.argtypes = [
            wintypes.HANDLE, ctypes.POINTER(MemoryCounters), wintypes.DWORD,
        ]
        process_api.GetProcessMemoryInfo.restype = wintypes.BOOL
        process = kernel.GetCurrentProcess()
        succeeded = process_api.GetProcessMemoryInfo(
            process, ctypes.byref(counters), counters.size,
        )
        if not succeeded:
            raise ctypes.WinError(ctypes.get_last_error())
        return counters.peak_working_set
    import resource
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == 'darwin':
        return peak
    return peak * 1024


class MeasuredBoard(Board):
    # Count real line clears; simulated clones still use ordinary Board.

    def __init__(self, width, height):
        super().__init__(width, height)
        self.line_clears = {'1': 0, '2': 0, '3': 0, '4': 0}

    def clean(self):
        points = super().clean()
        rows_for_points = {25: '1', 100: '2', 400: '3', 1600: '4'}
        if points in rows_for_points:
            rows = rows_for_points[points]
            self.line_clears[rows] += 1
        return points


class MeasuredPlayer:
    def __init__(self, player):
        self.player = player
        self.decisions = 0
        self.longest_decision = 0.0

    def choose_action(self, board):
        started = perf_counter()
        moves = self.player.choose_action(board)
        elapsed = perf_counter() - started
        self.decisions += 1
        if elapsed > self.longest_decision:
            self.longest_decision = elapsed
        return moves


def measure_stack(board):
    tallest = 0
    holes = 0
    for x in range(board.width):
        seen_block = False
        for y in range(board.height):
            if (x, y) in board.cells:
                if not seen_block:
                    height = board.height - y
                    tallest = max(tallest, height)
                seen_block = True
            elif seen_block:
                holes += 1
    return tallest, holes


def run_game(player_class, seed, block_limit, player_options=None):
    board = MeasuredBoard(BOARD_WIDTH, BOARD_HEIGHT)
    adversary = RandomAdversary(seed, block_limit)
    if player_class is RandomPlayer:
        player = player_class(seed)
    else:
        if player_options is None:
            player_options = {}
        player = player_class(**player_options)
    measured_player = MeasuredPlayer(player)
    started = perf_counter()
    cpu_started = process_time()
    status = 'top-out'
    previous_piece = None
    tallest_stack = 0
    most_holes = 0
    # Remove only the baseline's display output and artificial delay. Its
    # choices and the engine rules are unchanged.
    with redirect_stdout(io.StringIO()), patch('time.sleep'):
        try:
            for action in board.run(measured_player, adversary):
                if previous_piece is not None:
                    if board.falling is not previous_piece:
                        height, holes = measure_stack(board)
                        tallest_stack = max(tallest_stack, height)
                        most_holes = max(most_holes, holes)
                previous_piece = board.falling
        except BlockLimitException:
            status = 'block-limit'
    final_height, final_holes = measure_stack(board)
    return {
        'player': player_class.__name__,
        'seed': seed,
        'score': board.score,
        'pieces_generated': block_limit - adversary.blocks,
        'status': status,
        'seconds': round(perf_counter() - started, 3),
        'cpu_seconds': round(process_time() - cpu_started, 3),
        'decisions': measured_player.decisions,
        'longest_decision_seconds': round(measured_player.longest_decision, 4),
        'line_clears': board.line_clears,
        'highest_stack': tallest_stack,
        'most_holes': most_holes,
        'final_holes': final_holes,
        'fallback_decisions': getattr(player, 'fallback_decisions', 0),
        'search_decisions': getattr(player, 'search_decisions', 0),
        'planning_failures': getattr(player, 'planning_failures', 0),
        'average_search_depth': round(getattr(player, 'total_search_depth', 0)
                                      / max(1, getattr(player, 'search_decisions', 0)), 2),
        'maximum_search_depth': getattr(player, 'maximum_search_depth', 0),
        'budget_stops': getattr(player, 'budget_stops', 0),
        'last_failure': getattr(player, 'last_failure', None),
        'discards_used': 10 - board.discards_remaining,
        'bombs_used': 5 - board.bombs_remaining,
        'peak_process_memory_bytes': peak_memory_bytes(),
    }


def main():
    parser = argparse.ArgumentParser(description='Run repeatable games and record scores')
    parser.add_argument('--seeds', type=int, nargs='+', default=list(range(10)))
    parser.add_argument('--blocks', type=int, default=BLOCK_LIMIT)
    parser.add_argument('--player', choices=('both', 'selected', 'random'),
                        default='both')
    parser.add_argument('--output', type=Path, help='Optional JSON result file')
    parser.add_argument('--root-width', type=int, default=6)
    parser.add_argument('--preview-width', type=int, default=4)
    parser.add_argument('--time-limit', type=float, default=0.5)
    parser.add_argument('--weights', type=Path, help='JSON evaluation weights')
    parser.add_argument('--seed-type', choices=('integer', 'string'), default='integer')
    args = parser.parse_args()
    if args.blocks < 2:
        parser.error('--blocks must be at least 2 to include a preview')

    players = ([RandomPlayer, SelectedPlayer] if args.player == 'both' else
               [SelectedPlayer] if args.player == 'selected' else [RandomPlayer])
    results = []
    weights = None
    if args.weights is not None:
        weights = json.loads(args.weights.read_text(encoding='utf-8'))
    for player_class in players:
        for seed in args.seeds:
            if args.seed_type == 'string':
                seed = str(seed)
            options = {}
            if player_class is SelectedPlayer:
                options['weights'] = weights
                options['block_limit'] = args.blocks
                options['root_width'] = args.root_width
                options['preview_width'] = args.preview_width
                options['time_limit'] = args.time_limit
            result = run_game(player_class, seed, args.blocks, options)
            results.append(result)
            print('{player:16} seed={seed:4} score={score:6} '
                  'pieces={pieces_generated:3} {status:11} '
                  '{seconds:7.3f}s'.format(**result), flush=True)
        scores = [r['score'] for r in results
                  if r['player'] == player_class.__name__]
        print('{} median: {}'.format(player_class.__name__, median(scores)),
              flush=True)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(results, indent=2) + '\n',
                               encoding='utf-8')


if __name__ == '__main__':
    main()
