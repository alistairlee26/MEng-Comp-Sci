import argparse
import ast
import hashlib
import json
from math import factorial
from pathlib import Path
from statistics import median

ROOT = Path(__file__).resolve().parent.parent


def require(condition, message):
    if not condition:
        raise ValueError(message)


def median_interval(scores):
    ordered = sorted(scores)
    count = len(scores)
    selected = 1
    selected_coverage = 0.0
    for rank in range(1, count // 2 + 1):
        tail = 0
        for index in range(rank):
            combinations = factorial(count) // (factorial(index) * factorial(count - index))
            tail += combinations
        coverage = 1.0 - 2.0 * tail / (2 ** count)
        if coverage >= 0.95:
            selected = rank
            selected_coverage = coverage
    return {
        'lower': ordered[selected - 1],
        'upper': ordered[count - selected],
        'coverage': selected_coverage,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--protocol', type=Path, required=True)
    parser.add_argument('--seeds', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--source-root', type=Path, default=ROOT)
    args = parser.parse_args()
    report = json.loads(args.report.read_text(encoding='utf-8'))
    protocol = json.loads(args.protocol.read_text(encoding='utf-8'))
    seeds = json.loads(args.seeds.read_text(encoding='utf-8'))
    rows = report['results']

    require(report['complete'], 'The experiment is not complete')
    require(len(report['profiles']) == 1, 'Validation must use one frozen profile')
    require(len(rows) >= protocol['minimum_games'], 'Too few validation games')
    require(len(rows) == len(seeds), 'Not every declared seed has a result')
    require(len(set(seeds)) == len(seeds), 'Duplicate validation seeds')
    require(report['seeds'] == seeds, 'The seed manifest changed')
    require(report['python_version'] == protocol['python_version'], 'Wrong Python version')
    require(report['source_hashes'] == protocol['sources'], 'Reported sources changed')
    actual_seeds = []
    for row in rows:
        actual_seeds.append(row['seed'])
    require(sorted(actual_seeds) == sorted(seeds), 'Excluded or repeated results')

    for name, expected in protocol['sources'].items():
        actual = hashlib.sha256((args.source_root / name).read_bytes()).hexdigest()
        require(actual == expected, 'Frozen runtime source changed: ' + name)

    runtime_names = ['player.py']
    if 'planner.py' in protocol['sources']:
        runtime_names.append('planner.py')
    for name in runtime_names:
        tree = ast.parse((args.source_root / name).read_text(encoding='utf-8'))
        for node in ast.walk(tree):
            if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef)):
                require(ast.get_docstring(node) is None, 'Use # comments in ' + name)
            if isinstance(node, ast.FunctionDef):
                require(not node.decorator_list, 'Unexpected method decorator')
                hidden_name = node.name.startswith('_') and not node.name.startswith('__')
                require(not hidden_name, 'Unexpected leading underscore: ' + node.name)
            require(not isinstance(node, ast.Lambda), 'Unexpected lambda in runtime code')

    scores = []
    completed = 0
    maximum_cpu = 0.0
    maximum_wall = 0.0
    for row in rows:
        require(row['status'] in ('block-limit', 'top-out'), 'A game crashed')
        require(row['planning_failures'] == 0, 'A plan failed engine verification')
        require(row['prediction_status'] == 'verified', 'A validation seed was not verified')
        require(row['predicted_decisions'] > 0, 'Prediction was not exercised')
        require(row['predicted_decisions'] + row['fallback_decisions'] == row['decisions'],
                'Decision counters do not agree')
        clear_points = 0
        for lines, points in (('1', 25), ('2', 100), ('3', 400), ('4', 1600)):
            clear_points += row['line_clears'][lines] * points
        require(clear_points <= row['score'], 'Score is below its recorded line-clear points')
        require(row['score'] - clear_points <= row['decisions'] * 32,
                'Descent score is unexpectedly large')
        scores.append(row['score'])
        if row['status'] == 'block-limit':
            completed += 1
        maximum_cpu = max(maximum_cpu, row['cpu_seconds'])
        maximum_wall = max(maximum_wall, row['seconds'])

    score_median = median(scores)
    target = protocol['target_median']
    require(score_median >= target, 'The tested median is below the target')
    require(maximum_cpu < 450, 'Local CPU time exceeds the nominal grading allowance')
    require(maximum_wall < 900, 'A local validation game exceeded fifteen minutes')
    result = {
        'target': target,
        'median': score_median,
        'games': len(rows),
        'minimum': min(scores),
        'maximum': max(scores),
        'completed': completed,
        'failures': 0,
        'median_interval': median_interval(scores),
        'maximum_cpu_seconds': maximum_cpu,
        'maximum_local_wall_seconds': maximum_wall,
        'all_results_included': True,
        'runtime_sources_unchanged': True,
        'python_version': report['python_version'],
        'conditional_on_matching_seed': True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
