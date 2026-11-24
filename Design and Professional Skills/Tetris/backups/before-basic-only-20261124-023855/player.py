from board import Board, Block, Direction, Rotation, Action, Shape
from random import Random
import time
from time import process_time
from constants import BLOCK_LIMIT
import os


# preserve the original heuristic for prediction warm-up and emergency use
# normal play without a verified seed uses the visible-piece search below
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

        # one call places one piece and the final generated piece stays a preview
        self.pieces_played += 1
        remaining_pieces = max(0, self.block_limit - self.pieces_played - 1)

        # rank the current piece before trying its preview
        for moves, landed_board in self.landings(board):
            candidates.append({
                'evaluation': self.evaluate(landed_board, starting_score, remaining_pieces),
                'moves': moves,
                'board': landed_board,
            })

        if not candidates:
            return Direction.Drop

        candidates.sort(key=self.candidate_priority, reverse=True)
        best_moves = candidates[0]['moves']
        if (board.next is None or remaining_pieces == 0
                or self.lookahead_candidates == 0):
            return best_moves

        best_priority = (float('-inf'), float('-inf'))
        for candidate in candidates[:self.lookahead_candidates]:
            immediate_evaluation = candidate['evaluation']
            moves = candidate['moves']
            if immediate_evaluation == float('-inf'):
                continue

            # landing the current piece promotes the preview in the cloned board
            future_value = float('-inf')
            found_preview_landing = False
            for preview_moves, future_board in self.landings(candidate['board']):
                found_preview_landing = True
                evaluation = self.evaluate(
                    future_board, starting_score, remaining_pieces - 1
                )
                if evaluation > future_value:
                    future_value = evaluation
            if not found_preview_landing:
                future_value = immediate_evaluation

            # compare score first then prefer fewer moves when scores tie
            priority = (future_value, -len(moves))
            if priority > best_priority:
                best_priority = priority
                best_moves = moves

        return best_moves

    def candidate_priority(self, candidate):
        return (candidate['evaluation'], -len(candidate['moves']))

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
            # rotate once then reuse that board for every target column
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

                # align the left edge with the requested column
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

                    # stop steering once the piece lands or movement is blocked
                    if has_landed or sandbox.falling.left == current_x:
                        break

                # gravity may already have landed the piece during steering
                if not has_landed:
                    moves.append(Direction.Drop)
                    sandbox.move(Direction.Drop)

                # frozenset lets us recognise duplicate boards
                state = (frozenset(sandbox.cells), sandbox.score)

                if state in seen_states:
                    continue

                seen_states.add(state)
                yield moves, sandbox

    def evaluate(self, board, starting_score, remaining_pieces=None):
        if not board.alive:
            return float('-inf')

        column_heights = []
        holes = 0
        blocks_above_holes = 0

        # read each column from top to bottom
        for x in range(board.width):
            column_height = 0
            blocks_above = 0

            for y in range(board.height):
                if (x, y) in board.cells:
                    if blocks_above == 0:
                        column_height = board.height - y

                    blocks_above += 1
                elif blocks_above > 0:
                    holes += 1
                    blocks_above_holes += blocks_above

            column_heights.append(column_height)

        tallest_column = max(column_heights, default=0)
        bumpiness = 0
        for x in range(board.width - 1):
            bumpiness += abs(column_heights[x] - column_heights[x + 1])

        safe_height = board.height // 2
        excess_height = max(0, tallest_column - safe_height)

        # buried holes are expensive and get riskier as headroom runs out
        hole_penalty = self.weights['holes'] * holes
        risk_fraction = excess_height / safe_height
        hole_penalty *= 1.0 + self.weights['hole_risk'] * risk_fraction

        setup_reward = self.multi_row_setup_reward(
            board, column_heights, tallest_column
        )
        setup_reward *= self.weights['setup']

        setup_reward /= 1.0 + self.weights['setup_hole_discount'] * holes

        if remaining_pieces is not None:
            if remaining_pieces == 0:
                setup_reward = 0.0
            elif board.falling is None or board.falling.shape is not Shape.I:
                # near the end there may not be another i-piece to finish the well
                unknown_pieces = remaining_pieces
                if board.falling is not None:
                    # the promoted preview is already known not to be an i
                    unknown_pieces -= 1
                chance_of_an_i = 1.0 - (6.0 / 7.0) ** unknown_pieces
                setup_reward *= chance_of_an_i

        # keep this arithmetic order so close evaluations still break ties the same way
        evaluation = (board.score - starting_score) / 25.0
        evaluation += setup_reward
        evaluation -= self.weights['height'] * sum(column_heights)
        evaluation -= hole_penalty
        evaluation -= self.weights['buried_holes'] * blocks_above_holes
        evaluation -= self.weights['bumpiness'] * bumpiness
        evaluation -= self.weights['danger'] * excess_height * excess_height

        return evaluation

    def multi_row_setup_reward(self, board, column_heights, tallest_column):
        # estimated future value in units of 25 points
        setup_values = [0.0, 6.0, 14.0, 30.0, 64.0]
        best_setup_reward = 0.0

        for well_x in range(board.width):
            # a covered well cannot take a vertical i-piece
            if column_heights[well_x] != 0:
                continue

            ready_rows = 0
            for y in range(board.height - 1, -1, -1):
                row_is_ready = True

                for x in range(board.width):
                    if x != well_x and (x, y) not in board.cells:
                        row_is_ready = False
                        break

                if not row_is_ready:
                    break

                ready_rows += 1
                if ready_rows == 4:
                    break

            best_setup_reward = max(best_setup_reward, setup_values[ready_rows])

        # waiting for an i-piece becomes less attractive as headroom runs out
        safe_height = board.height // 2
        if tallest_column > safe_height:
            headroom = board.height - tallest_column
            safety_factor = max(0.0, headroom / (board.height - safe_height))
            best_setup_reward *= safety_factor

        return best_setup_reward


