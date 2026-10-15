import json
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from obsidian_tldraw_bridge.obsidian import Client, BridgeError

class TransportTest(unittest.TestCase):
    def client(self):
        with patch("obsidian_tldraw_bridge.obsidian.find_cli", return_value="/app/obsidian"):
            return Client("Vault with spaces")

    def test_code_is_argv_not_shell(self):
        client = self.client()
        code = 'require("a path;$(touch nope)")'
        proc = subprocess.CompletedProcess([],0,'installer warning\n=> {"ok":true}\n','')
        with patch("subprocess.run", return_value=proc) as run:
            self.assertEqual(client.evaluate(code), {"ok":True})
            self.assertEqual(run.call_args.args[0][-1], "code="+code)
            self.assertNotIn("shell", run.call_args.kwargs)

    def test_dispatch_poll_and_forget_use_loader_with_runtime_path(self):
        client = self.client()
        with patch.object(client, "evaluate", side_effect=[None, {"status":"complete", "result":{}}, {"forgotten":True}]) as evaluate:
            client.call("doctor")
            calls = [item.args[0] for item in evaluate.call_args_list]
            for code in calls:
                self.assertIn("loader.cjs", code)
                self.assertIn(json.dumps(client.module), code)
            self.assertIn(".dispatch(app,", calls[0])
            self.assertIn(".poll(app,", calls[1])
            self.assertIn(".forget(app,", calls[2])

    def test_lost_dispatch_output_still_polls(self):
        client = self.client()
        with patch.object(client, "evaluate", side_effect=[None,{"status":"running"},{"status":"complete","result":{"saved":True}}]):
            self.assertEqual(client.call("saved",{},"test-id"), {"saved":True})

    def test_failures_are_not_retried(self):
        client = self.client()
        with patch.object(client,"evaluate",side_effect=[None,{"status":"failed","error":"Revision conflict"}]) as evaluate:
            with self.assertRaisesRegex(BridgeError,"Revision conflict"):
                client.call("batch",{},"test-id")
            self.assertEqual(evaluate.call_count,2)

    def test_automatic_results_are_released(self):
        client = self.client()
        with patch.object(client,"evaluate",side_effect=[None,{"status":"complete","result":{"saved":True}},{"forgotten":True}]) as evaluate:
            self.assertEqual(client.call("saved"),{"saved":True})
            self.assertIn(".forget(app,",evaluate.call_args.args[0])

    def test_cleanup_failure_does_not_hide_success(self):
        client = self.client()
        with patch.object(client,"evaluate",side_effect=[None,{"status":"complete","result":{"saved":True}},BridgeError("cleanup failed")]):
            self.assertEqual(client.call("saved"),{"saved":True})

    def test_failed_automatic_results_are_released(self):
        client = self.client()
        with patch.object(client,"evaluate",side_effect=[None,{"status":"failed","error":"conflict"},{"forgotten":True}]) as evaluate:
            with self.assertRaisesRegex(BridgeError,"conflict"):
                client.call("batch")
            self.assertIn(".forget(app,",evaluate.call_args.args[0])

if __name__ == "__main__":
    unittest.main()
