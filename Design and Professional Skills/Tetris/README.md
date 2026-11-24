# Tetris basic heuristic player

The default is now `SelectedPlayer = HeuristicPlayer`. It uses the current piece,
the visible preview and the ordinary game rules. Seed prediction, seed verification,
whole-game planning, saved paths and predictive beam search have been removed.

The existing ordinary player's scoring weights, candidate limits, resource costs,
placement simulation and move verification are preserved. Bombs and discards remain
available. The older evaluator is retained as `FallbackPlayer` for emergency moves;
its engine-based landing generator also models immediate bomb preparations.

## Backup

Before changing the implementation, the complete project sources, local tools,
configuration, tests, documentation and reports were saved in:

[backups/before-basic-only-20261124-023855](backups/before-basic-only-20261124-023855)

That folder contains the original `player.py`, a `workspace.zip` archive and a hash
manifest. The archive excludes Git internals, installed Python environments,
temporary setup files, caches and previous backups. It includes the old predictive
launchers and configuration. The backup remains local and is ignored by Git.

## Run locally

| Action | Command |
| --- | --- |
| Watch the player | `.\scripts\watch.cmd` |
| Watch another local sequence | `.\scripts\watch.cmd -Seed 17` |
| Play manually | `.\scripts\play.cmd` |
| Watch in Tkinter | `.\scripts\watch-tk.cmd` |
| Watch in the terminal | `.\scripts\watch-terminal.cmd` |

The launchers use `.venv` in this folder. `-Seed` selects the game's local piece
sequence; the player never receives or reads that seed. Predictive launchers and
`-Predict` / `-LiveSearch` switches have been removed. Normal play calculates each
move as the game runs.

Arrows move or rotate, Space drops, z rotates anticlockwise, d discards, b prepares
a bomb, and Esc exits.

## Set up on another computer

