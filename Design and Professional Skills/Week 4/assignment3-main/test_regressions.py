"""Run with python -m unittest -v test_regressions (no extra packages)."""

import unittest
from unittest.mock import Mock, patch

import fr_model
import test_model
from fr_controller import Controller
from fr_model import Frog, Log, Model, Turtle
from fr_settings import CANVAS_WIDTH, GRID_SIZE, Direction
from fr_view import TimeView, TurtleView


class GameplayTests(unittest.TestCase):
    def setUp(self):
        self.clock = patch('time.time', return_value=1000.0)
        self.now = self.clock.start()
        self.addCleanup(self.clock.stop)
        self.controller = Mock()
        self.model = Model(self.controller)
        fr_model.speed = 1.0

    def finish_pause(self):
        self.now.return_value = self.model.pause_end_time + 0.01
        self.model.update()

    def test_respawn_after_death(self):
        self.model.frog.x = -1
        self.model.update()
        self.assertEqual(self.model.lives, 6)
        self.assertTrue(self.model.paused)
        self.finish_pause()
        self.assertEqual(self.model.frog.get_position(), (500, 600))
        self.model.update()
        self.assertEqual(self.model.lives, 6)

    def test_safe_landing_and_riding(self):
        for cls, direction in [(Log, Direction.RIGHT), (Turtle, Direction.LEFT)]:
            with self.subTest(platform=cls.__name__):
                platform = cls(400, 320, 200, direction, 2)
                self.model.logs = [platform]
                self.model.frog = Frog(500, 320)
                self.model.check_frog_crossing_river()
                self.assertEqual(self.model.lives, 7)
                platform.move()
                self.model.check_frog_crossing_river()
                self.assertEqual(self.model.frog.x, 502 if direction == Direction.RIGHT else 498)

    def test_open_water_is_still_fatal(self):
        self.model.logs = []
        self.model.frog.y = 320
        self.model.check_frog()
        self.assertEqual(self.model.lives, 6)

    def test_all_five_visible_homes_advance_level(self):
        self.assertEqual(self.model.homes_x, [100, 300, 500, 700, 900])
        self.assertEqual(len(self.model.homes_occupied), 5)
        for x in [100, 300, 500, 700, 900]:
            self.model.frog.x, self.model.frog.y = x, 120
            self.model.check_frog()
            self.finish_pause()
        self.assertEqual(self.model.level, 2)
        self.assertEqual(self.model.lives, 7)
        self.assertEqual(self.model.frogs_home, 0)
        self.assertEqual(self.model.homes_occupied, [False] * 5)
        self.assertGreaterEqual(self.model.score, 1000)

    def test_occupied_home_and_bank_are_fatal(self):
        self.model.homes_occupied[2] = True
        self.model.frog.x, self.model.frog.y = 500, 120
        self.model.check_frog()
        self.assertEqual(self.model.lives, 6)
        self.finish_pause()
        self.model.frog.x, self.model.frog.y = 200, 120
        self.model.check_frog()
        self.assertEqual(self.model.lives, 5)

    def test_restart_after_game_over_accepts_input(self):
        self.model.score = 900
        self.model.game_over()
        self.model.restart()
        self.assertTrue(self.model.game_running)
        self.assertEqual((self.model.level, self.model.score, self.model.lives), (1, 0, 7))
        self.model.move_frog(Direction.LEFT)
        self.assertEqual(self.model.frog.x, 480)

    def test_reset_cancels_jump_and_log_attachment(self):
        frog = self.model.frog
        frog.move_with(Log(400, 600, 200, Direction.RIGHT, 1))
        frog.move(Direction.UP)
        self.model.restart()
        self.now.return_value += 0.2
        frog.finish_move()
        self.assertEqual(frog.get_position(), (500, 600))
        self.assertFalse(frog.moving)
        self.assertIsNone(frog.on_log())

    def test_timeout_ends_game_once(self):
        self.now.return_value = self.model.end_time
        self.model.update()
        self.assertFalse(self.model.game_running)
        self.model.update()
        self.controller.game_over.assert_called_once()

    def test_timeout_during_death_pause(self):
        self.now.return_value = self.model.end_time - 0.5
        self.model.died()
        self.now.return_value += 0.5
        self.model.update()
        self.assertFalse(self.model.game_running)
        self.assertFalse(self.model.paused)

    def test_completed_level_can_advance_during_celebration(self):
        self.model.frogs_home = 5
        self.now.return_value = self.model.end_time - 0.5
        self.model.level_finished()
        self.finish_pause()
        self.assertEqual(self.model.level, 2)
        self.assertTrue(self.model.game_running)

    def test_downward_exit_costs_one_life(self):
        self.model.move_frog(Direction.DOWN)
        self.now.return_value += 0.2
        self.model.update()
        self.model.update()
        self.assertEqual(self.model.lives, 6)
        self.finish_pause()
        self.assertEqual(self.model.frog.get_position(), (500, 600))

    def test_later_levels_can_be_generated(self):
        for level in [6, 7, 8, 20]:
            with self.subTest(level=level):
                self.model.level = level
                self.model.reset_level()
                self.assertTrue(self.model.logs)
                self.assertTrue(all(obj.width >= 80 for obj in self.model.logs))

    def test_turtles_draw_inside_their_collision_extent(self):
        canvas = Mock()
        turtle = Turtle(400, 320, GRID_SIZE * 2, Direction.LEFT, 1)
        TurtleView(canvas, turtle, ['first_image', 'second_image'])
        centers = [call.args[0] for call in canvas.create_image.call_args_list]
        self.assertEqual(centers, [GRID_SIZE / 2, GRID_SIZE * 1.5])

    def test_time_bar_fits_and_disappears_at_expiry(self):
        canvas = Mock()
        timer = TimeView(canvas)
        timer.reset(self.model.end_time)
        timer.update(1000)
        full = canvas.create_rectangle.call_args.args
        self.assertGreaterEqual(full[0], 0)
        self.assertLessEqual(full[2], CANVAS_WIDTH)
        timer.update(1060)
        half = canvas.create_rectangle.call_args.args
        self.assertAlmostEqual(half[2] - half[0], (full[2] - full[0]) / 2)
        timer.update(1120)
        empty = canvas.create_rectangle.call_args.args
        self.assertEqual(empty[0], empty[2])

    def test_controller_discards_old_cars(self):
        controller = Controller.__new__(Controller)
        controller.cars = [object()]
        controller.river_objects = [object()]
        controller.views = [Mock()]
        controller.unregister_objects()
        self.assertEqual(controller.cars, [])
        self.assertEqual(controller.river_objects, [])
        controller.views[0].unregister_objects.assert_called_once()


class StarterTests(unittest.TestCase):
    def test_original_tests(self):
        for name in ['test_river_object', 'test_car', 'test_frog',
                     'test_model_pause', 'test_model']:
            with self.subTest(name=name):
                fr_model.speed = 1.0
                getattr(test_model, name)()


if __name__ == '__main__':
    unittest.main()
