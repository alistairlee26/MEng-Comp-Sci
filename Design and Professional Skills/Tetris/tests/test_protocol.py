import json
import os
from pathlib import Path
import subprocess
import sys
from threading import Thread
import unittest

ROOT = Path(__file__).resolve().parent.parent


def pipe_lines(source, destination):
    try:
        for line in source:
            destination.write(line)
            destination.flush()
    except (BrokenPipeError, OSError, ValueError):
        pass
    finally:
        try:
            destination.close()
        except (OSError, ValueError):
            pass


class ProtocolTests(unittest.TestCase):
    def play(self, player_seed):
        referee_environment = os.environ.copy()
        referee_environment['SEED'] = 'protocol-live-game-725139'
        player_environment = os.environ.copy()
        player_environment.pop('SEED', None)
        if player_seed is not None:
            player_environment['SEED'] = player_seed

        player = subprocess.Popen(
            [sys.executable, '-u', str(ROOT / 'tests/protocol_player.py')],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            universal_newlines=True, cwd=str(ROOT), env=player_environment,
        )
        referee = subprocess.Popen(
            [sys.executable, '-u', str(ROOT / 'tests/protocol_referee.py')],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            universal_newlines=True, cwd=str(ROOT), env=referee_environment,
        )
        threads = [
            Thread(target=pipe_lines, args=(player.stdout, referee.stdin)),
            Thread(target=pipe_lines, args=(referee.stdout, player.stdin)),
        ]
        for thread in threads:
            thread.daemon = True
            thread.start()
        try:
            referee.wait(timeout=20)
            player.wait(timeout=20)
            referee_log = referee.stderr.read()
            player_log = player.stderr.read()
            self.assertEqual(referee.returncode, 0, referee_log)
            self.assertEqual(player.returncode, 0, player_log)
            self.assertIn('WON', referee_log)
            metrics = json.loads(player_log.strip().splitlines()[-1])
            self.assertEqual(metrics['failures'], 0)
            return metrics
        finally:
            for process in (player, referee):
                if process.poll() is None:
                    process.kill()
                process.wait()
            for thread in threads:
                thread.join(timeout=1)
            for stream in (player.stdout, player.stderr, referee.stdout, referee.stderr):
                stream.close()

    def test_matching_environment_seed_does_not_enable_prediction(self):
        metrics = self.play('protocol-live-game-725139')
        self.assertEqual(metrics['searches'], 11)
        self.assertEqual(metrics['fallback'], 0)

    def test_supplied_protocol_handles_a_missing_seed(self):
        metrics = self.play(None)
        self.assertEqual(metrics['searches'], 11)
        self.assertEqual(metrics['fallback'], 0)

    def test_unrelated_environment_seed_does_not_affect_basic_play(self):
        metrics = self.play('wrong-player-seed')
        self.assertEqual(metrics['searches'], 11)
        self.assertEqual(metrics['fallback'], 0)


if __name__ == '__main__':
    unittest.main()