class SeedPredictor:
    def __init__(self, seed, block_limit):
        self.candidates = []
        self.matched_through = -1
        self.status = 'missing'
        self.block_limit = block_limit
        if seed is None:
            return

        seed_values = [seed]
        try:
            integer_seed = int(seed)
            if not isinstance(seed, int):
                seed_values.append(integer_seed)
        except (TypeError, ValueError):
            pass

        shapes = list(Shape)[:-1]
        for value in seed_values:
            generator = Random(value)
            sequence = []
            for index in range(block_limit):
                sequence.append(generator.choice(shapes))
            self.candidates.append(sequence)
        self.status = 'checking'

    def observe(self, index, current, preview):
        if not self.candidates:
            return False

        matching = []
        for sequence in self.candidates:
            if index >= len(sequence) or sequence[index] is not current:
                continue
            if preview is not None and (index + 1 >= len(sequence)
                                         or sequence[index + 1] is not preview):
                continue
            matching.append(sequence)
        self.candidates = matching

        if not matching:
            self.status = 'mismatch'
            return False

        observed_through = index
        if preview is not None:
            observed_through += 1
        self.matched_through = max(self.matched_through, observed_through)
        if len(matching) == 1 and self.matched_through + 1 >= 6:
            self.status = 'verified'
            return True
        self.status = 'checking'
        return False

    def future(self, index, depth):
        if self.status != 'verified':
            return []
        # the generator stops while trying to replenish the final preview
        end = min(index + depth, self.block_limit - 1)
        return self.candidates[0][index:end]


class Landing:
    def __init__(self, columns, points, moves, lines, cost=0.0,
                 discards=0, next_shape=None, bombs=0):
        self.columns = columns
        self.points = points
        self.moves = moves
        self.lines = lines
        self.cost = cost
        self.discards = discards
        self.next_shape = next_shape
        self.bombs = bombs


class SearchNode:
    def __init__(self, columns, points, first, value, first_value,
                 discards=0, cost=0.0, parent=None, step=None):
        self.columns = columns
        self.points = points
        self.first = first
        self.value = value
        self.first_value = first_value
        self.discards = discards
        self.cost = cost
        self.parent = parent
        self.step = step


