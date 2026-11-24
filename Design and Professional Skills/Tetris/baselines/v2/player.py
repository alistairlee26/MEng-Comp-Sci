from board import Direction, Rotation, Action, Shape
from random import Random
import time
from constants import BLOCK_LIMIT
import os
from planner import Planner, SeedPredictor, Landing


# Preserve the original heuristic for prediction warm-up and emergency use.
# Normal play without a verified seed uses the visible-piece search below.
DEFAULT_WEIGHTS = {
    'height': 0.45,
    'holes': 6.0,
    'buried_holes': 0.25,
    'bumpiness': 0.35,
    'danger': 0.75,
    'setup': 1.0,
    'setup_hole_discount': 0.0,
    'hole_risk': 0.0,
}


class Player:
    def choose_action(self, board):
        raise NotImplementedError("choose_action must be implemented by subclasses")

class RandomPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)

    def print_board(self, board):
        print("--------")
        for y in range(24):
            s = ""
            for x in range(10):
                if (x,y) in board.cells:
                    s += "#"
                else:
                    s += "."
            print(s, y)


    def choose_action(self, board):
        self.print_board(board)
        time.sleep(0.5)
        if self.random.random() > 0.97:
            # 3% chance we'll discard or drop a bomb
            return self.random.choice([
                Action.Discard,
                Action.Bomb,
            ])
        else:
            # 97% chance we'll make a normal move
            return self.random.choice([
                Direction.Left,
                Direction.Right,
                Direction.Down,
                Rotation.Anticlockwise,
                Rotation.Clockwise,
            ])


