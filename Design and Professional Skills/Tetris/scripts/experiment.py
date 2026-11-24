import argparse
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
from pathlib import Path
from statistics import median
import sys
import hashlib
import platform

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from player import HeuristicPlayer
from scripts.benchmark import run_game


def run_case(profile, seed, block_limit):
    options = profile.get('options', {}).copy()
    options['block_limit'] = block_limit
    try:
        result = run_game(HeuristicPlayer, seed, block_limit, options)
        result['profile'] = profile['name']
        return result
    except Exception as error:
        return {
            'profile': profile['name'], 'seed': seed, 'score': 0,
            'status': 'error', 'error': repr(error),
        }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--profiles', type=Path, required=True)
    parser.add_argument('--seeds', nargs='+')
    parser.add_argument('--seed-file', type=Path)
    parser.add_argument('--blocks', type=int, default=400)
    parser.add_argument('--workers', type=int, default=3)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--integer-seeds', action='store_true')
    args = parser.parse_args()
    profiles = json.loads(args.profiles.read_text(encoding='utf-8'))
    seeds = args.seeds
    if args.seed_file is not None:
        seeds = json.loads(args.seed_file.read_text(encoding='utf-8'))
    if not seeds:
        parser.error('Supply --seeds or --seed-file')
    if args.integer_seeds:
        seeds = [int(seed) for seed in seeds]

    source_hashes = {}
    for name in ('player.py', 'board.py', 'adversary.py', 'constants.py'):
        source_hashes[name] = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
    report = {
        'profiles': profiles, 'seeds': seeds, 'results': [], 'complete': False,
        'python_version': platform.python_version(), 'source_hashes': source_hashes,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        jobs = []
        for profile in profiles:
            for seed in seeds:
                jobs.append(executor.submit(run_case, profile, seed, args.blocks))
        for job in as_completed(jobs):
            result = job.result()
            report['results'].append(result)
            args.output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
            print(json.dumps(result, sort_keys=True), flush=True)

    summaries = []
    for profile in profiles:
        scores = []
        completed = 0
        errors = 0
        for result in report['results']:
            if result['profile'] != profile['name']:
                continue
            scores.append(result['score'])
            if result['status'] == 'block-limit':
                completed += 1
            if result['status'] == 'error':
                errors += 1
        summaries.append({
            'profile': profile['name'], 'median': median(scores),
            'minimum': min(scores), 'maximum': max(scores),
            'completed': completed, 'games': len(scores), 'errors': errors,
        })
    report['summary'] = summaries
    report['complete'] = True
    args.output.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(summaries), flush=True)


if __name__ == '__main__':
    main()