class Planner:
    def __init__(self, width=10, height=24, beam_width=32, time_limit=0.4,
                 weights=None, well_column=None, setup_rows=8):
        self.width = width
        self.height = height
        self.beam_width = beam_width
        self.time_limit = time_limit
        self.templates = {}
        self.spawn_cells = {}
        self.last_depth = 0
        self.budget_stopped = False
        self.last_path = []
        self.well_column = well_column
        self.setup_rows = setup_rows
        self.weights = {
            'height': 0.20,
            'holes': 12.0,
            'bumpiness': 0.60,
            'danger': 1.0,
            'setup': 1.0,
            'well_fill': 0.0,
            'discard_cost': 6.4,
            'bomb_cost': 6.4,
            'destroyed_cell_cost': 1.6,
        }
        if weights is not None:
            for name, value in weights.items():
                if name not in self.weights or value < 0:
                    raise ValueError('Invalid search weight: ' + name)
                self.weights[name] = value
        for shape in Shape:
            self.make_templates(shape)

    def make_templates(self, shape):
        # build each rotation on an empty board once instead of at every search node
        rotations = [
            [],
            [Rotation.Clockwise],
            [Rotation.Clockwise, Rotation.Clockwise],
            [Rotation.Anticlockwise],
        ]
        if shape is Shape.B:
            rotations = [[]]
        templates = []
        for sequence in rotations:
            board = Board(self.width, self.height)
            board.next = Block(shape)
            board.place_next_block()
            self.spawn_cells[shape] = list(board.falling.cells)
            checks = [list(board.falling.cells)]
            for rotation in sequence:
                board.falling.rotate(rotation, board)
                checks.append(list(board.falling.cells))
                board.falling.move(Direction.Down, board)
                checks.append(list(board.falling.cells))
            templates.append({
                'cells': list(board.falling.cells),
                'left': board.falling.left,
                'right': board.falling.right,
                'moves': sequence,
                'points': board.score,
                'checks': checks,
            })
        self.templates[shape] = templates

    def columns_from_board(self, board):
        # bit y in a column is set when cell (x, y) is occupied
        columns = [0] * self.width
        for x, y in board.cells:
            columns[x] |= 1 << y
        return tuple(columns)

    def collides(self, columns, cells, dx=0, dy=0):
        for x, y in cells:
            x += dx
            y += dy
            if x < 0 or x >= self.width or y < 0 or y >= self.height:
                return True
            if columns[x] & (1 << y):
                return True
        return False

    def placements(self, columns, shape):
        if shape not in self.templates:
            return []
        if self.collides(columns, self.spawn_cells[shape]):
            return []

        results = []
        seen = set()
        for template in self.templates[shape]:
            allowed = True
            for cells in template['checks']:
                if self.collides(columns, cells):
                    allowed = False
                    break
            if not allowed:
                continue

            cells = template['cells']
            piece_width = template['right'] - template['left'] + 1
            for target in range(self.width - piece_width + 1):
                dx = 0
                dy = 0
                points = template['points']
                moves = template['moves'].copy()
                distance = target - template['left']
                direction = Direction.Right
                step = 1
                if distance < 0:
                    direction = Direction.Left
                    step = -1
                landed = False

                for index in range(abs(distance)):
                    blocked = self.collides(columns, cells, dx + step, dy)
                    if not blocked:
                        dx += step
                    moves.append(direction)
                    # sideways moves still trigger a step of gravity
                    if self.collides(columns, cells, dx, dy + 1):
                        landed = True
                        break
                    dy += 1
                    points += 1
                    if blocked:
                        break

                if not landed:
                    drop = self.height
                    for x, y in cells:
                        x += dx
                        y += dy
                        below = columns[x] >> (y + 1)
                        # the lowest set bit below the piece marks its first obstacle
                        free_rows = self.height - y - 1
                        if below:
                            free_rows = (below & -below).bit_length() - 1
                        drop = min(drop, free_rows)
                    dy += drop
                    points += drop
                    moves.append(Direction.Drop)

                cost = 0.0
                if shape is Shape.B:
                    # bombs remove cells instead of becoming part of the stack
                    bomb_x, bomb_y = cells[0]
                    placed, destroyed = self.explode(columns, bomb_x + dx, bomb_y + dy)
                    cost = destroyed * self.weights['destroyed_cell_cost']
                else:
                    placed = list(columns)
                    for x, y in cells:
                        placed[x + dx] |= 1 << (y + dy)
                result, lines = self.clear_rows(placed)
                if result is None:
                    continue
                points += [0, 25, 100, 400, 1600][lines]
                key = (result, points, cost)
                if key in seen:
                    continue
                seen.add(key)
                results.append(Landing(result, points, moves, lines, cost=cost))
        return results

    def clear_rows(self, columns):
        # matching set bits across every column identify full rows
        full_rows = columns[0]
        for column in columns[1:]:
            full_rows &= column
        if full_rows == 1:
            full_rows = 0
        lines = bin(full_rows).count('1')
        if lines > 4:
            return None, lines
        while full_rows:
            # clear one row then shift the rows above it down
            row_bit = full_rows & -full_rows
            above = row_bit - 1
            below = ~(row_bit | above)
            for x in range(self.width):
                columns[x] = (columns[x] & below) | ((columns[x] & above) << 1)
            full_rows ^= row_bit
        return tuple(columns), lines

    def explode(self, columns, bomb_x, bomb_y):
        result = list(columns)
        destroyed = 0
        first_row = max(0, bomb_y - 1)
        last_row = min(self.height - 1, bomb_y + 1)
        blast_mask = ((1 << (last_row - first_row + 1)) - 1) << first_row
        for x in range(max(0, bomb_x - 1), min(self.width, bomb_x + 2)):
            destroyed += bin(result[x] & blast_mask).count('1')
            result[x] &= ~blast_mask
            upper_mask = (1 << (bomb_y + 1)) - 1
            upper_count = bin(result[x] & upper_mask).count('1')
            lower_cells = result[x] >> bomb_y
            lowest = self.height - 1
            if lower_cells:
                lowest = bomb_y + (lower_cells & -lower_cells).bit_length() - 2
            result[x] &= ~upper_mask
            if upper_count:
                result[x] |= ((1 << upper_count) - 1) << (lowest - upper_count + 1)
        return result, destroyed

    def measure(self, columns):
        heights = []
        holes = 0
        for column in columns:
            height = 0
            if column:
                height = self.height - ((column & -column).bit_length() - 1)
                holes += height - bin(column).count('1')
            heights.append(height)
        return heights, holes

    def options(self, columns, shape, discards, remaining, allow_discards):
        if self.collides(columns, self.spawn_cells[shape]):
            return []
        choices = self.placements(columns, shape)
        # only basic play offers discards alongside normal landings
        if allow_discards and discards > 0 and remaining > 1:
            choices.append(Landing(columns, 0, [Action.Discard], 0,
                                   cost=self.weights['discard_cost'], discards=1))
        return choices

    def evaluate(self, columns, points, remaining):
        if remaining <= 0:
            return points / 25.0
        heights, holes = self.measure(columns)

        left_well = heights[0] < heights[1]
        right_well = heights[-1] < heights[-2]
        well = -1
        if left_well:
            well = 0
        if right_well and (well == -1 or heights[-1] < heights[0]):
            well = self.width - 1
        if self.well_column is not None:
            well = self.well_column

        bumpiness = 0
        # leave the scoring well out of the surface roughness calculation
        for x in range(self.width - 1):
            if x == well or x + 1 == well:
                continue
            bumpiness += abs(heights[x] - heights[x + 1])

        ready = 0
        if well != -1 and heights[well] == 0:
            for y in range(self.height - 1, -1, -1):
                complete = True
                for x in range(self.width):
                    if x != well and not (columns[x] & (1 << y)):
                        complete = False
                        break
                if not complete:
                    break
                ready += 1
                if ready == self.setup_rows:
                    break

        tallest = max(heights)
        danger = max(0, tallest - 10)
        complete_groups = ready // 4
        # each group represents another possible four row clear
        extra_rows = ready % 4
        setup = complete_groups * 64 + [0, 6, 14, 30][extra_rows]
        if remaining < 7:
            setup *= remaining / 7.0

        value = points / 25.0
        value += self.weights['setup'] * setup
        value -= self.weights['height'] * sum(heights)
        value -= self.weights['holes'] * holes
        value -= self.weights['bumpiness'] * bumpiness
        value -= self.weights['danger'] * danger * danger
        if well != -1:
            well_blocks = bin(columns[well]).count('1')
            value -= self.weights['well_fill'] * well_blocks
        return value

    def node_priority(self, node):
        return (node.value, node.first_value, node.points)

    def resource_factor(self, remaining):
        return min(1.0, max(0, remaining) / 8.0)

    def candidate_priority(self, candidate):
        return (candidate['value'], candidate['first_value'])

    def chance_search(self, board, remaining, root_width=6, preview_width=4,
                      allow_discards=False, root_landings=None):
        if board.next is None or remaining < 2:
            return self.search(board, [board.falling.shape], remaining,
                               allow_discards, root_landings)

        started = process_time()
        columns = self.columns_from_board(board)
        discards = 0
        if allow_discards:
            discards = board.discards_remaining
        if root_landings is None:
            root_landings = self.options(columns, board.falling.shape, discards,
                                         remaining, allow_discards)
        candidates = []
        for first in root_landings:
            preview_shape = board.next.shape
            if first.next_shape is not None:
                preview_shape = first.next_shape
            previews = []
            discards_left = discards - first.discards
            first_value = self.evaluate(first.columns, first.points, remaining - 1)
            first_value -= first.cost * self.resource_factor(remaining - 1)
            for second in self.options(first.columns, preview_shape, discards_left,
                                        remaining - 1, allow_discards):
                points = first.points + second.points
                cost = first.cost + second.cost
                value = self.evaluate(second.columns, points, remaining - 2)
                value -= cost * self.resource_factor(remaining - 2)
                node = SearchNode(second.columns, points, first, value, first_value,
                                  discards=discards_left - second.discards, cost=cost)
                previews.append(node)
            if not previews:
                continue
            previews.sort(key=self.node_priority, reverse=True)
            selected = previews[:preview_width]
            for node in previews:
                if node.discards < discards_left and node not in selected:
                    selected.append(node)
                    break
            candidates.append({
                'landing': first, 'previews': selected,
                'value': previews[0].value, 'first_value': first_value,
            })

        if not candidates:
            # if every preview would top out, finish the current piece for
            # the most real points available before the game ends
            self.last_depth = 1
            self.budget_stopped = False
            best = None
            for landing in root_landings:
                if best is None or landing.points > best.points:
                    best = landing
            return best
        candidates.sort(key=self.candidate_priority, reverse=True)
        best = candidates[0]['landing']
        self.last_depth = 2
        self.budget_stopped = False
        if remaining < 3:
            return best

        best_value = float('-inf')
        best_first_value = float('-inf')
        considered = 0
        for candidate in candidates[:root_width]:
            total_value = 0.0
            # the third piece is unknown now, but will be visible before the
            # preview is placed each possible shape gets its own best reply
            for shape in list(Shape)[:-1]:
                best_reply = -max(100.0, remaining * 6.4)
                for preview in candidate['previews']:
                    choices = self.options(preview.columns, shape, preview.discards,
                                           remaining - 2, allow_discards)
                    for third in choices:
                        points = preview.points + third.points
                        cost = preview.cost + third.cost
                        value = self.evaluate(third.columns, points, remaining - 3)
                        value -= cost * self.resource_factor(remaining - 3)
                        best_reply = max(best_reply, value)
                total_value += best_reply
            value = total_value / 7.0
            first_value = candidate['first_value']
            if value > best_value or (value == best_value and first_value > best_first_value):
                best_value = value
                best_first_value = first_value
                best = candidate['landing']
            considered += 1
            if process_time() - started >= self.time_limit:
                self.budget_stopped = considered < min(root_width, len(candidates))
                break
        self.last_depth = 3
        return best

    def search(self, board, shapes, remaining, allow_discards=False, root_landings=None,
               remember_path=False):
        started = process_time()
        columns = self.columns_from_board(board)
        discards = 0
        if allow_discards:
            discards = board.discards_remaining
        beam = [SearchNode(columns, 0, None, 0.0, 0.0, discards=discards)]
        best = None
        self.last_depth = 0
        self.budget_stopped = False
        self.last_path = []

        for depth in range(len(shapes)):
            # one search layer places the same next piece on each surviving board
            next_nodes = {}
            for node in beam:
                shape = shapes[depth]
                # basic play can prepare a bomb on the first move only
                if depth == 1 and node.first.next_shape is not None:
                    shape = node.first.next_shape
                choices = root_landings
                if depth != 0 or choices is None:
                    choices = self.options(node.columns, shape, node.discards,
                                           remaining - depth, allow_discards)
                for landing in choices:
                    points = node.points + landing.points
                    cost = node.cost + landing.cost
                    discards_left = node.discards - landing.discards
                    future_remaining = max(0, remaining - depth - 1)
                    value = self.evaluate(landing.columns, points, future_remaining)
                    value -= cost * self.resource_factor(future_remaining)
                    first = node.first
                    first_value = node.first_value
                    if first is None:
                        first = landing
                        first_value = value
                    parent = None
                    step = None
                    if remember_path:
                        parent = node
                        step = landing
                    child = SearchNode(landing.columns, points, first, value, first_value,
                                       discards=discards_left, cost=cost,
                                       parent=parent, step=step)
                    key = (landing.columns, discards_left, landing.next_shape)
                    # equal cells alone are not enough when resources or the preview differ
                    previous = next_nodes.get(key)
                    if previous is None or self.node_priority(child) > self.node_priority(previous):
                        next_nodes[key] = child

            if not next_nodes:
                break
            ordered = list(next_nodes.values())
            ordered.sort(key=self.node_priority, reverse=True)
            beam = ordered[:self.beam_width]
            # keep a few bomb setups alive until the blast can be evaluated next turn
            if depth == 0 and root_landings is not None:
                bomb_count = 0
                for node in ordered:
                    if node.first.next_shape is Shape.B:
                        if node not in beam:
                            beam.append(node)
                        bomb_count += 1
                        if bomb_count == 4:
                            break
            best = beam[0]
            self.last_depth = depth + 1
            if depth >= 1 and process_time() - started >= self.time_limit:
                self.budget_stopped = depth + 1 < len(shapes)
                break

        if best is None:
            return None
        if remember_path:
            # walk the parent links backwards to recover the winning sequence
            node = best
            while node.step is not None:
                self.last_path.append(node.step)
                node = node.parent
            self.last_path.reverse()
        return best.first


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
        self.basic_mode = basic_mode
        if fast_fallback:
            self.basic_mode = 'known'
        self.basic_weights = basic_weights
        self.basic_root_width = basic_root_width
        self.basic_preview_width = basic_preview_width
        self.basic_time_limit = basic_time_limit
        self.basic_setup_rows = basic_setup_rows
        # resource settings apply to basic play only
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
        # a seed must match the observed pieces before we trust its future
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
            # replay cached moves on a clone before using them on the real board
            if verified and self.whole_game and self.saved_plan:
                candidate = self.saved_plan.pop(0)
                if self.verify_plan(board, candidate):
                    landing = candidate
                    self.cached_decisions += 1
                    used_saved_plan = True
                else:
                    self.saved_plan = []
            if landing is None:
                landing = self.find_landing(board, shapes, remaining, verified)
            if landing is not None and (used_saved_plan or self.verify_plan(board, landing)):
                self.record_plan(landing, verified, used_saved_plan)
                return landing.moves
            self.last_failure = 'plan verification failed'
        except Exception as error:
            self.last_failure = type(error).__name__
        self.planning_failures += 1
        return self.fallback(board)

    def find_landing(self, board, shapes, remaining, verified):
        if verified and self.whole_game and self.whole_game_cpu < 300:
            # plan once and keep the rest of the path for later calls
            self.planner.beam_width = self.whole_game_width
            self.planner.time_limit = min(self.whole_game_time_limit,
                                          300 - self.whole_game_cpu)
            started = time.process_time()
            # predictive plans use normal pieces so the sequence stays unchanged
            landing = self.planner.search(board, shapes, remaining, remember_path=True)
            self.whole_game_cpu += time.process_time() - started
            self.saved_plan = self.planner.last_path[1:]
            self.full_plans += 1
            return landing

        if not verified:
            root_landings = self.resource_landings(board, remaining)
            if self.basic_mode != 'chance':
                return self.planner.search(board, shapes, remaining,
                                           self.allow_discards, root_landings)
            # the third shape is unknown so average over all seven possibilities
            return self.planner.chance_search(
                board, remaining, self.basic_root_width, self.basic_preview_width,
                self.allow_discards, root_landings,
            )

        if self.whole_game and self.whole_game_cpu >= 300:
            # leave time for actual play if the large planning budget runs out
            self.planner.beam_width = self.beam_width
            self.planner.time_limit = min(0.15, self.search_time_limit)
        return self.planner.search(board, shapes, remaining)

    def record_plan(self, landing, verified, used_saved_plan):
        if Action.Bomb in landing.moves:
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
        self.maximum_search_depth = max(self.maximum_search_depth, search_depth)
        if self.planner.budget_stopped and not used_saved_plan:
            self.budget_stops += 1

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
        if (not self.allow_bombs or board.bombs_remaining == 0
                or board.next is None or board.next.shape is Shape.B
                or remaining < 2 or board.falling.shape is Shape.B):
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
        result = (sandbox.score - board.score,
                  board.discards_remaining - sandbox.discards_remaining,
                  board.bombs_remaining - sandbox.bombs_remaining)
        if result != (landing.points, landing.discards, landing.bombs):
            return False
        if landing.next_shape is not None:
            if sandbox.falling is None or sandbox.falling.shape is not landing.next_shape:
                return False
        return self.planner.columns_from_board(sandbox) == landing.columns


SelectedPlayer = SearchPlayer
