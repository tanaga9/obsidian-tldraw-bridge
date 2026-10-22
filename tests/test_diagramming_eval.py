"""Behavioral checks for the repository-only evaluation recorder."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('diagramming_eval', ROOT / 'scripts/diagramming_eval.py')
eval_run = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(eval_run)


class EvaluationRecorderTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.initial = {'records': [
            {'id': 'shape:worker', 'typeName': 'shape', 'type': 'geo', 'props': {'w': 100}},
            {'id': 'shape:client', 'typeName': 'shape', 'type': 'geo', 'props': {'w': 200}},
        ]}
        self.scope = {'editable_ids': ['shape:worker'], 'protected_ids': ['shape:client'],
                      'existing_defects': [], 'allow_new_records': False}
        eval_run.write(self.root / 'initial.json', self.initial)
        eval_run.write(self.root / 'scope.json', self.scope)
        self.run = self.root / 'trial'

    def start(self):
        return eval_run.start(self.run, 'diagnose', self.root / 'scope.json', self.root / 'initial.json', [])

    def reviewed(self, final=None, task='pass', quality='pass'):
        final = copy.deepcopy(final if final is not None else self.initial)
        final.update(path='trial.md', revision='revision-1')
        state = self.root / 'final.json'
        preview = self.root / 'preview.webp'
        receipt, saved = self.root / 'preview.json', self.root / 'saved.json'
        eval_run.write(state, final)
        preview.write_bytes(b'fixture-preview-bytes')
        eval_run.write(receipt, {'revision': 'revision-1', 'path': str(preview.resolve()), 'sha256': eval_run.digest(preview)})
        eval_run.write(saved, {'saved': True, 'path': 'trial.md', 'revision': 'revision-1'})
        prepared = eval_run.prepare_review(self.run, state, preview, receipt, saved)
        target, review = Path(prepared['target']), Path(prepared['review'])
        data = eval_run.read(review)
        data.update(task={'status': task, 'evidence': 'Reviewed task in frozen artifacts'},
                    affected_quality={'status': quality, 'evidence': 'Reviewed labels and saved receipt'})
        eval_run.write(review, data)
        return state, review, target

    def test_initial_scope_must_cover_records_and_known_defects_must_be_reviewed(self):
        bad = copy.deepcopy(self.scope)
        bad['protected_ids'] = []
        with self.assertRaises(ValueError):
            eval_run.validate_scope(bad, eval_run.records(self.initial))
        bad = copy.deepcopy(self.scope)
        bad['existing_defects'] = [{'id': 'worker', 'record_ids': ['shape:worker'],
                                    'scope': 'editable', 'status': 'verify', 'description': 'Inspect text'}]
        with self.assertRaises(ValueError):
            eval_run.validate_scope(bad, eval_run.records(self.initial))

    def test_editable_change_passes_preservation_without_claiming_visual_success(self):
        self.start()
        final = copy.deepcopy(self.initial)
        final['records'][0]['props']['w'] = 300
        eval_run.write(self.root / 'final.json', final)
        checked = eval_run.check(self.run, self.root / 'final.json')
        self.assertEqual(checked['dimensions']['preservation']['status'], 'pass')
        self.assertEqual(checked['dimensions']['preservation']['protected_count'], 1)
        self.assertEqual(checked['overall'], 'unassessed')

    def test_protected_edits_deletions_and_unlisted_additions_fail(self):
        self.start()
        for final in [
            {'records': self.initial['records'][:1]},
            {'records': self.initial['records'] + [{'id': 'shape:extra', 'typeName': 'shape'}]},
            {'records': [self.initial['records'][0], {**self.initial['records'][1], 'x': 90}]},
        ]:
            with self.subTest(final=final):
                eval_run.write(self.root / 'final.json', final)
                self.assertEqual(eval_run.check(self.run, self.root / 'final.json')['overall'], 'fail')

    def test_quality_failure_remains_failure_when_task_and_preservation_pass(self):
        self.start()
        state, review, target = self.reviewed(quality='fail')
        checked = eval_run.check(self.run, state, review, target)
        self.assertEqual(checked['overall'], 'fail')
        self.assertEqual(checked['dimensions']['preservation']['status'], 'pass')

    def test_bound_review_passes_and_uses_frozen_artifacts(self):
        self.start()
        state, review, target = self.reviewed()
        self.assertEqual(eval_run.check(self.run, state, review, target)['overall'], 'pass')
        self.assertEqual((target.parent / 'preview.webp').read_bytes(), b'fixture-preview-bytes')
        # The reviewer evaluates copies; changing a source image cannot rewrite them.
        (self.root / 'preview.webp').write_bytes(b'a later export')
        self.assertEqual(eval_run.check(self.run, state, review, target)['overall'], 'pass')

    def test_stale_review_cannot_pass_after_editable_state_changes(self):
        self.start()
        state, review, target = self.reviewed()
        self.assertEqual(eval_run.check(self.run, state, review, target)['overall'], 'pass')
        data = eval_run.read(state)
        data['records'][0]['props']['w'] = 300
        eval_run.write(state, data)
        checked = eval_run.check(self.run, state, review, target)
        self.assertEqual(checked['overall'], 'unassessed')
        self.assertEqual(checked['review_binding']['status'], 'invalid')
        self.assertEqual(eval_run.read(self.run / 'checks.json')['overall'], 'unassessed')

    def test_review_for_other_target_or_trial_is_rejected(self):
        self.start()
        state, old_review, old_target = self.reviewed()
        old_data = eval_run.read(old_review)
        state, review, target = self.reviewed()
        eval_run.write(review, old_data)
        self.assertEqual(eval_run.check(self.run, state, review, target)['overall'], 'unassessed')
        other = self.root / 'other-trial'
        eval_run.start(other, 'diagnose', self.root / 'scope.json', self.root / 'initial.json', [])
        self.assertEqual(eval_run.check(other, state, old_review, old_target)['overall'], 'unassessed')

    def test_unbound_review_is_unassessed_and_modified_bundle_is_rejected(self):
        self.start()
        state, review, target = self.reviewed()
        self.assertEqual(eval_run.check(self.run, state, review)['overall'], 'unassessed')
        (target.parent / 'preview.webp').write_bytes(b'changed')
        self.assertEqual(eval_run.check(self.run, state, review, target)['overall'], 'unassessed')

    def test_prepare_review_rejects_wrong_revision_image_path_or_unsaved_note(self):
        self.start()
        self.reviewed()
        state, preview = self.root / 'final.json', self.root / 'preview.webp'
        receipt, saved = self.root / 'preview.json', self.root / 'saved.json'
        for change in [{'revision': 'another'}, {'path': str(self.root / 'other.webp')}]:
            data = {'revision': 'revision-1', 'path': str(preview.resolve()), 'sha256': eval_run.digest(preview), **change}
            eval_run.write(receipt, data)
            with self.assertRaises(ValueError):
                eval_run.prepare_review(self.run, state, preview, receipt, saved)
        eval_run.write(receipt, {'revision': 'revision-1', 'path': str(preview.resolve()), 'sha256': eval_run.digest(preview)})
        for data in [{'saved': False, 'path': 'trial.md', 'revision': 'revision-1'},
                     {'saved': True, 'path': 'other.md', 'revision': 'revision-1'},
                     {'saved': True, 'path': 'trial.md'},
                     {'saved': True, 'path': 'trial.md', 'revision': 'older-revision'}]:
            eval_run.write(saved, data)
            with self.assertRaises(ValueError):
                eval_run.prepare_review(self.run, state, preview, receipt, saved)

    def test_self_consistent_bundle_with_stale_or_missing_saved_revision_is_rejected(self):
        self.start()
        for revision in [None, 'older-revision']:
            state, review, target = self.reviewed()
            saved = {'saved': True, 'path': 'trial.md'}
            if revision is not None:
                saved['revision'] = revision
            eval_run.write(target.parent / 'saved.json', saved)
            data = eval_run.read(target)
            data['artifacts']['saved.json'] = eval_run.digest(target.parent / 'saved.json')
            eval_run.write(target, data)
            judgment = eval_run.read(review)
            judgment['target_sha256'] = eval_run.digest(target)
            eval_run.write(review, judgment)
            result = eval_run.check(self.run, state, review, target)
            self.assertEqual(result['overall'], 'unassessed')

    def test_prepare_review_rejects_missing_hash_and_overwritten_preview(self):
        self.start()
        self.reviewed()
        state, preview = self.root / 'final.json', self.root / 'preview.webp'
        receipt, saved = self.root / 'preview.json', self.root / 'saved.json'
        original = eval_run.read(receipt)
        del original['sha256']
        eval_run.write(receipt, original)
        with self.assertRaisesRegex(ValueError, 'Preview bytes'):
            eval_run.prepare_review(self.run, state, preview, receipt, saved)
        original['sha256'] = eval_run.digest(preview)
        eval_run.write(receipt, original)
        preview.write_bytes(b'overwritten before freezing')
        with self.assertRaisesRegex(ValueError, 'Preview bytes'):
            eval_run.prepare_review(self.run, state, preview, receipt, saved)

    def test_preview_replaced_during_copy_is_rejected(self):
        self.start()
        self.reviewed()
        original_copy = eval_run.shutil.copyfile
        preview = self.root / 'preview.webp'

        def replace_preview(source, destination):
            if Path(source) == preview:
                preview.write_bytes(b'replaced during copy')
            return original_copy(source, destination)

        with patch.object(eval_run.shutil, 'copyfile', side_effect=replace_preview):
            with self.assertRaisesRegex(ValueError, 'Preview changed'):
                eval_run.prepare_review(self.run, self.root / 'final.json', preview,
                                       self.root / 'preview.json', self.root / 'saved.json')

    def test_bundle_hashes_cannot_hide_missing_or_stale_export_hash(self):
        self.start()
        for mode in ['missing', 'stale']:
            state, review, target = self.reviewed()
            receipt_path = target.parent / 'preview-receipt.json'
            receipt = eval_run.read(receipt_path)
            if mode == 'missing':
                del receipt['sha256']
            else:
                (target.parent / 'preview.webp').write_bytes(b'different image')
            eval_run.write(receipt_path, receipt)
            data = eval_run.read(target)
            for name in ['preview-receipt.json', 'preview.webp']:
                data['artifacts'][name] = eval_run.digest(target.parent / name)
            eval_run.write(target, data)
            judgment = eval_run.read(review)
            judgment['target_sha256'] = eval_run.digest(target)
            eval_run.write(review, judgment)
            result = eval_run.check(self.run, state, review, target)
            self.assertEqual(result['overall'], 'unassessed')
            self.assertIn('preview bytes', result['review_binding']['errors'][0])

    def property_scope(self):
        self.initial['records'][0]['props']['richText'] = {'type': 'doc', 'content': [{'text': 'Keep exactly'}]}
        self.initial['records'][0]['toId'] = 'shape:client'
        self.scope['preserve_properties'] = [{'id': 'shape:worker', 'paths': [['props', 'richText'], ['toId']]}]
        eval_run.write(self.root / 'initial.json', self.initial)
        eval_run.write(self.root / 'scope.json', self.scope)

    def test_property_invariants_allow_resize_but_reject_text_changes_and_reconnection(self):
        self.property_scope()
        self.start()
        final = copy.deepcopy(self.initial)
        final['records'][0]['props']['w'] = 400
        state, review, target = self.reviewed(final)
        self.assertEqual(eval_run.check(self.run, state, review, target)['overall'], 'pass')
        for kind in ['text', 'target', 'missing-property', 'missing-record']:
            damaged = copy.deepcopy(final)
            if kind == 'text': damaged['records'][0]['props']['richText']['content'][0]['text'] = 'Changed'
            elif kind == 'target': damaged['records'][0]['toId'] = 'shape:other'
            elif kind == 'missing-property': del damaged['records'][0]['props']['richText']
            else: damaged['records'].pop(0)
            state, review, target = self.reviewed(damaged)
            checked = eval_run.check(self.run, state, review, target)
            self.assertEqual(checked['overall'], 'fail', kind)
            self.assertTrue(checked['dimensions']['preservation']['property_violations'], kind)

    def test_invalid_property_paths_and_nonexistent_properties_are_rejected(self):
        self.property_scope()
        for rule in [
            {'id': 'shape:missing', 'paths': [['props']]},
            {'id': 'shape:worker', 'paths': [['props', 'missing']]},
            {'id': 'shape:worker', 'paths': ['props.richText']},
            {'id': 'shape:worker', 'paths': [['props'], ['props']]},
        ]:
            scope = {**self.scope, 'preserve_properties': [rule]}
            with self.assertRaises(ValueError):
                eval_run.validate_scope(scope, eval_run.records(self.initial))

    def test_exact_preservation_distinguishes_json_booleans_and_numbers(self):
        self.initial['records'][1]['isLocked'] = True
        eval_run.write(self.root / 'initial.json', self.initial)
        self.start()
        final = copy.deepcopy(self.initial)
        final['records'][1]['isLocked'] = 1
        eval_run.write(self.root / 'final.json', final)
        self.assertEqual(eval_run.check(self.run, self.root / 'final.json')['overall'], 'fail')

    def test_frozen_scope_cannot_be_relaxed_after_edit(self):
        self.start()
        changed = eval_run.read(self.run / 'scope.json')
        changed['allow_new_records'] = True
        eval_run.write(self.run / 'scope.json', changed)
        with self.assertRaises(ValueError):
            eval_run.finish(self.run, 'complete')

    def test_changed_frozen_input_cannot_silently_enter_trial(self):
        prompt = self.root / 'prompt.md'
        prompt.write_text('original', encoding='utf-8')
        eval_run.start(self.run, 'compare', self.root / 'scope.json', self.root / 'initial.json', [prompt])
        prompt.write_text('changed', encoding='utf-8')
        with self.assertRaises(ValueError):
            eval_run.finish(self.run, 'complete')

    def test_creation_scope_allows_new_records_but_not_protected_edits(self):
        self.scope['allow_new_records'] = True
        eval_run.write(self.root / 'scope.json', self.scope)
        self.start()
        final = copy.deepcopy(self.initial)
        final['records'].append({'id': 'shape:new', 'typeName': 'shape'})
        eval_run.write(self.root / 'final.json', final)
        self.assertEqual(eval_run.check(self.run, self.root / 'final.json')['dimensions']['preservation']['status'], 'pass')
        final['records'][1]['props']['w'] = 80
        eval_run.write(self.root / 'final.json', final)
        self.assertEqual(eval_run.check(self.run, self.root / 'final.json')['overall'], 'fail')

    def test_call_records_bridge_error_even_with_successful_exit_and_keeps_unknown_metrics(self):
        self.start()
        cmd = [sys.executable, '-c', 'print(\'{"error":{"code":"SAVE_UNCONFIRMED","outcome":"applied"}}\')']
        proc = subprocess.run([sys.executable, str(ROOT / 'scripts/diagramming_eval.py'),
                               'call', '--run-dir', str(self.run), '--kind', 'bridge', '--', *cmd],
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn('SAVE_UNCONFIRMED', proc.stdout)
        metrics = eval_run.finish(self.run, 'failed')
        self.assertEqual(metrics['bridge_calls'], 1)
        self.assertEqual(metrics['failed_calls'], 1)
        self.assertIsNone(metrics['agent_tool_calls'])
        self.assertIsNone(metrics['human_repair_minutes'])
        self.assertGreaterEqual(metrics['elapsed_seconds'], 0)
        with self.assertRaises(ValueError):
            eval_run.finish(self.run, 'complete')

    def test_pending_call_prevents_complete_but_allows_incomplete(self):
        self.start()
        eval_run.write(self.run / 'calls/pending.json', {'id': 'pending', 'kind': 'bridge', 'status': 'running'})
        with self.assertRaises(ValueError):
            eval_run.finish(self.run, 'complete')
        self.assertEqual(eval_run.finish(self.run, 'incomplete')['unresolved_calls'], ['pending'])

    def test_launch_failure_is_recorded(self):
        self.start()
        with patch('subprocess.run', side_effect=OSError('unavailable')), patch('sys.stderr'):
            self.assertEqual(eval_run.call(self.run, 'other', ['unavailable']), 1)
        metrics = eval_run.finish(self.run, 'failed')
        self.assertEqual(metrics['process_calls'], 1)
        self.assertEqual(metrics['failed_calls'], 1)

    def test_cli_does_not_evaluate_command_text_as_shell(self):
        self.start()
        literal = '$(touch should-not-exist); echo unexpected'
        proc = subprocess.run([sys.executable, str(ROOT / 'scripts/diagramming_eval.py'),
                               'call', '--run-dir', str(self.run), '--kind', 'other', '--',
                               sys.executable, '-c', 'import sys;print(sys.argv[1])', literal],
                              capture_output=True, text=True, cwd=self.root)
        self.assertEqual(proc.stdout.strip(), literal)
        self.assertFalse((self.root / 'should-not-exist').exists())

    def test_partial_fixture_has_seven_protected_shape_binding_records(self):
        scope = eval_run.read(ROOT / 'docs/evaluations/diagramming/partial-edit.scope.example.json')
        initial = eval_run.read(ROOT / 'docs/evaluations/diagramming/partial-edit.initial.json')
        values = []
        for operation in initial:
            for field, type_name in [('shapes', 'shape'), ('bindings', 'binding')]:
                values.extend({**x, 'typeName': type_name} for x in operation.get(field, []))
        for defect in scope['existing_defects']:
            defect['status'] = 'observed'
        eval_run.validate_scope(scope, eval_run.records(values))
        self.assertEqual(len(scope['protected_ids']), 7)


if __name__ == '__main__':
    unittest.main()
