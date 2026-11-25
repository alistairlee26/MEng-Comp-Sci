from board import Block, Direction, Rotation, Shape
from constants import BLOCK_LIMIT

NORMAL_SHAPES = tuple(shape for shape in Shape if shape is not Shape.B)
FIRST_MOVE_LIMIT = 6
PREVIEW_REPLY_LIMIT = 4

ROTATION_PLANS = (
    (),
    (Rotation.Clockwise,),
    (Rotation.Clockwise, Rotation.Clockwise),
    (Rotation.Anticlockwise,),
)

class Player:
    def choose_action(self, board):
        raise NotImplementedError


class MyPlayer(Player):
    def __init__(self, depth=2):
        if not isinstance(depth, int) or depth < 1:
            raise ValueError('depth must be a positive integer')
        self.depth = depth
        self.turn = 0

    def choose_action(self, board):
        moves = self.search(board)
        self.turn += 1
        return moves

    def search(self, board):
        _, moves = self.search_position(board, depth=self.depth)
        return moves


    # returns value of the position, moves to reach there
    def search_position(self, board, depth, remaining=None):
        if remaining is None:
            remaining = BLOCK_LIMIT - 1 - self.turn

        depth = min(depth, remaining)
        if depth <= 0 or board.falling is None:
            return self.evaluate(board, remaining), []
        if not board.alive:
            return self.top_out_value(board, remaining), []

        if depth >= 3 and board.next is not None:
            landings = self.shortlist(board, remaining)
            if not landings:
                return self.search_position(board, depth=2, remaining=remaining) # this is a fallback if the shortlist function fails
            loss_value = self.top_out_value(board, remaining)
        else:
            landings = ((moves, trial, None) for moves, trial in self.placements(board))

        best_moves = [Direction.Drop]
        best_rank = (False, -1_000_000, 0) # compares left to right
        for moves, trial, preview_boards in landings: # preview boards is populated after the boards of the previews are landed ????
            # landing the current piece spawns the preview
            if preview_boards is None:
                value, _ = self.search_position(trial, depth - 1, remaining - 1)
                rank = (trial.alive, value, -len(moves))
            else:
                value = self.expected_value(preview_boards, depth - 2, remaining - 2, loss_value)
                rank = (True, value, 0)  # keep shortlist order on a tie

            if rank > best_rank:
                best_rank = rank
                best_moves = moves
        return best_rank[1], best_moves

    def expected_value(self, preview_boards, depth, remaining, loss_value):
        total = 0.0
        for shape in NORMAL_SHAPES:
            scores = []
            for after_preview in preview_boards:
                # ordinary placements work the same with any preview
                trial = after_preview.clone()
                trial.next = Block(shape)
                trial.place_next_block()
                if not trial.alive:
                    continue

                if depth == 1:
                    value, _ = self.search_position(trial, depth, remaining)
                else:
                    # draw C's preview before placing C
                    draw_total = 0.0
                    for next_shape in NORMAL_SHAPES:
                        branch = trial.clone()
                        branch.next = Block(next_shape)
                        draw_value, _ = self.search_position(branch, depth, remaining)
                        draw_total += draw_value
                    value = draw_total / len(NORMAL_SHAPES)

                scores.append(value)
            total += max(scores, default=loss_value)
        return total / len(NORMAL_SHAPES)

    def top_out_value(self, board, remaining):
        return board.score / 25.0 - max(100, remaining * 6.4)

    def shortlist(self, board, remaining):
        def score(result):
            return result[0]

        candidates = []
        for moves, after_current in self.unique_placements(board):
            if not after_current.alive:
                continue

            replies = []
            for _, after_preview in self.unique_placements(after_current):
                value = self.evaluate(after_preview, remaining - 2)
                replies.append((value, after_preview))

            if not replies:
                continue

            replies.sort(key=score, reverse=True)
            rank = (replies[0][0], -len(moves))
            preview_boards = [trial for _, trial in replies[:PREVIEW_REPLY_LIMIT]]
            candidates.append((rank, moves, after_current, preview_boards))

        candidates.sort(key=score, reverse=True)
        return [
            (moves, after_current, preview_boards)
            for _, moves, after_current, preview_boards in candidates[:FIRST_MOVE_LIMIT]
        ]

    def unique_placements(self, board):
        unique = {}
        for moves, trial in self.placements(board):
            key = (frozenset(trial.cells), trial.score) # create a hashable dictionary key
            previous = unique.get(key)
            if previous is None or len(moves) < len(previous[0]):
                unique[key] = (moves, trial) # return the least moves one
        return unique.values() # yep

    def placements(self, board):
        for rotations in ROTATION_PLANS:
            rotated = board.clone()
            rotation_moves = []
            landed = False
            for rotation in rotations:
                rotation_moves.append(rotation)
                landed = rotated.rotate(rotation)
                if landed:
                    break
            if landed:
                yield rotation_moves, rotated
                continue

            left = rotated.falling.left
            right = rotated.falling.right
            for offset in range(-left, board.width - right):
                trial = rotated.clone()
                moves = rotation_moves.copy()
                direction = Direction.Left if offset < 0 else Direction.Right
                for _ in range(abs(offset)):
                    moves.append(direction)
                    if trial.move(direction): # returns true if the piece has landed after
                        break
                else: # gravity hasnt landed the pieces so drop the piece down
                    moves.append(Direction.Drop)
                    trial.move(Direction.Drop)
                yield moves, trial

    def evaluate(self, board, remaining=None):
        if remaining is None:
            remaining = BLOCK_LIMIT - 1 - self.turn

        # points
        value = board.score / 25.0
        if remaining <= 0:
            return value

        height_weight = 0.20
        hole_weight = 12.0
        bumpiness_weight = 0.60
        danger_weight = 1.0
        setup_weight = 1.0
        well_fill_weight = 0.0

        # column heights
        heights = [0] * board.width
        for x, y in board.cells:
            cell_height = board.height - y
            if cell_height > heights[x]:
                heights[x] = cell_height

        total_height = sum(heights)

        # Empty cells below each column's top block are holes.
        holes = total_height - len(board.cells)

        # pick the lower edge well
        well_column = None
        if board.width > 1:
            if heights[0] < heights[1]:
                well_column = 0

            right_edge = board.width - 1
            if heights[right_edge] < heights[right_edge - 1]:
                if well_column is None or heights[right_edge] < heights[well_column]:
                    well_column = right_edge

        # bumpiness outside the well
        bumpiness = 0
        for x in range(board.width - 1):
            if x == well_column or x + 1 == well_column:
                continue
            bumpiness += abs(heights[x] - heights[x + 1])

        # rows ready for a four-line clear
        setup = 0
        if well_column is not None and heights[well_column] == 0:
            ready_rows = 0
            for offset in range(min(8, board.height)):
                y = board.height - 1 - offset
                row_ready = True
                for x in range(board.width):
                    if x != well_column and (x, y) not in board.cells:
                        row_ready = False
                        break
                if not row_ready:
                    break
                ready_rows += 1

            full_groups = ready_rows // 4
            extra_rows = ready_rows % 4
            partial_rewards = (0, 6, 14, 30)
            setup = full_groups * 64 + partial_rewards[extra_rows]
            if remaining < 7:
                setup *= remaining / 7.0

        # danger above ten rows
        highest_column = max(heights)
        danger = max(0, highest_column - 10)

        # occupied cells in the well
        well_fill = 0
        if well_column is not None and well_fill_weight:
            for x, _ in board.cells:
                if x == well_column:
                    well_fill += 1

        value += setup_weight * setup
        value -= height_weight * total_height
        value -= hole_weight * holes
        value -= bumpiness_weight * bumpiness
        value -= danger_weight * danger * danger
        value -= well_fill_weight * well_fill
        return value


SelectedPlayer = MyPlayer
