from board import Board, Block, Direction, Rotation, Shape, Action
from random import Random
from time import process_time


class SeedPredictor:
    def __init__(self, seed, block_limit):
        self.candidates = []
        self.matched_through = -1
        self.status = 'missing'
        self.block_limit = block_limit
        self.replacements = set()
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
            if preview is not None:
                if index + 1 >= len(sequence):
                    continue
                if sequence[index + 1] is not preview:
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
        observed_random_pieces = self.matched_through + 1
        for position in self.replacements:
            if position <= self.matched_through:
                observed_random_pieces -= 1
        if len(matching) == 1 and observed_random_pieces >= 6:
            self.status = 'verified'
            return True
        self.status = 'checking'
        return False

    def future(self, index, depth):
        if self.status != 'verified':
            return []
        # The generator stops while trying to replenish the final preview.
        end = min(index + depth, self.block_limit - 1)
        return self.candidates[0][index:end]

    def replace(self, index, shape):
        for sequence in self.candidates:
            if index < len(sequence):
                sequence[index] = shape
        self.replacements.add(index)


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
                 discards=0, cost=0.0, parent=None, step=None,
                 bombs=0, next_shape=None):
        self.columns = columns
        self.points = points
        self.first = first
        self.value = value
        self.first_value = first_value
        self.discards = discards
        self.cost = cost
        self.parent = parent
        self.step = step
        self.bombs = bombs
        self.next_shape = next_shape


class Planner:
    def __init__(self, width=10, height=24, beam_width=32, time_limit=0.4,
                 weights=None, well_column=None, setup_rows=8):
        self.width = width
        self.height = height
        self.beam_width = beam_width
        self.time_limit = time_limit
        self.templates = {}
        self.bomb_templates = {}
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
            if shape is not Shape.B:
                self.make_templates(shape, prepare_bomb=True)

    def make_templates(self, shape, prepare_bomb=False):
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
            prefix = []
            if prepare_bomb:
                board.next = Block(Shape.O)
                board.bomb()
                prefix = [Action.Bomb]
                checks.append(list(board.falling.cells))
            for rotation in sequence:
                board.falling.rotate(rotation, board)
                checks.append(list(board.falling.cells))
                board.falling.move(Direction.Down, board)
                checks.append(list(board.falling.cells))
            templates.append({
                'cells': list(board.falling.cells),
                'left': board.falling.left,
                'right': board.falling.right,
                'moves': prefix + sequence,
                'points': board.score,
                'checks': checks,
            })
        if prepare_bomb:
            self.bomb_templates[shape] = templates
        else:
            self.templates[shape] = templates

    def columns_from_board(self, board):
        # Bit y in a column is set when cell (x, y) is occupied.
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

    def placements(self, columns, shape, prepare_bomb=False):
        if shape not in self.templates:
            return []
        if self.collides(columns, self.spawn_cells[shape]):
            return []

        results = []
        seen = set()
        templates = self.templates
        if prepare_bomb:
            templates = self.bomb_templates
        for template in templates[shape]:
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
                        free_rows = self.height - y - 1
                        if below:
                            free_rows = (below & -below).bit_length() - 1
                        drop = min(drop, free_rows)
                    dy += drop
                    points += drop
                    moves.append(Direction.Drop)

                cost = 0.0
                bombs = 0
                next_shape = None
                if prepare_bomb:
                    cost = self.weights['bomb_cost']
                    bombs = 1
                    next_shape = Shape.B
                if shape is Shape.B:
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
                results.append(Landing(result, points, moves, lines, cost=cost,
                                       bombs=bombs, next_shape=next_shape))
        return results

    def clear_rows(self, columns):
        full_rows = columns[0]
        for column in columns[1:]:
            full_rows &= column
        if full_rows == 1:
            full_rows = 0
        lines = bin(full_rows).count('1')
        if lines > 4:
            return None, lines
        while full_rows:
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

    def options(self, columns, shape, discards, remaining, allow_discards,
                bombs=0, allow_bombs=False):
        if self.collides(columns, self.spawn_cells[shape]):
            return []
        choices = self.placements(columns, shape)
        if allow_bombs and bombs > 0 and remaining > 1 and shape is not Shape.B:
            heights, holes = self.measure(columns)
            if max(heights) >= 14 or holes >= 3:
                choices.extend(self.placements(columns, shape, prepare_bomb=True))
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
            # If every preview would top out, finish the current piece for
            # the most real points available before the game ends.
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
            # The third piece is unknown now, but will be visible before the
            # preview is placed. Each possible shape gets its own best reply.
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
               remember_path=False, allow_bombs=False):
        started = process_time()
        columns = self.columns_from_board(board)
        discards = 0
        if allow_discards:
            discards = board.discards_remaining
        bombs = board.bombs_remaining
        beam = [SearchNode(columns, 0, None, 0.0, 0.0, discards=discards, bombs=bombs)]
        best = None
        self.last_depth = 0
        self.budget_stopped = False
        self.last_path = []

        for depth in range(len(shapes)):
            next_nodes = {}
            for node in beam:
                shape = shapes[depth]
                if node.next_shape is not None:
                    shape = node.next_shape
                choices = root_landings
                if depth != 0 or choices is None:
                    choices = self.options(node.columns, shape, node.discards,
                                           remaining - depth, allow_discards,
                                           node.bombs, allow_bombs)
                for landing in choices:
                    points = node.points + landing.points
                    cost = node.cost + landing.cost
                    discards_left = node.discards - landing.discards
                    bombs_left = node.bombs - landing.bombs
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
                                       parent=parent, step=step, bombs=bombs_left,
                                       next_shape=landing.next_shape)
                    key = (landing.columns, discards_left, bombs_left, landing.next_shape)
                    previous = next_nodes.get(key)
                    if previous is None or self.node_priority(child) > self.node_priority(previous):
                        next_nodes[key] = child

            if not next_nodes:
                break
            ordered = list(next_nodes.values())
            ordered.sort(key=self.node_priority, reverse=True)
            beam = ordered[:self.beam_width]
            if depth == 0 or allow_bombs:
                bomb_count = 0
                for node in ordered:
                    if node.next_shape is Shape.B:
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
            node = best
            while node.step is not None:
                self.last_path.append(node.step)
                node = node.parent
            self.last_path.reverse()
        return best.first
