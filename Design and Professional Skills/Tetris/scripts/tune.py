# Compare basic fallback weights on training seeds, then validate the winner.

import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
from pathlib import Path
import random
from statistics import median
import subprocess
import sys
import types

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from player import FallbackPlayer
from scripts.benchmark import run_game


def make_profiles(trials):
    profiles = [
        {
            'name': 'wider-search',
            'lookahead_candidates': 12,
            'weights': {
                'height': 0.45, 'holes': 6.0, 'buried_holes': 0.25,
                'bumpiness': 0.35, 'danger': 0.75, 'setup': 1.0,
                'setup_hole_discount': 0.0, 'hole_risk': 0.0,
            },
        },
        {
            'name': 'balanced',
            'lookahead_candidates': 12,
            'weights': {
                'height': 0.45, 'holes': 8.0, 'buried_holes': 0.30,
                'bumpiness': 0.35, 'danger': 1.0, 'setup': 0.85,
                'setup_hole_discount': 0.10, 'hole_risk': 1.0,
            },
        },
        {
            'name': 'cautious',
            'lookahead_candidates': 12,
            'weights': {
                'height': 0.50, 'holes': 10.0, 'buried_holes': 0.40,
                'bumpiness': 0.40, 'danger': 1.25, 'setup': 0.65,
                'setup_hole_discount': 0.15, 'hole_risk': 1.5,
            },
        },
    ]
    generator = random.Random(20261123)
    while len(profiles) < trials:
        weights = {}
        for name, value in profiles[1]['weights'].items():
            weights[name] = round(value * generator.uniform(0.7, 1.3), 4)
        profiles.append({
            'name': 'trial-' + str(len(profiles) + 1),
            'lookahead_candidates': 12,
            'weights': weights,
        })
    return profiles[:trials]


def load_baseline(reference):
    # Read an immutable version of player.py from this repository's history.
    source = subprocess.check_output(
        ['git', 'show', reference + ':player.py'], cwd=str(ROOT),
        universal_newlines=True,
    )
    module = types.ModuleType('tuning_baseline')
    exec(compile(source, reference + ':player.py', 'exec'), module.__dict__)
    return module.SelectedPlayer


def run_job(profile, seed, block_limit, baseline_reference):
    try:
        if profile['name'] == 'submitted':
            player_class = load_baseline(baseline_reference)
            options = {}
        else:
            player_class = FallbackPlayer
            options = {
                'lookahead_candidates': profile['lookahead_candidates'],
                'weights': profile['weights'],
                'block_limit': block_limit,
            }
        result = run_game(player_class, seed, block_limit, options)
        result['profile'] = profile['name']
        return result
    except Exception as error:
        return {
            'profile': profile['name'], 'seed': seed, 'score': 0,
            'status': 'error', 'error': repr(error),
        }


def compare(profiles, seeds, args):
    results = []
    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        futures = []
        for profile in profiles:
            for seed in seeds:
                futures.append(executor.submit(
                    run_job, profile, seed, args.blocks, args.baseline_ref
                ))
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(json.dumps(result, sort_keys=True), flush=True)
    return results


def summarise(profiles, results):
    summaries = []
    for profile in profiles:
        games = []
        for result in results:
            if result['profile'] == profile['name']:
                games.append(result)
        scores = []
        completed = 0
        errors = 0
        for game in games:
            scores.append(game['score'])
            if game['status'] == 'block-limit':
                completed += 1
            if game['status'] == 'error':
                errors += 1
        summaries.append({
            'profile': profile['name'],
            'median': median(scores),
            'minimum': min(scores),
            'completed': completed,
            'games': len(games),
            'errors': errors,
        })
    return summaries


def main():
    parser = argparse.ArgumentParser(description='Compare basic fallback weights')
    parser.add_argument('--train-seeds', nargs='+', type=int, default=[0, 1, 2, 42])
    parser.add_argument('--validation-seeds', nargs='+', type=int,
                        default=[100, 101, 102])
    parser.add_argument('--trials', type=int, default=3)
    parser.add_argument('--workers', type=int, default=3)
    parser.add_argument('--blocks', type=int, default=400)
    parser.add_argument('--baseline-ref', default='157dc6f')
    parser.add_argument('--output', type=Path, default=ROOT / '.setup/tuning-results.json')
    args = parser.parse_args()
    if set(args.train_seeds).intersection(args.validation_seeds):
        parser.error('Training and validation seeds must be separate')
    if args.trials < 1 or args.workers < 1 or args.blocks < 2:
        parser.error('Use positive trials/workers and at least two blocks')

    profiles = make_profiles(args.trials)
    training_results = compare(profiles, args.train_seeds, args)
    training_summary = summarise(profiles, training_results)
    print('Training summary: ' + json.dumps(training_summary), flush=True)

    winner = None
    best_key = None
    for summary in training_summary:
        if summary['errors']:
            continue
        key = (summary['median'], summary['minimum'], summary['completed'])
        if best_key is None or key > best_key:
            best_key = key
            for profile in profiles:
                if profile['name'] == summary['profile']:
                    winner = profile
    if winner is None:
        raise RuntimeError('Every profile encountered an error')

    print('Selected using training seeds only: ' + json.dumps(winner), flush=True)
    validation_profiles = [{'name': 'submitted'}, winner]
    validation_results = compare(validation_profiles, args.validation_seeds, args)
    validation_summary = summarise(validation_profiles, validation_results)
    report = {
        'baseline_ref': args.baseline_ref,
        'block_limit': args.blocks,
        'train_seeds': args.train_seeds,
        'validation_seeds': args.validation_seeds,
        'profiles': profiles,
        'selected': winner,
        'training_results': training_results,
        'training_summary': training_summary,
        'validation_results': validation_results,
        'validation_summary': validation_summary,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    weights_path = args.output.with_name(args.output.stem + '-weights.json')
    weights_path.write_text(json.dumps(winner['weights'], indent=2) + '\n',
                            encoding='utf-8')
    print('Validation summary: ' + json.dumps(validation_summary), flush=True)
    print('Report: ' + str(args.output), flush=True)
    print('Selected weights: ' + str(weights_path), flush=True)


if __name__ == '__main__':
    main()