class HeuristicPlayer(Player):

    def __init__(self, lookahead_candidates=4, weights=None,
                 block_limit=BLOCK_LIMIT):
        if lookahead_candidates < 0:
            lookahead_candidates = 0

        self.lookahead_candidates = lookahead_candidates
        self.weights = DEFAULT_WEIGHTS.copy()
        if weights is not None:
            for name, value in weights.items():
                if name not in self.weights:
                    raise ValueError('Unknown evaluation weight: ' + name)
                if value < 0:
                    raise ValueError('Evaluation weights must be nonnegative')
                self.weights[name] = value

        self.block_limit = block_limit
        self.pieces_played = 0

    def choose_action(self, board):
        starting_score = board.score
        candidates = []

        # Every returned plan finishes its current piece. With this contract,
        # one call represents one played piece. The last generated piece is
        # reserved as a preview when the engine reaches its generation limit.
        self.pieces_played += 1
        remaining_pieces = self.block_limit - self.pieces_played - 1
        if remaining_pieces < 0:
            remaining_pieces = 0

        # Step 1: simulate the possible landings of the current piece.
        for moves, landed_board in self.landings(board):
            evaluation = self.evaluate(
                landed_board, starting_score, remaining_pieces
            )

            candidate = {
                'evaluation': evaluation,
                'moves': moves,
                'board': landed_board,
            }
            candidates.append(candidate)

        if len(candidates) == 0:
            return Direction.Drop

        # Step 2: rank the immediate results, best first.
        candidates.sort(key=self.candidate_priority, reverse=True)
        best_candidate = candidates[0]
        best_moves = best_candidate['moves']

        if board.next is None:
            return best_moves

        if remaining_pieces == 0:
            return best_moves

        if self.lookahead_candidates == 0:
            return best_moves

        # Step 3: examine the preview for only the most promising candidates.
        best_future_evaluation = float('-inf')
        shortest_best_plan = float('inf')
        shortlist = candidates[:self.lookahead_candidates]

        for candidate in shortlist:
            immediate_evaluation = candidate['evaluation']
            moves = candidate['moves']
            landed_board = candidate['board']

            if immediate_evaluation == float('-inf'):
                continue

            # The first landing has promoted the preview into the active piece.
            # Score both placements relative to the original starting score.
            candidate_future_evaluation = float('-inf')
            found_preview_landing = False

            for preview_moves, future_board in self.landings(landed_board):
                found_preview_landing = True
                evaluation = self.evaluate(
                    future_board, starting_score, remaining_pieces - 1
                )

                if evaluation > candidate_future_evaluation:
                    candidate_future_evaluation = evaluation

            if not found_preview_landing:
                candidate_future_evaluation = immediate_evaluation

            # Preserve the tested baseline ordering: prefer a higher two-piece
            # evaluation, then a shorter current-piece plan when scores match.
            move_count = len(moves)
            better_evaluation = (
                candidate_future_evaluation > best_future_evaluation
            )
            equal_evaluation = (
                candidate_future_evaluation == best_future_evaluation
            )
            shorter_plan = move_count < shortest_best_plan
            prefer_candidate = better_evaluation or (equal_evaluation and shorter_plan)

            if prefer_candidate:
                best_future_evaluation = candidate_future_evaluation
                shortest_best_plan = move_count
                best_moves = moves

        return best_moves

    def candidate_priority(self, candidate):
        evaluation = candidate['evaluation']
        move_count = len(candidate['moves'])

        # Sorting largest first favours high evaluations. Negating the move
        # count makes a shorter plan rank higher when evaluations are equal.
        return (evaluation, -move_count)

    def landings(self, board):
        if board.falling is None:
            return

        rotation_sequences = [
            [],
            [Rotation.Clockwise],
            [Rotation.Clockwise, Rotation.Clockwise],
            [Rotation.Anticlockwise],
        ]
        seen_states = set()

        for rotations in rotation_sequences:
            # All target columns share the same rotations. Perform this prefix
            # once, then clone it for each target instead of repeating it.
            rotated_board = board.clone()
            rotation_moves = []
            has_landed = False
            for rotation in rotations:
                rotation_moves.append(rotation)
                has_landed = rotated_board.rotate(rotation)
                if has_landed:
                    break

            if has_landed:
                state = (frozenset(rotated_board.cells), rotated_board.score)
                if state not in seen_states:
                    seen_states.add(state)
                    yield rotation_moves, rotated_board
                continue

            for target_x in range(board.width):
                sandbox = rotated_board.clone()
                moves = rotation_moves.copy()
                has_landed = False

                # Align the left edge with the requested column.
                while not has_landed:
                    current_x = sandbox.falling.left

                    if current_x == target_x:
                        break

                    if current_x > target_x:
                        direction = Direction.Left
                    else:
                        direction = Direction.Right

                    moves.append(direction)
                    has_landed = sandbox.move(direction)

                    if has_landed:
                        break

                    if sandbox.falling.left == current_x:
                        # Sideways movement was blocked. Try dropping here.
                        break

                # Gravity may already have landed the piece during steering.
                if not has_landed:
                    moves.append(Direction.Drop)
                    sandbox.move(Direction.Drop)

                # Different plans can produce the same result. A frozenset is
                # an immutable set, so it can be part of a set membership key.
                occupied_cells = frozenset(sandbox.cells)
                state = (occupied_cells, sandbox.score)

                if state in seen_states:
                    continue

                seen_states.add(state)
                yield moves, sandbox

    def evaluate(self, board, starting_score, remaining_pieces=None):
        if not board.alive:
            return float('-inf')

        column_heights = []
        total_height = 0
        tallest_column = 0
        holes = 0
        blocks_above_holes = 0

        # Read each column from top to bottom.
        for x in range(board.width):
            column_height = 0
            blocks_above = 0

            for y in range(board.height):
                if (x, y) in board.cells:
                    if blocks_above == 0:
                        column_height = board.height - y

                    blocks_above += 1
                else:
                    if blocks_above > 0:
                        holes += 1
                        blocks_above_holes += blocks_above

            column_heights.append(column_height)
            total_height += column_height

            if column_height > tallest_column:
                tallest_column = column_height

        # Measure the height differences between neighbouring columns.
        bumpiness = 0
        for x in range(board.width - 1):
            left_height = column_heights[x]
            right_height = column_heights[x + 1]
            height_difference = abs(left_height - right_height)
            bumpiness += height_difference

        # Apply an extra penalty once the stack exceeds half the board height.
        safe_height = board.height // 2
        excess_height = tallest_column - safe_height
        if excess_height < 0:
            excess_height = 0

        # The engine has already awarded descent and line-clear points.
        # Dividing by 25 scales the rewards to 1, 4, 16 and 64 for line clears.
        score_gain = board.score - starting_score
        score_reward = score_gain / 25.0
        height_penalty = self.weights['height'] * total_height
        hole_penalty = self.weights['holes'] * holes
        buried_hole_penalty = self.weights['buried_holes'] * blocks_above_holes
        bumpiness_penalty = self.weights['bumpiness'] * bumpiness
        danger_penalty = self.weights['danger'] * excess_height * excess_height

        # A hole becomes harder to repair when little headroom remains.
        risk_fraction = excess_height / safe_height
        hole_risk_multiplier = 1.0 + self.weights['hole_risk'] * risk_fraction
        hole_penalty *= hole_risk_multiplier

        setup_reward = self.multi_row_setup_reward(
            board, column_heights, tallest_column
        )
        setup_reward *= self.weights['setup']

        # Discount an unfinished scoring setup when the surrounding stack is
        # already damaged. Real line-clear points are never discounted.
        setup_discount = 1.0 + self.weights['setup_hole_discount'] * holes
        setup_reward /= setup_discount

        if remaining_pieces is not None:
            if remaining_pieces == 0:
                setup_reward = 0.0
            elif board.falling is None or board.falling.shape is not Shape.I:
                # Unknown draws have a 1/7 chance of being an I-piece. Near
                # the end, there may be too few draws to cash a prepared well.
                unknown_pieces = remaining_pieces
                if board.falling is not None:
                    # The promoted preview is already known not to be an I.
                    unknown_pieces -= 1
                chance_of_an_i = 1.0 - (6.0 / 7.0) ** unknown_pieces
                setup_reward *= chance_of_an_i

        evaluation = score_reward
        evaluation += setup_reward
        evaluation -= height_penalty
        evaluation -= hole_penalty
        evaluation -= buried_hole_penalty
        evaluation -= bumpiness_penalty
        evaluation -= danger_penalty

        return evaluation

    def multi_row_setup_reward(self, board, column_heights, tallest_column):
        # These are estimates of future value, not extra points in the game.
        # A completed four-row clear still earns its actual 1600 points.
        setup_values = [0.0, 6.0, 14.0, 30.0, 64.0]
        best_setup_reward = 0.0

        for well_x in range(board.width):
            # The column must be open from the top down. A covered gap is a
            # buried hole, not an opportunity to drop a vertical I-piece.
            if column_heights[well_x] != 0:
                continue

            ready_rows = 0
            for y in range(board.height - 1, -1, -1):
                row_is_ready = True

                for x in range(board.width):
                    if x == well_x:
                        continue

                    if (x, y) not in board.cells:
                        row_is_ready = False
                        break

                if not row_is_ready:
                    break

                ready_rows += 1
                if ready_rows == 4:
                    break

            setup_reward = setup_values[ready_rows]
            if setup_reward > best_setup_reward:
                best_setup_reward = setup_reward

        # Waiting for an I-piece becomes less attractive as headroom runs out.
        safe_height = board.height // 2
        if tallest_column > safe_height:
            headroom = board.height - tallest_column
            safe_headroom = board.height - safe_height
            safety_factor = headroom / safe_headroom
            if safety_factor < 0:
                safety_factor = 0.0
            best_setup_reward *= safety_factor

        return best_setup_reward


