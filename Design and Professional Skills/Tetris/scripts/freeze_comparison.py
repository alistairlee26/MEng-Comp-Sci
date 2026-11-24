import argparse
import hashlib
import json
from pathlib import Path
from secrets import token_hex


ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--games', type=int, default=10)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Choose a new output name; preserve existing frozen protocols')
    basic = json.loads((ROOT / 'configs/basic.json').read_text(encoding='utf-8'))[0]
    profiles = [basic]
    source_names = ('player.py', 'board.py', 'adversary.py', 'constants.py')
    sources = {}
    for name in source_names:
        sources[name] = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
    # collect parameters and source hashes before generating the holdout
    seeds = []
    for index in range(args.games):
        seeds.append('basic-validation-' + token_hex(16))
    protocol = {
        'python_version': '3.7.9', 'sources': sources,
        'profiles': profiles, 'seeds': seeds,
        'rules': [
            'All outcomes count, including early losses and crashes.',
            'No tuning against these seeds; changed parameters require a fresh batch.',
            'Authoritative string seeds control only the referee.',
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(protocol, indent=2) + '\n', encoding='utf-8')
    stem = args.output.with_suffix('')
    stem.with_name(stem.name + '-profiles.json').write_text(
        json.dumps(profiles, indent=2) + '\n', encoding='utf-8')
    stem.with_name(stem.name + '-seeds.json').write_text(
        json.dumps(seeds, indent=2) + '\n', encoding='utf-8')
    print('Frozen {} seeds and {} profiles in {}'.format(
        len(seeds), len(profiles), args.output))


if __name__ == '__main__':
    main()
