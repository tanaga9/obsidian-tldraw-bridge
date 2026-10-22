#!/usr/bin/env python3
"""Maintainer-only trial timing and scoped record checks; standard library only."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone


def now():
    return datetime.now(timezone.utc).isoformat()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path, value):
    path = Path(path)
    temporary = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    os.replace(temporary, path)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def same_value(left, right):
    # JSON booleans and numbers must not compare equal through Python's True == 1.
    return json.dumps(left, sort_keys=True, allow_nan=False) == json.dumps(right, sort_keys=True, allow_nan=False)


def property_at(record, path):
    value = record
    for key in path:
        if not isinstance(value, dict) or key not in value:
            raise KeyError(key)
        value = value[key]
    return value


def records(data):
    values = data['records'] if isinstance(data, dict) else data
    if not isinstance(values, list):
        raise ValueError('State must be a records array or an object containing records.')
    result = {}
    for record in values:
        if record.get('typeName') not in ('shape', 'binding'):
            continue
        key = record['id']
        if key in result:
            raise ValueError('Duplicate record ID: ' + key)
        result[key] = record
    return result


def validate_scope(scope, initial):
    groups = []
    for name in ('editable_ids', 'protected_ids'):
        values = scope[name]
        if not isinstance(values, list) or any(not isinstance(x, str) for x in values):
            raise ValueError(name + ' must be an array of IDs.')
        if len(set(values)) != len(values):
            raise ValueError('Duplicate IDs in ' + name)
        groups.append(set(values))
    editable, protected = groups
    if editable & protected or set(initial) - editable - protected or protected - set(initial):
        raise ValueError('Classify every initial shape/binding exactly once; protected IDs must exist.')
    if not isinstance(scope.get('allow_new_records', False), bool):
        raise ValueError('allow_new_records must be boolean.')
    properties = scope.get('preserve_properties', [])
    if not isinstance(properties, list):
        raise ValueError('preserve_properties must be an array.')
    seen_paths = set()
    for rule in properties:
        key, paths = rule['id'], rule['paths']
        if key not in editable or key not in initial or not isinstance(paths, list) or not paths:
            raise ValueError('Property rules need an existing editable record and nonempty paths.')
        for path in paths:
            if not isinstance(path, list) or not path or any(not isinstance(p, str) or not p for p in path):
                raise ValueError('Property paths must be nonempty arrays of object keys.')
            identity = (key, tuple(path))
            if identity in seen_paths:
                raise ValueError('Duplicate preserved property.')
            seen_paths.add(identity)
            try:
                property_at(initial[key], path)
            except KeyError:
                raise ValueError('Preserved property is missing initially: ' + key + ' ' + repr(path))
    seen = set()
    for defect in scope['existing_defects']:
        if defect['id'] in seen:
            raise ValueError('Duplicate defect ID.')
        seen.add(defect['id'])
        if defect['status'] not in ('observed', 'not_observed'):
            raise ValueError('Inspect initial previews and classify known defects before starting.')
        ids = set(defect['record_ids'])
        pool = {'editable': editable, 'protected': protected}.get(defect['scope'])
        if not ids or not ids <= set(initial) or pool is None or not ids <= pool:
            raise ValueError('Defect record IDs must exist in their declared scope.')
        if not defect.get('description'):
            raise ValueError('Defects need an observation description.')


def start(run_dir, mode, scope_path, initial_path, inputs):
    scope, initial = read(scope_path), read(initial_path)
    validate_scope(scope, records(initial))
    frozen_inputs = [{'path': str(Path(p).resolve()), 'sha256': digest(p)} for p in inputs]
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=False)
    write(run_dir / 'scope.json', scope)
    write(run_dir / 'initial-state.json', initial)
    (run_dir / 'calls').mkdir()
    write(run_dir / 'trial.json', {
        'schema_version': 2, 'trial_id': uuid.uuid4().hex, 'mode': mode, 'started_at': now(),
        'started_monotonic': time.monotonic(), 'clock_host': platform.node(),
        'clock_session': 'same host/boot required; finish before moving the run directory',
        'scope_sha256': digest(run_dir / 'scope.json'),
        'initial_sha256': digest(run_dir / 'initial-state.json'), 'inputs': frozen_inputs,
        'metric_definition': 'One call event per child process; bridge_calls counts kind=bridge, including failures/help. Not agent tool calls.',
    })
    return {'run_dir': str(run_dir), 'status': 'started'}


def frozen(run_dir):
    run_dir = Path(run_dir)
    trial = read(run_dir / 'trial.json')
    if digest(run_dir / 'scope.json') != trial['scope_sha256'] or digest(run_dir / 'initial-state.json') != trial['initial_sha256']:
        raise ValueError('Frozen scope or initial state changed; start a new trial.')
    if any(digest(item['path']) != item['sha256'] for item in trial['inputs']):
        raise ValueError('A frozen input changed; start a new trial.')
    return run_dir, trial


def call(run_dir, kind, command):
    run_dir, _ = frozen(run_dir)
    if (run_dir / 'metrics.json').exists():
        raise ValueError('Trial already finished.')
    if not command:
        raise ValueError('Supply a command after --.')
    ident = uuid.uuid4().hex
    base = run_dir / 'calls' / ident
    event = {'id': ident, 'kind': kind, 'command': command, 'started_at': now(), 'status': 'running',
             'stdout': base.name + '.stdout', 'stderr': base.name + '.stderr'}
    write(base.with_suffix('.json'), event)
    begun = time.monotonic()
    code = 1
    try:
        with base.with_suffix('.stdout').open('wb') as out, base.with_suffix('.stderr').open('wb') as err:
            proc = subprocess.run(command, stdout=out, stderr=err, check=False)
        code = proc.returncode
        event.update(status='complete', exit_code=code)
        if kind == 'bridge':
            try:
                response = read(base.with_suffix('.stdout'))
                if isinstance(response, dict):
                    event['bridge_error'] = response.get('error')
            except (ValueError, UnicodeError):
                event['response_not_json'] = True
    except OSError as error:
        event.update(status='launch_failed', exit_code=None, launch_error=str(error))
    finally:
        event.update(ended_at=now(), elapsed_seconds=time.monotonic() - begun)
        write(base.with_suffix('.json'), event)
    for suffix, stream in (('.stdout', sys.stdout.buffer), ('.stderr', sys.stderr.buffer)):
        path = base.with_suffix(suffix)
        if path.exists():
            with path.open('rb') as content:
                shutil.copyfileobj(content, stream)
    if event['status'] == 'launch_failed':
        print(event['launch_error'], file=sys.stderr)
    return code


def finish(run_dir, status):
    run_dir, trial = frozen(run_dir)
    if (run_dir / 'metrics.json').exists():
        raise ValueError('Trial already finished; keep original metrics.')
    events = [read(p) for p in sorted((run_dir / 'calls').glob('*.json'))]
    pending = [e['id'] for e in events if e['status'] == 'running']
    if status == 'complete' and pending:
        raise ValueError('Unresolved call events remain; do not claim completion.')
    same_host = trial['clock_host'] == platform.node()
    duration = time.monotonic() - trial['started_monotonic']
    metrics = {
        'schema_version': 1, 'status': status, 'started_at': trial['started_at'], 'ended_at': now(),
        'elapsed_seconds': duration if same_host and duration >= 0 else None,
        'elapsed_clock': 'monotonic on same host/boot',
        'process_calls': len(events), 'bridge_calls': sum(e['kind'] == 'bridge' for e in events),
        'failed_calls': sum(e['status'] == 'launch_failed' or e.get('exit_code', 0) not in (0, None) or bool(e.get('bridge_error')) for e in events),
        'unresolved_calls': pending, 'agent_tool_calls': None, 'actual_tokens': None,
        'human_repair_minutes': None,
    }
    write(run_dir / 'metrics.json', metrics)
    return metrics


def prepare_review(run_dir, final_path, preview_path, preview_receipt_path, saved_path):
    run_dir, trial = frozen(run_dir)
    if not trial.get('trial_id'):
        raise ValueError('Start a new trial to prepare a bound review target.')
    state, receipt, saved = read(final_path), read(preview_receipt_path), read(saved_path)
    records(state)
    revision, note = state.get('revision'), state.get('path')
    if not isinstance(revision, str) or not revision or not isinstance(note, str) or not note:
        raise ValueError('Final state must identify its note and revision.')
    if receipt.get('revision') != revision:
        raise ValueError('Preview receipt is for a different revision.')
    if Path(receipt.get('path', '')).resolve() != Path(preview_path).resolve():
        raise ValueError('Preview path does not match its export receipt.')
    if receipt.get('sha256') != digest(preview_path):
        raise ValueError('Preview bytes do not match the export receipt; capture them again.')
    if saved.get('saved') is not True or saved.get('path') != note or saved.get('revision') != revision:
        raise ValueError('A confirmed saved receipt for the same note and revision is required.')
    target_dir = run_dir / 'review-targets' / uuid.uuid4().hex
    target_dir.mkdir(parents=True)
    artifacts = {}
    for name, source in [('state.json', final_path), ('preview' + Path(preview_path).suffix, preview_path),
                         ('preview-receipt.json', preview_receipt_path), ('saved.json', saved_path)]:
        destination = target_dir / name
        shutil.copyfile(source, destination)
        artifacts[name] = digest(destination)
        if name.startswith('preview.') and artifacts[name] != receipt['sha256']:
            raise ValueError('Preview changed while preparing review; capture it again.')
    if read(target_dir / 'state.json') != state or read(target_dir / 'preview-receipt.json') != receipt or read(target_dir / 'saved.json') != saved:
        raise ValueError('Artifacts changed while preparing review; capture them again.')
    target = {'schema_version': 1, 'target_id': target_dir.name, 'trial_id': trial['trial_id'], 'revision': revision, 'note': note,
              'scope_sha256': trial['scope_sha256'], 'initial_sha256': trial['initial_sha256'],
              'artifacts': artifacts}
    write(target_dir / 'target.json', target)
    write(target_dir / 'review.json', {
        'target_sha256': digest(target_dir / 'target.json'),
        'task': {'status': 'unassessed', 'evidence': None},
        'affected_quality': {'status': 'unassessed', 'evidence': None},
    })
    return {'target': str(target_dir / 'target.json'), 'review': str(target_dir / 'review.json'),
            'instruction': 'Inspect these frozen artifacts, then fill this review. A new state requires a new target and review.'}


def review_errors(run_dir, trial, final_path, review, target_path):
    if not target_path:
        return ['A review target is required.']
    target_path = Path(target_path)
    try:
        if target_path.resolve().parent.parent != (run_dir / 'review-targets').resolve():
            return ['Review target must belong to this trial.']
        target = read(target_path)
        if not isinstance(target, dict):
            return ['Invalid review target object.']
        if review.get('target_sha256') != digest(target_path):
            return ['Review is not bound to this target.']
        for key in ('trial_id', 'scope_sha256', 'initial_sha256'):
            if not target.get(key) or target[key] != trial.get(key):
                return ['Review target belongs to a different trial or scope.']
        if target['artifacts'].get('state.json') != digest(final_path):
            return ['Final state differs from the reviewed snapshot.']
        expected = {'state.json', 'preview-receipt.json', 'saved.json'}
        names = set(target['artifacts'])
        if not expected < names or len(names) != 4:
            return ['Review target must contain state, preview, export receipt, and saved receipt.']
        for name, checksum in target['artifacts'].items():
            if Path(name).name != name or digest(target_path.parent / name) != checksum:
                return ['A reviewed artifact changed.']
        state = read(target_path.parent / 'state.json')
        receipt = read(target_path.parent / 'preview-receipt.json')
        saved = read(target_path.parent / 'saved.json')
        preview_name = next(iter(names - expected))
        if receipt.get('sha256') != target['artifacts'][preview_name]:
            return ['Reviewed preview bytes do not match the export receipt.']
        revision, note = state.get('revision'), state.get('path')
        if not isinstance(revision, str) or not revision or not isinstance(note, str) or not note:
            return ['Reviewed state must identify its note and revision.']
        if target.get('revision') != revision or target.get('note') != note or receipt.get('revision') != revision:
            return ['Reviewed target and preview must identify the final revision.']
        if saved.get('saved') is not True or saved.get('path') != note or saved.get('revision') != revision:
            return ['Reviewed saved receipt must confirm the same note and revision.']
    except (OSError, ValueError, KeyError, TypeError) as error:
        return ['Invalid review target: ' + str(error)]
    return []


def check(run_dir, final_path, review_path=None, target_path=None):
    run_dir, trial = frozen(run_dir)
    scope = read(run_dir / 'scope.json')
    initial, final = records(read(run_dir / 'initial-state.json')), records(read(final_path))
    editable, protected = set(scope['editable_ids']), set(scope['protected_ids'])
    changed = {key for key in set(initial) | set(final) if not same_value(initial.get(key), final.get(key))}
    allowed_additions = set(final) - set(initial) if scope.get('allow_new_records', False) else set()
    forbidden = changed - editable - allowed_additions
    violations = []
    property_count = 0
    for rule in scope.get('preserve_properties', []):
        for path in rule['paths']:
            property_count += 1
            try:
                matches = same_value(property_at(initial[rule['id']], path), property_at(final[rule['id']], path))
            except KeyError:
                matches = False
            if not matches:
                violations.append({'id': rule['id'], 'path': path})
    review = read(review_path) if review_path else {}
    if not isinstance(review, dict):
        raise ValueError('Review must be an object.')
    errors = review_errors(run_dir, trial, final_path, review, target_path) if review_path else []
    dimensions = {}
    for name in ('task', 'affected_quality'):
        item = review.get(name, {'status': 'unassessed', 'evidence': None}) if not errors else {'status': 'unassessed', 'evidence': None}
        if item.get('status') not in ('pass', 'fail', 'unassessed'):
            raise ValueError('Invalid review status: ' + name)
        if item['status'] != 'unassessed' and not item.get('evidence'):
            raise ValueError('A visual/meaning verdict needs evidence: ' + name)
        dimensions[name] = item
    dimensions['preservation'] = {'status': 'fail' if forbidden or violations else 'pass',
                                  'protected_count': len(protected), 'unauthorized_changes': sorted(forbidden),
                                  'preserved_property_count': property_count, 'property_violations': violations}
    verdicts = [d['status'] for d in dimensions.values()]
    result = {'schema_version': 2, 'dimensions': dimensions, 'changed_records': sorted(changed),
              'final_state_sha256': digest(final_path),
              'review_binding': {'status': 'invalid' if errors else ('verified' if review_path else 'unassessed'),
                                 'errors': errors, 'target_sha256': review.get('target_sha256') if not errors else None,
                                 'review_sha256': digest(review_path) if review_path else None},
              'existing_defects': scope['existing_defects'], 'reviewed_defect_outcomes': review.get('defect_outcomes', []) if not errors else [],
              'overall': 'fail' if 'fail' in verdicts else ('pass' if all(v == 'pass' for v in verdicts) else 'unassessed'),
              'limits': 'Record equality does not prove readable rendering, correct meaning, or saved persistence. Inspect previews and saved receipts.'}
    write(run_dir / 'checks.json', result)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='action', required=True)
    p = commands.add_parser('start')
    p.add_argument('--run-dir', required=True); p.add_argument('--mode', choices=['diagnose', 'compare'], required=True)
    p.add_argument('--scope', required=True); p.add_argument('--initial-state', required=True)
    p.add_argument('--input', action='append', default=[])
    p = commands.add_parser('call')
    p.add_argument('--run-dir', required=True); p.add_argument('--kind', choices=['bridge', 'other'], required=True)
    p.add_argument('command', nargs=argparse.REMAINDER)
    p = commands.add_parser('finish')
    p.add_argument('--run-dir', required=True); p.add_argument('--status', choices=['complete', 'failed', 'incomplete'], required=True)
    p = commands.add_parser('check')
    p.add_argument('--run-dir', required=True); p.add_argument('--final-state', required=True); p.add_argument('--review'); p.add_argument('--review-target')
    p = commands.add_parser('prepare-review')
    p.add_argument('--run-dir', required=True); p.add_argument('--final-state', required=True)
    p.add_argument('--preview', required=True); p.add_argument('--preview-receipt', required=True); p.add_argument('--saved', required=True)
    args = parser.parse_args()
    try:
        if args.action == 'start': result = start(args.run_dir, args.mode, args.scope, args.initial_state, args.input)
        elif args.action == 'call': return call(args.run_dir, args.kind, args.command[1:] if args.command[:1] == ['--'] else args.command)
        elif args.action == 'finish': result = finish(args.run_dir, args.status)
        elif args.action == 'prepare-review': result = prepare_review(args.run_dir, args.final_state, args.preview, args.preview_receipt, args.saved)
        else: result = check(args.run_dir, args.final_state, args.review, args.review_target)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({'error': str(error)}), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