class SearchPlayer(Player):
    def __init__(self, lookahead_candidates=4, weights=None,
                 block_limit=BLOCK_LIMIT, beam_width=32, prediction_depth=8,
                 seed=None, use_prediction=True, search_weights=None,
                 well_column=None, setup_rows=12, search_time_limit=0.4,
                 fast_fallback=False, basic_mode='chance', basic_weights=None,
                 basic_root_width=6, basic_preview_width=4,
                 basic_time_limit=0.5, basic_setup_rows=8,
                 allow_discards=True, allow_bombs=True,
                 whole_game=True, whole_game_width=256, whole_game_time_limit=260):
        self.basic = HeuristicPlayer(lookahead_candidates, weights, block_limit)
        if seed is None:
            seed = os.getenv('SEED')
        if not use_prediction:
            seed = None
        self.predictor = SeedPredictor(seed, block_limit)
        self.block_limit = block_limit
        self.beam_width = beam_width
        self.prediction_depth = prediction_depth
        self.search_weights = search_weights
        self.well_column = well_column
        self.setup_rows = setup_rows
        self.search_time_limit = search_time_limit
        self.fast_fallback = fast_fallback
        self.basic_mode = basic_mode
        if fast_fallback:
            self.basic_mode = 'known'
        self.basic_weights = basic_weights
        self.basic_root_width = basic_root_width
        self.basic_preview_width = basic_preview_width
        self.basic_time_limit = basic_time_limit
        self.basic_setup_rows = basic_setup_rows
        self.allow_discards = allow_discards
        self.allow_bombs = allow_bombs
        self.whole_game = whole_game
        self.whole_game_width = whole_game_width
        self.whole_game_time_limit = whole_game_time_limit
        self.saved_plan = []
        self.full_plans = 0
        self.cached_decisions = 0
        self.whole_game_cpu = 0.0
        self.planner = None
        self.predictive_planner = None
        self.visible_planner = None
        self.turn = 0
        self.predicted_decisions = 0
        self.fallback_decisions = 0
        self.planning_failures = 0
        self.last_failure = None
        self.total_search_depth = 0
        self.maximum_search_depth = 0
        self.budget_stops = 0
        self.known_decisions = 0
        self.bomb_decisions = 0
        self.discard_decisions = 0

    def choose_action(self, board):
        index = self.turn
        self.turn += 1
        self.basic.pieces_played = index
        preview = None
        if board.next is not None:
            preview = board.next.shape
        verified = self.predictor.observe(index, board.falling.shape, preview)
        if not verified:
            self.saved_plan = []
        if not verified and (self.basic_mode == 'legacy' or self.predictor.status == 'checking'):
            return self.fallback(board)

        if verified:
            depth = self.prediction_depth
            if self.whole_game:
                depth = self.block_limit
            shapes = self.predictor.future(index, depth)
        else:
            shapes = [board.falling.shape]
            if preview is not None and index + 2 < self.block_limit:
                shapes.append(preview)
        if not shapes:
            return self.fallback(board)

        try:
            if verified:
                if self.predictive_planner is None:
                    self.predictive_planner = self.make_planner(board, self.search_weights)
                self.planner = self.predictive_planner
            else:
                if self.visible_planner is None:
                    self.visible_planner = self.make_planner(
                        board, self.basic_weights, self.basic_time_limit,
                        self.basic_setup_rows,
                    )
                self.planner = self.visible_planner
            remaining = self.block_limit - index - 1
            landing = None
            used_saved_plan = False
            if verified and self.whole_game and self.saved_plan:
                candidate = self.saved_plan.pop(0)
                if self.verify_plan(board, candidate):
                    landing = candidate
                    self.cached_decisions += 1
                    used_saved_plan = True
                else:
                    self.saved_plan = []
            root_landings = None
            if landing is None:
                root_landings = self.resource_landings(board, remaining)
            if landing is None and verified and self.whole_game and self.whole_game_cpu < 300:
                self.planner.beam_width = self.whole_game_width
                self.planner.time_limit = min(self.whole_game_time_limit,
                                              300 - self.whole_game_cpu)
                started = time.process_time()
                landing = self.planner.search(board, shapes, remaining,
                                              self.allow_discards, root_landings,
                                              remember_path=True,
                                              allow_bombs=self.allow_bombs)
                self.whole_game_cpu += time.process_time() - started
                self.saved_plan = self.planner.last_path[1:]
                self.full_plans += 1
            elif landing is None and not verified and self.basic_mode == 'chance':
                landing = self.planner.chance_search(
                    board, remaining, self.basic_root_width, self.basic_preview_width,
                    self.allow_discards, root_landings,
                )
            elif landing is None:
                if self.whole_game and self.whole_game_cpu >= 300:
                    self.planner.beam_width = self.beam_width
                    self.planner.time_limit = min(0.15, self.search_time_limit)
                landing = self.planner.search(board, shapes, remaining,
                                              self.allow_discards, root_landings)
            if landing is not None and self.verify_plan(board, landing):
                if Action.Bomb in landing.moves:
                    self.predictor.replace(index + 1, Shape.B)
                    self.bomb_decisions += 1
                if Action.Discard in landing.moves:
                    self.discard_decisions += 1
                if verified:
                    self.predicted_decisions += 1
                else:
                    self.known_decisions += 1
                    self.fallback_decisions += 1
                search_depth = self.planner.last_depth
                if used_saved_plan:
                    search_depth = 0
                self.total_search_depth += search_depth
                self.maximum_search_depth = max(self.maximum_search_depth,
                                                search_depth)
                if self.planner.budget_stopped and not used_saved_plan:
                    self.budget_stops += 1
                return landing.moves
            self.last_failure = 'plan verification failed'
        except Exception as error:
            self.last_failure = type(error).__name__
        self.planning_failures += 1
        return self.fallback(board)

    def make_planner(self, board, weights, time_limit=None, setup_rows=None):
        if time_limit is None:
            time_limit = self.search_time_limit
        if setup_rows is None:
            setup_rows = self.setup_rows
        return Planner(board.width, board.height, self.beam_width,
                       time_limit=time_limit, weights=weights,
                       well_column=self.well_column, setup_rows=setup_rows)

    def resource_landings(self, board, remaining):
        if not self.allow_discards and not self.allow_bombs:
            return None
        columns = self.planner.columns_from_board(board)
        choices = self.planner.options(columns, board.falling.shape,
                                       board.discards_remaining, remaining,
                                       self.allow_discards)
        if not self.allow_bombs or board.bombs_remaining == 0:
            return choices
        if board.next is None or board.next.shape is Shape.B or remaining < 2:
            return choices
        if board.falling.shape is Shape.B:
            return choices
        heights, holes = self.planner.measure(columns)
        if max(heights) < 14 and holes < 3:
            return choices

        sandbox = board.clone()
        landed = sandbox.bomb()
        bomb_cost = self.planner.weights['bomb_cost']
        if landed:
            choices.append(Landing(self.planner.columns_from_board(sandbox),
                                   sandbox.score - board.score, [Action.Bomb], 0,
                                   cost=bomb_cost, next_shape=Shape.B, bombs=1))
        else:
            for moves, after in self.basic.landings(sandbox):
                plan = [Action.Bomb] + moves
                choices.append(Landing(self.planner.columns_from_board(after),
                                       after.score - board.score, plan, 0,
                                       cost=bomb_cost, next_shape=Shape.B, bombs=1))
        return choices

    def fallback(self, board):
        self.fallback_decisions += 1
        return self.basic.choose_action(board)

    def verify_plan(self, board, landing):
        sandbox = board.clone()
        landed = False
        for index, move in enumerate(landing.moves):
            if move is Action.Discard:
                landed = sandbox.discard()
            elif move is Action.Bomb:
                landed = sandbox.bomb()
            elif move is None:
                landed = sandbox.skip()
            elif isinstance(move, Rotation):
                landed = sandbox.rotate(move)
            else:
                landed = sandbox.move(move)
            if landed:
                if index != len(landing.moves) - 1:
                    return False
                break
        if not landed:
            return False
        if sandbox.score - board.score != landing.points:
            return False
        if board.discards_remaining - sandbox.discards_remaining != landing.discards:
            return False
        if board.bombs_remaining - sandbox.bombs_remaining != landing.bombs:
            return False
        if landing.next_shape is not None:
            if sandbox.falling is None or sandbox.falling.shape is not landing.next_shape:
                return False
        return self.planner.columns_from_board(sandbox) == landing.columns


SelectedPlayer = SearchPlayer
