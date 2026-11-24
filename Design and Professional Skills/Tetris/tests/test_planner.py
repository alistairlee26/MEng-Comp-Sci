import os
from random import Random
import unittest
from unittest.mock import patch

from board import Action, Block, Board, Rotation, Shape
from player import FallbackPlayer, HeuristicPlayer, Landing, Planner, SelectedPlayer


class PlannerTests(unittest.TestCase):
    def make_board(self, shape, cells):
        board = Board(10, 24)
        board.cells = set(cells)
        board.cellcolor = {}
        for cell in cells:
            board.cellcolor[cell] = 'blue'
        board.next = Block(shape)
        board.place_next_block()
        board.next = Block(Shape.O)
        return board


    def test_fast_landings_match_the_real_engine(self):
        generator = Random(835721)
        patterns = [[], [(x, y) for x in range(1, 10) for y in range(20, 24)]]
        for pattern in range(5):
            cells = []
            for x in range(10):
                height = generator.randrange(9)
                for y in range(24 - height, 24):
                    if generator.random() > 0.10:
                        cells.append((x, y))
            patterns.append(cells)
        # A rescue search also has to model gravity near the spawn correctly.
        for height in (14, 19, 22):
            cells = []
            for x in range(10):
                if x == 0:
                    continue
                for y in range(24 - height, 24):
                    if generator.random() > 0.08:
                        cells.append((x, y))
            patterns.append(cells)

        planner = Planner()
        compared = 0
        for shape in Shape:
            for cells in patterns:
                board = self.make_board(shape, cells)
                columns = planner.columns_from_board(board)
                for landing in planner.placements(columns, shape):
                    sandbox = board.clone()
                    for index, move in enumerate(landing.moves):
                        if isinstance(move, Rotation):
                            landed = sandbox.rotate(move)
                        else:
                            landed = sandbox.move(move)
                        if landed:
                            self.assertEqual(index, len(landing.moves) - 1)
                            break
                    self.assertTrue(landed)
                    self.assertEqual(planner.columns_from_board(sandbox), landing.columns)
                    self.assertEqual(sandbox.score - board.score, landing.points)
                    compared += 1
        self.assertGreater(compared, 1000)


    def test_visible_piece_search_does_not_read_the_seed(self):
        board = self.make_board(Shape.T, [])
        board.next = Block(Shape.L)
        options = {
            'root_width': 2, 'preview_width': 2,
            'time_limit': 10,
        }
        with patch.dict(os.environ, {'SEED': 'first-unrelated-seed'}):
            first = HeuristicPlayer(**options)
            first_moves = first.choose_action(board)
        with patch.dict(os.environ, {'SEED': 'second-unrelated-seed'}):
            second = HeuristicPlayer(**options)
            second_moves = second.choose_action(board)
        self.assertEqual(first_moves, second_moves)
        self.assertFalse(hasattr(first, 'predictor'))
        self.assertEqual(first.search_decisions, 1)


    def test_bomb_root_plans_replay_on_the_actual_engine(self):
        from board import Action
        cells = []
        for x in range(1, 10):
            for y in range(10, 24):
                if (x, y) not in ((4, 18), (4, 20), (7, 19)):
                    cells.append((x, y))
        board = self.make_board(Shape.O, cells)
        player = HeuristicPlayer(allow_bombs=True)
        player.planner = player.make_planner(board)
        choices = player.resource_landings(board, 100)
        bomb_plans = []
        for landing in choices:
            if Action.Bomb in landing.moves:
                bomb_plans.append(landing)
                self.assertTrue(player.verify_plan(board, landing))
                self.assertEqual(landing.next_shape, Shape.B)
        self.assertTrue(bomb_plans)


    def test_an_available_four_row_clear_is_preferred_to_discarding(self):
        from board import Action
        board = self.make_board(Shape.I, [(x, y) for x in range(1, 10)
                                        for y in range(20, 24)])
        player = HeuristicPlayer(allow_discards=True)
        moves = player.choose_action(board)
        self.assertNotIn(Action.Discard, moves)
        sandbox = board.clone()
        for move in moves:
            if isinstance(move, Rotation):
                landed = sandbox.rotate(move)
            else:
                landed = sandbox.move(move)
            if landed:
                break
        self.assertGreaterEqual(sandbox.score, 1600)


    def test_terminal_evaluation_only_counts_real_points(self):
        planner = Planner()
        empty = (0,) * 10
        damaged = (0, 1 << 3) + (0,) * 8
        self.assertEqual(planner.evaluate(empty, 400, 0), 16)
        self.assertEqual(planner.evaluate(damaged, 400, 0), 16)


    def test_no_resources_are_invented_after_exhaustion(self):
        from board import Action
        board = self.make_board(Shape.O, [(x, y) for x in range(1, 10)
                                        for y in range(10, 24)])
        board.discards_remaining = 0
        board.bombs_remaining = 0
        player = HeuristicPlayer(allow_discards=True, allow_bombs=True)
        player.planner = player.make_planner(board)
        for landing in player.resource_landings(board, 100):
            self.assertNotIn(Action.Bomb, landing.moves)
            self.assertNotIn(Action.Discard, landing.moves)


    def test_selected_player_is_the_basic_heuristic(self):
        self.assertIs(SelectedPlayer, HeuristicPlayer)
        player = SelectedPlayer()
        self.assertEqual(player.root_width, 6)
        self.assertEqual(player.preview_width, 4)
        self.assertEqual(player.time_limit, 0.5)
        self.assertEqual(player.setup_rows, 8)
        self.assertFalse(hasattr(player, 'saved_plan'))

    def test_default_player_never_reads_environment_variables(self):
        board = self.make_board(Shape.T, [])
        with patch('os.getenv', side_effect=AssertionError('environment read')):
            player = HeuristicPlayer(root_width=2, preview_width=2)
            moves = player.choose_action(board)
        self.assertTrue(moves)
        self.assertEqual(player.planning_failures, 0)
        self.assertEqual(player.search_decisions, 1)

    def test_discard_permanently_removes_current_piece_and_promotes_preview(self):
        board = self.make_board(Shape.T, [])
        board.next = Block(Shape.S)
        player = HeuristicPlayer()
        player.planner = player.make_planner(board)
        for landing in player.resource_landings(board, 20):
            if Action.Discard in landing.moves:
                self.assertTrue(player.verify_plan(board, landing))
                break
        else:
            self.fail('available discard omitted')
        self.assertTrue(board.discard())
        self.assertEqual(board.falling.shape, Shape.S)
        self.assertIsNone(board.next)
        self.assertEqual(board.discards_remaining, 9)

    def test_final_piece_uses_actual_points_and_preserves_input(self):
        board = self.make_board(Shape.I, [(x, y) for x in range(1, 10)
                                         for y in range(20, 24)])
        cells = board.cells.copy()
        player = HeuristicPlayer(block_limit=2)
        moves = player.choose_action(board)
        self.assertEqual(player.planner.last_depth, 1)
        self.assertEqual(board.cells, cells)
        self.assertNotIn(Action.Bomb, moves)
        self.assertNotIn(Action.Discard, moves)
        sandbox = board.clone()
        for move in moves:
            if isinstance(move, Rotation):
                sandbox.rotate(move)
            else:
                sandbox.move(move)
        self.assertGreaterEqual(sandbox.score, 1600)
        self.assertEqual(player.planning_failures, 0)

    def test_basic_player_supports_a_missing_preview(self):
        board = self.make_board(Shape.T, [])
        board.next = None
        player = HeuristicPlayer()
        self.assertTrue(player.choose_action(board))
        self.assertEqual(player.planner.last_depth, 1)
        self.assertEqual(player.planning_failures, 0)

    def test_all_shapes_including_a_bomb_have_verified_moves(self):
        for shape in Shape:
            with self.subTest(shape=shape):
                board = self.make_board(shape, [])
                player = HeuristicPlayer(root_width=2, preview_width=2)
                self.assertTrue(player.choose_action(board))
                self.assertEqual(player.search_decisions, 1)
                self.assertEqual(player.planning_failures, 0)

    def test_failed_plan_uses_the_same_emergency_heuristic(self):
        board = self.make_board(Shape.T, [])
        expected = FallbackPlayer().choose_action(board)
        invalid = Landing((0,) * 10, 999999, [])
        with patch.object(Planner, 'search', return_value=invalid):
            player = HeuristicPlayer()
            moves = player.choose_action(board)
        self.assertEqual(moves, expected)
        self.assertEqual(player.fallback_decisions, 1)
        self.assertEqual(player.search_decisions, 0)
        self.assertEqual(player.planning_failures, 1)


if __name__ == '__main__':
    unittest.main()
