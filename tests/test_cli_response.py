"""A confirmed evaluation response must not depend on the CLI child's exit."""
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from obsidian_tldraw_bridge.obsidian import Client, _evaluation_response


class EvaluationFrameTests(unittest.TestCase):
    token = 'invocation-token'

    def frame(self, **fields):
        return b'=> ' + json.dumps({'bridgeResponseToken': self.token, **fields}, ensure_ascii=False).encode('utf-8') + b'\n'

    def test_only_matching_tagged_frame_is_a_response(self):
        value = '{"saved":true}'
        data = b'=> {"saved":false}\n' + self.frame(value=value) + b'=> {"log":"after reply"}\n'
        self.assertEqual(_evaluation_response(data, self.token), b'=> {"saved":true}\n')
        self.assertIsNone(_evaluation_response(self.frame(value=value), 'different-token'))

    def test_partial_frame_waits_for_newline_or_process_exit(self):
        frame = self.frame(value='42')
        self.assertIsNone(_evaluation_response(frame[:-2], self.token))
        self.assertIsNone(_evaluation_response(frame[:-1], self.token))
        self.assertEqual(_evaluation_response(frame[:-1], self.token, final=True), b'=> 42\n')

    def test_undefined_is_confirmed_but_has_no_json_value(self):
        self.assertEqual(_evaluation_response(self.frame(), self.token), b'')

    def test_native_json_and_unicode_keep_their_values(self):
        for value in (None, False, 42, {'text': '青\u0085\u2028\u2029😀'}):
            with self.subTest(value=value):
                response = _evaluation_response(self.frame(value=value), self.token)
                self.assertEqual(json.loads(response[3:]), value)


class CliExitTests(unittest.TestCase):
    token = 'invocation-token'

    def frame(self, value='{"saved":true}', token=None):
        return '=> ' + json.dumps({'bridgeResponseToken': token or self.token, 'value': value}) + '\n'

    def start_tracking(self, argv, **kwargs):
        process = self.real_popen(argv, **kwargs)
        self.processes.append(process)
        return process

    def setUp(self):
        self.real_popen = subprocess.Popen
        self.processes = []

    def tearDown(self):
        for process in self.processes:
            if process.poll() is None:
                process.kill()
            process.wait()

    def test_complete_reply_reaps_a_cli_that_does_not_exit(self):
        code = 'import sys,time;sys.stdout.write(' + repr(self.frame()) + ');sys.stdout.flush();time.sleep(10)'
        with patch('subprocess.Popen', side_effect=self.start_tracking):
            result = Client._run_cli([sys.executable, '-c', code], timeout=2, response_token=self.token)
        self.assertTrue(result.response_reaped)
        self.assertEqual(result.stdout, b'=> {"saved":true}\n')
        self.assertIsNotNone(self.processes[0].poll())

    def test_split_reply_is_not_returned_until_complete(self):
        frame = self.frame()
        code = ('import sys,time;sys.stdout.write(' + repr(frame[:12]) + ');sys.stdout.flush();time.sleep(.05);'
                'sys.stdout.write(' + repr(frame[12:]) + ');sys.stdout.flush();time.sleep(10)')
        with patch('subprocess.Popen', side_effect=self.start_tracking):
            result = Client._run_cli([sys.executable, '-c', code], timeout=2, response_token=self.token)
        self.assertTrue(result.response_reaped)
        self.assertEqual(result.stdout, b'=> {"saved":true}\n')

    def test_wrong_tag_cannot_turn_a_timeout_into_success(self):
        code = 'import sys,time;sys.stdout.write(' + repr(self.frame(token='other')) + ');sys.stdout.flush();time.sleep(10)'
        with patch('subprocess.Popen', side_effect=self.start_tracking):
            with self.assertRaises(subprocess.TimeoutExpired):
                Client._run_cli([sys.executable, '-c', code], timeout=.15, response_token=self.token)
        self.assertIsNotNone(self.processes[0].poll())

    def test_prompt_nonzero_exit_is_not_hidden_by_a_reply(self):
        code = 'import sys;sys.stdout.write(' + repr(self.frame()) + ');sys.stdout.flush();sys.stderr.write("CLI failed");sys.exit(7)'
        with patch('subprocess.Popen', side_effect=self.start_tracking):
            result = Client._run_cli([sys.executable, '-c', code], timeout=2, response_token=self.token)
        self.assertEqual(result.returncode, 7)
        self.assertFalse(result.response_reaped)
        self.assertEqual(result.stderr, b'CLI failed')

    def test_evaluate_accepts_confirmed_reply_without_retrying(self):
        with patch('obsidian_tldraw_bridge.obsidian.find_cli', return_value='unused-cli'):
            client = Client('test-vault', timeout=2)
        def start(argv, **kwargs):
            token = json.loads(re.search(r'bridgeResponseToken:("[^"\\]*")', argv[-1]).group(1))
            code = 'import sys,time;sys.stdout.write(' + repr(self.frame(token=token)) + ');sys.stdout.flush();time.sleep(10)'
            return self.start_tracking([sys.executable, '-c', code], **kwargs)
        with patch('subprocess.Popen', side_effect=start):
            self.assertEqual(client.evaluate('JSON.stringify({saved:true})'), {'saved': True})
        self.assertEqual(len(self.processes), 1)

    def test_confirmed_undefined_keeps_missing_ok_and_cleans_payload(self):
        with tempfile.TemporaryDirectory() as directory, \
                patch('obsidian_tldraw_bridge.obsidian.tempfile.tempdir', directory), \
                patch('obsidian_tldraw_bridge.obsidian.find_cli', return_value='unused-cli'):
            client = Client('test-vault', timeout=2)
            def start(argv, **kwargs):
                token = json.loads(re.search(r'bridgeResponseToken:("[^"\\\\]*")', argv[-1]).group(1))
                frame = '=> ' + json.dumps({'bridgeResponseToken': token}) + '\n'
                code = 'import sys,time;sys.stdout.write(' + repr(frame) + ');sys.stdout.flush();time.sleep(10)'
                return self.start_tracking([sys.executable, '-c', code], **kwargs)
            with patch('subprocess.Popen', side_effect=start):
                self.assertIsNone(client.evaluate('void 0', missing_ok=True))
            self.assertEqual(list(Path(directory).iterdir()), [])
