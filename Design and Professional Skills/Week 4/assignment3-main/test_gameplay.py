"""Scripted Tk gameplay checks; briefly opens and then closes the game window.

Run: python test_gameplay.py
Use --diagnose to print failures without stopping on the first one.
"""

import sys
from unittest.mock import patch

from fr_controller import Controller
from fr_model import Log
from fr_settings import Direction


def main():
    diagnose = '--diagnose' in sys.argv
    with patch('time.time', return_value=1000.0) as now:
        game = Controller()
        model = game.model

        def render():
            for view in game.views:
                view.update()
            game.root.update()

        def check(label, actual, expected):
            print(f'{label}: {actual!r}; expected {expected!r}', flush=True)
            if not diagnose:
                assert actual == expected, label

        try:
            render()
            game.root.focus_force()
            game.root.update()
            game.root.event_generate('<KeyPress-Left>')
            now.return_value += 0.2
            model.update()
            render()
            check('Left arrow completes a jump', model.frog.get_position(), (460, 600))

            model.frog.x = -1
            model.update()
            render()
            now.return_value += 1.1
            model.update()
            render()
            check('Respawn', model.frog.get_position(), (500, 600))

            model.restart()
            model.frog.x, model.frog.y = 500, 320
            model.logs = [Log(400, 320, 200, Direction.RIGHT, 2)]
            game.unregister_objects()
            model.cars.clear()
            game.register_river_object(model.logs[0])
            model.update()
            render()
            check('Landing on a log keeps seven lives', model.lives, 7)

            model.restart()
            model.frog.x, model.frog.y = 100, 120
            model.check_frog()
            render()
            check('Leftmost visible home accepts a frog', model.frogs_home, 1)

            if not diagnose:
                now.return_value += 1.1
                model.update()
                for x in [300, 500, 700, 900]:
                    model.frog.x, model.frog.y = x, 120
                    model.check_frog()
                    render()
                    now.return_value += 1.1
                    model.update()
                render()
                check('Five homes advance the level', model.level, 2)
                check('Old home sprites removed', len(game.views[0].home_frogs), 0)
                check('Car registry matches the current level', len(game.cars), len(model.cars))

            model.restart()
            now.return_value = model.end_time
            model.update()
            render()
            check('Time limit ends the game', model.game_running, False)
            model.game_over() if model.game_running else None
            game.root.event_generate('<KeyPress-r>')
            render()
            check('Restart resumes the game', model.game_running, True)
            check('Restart clears Game Over', game.views[0].messages_displayed, False)
        finally:
            game.root.destroy()


if __name__ == '__main__':
    main()
