from pathlib import Path
import subprocess
import sys
import unittest

from board import Block, Board, Direction, Rotation, Shape
from constants import PREFIX
from player import FallbackPlayer


def make_board(shape=Shape.I, preview=Shape.O):
    board = Board(10, 24)
    board.next = Block(shape)
    board.place_next_block()
    if preview is not None:
        board.next = Block(preview)
    return board


def occupy(board, cells):
    board.cells = set(cells)
    board.cellcolor = {cell: 'blue' for cell in board.cells}


def play_plan(board, moves):
    for index, move in enumerate(moves):
        if isinstance(move, Rotation):
            landed = board.rotate(move)
        else:
            landed = board.move(move)
        if landed:
            if index != len(moves) - 1:
                raise AssertionError('Plan continues after its piece lands')
            return
    raise AssertionError('Plan did not land its piece')


class FallbackPlayerTests(unittest.TestCase):
    def test_search_does_not_change_input(self):
        board = make_board()
        occupy(board, [(0, 23), (1, 23), (1, 22)])
        before = (board.cells.copy(), board.cellcolor.copy(), board.score,
                  board.falling.cells.copy(), board.next.cells.copy(),
                  board.discards_remaining, board.bombs_remaining)
        moves = FallbackPlayer().choose_action(board)
        after = (board.cells, board.cellcolor, board.score,
                 board.falling.cells, board.next.cells,
                 board.discards_remaining, board.bombs_remaining)
        self.assertEqual(before, after)
        self.assertTrue(moves)
        play_plan(board.clone(), moves)

    def test_takes_available_four_row_clear(self):
        board = make_board()
        occupy(board, [(x, y) for x in range(1, 10)
                       for y in range(20, 24)])
        play_plan(board, FallbackPlayer().choose_action(board))
        self.assertGreaterEqual(board.score, 1600)
        self.assertEqual(board.cells, set())

    def test_builds_four_row_setup_instead_of_cashing_three_rows(self):
        board = make_board(shape=Shape.I, preview=Shape.O)
        cells = [(x, y) for x in range(1, 10) for y in range(21, 24)]
        cells.extend((x, 20) for x in range(1, 6))
        occupy(board, cells)

        # Even without preview search, the player can recognise a preparation:
        # fill the four gaps in row 20 instead of clearing the bottom three now.
        player = FallbackPlayer(lookahead_candidates=0)
        play_plan(board, player.choose_action(board))
        self.assertEqual(len(board.cells), 36)
        self.assertLess(board.score, 25)
        for y in range(20, 24):
            self.assertNotIn((0, y), board.cells)
            for x in range(1, 10):
                self.assertIn((x, y), board.cells)

    def test_covered_well_does_not_receive_setup_reward(self):
        board = make_board()
        cells = [(x, y) for x in range(1, 10) for y in range(20, 24)]
        cells.append((0, 18))
        occupy(board, cells)
        heights = [6] + [4] * 9
        reward = FallbackPlayer().multi_row_setup_reward(board, heights, 6)
        self.assertEqual(reward, 0.0)

    def test_high_stacks_reduce_the_setup_reward(self):
        board = make_board()
        cells = [(x, y) for x in range(1, 10) for y in range(20, 24)]
        occupy(board, cells)
        low_heights = [0] + [4] * 9
        low_reward = FallbackPlayer().multi_row_setup_reward(board, low_heights, 4)

        board.cells.add((9, 4))
        board.cellcolor[(9, 4)] = 'blue'
        high_heights = [0] + [4] * 8 + [20]
        high_reward = FallbackPlayer().multi_row_setup_reward(board, high_heights, 20)
        self.assertGreater(low_reward, high_reward)
        self.assertGreater(high_reward, 0.0)

    def test_stops_plan_when_gravity_lands_piece_early(self):
        board = make_board()
        occupy(board, [(x, y) for x in range(1, 10)
                       for y in range(4, 24)])
        moves = FallbackPlayer().choose_action(board)
        play_plan(board.clone(), moves)
        plans = list(FallbackPlayer().landings(board))
        self.assertTrue(any(len(plan) == 1 for plan, _ in plans))
        for plan, _ in plans:
            play_plan(board.clone(), plan)

    def test_final_playable_piece_cashes_points_instead_of_preparing(self):
        board = make_board(shape=Shape.I, preview=Shape.I)
        cells = [(x, y) for x in range(1, 10) for y in range(21, 24)]
        cells.extend((x, 20) for x in range(1, 6))
        occupy(board, cells)
        player = FallbackPlayer(block_limit=2)
        play_plan(board, player.choose_action(board))
        self.assertGreaterEqual(board.score, 400)

    def test_unfinished_setup_has_no_bonus_after_budget_is_exhausted(self):
        board = make_board()
        occupy(board, [(x, y) for x in range(1, 10)
                       for y in range(20, 24)])
        player = FallbackPlayer()
        early_value = player.evaluate(board, 0, remaining_pieces=100)
        final_value = player.evaluate(board, 0, remaining_pieces=0)
        self.assertGreater(early_value, final_value)

    def test_known_non_i_preview_does_not_count_as_an_unknown_draw(self):
        board = make_board(shape=Shape.O, preview=None)
        occupy(board, [(x, y) for x in range(1, 10)
                       for y in range(20, 24)])
        player = FallbackPlayer()
        one_piece_left = player.evaluate(board, 0, remaining_pieces=1)
        no_pieces_left = player.evaluate(board, 0, remaining_pieces=0)
        self.assertEqual(one_piece_left, no_pieces_left)

    def test_custom_weights_do_not_change_other_players(self):
        original = FallbackPlayer()
        changed = FallbackPlayer(weights={'holes': 15.0})
        self.assertNotEqual(original.weights['holes'], changed.weights['holes'])
        self.assertEqual(original.weights, FallbackPlayer().weights)

    def test_benchmark_counts_real_clears_not_simulated_clears(self):
        from scripts.benchmark import MeasuredBoard
        board = MeasuredBoard(10, 24)
        board.next = Block(Shape.I)
        board.place_next_block()
        board.next = Block(Shape.O)
        occupy(board, [(x, y) for x in range(1, 10)
                       for y in range(20, 24)])
        moves = FallbackPlayer().choose_action(board)
        self.assertEqual(board.line_clears['4'], 0)
        play_plan(board, moves)
        self.assertEqual(board.line_clears['4'], 1)

    def test_benchmark_obeys_preview_generation_budget(self):
        from scripts.benchmark import run_game
        result = run_game(FallbackPlayer, 0, 2, {'block_limit': 2})
        self.assertEqual(result['status'], 'block-limit')
        self.assertEqual(result['pieces_generated'], 2)
        self.assertEqual(result['decisions'], 1)

    def test_no_preview_is_supported(self):
        board = make_board(shape=Shape.T, preview=None)
        play_plan(board, FallbackPlayer().choose_action(board))
        self.assertIsNone(board.falling)

    def test_all_regular_shapes_and_bomb_produce_landing_plans(self):
        for shape in Shape:
            with self.subTest(shape=shape):
                board = make_board(shape=shape)
                play_plan(board, FallbackPlayer().choose_action(board))

    def test_same_position_has_same_plan(self):
        board = make_board(shape=Shape.L)
        self.assertEqual(FallbackPlayer().choose_action(board),
                         FallbackPlayer().choose_action(board))

    def test_default_search_avoids_regressed_temporary_hole(self):
        from scripts.benchmark import measure_stack
        board = make_board(shape=Shape.J, preview=Shape.J)
        occupy(board, [
            (0, 21), (0, 22), (0, 23),
            (1, 21), (1, 22), (1, 23),
            (2, 22), (2, 23), (3, 22), (3, 23),
            (4, 22), (4, 23), (5, 23), (7, 23),
            (9, 22), (9, 23),
        ])
        # This position exposed the wider-search regression: a ninth-ranked
        # candidate creates a temporary hole for an equal two-piece evaluation.
        # Keep the four-candidate baseline as the default until a wider search
        # is shown to improve a larger comparison including this case.
        player = FallbackPlayer()
        self.assertEqual(player.lookahead_candidates, 4)
        moves = player.choose_action(board)
        play_plan(board, moves)
        height, holes = measure_stack(board)
        self.assertEqual(holes, 0)

    def test_player_runs_through_supplied_server_protocol(self):
        messages = '\n'.join(PREFIX + ' ' + shape
                             for shape in ('I', 'O', 'T', 'L', 'WON')) + '\n'
        result = subprocess.run(
            [sys.executable, '-u', 'server.py'],
            input=messages, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            universal_newlines=True, timeout=10,
            cwd=str(Path(__file__).resolve().parent.parent),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        actions = result.stdout.splitlines()
        self.assertTrue(actions)
        allowed = {PREFIX + ' ' + action.value for action in Direction}
        allowed.update(PREFIX + ' ' + action.value for action in Rotation)
        self.assertTrue(all(action in allowed for action in actions), actions)


if __name__ == '__main__':
    unittest.main()