Clone or download [MEng-Comp-Sci on GitHub](https://github.com/alistairlee26/MEng-Comp-Sci),
then open `Design and Professional Skills/Tetris`. The full workspace is stored
there as ordinary files, including local tools, tests, reports and backups.

Create a fresh environment using Python 3.11, the version used locally:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-local.txt
.\scripts\watch.cmd
```

Run the tests with `.\.venv\Scripts\python.exe -m unittest discover -s tests -v`.
The portable Python 3.7 interpreter under `.setup` is not included; testing under
3.7.9 requires installing that interpreter separately.

The GitHub clone is for development. It does not contain the separate GitLab
checkout metadata or its local submission hooks, and pushing this clone goes to
GitHub. For a later university submission, clone the GitLab repository separately
and copy the intended `player.py` into that submission checkout.

All existing workspace files are tracked by the parent GitHub repository. The
Tetris ignore rules keep new supporting files out of submissions; to publish a new
supporting file to GitHub, deliberately add its exact path with `git add -f` from
the parent repository. On the laptop, `git -C ..` from Tetris addresses the parent
GitHub repository; plain `git` inside Tetris still addresses the GitLab checkout.

## Read the code

All submitted bot logic remains in [player.py](player.py).

| Class | Purpose |
| --- | --- |
| `Player` | Defines the engine's action-selection interface |
| `RandomPlayer` | Retains the supplied random benchmark opponent |
| `FallbackPlayer` | Provides the original emergency heuristic and engine landings |
| `Landing` | Records one placement's cells, points, moves and resource use |
| `Preview` | Records a possible result after placing the visible preview |
| `Planner` | Simulates placements and evaluates the short search |
| `HeuristicPlayer` | Runs the ordinary search, handles resources and verifies moves |

Start with `HeuristicPlayer.choose_action`, then `Planner.search`,
`Planner.evaluate` and `Planner.placements`.

## How one decision works

1. **Count the remaining pieces.** The generator's 400 draws include an unplayable
   final preview, leaving 399 decisions. Discards consume that same supply. The
   player advances its turn counter once per decision.
2. **Represent the board compactly.** Each column is an integer whose set bits
   indicate occupied rows. Collision checks, drops and row removal use these bits.
3. **Generate reachable landings.** Templates describe the available rotations.
   Each horizontal target is simulated with the engine's compulsory gravity after
   steering and rotation. Plans stop immediately if that gravity lands the piece.
4. **Include resource choices.** An available discard is another current-piece
   choice. Bomb preparation is considered when the stack is at least fourteen
   rows high or contains at least three holes. Engine clones generate the moves
   after preparing a bomb, including its gravity step and replaced preview.
5. **Examine the preview.** For every current-piece choice, try the preview's
   placements. Keep the best four responses, with room for an additional discard
   response. Rank the current choices and retain the best six.
6. **Consider the unknown third piece.** Independently test each of the seven
   possible normal shapes. Each shape gets its own best response, because it will
   be visible before the currently previewed piece is played. Average those seven
   values to rank the current choice. This does not assume a known future sequence.
7. **Respect the computation budget.** Search checks CPU time after completing a
   current-choice evaluation, with a default limit of 0.5 CPU seconds per decision.
   It can finish that evaluation slightly beyond the limit. Machine load and
   interpreter speed can therefore affect how many candidates finish.
8. **Handle short or blocked futures.** With one playable piece or no preview,
   compare immediate placements directly. With only two pieces left, stop after
   the preview. If every preview would lose, choose the current landing with the
   most immediate points.
9. **Verify the selected moves.** Replay them on an actual engine clone. Confirm
   that the final action lands the piece and that cells, score, resource use and
   any forced bomb preview match the simulation. If search fails, use the original
   emergency heuristic.

Only the current moves are returned. The next call searches the new board again.

## Evaluation and scoring

The engine awards one point for each descended row. Simultaneously clearing one,
two, three or four rows earns 25, 100, 400 or 1,600 points. The planner applies those
actual rewards before evaluating the resulting board.

For non-terminal positions, the evaluation starts with earned points divided by
25, adds the estimated value of prepared four-row clears and subtracts penalties:

| Main weight | Default |
| --- | ---: |
| Total column height | 0.20 |
| Holes | 12.0 |
| Surface bumpiness | 0.60 |
| Squared height above ten rows | 1.0 |
| Prepared-row reward multiplier | 1.0 |
| Occupied scoring-well cells | 0.0 |

The planner chooses a possible left or right edge well and excludes that well from
surface bumpiness. Consecutive bottom rows filled everywhere except the empty well
receive setup values of 6, 14 and 30 for partial groups, and 64 per complete group
of four. Up to eight prepared rows count. The setup reward fades over the last
seven playable pieces; at the end only actual points count.

A discarded or replaced tetromino costs 6.4 evaluation units, while a bomb blast
costs 1.6 per destroyed cell. These are estimates of sacrificed scoring material,
not deductions from the actual game score. The costs fade over the last eight
pieces. The player can therefore sensibly finish with unused resources.

The original emergency evaluator has its own `FALLBACK_WEIGHTS`. Its different
hole and setup calculations are preserved to avoid changing emergency behaviour.

## Configuration and diagnostics

Normal defaults live directly in `HeuristicPlayer.__init__` and `Planner.__init__`.
Benchmark profiles in [configs/basic.json](configs/basic.json) and
[configs/no-resources.json](configs/no-resources.json) are loaded only when explicitly
passed to the experiment tool.

The main constructor accepts `root_width`, `preview_width`, `time_limit`, `weights`,
`setup_rows`, `well_column`, `allow_discards`, `allow_bombs` and `block_limit`.
`fallback_candidates` and `fallback_weights` configure the emergency player.
There are no prediction or whole-game options.

`search_decisions` counts verified ordinary plans. `fallback_decisions` counts
actual emergency calls; older reports counted normal visible searches differently.
Other counters record failures, completed search depth and CPU-budget stops.

## Verification

Run the tests with the grader's Python version:

```powershell
.\.setup\python37\python.exe -m unittest discover -s tests -v
```

The tests cover the fast simulator against the engine, resource handling, missing
previews, end-game scoring, fallback behaviour, and the two-process referee/player
protocol. Supplying a matching, incorrect or missing environment seed always uses
the same ordinary player.

The full-game regression checks preserved every decision and board state for seed
42 at 56,947 points and a comparison seed at 36,436 points, including that game's
early loss. These are preservation checks rather than new tuning results.
Detailed checks are recorded in [reports/basic-only-refactor.json](reports/basic-only-refactor.json).
Earlier reports remain historical evidence for their recorded source versions.

Run a short local benchmark:

```powershell
.\.venv\Scripts\python.exe scripts/benchmark.py --player selected --seeds 42 --blocks 30
```

Run ordinary profile experiments:

```powershell
.\.venv\Scripts\python.exe scripts/experiment.py --profiles configs/basic.json --seeds development-0 --workers 1 --output .setup/basic-experiment.json
```

The benchmark seeds control the referee only. Local experiments may use separate
processes for independent games; the submitted player uses one process and only
the Python standard library.

## Git workflow

Supporting files and backups stay local. Only `player.py` changes should be staged
for a submission; original starter game files remain tracked. Local commit and
push hooks reject changes outside `player.py`.

```powershell
git add -- player.py
git commit -m "Simplify basic player"
git push
```

Pushing can queue a grader run. This refactor has not been pushed. See
[docs/git-workflow.md](docs/git-workflow.md) for the local guards and their scope.
