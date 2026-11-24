import argparse
import ast
import hashlib
import json
from pathlib import Path
from statistics import median


ROOT = Path(__file__).resolve().parent.parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--protocol', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--source-root', type=Path, default=ROOT)
    args = parser.parse_args()
    report = json.loads(args.report.read_text(encoding='utf-8'))
    protocol = json.loads(args.protocol.read_text(encoding='utf-8'))
    require(report['complete'], 'Comparison is unfinished')
    require(report['python_version'] == '3.7.9', 'Use the grading interpreter version')
    require(report['profiles'] == protocol['profiles'], 'Profiles changed after freezing')
    require(report['seeds'] == protocol['seeds'], 'Seed manifest changed')
    require(len(set(report['seeds'])) == len(report['seeds']), 'Duplicate seeds')
    require(len(report['seeds']) >= 10, 'Use at least ten fresh paired games')
    require(report['source_hashes'] == protocol['sources'], 'Runtime sources changed')
    require(report['baseline_hashes'] == protocol['baseline_sources'], 'Baseline changed')
    for names, folder in ((protocol['sources'], args.source_root),
                          (protocol['baseline_sources'], ROOT)):
        for name, expected in names.items():
            digest = hashlib.sha256((folder / name).read_bytes()).hexdigest()
            require(digest == expected, 'Frozen source changed: ' + name)

    runtime_names = ['player.py']
    if 'planner.py' in protocol['sources']:
        runtime_names.append('planner.py')
    for name in runtime_names:
        tree = ast.parse((args.source_root / name).read_text(encoding='utf-8'))
        for node in ast.walk(tree):
            require(not isinstance(node, ast.Lambda), 'Use readable named helpers')
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef)):
                require(ast.get_docstring(node) is None, 'Use # comments')
            if isinstance(node, ast.FunctionDef):
                require(not node.decorator_list, 'Unexpected decorator')
                hidden = node.name.startswith('_') and not node.name.startswith('__')
                require(not hidden, 'Unexpected private helper: ' + node.name)

    results = {}
    profiles = {profile['name']: profile for profile in protocol['profiles']}
    for row in report['results']:
        key = (row['profile'], row['seed'])
        require(key not in results, 'Duplicate result')
        require(row['profile'] in profiles, 'Undeclared profile')
        require(row['seed'] in protocol['seeds'], 'Undeclared seed')
        require(row['status'] in ('top-out', 'block-limit'), 'A game crashed')
        require(row['planning_failures'] == 0, 'A plan failed verification')
        require(row['predicted_decisions'] + row['fallback_decisions'] == row['decisions'],
                'Decision counts disagree')
        require(row['cpu_seconds'] < 450, 'CPU allowance exceeded')
        require(row['seconds'] < 900, 'Local wall time exceeded fifteen minutes')
        require(row['peak_process_memory_bytes'] < 256 * 1024 * 1024, 'Memory limit exceeded')
        require(0 <= row['discards_used'] <= 10, 'Invalid discard accounting')
        require(0 <= row['bombs_used'] <= 5, 'Invalid bomb accounting')
        clear_points = 0
        for lines, points in (('1', 25), ('2', 100), ('3', 400), ('4', 1600)):
            clear_points += row['line_clears'][lines] * points
        require(0 <= row['score'] - clear_points <= row['decisions'] * 32,
                'Line-clear and descent scores disagree')
        profile = profiles[row['profile']]
        if profile['prediction'] == 'missing':
            require(row['predicted_decisions'] == 0, 'Basic player read an unavailable seed')
            require(row['prediction_status'] == 'missing', 'Basic player used prediction')
        else:
            require(row['prediction_status'] == 'verified', 'Prediction lost alignment')
            require(row['predicted_decisions'] > 0, 'Prediction was never used')
            if profile.get('options', {}).get('whole_game', False):
                require(row['full_plans'] > 0, 'Whole-game planning was never used')
                require(row['cached_decisions'] > 0, 'No saved moves were reused')
        results[key] = row
    require(len(results) == len(profiles) * len(protocol['seeds']), 'Missing game results')

    summaries = []
    for pair in protocol['comparisons']:
        before = []
        after = []
        differences = []
        rows = []
        for seed in protocol['seeds']:
            old = results[(pair['before'], seed)]
            new = results[(pair['after'], seed)]
            before.append(old['score'])
            after.append(new['score'])
            differences.append(new['score'] - old['score'])
            rows.append(new)
        require(median(after) > median(before), 'Median did not improve: ' + pair['after'])
        summaries.append({
            'before': pair['before'], 'after': pair['after'], 'games': len(after),
            'baseline_median': median(before), 'new_median': median(after),
            'median_paired_gain': median(differences),
            'wins': sum(difference > 0 for difference in differences),
            'losses': sum(difference < 0 for difference in differences),
            'minimum': min(after), 'maximum': max(after),
            'completed': sum(row['status'] == 'block-limit' for row in rows),
            'maximum_cpu_seconds': max(row['cpu_seconds'] for row in rows),
            'maximum_local_wall_seconds': max(row['seconds'] for row in rows),
            'peak_process_memory_bytes': max(row['peak_process_memory_bytes'] for row in rows),
            'bombs_used': sum(row['bombs_used'] for row in rows),
            'discards_used': sum(row['discards_used'] for row in rows),
        })
    output = {'passed': True, 'all_outcomes_included': True, 'comparisons': summaries}
    args.output.write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
