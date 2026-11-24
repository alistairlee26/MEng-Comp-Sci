from board import Board, Block, Direction, Rotation, Shape
from random import Random
from time import process_time


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
        if len(matching) == 1 and self.matched_through >= 5:
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


class Landing:
    def __init__(self, columns, points, moves, lines):
        self.columns = columns
        self.points = points
        self.moves = moves
        self.lines = lines


class SearchNode:
    def __init__(self, columns, points, first, value, first_value):
        self.columns = columns
        self.points = points
        self.first = first
        self.value = value
        self.first_value = first_value


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
        self.well_column = well_column
        self.setup_rows = setup_rows
        self.weights = {
            'height': 0.20,
            'holes': 12.0,
            'bumpiness': 0.60,
            'danger': 1.0,
            'setup': 1.0,
            'well_fill': 0.0,
        }
        if weights is not None:
            for name, value in weights.items():
                if name not in self.weights or value < 0:
                    raise ValueError('Invalid search weight: ' + name)
                self.weights[name] = value
        for shape in list(Shape)[:-1]:
            self.make_templates(shape)

    def make_templates(self, shape):
        rotations = [
            [],
            [Rotation.Clockwise],
            [Rotation.Clockwise, Rotation.Clockwise],
            [Rotation.Anticlockwise],
        ]
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

                placed = list(columns)
                for x, y in cells:
                    placed[x + dx] |= 1 << (y + dy)
                full_rows = placed[0]
                for column in placed[1:]:
                    full_rows &= column
                if full_rows == 1:
                    full_rows = 0
                lines = bin(full_rows).count('1')
                if lines > 4:
                    continue
                points += [0, 25, 100, 400, 1600][lines]

                while full_rows:
                    row_bit = full_rows & -full_rows
                    above = row_bit - 1
                    below = ~(row_bit | above)
                    for x in range(self.width):
                        placed[x] = (placed[x] & below) | ((placed[x] & above) << 1)
                    full_rows ^= row_bit

                result = tuple(placed)
                key = (result, points)
                if key in seen:
                    continue
                seen.add(key)
                results.append(Landing(result, points, moves, lines))
        return results

    def evaluate(self, columns, points, remaining):
        heights = []
        holes = 0
        for column in columns:
            height = 0
            if column:
                height = self.height - ((column & -column).bit_length() - 1)
                holes += height - bin(column).count('1')
            heights.append(height)

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

    def search(self, board, shapes, remaining):
        started = process_time()
        columns = self.columns_from_board(board)
        beam = [SearchNode(columns, 0, None, 0.0, 0.0)]
        best = None
        self.last_depth = 0
        self.budget_stopped = False

        for depth in range(len(shapes)):
            next_nodes = {}
            for node in beam:
                for landing in self.placements(node.columns, shapes[depth]):
                    points = node.points + landing.points
                    value = self.evaluate(landing.columns, points,
                                          max(0, remaining - depth - 1))
                    first = node.first
                    first_value = node.first_value
                    if first is None:
                        first = landing
                        first_value = value
                    child = SearchNode(landing.columns, points, first, value, first_value)
                    previous = next_nodes.get(landing.columns)
                    if previous is None or self.node_priority(child) > self.node_priority(previous):
                        next_nodes[landing.columns] = child

            if not next_nodes:
                break
            ordered = list(next_nodes.values())
            ordered.sort(key=self.node_priority, reverse=True)
            beam = ordered[:self.beam_width]
            best = beam[0]
            self.last_depth = depth + 1
            if depth >= 1 and process_time() - started >= self.time_limit:
                self.budget_stopped = depth + 1 < len(shapes)
                break

        if best is None:
            return None
        return best.first
