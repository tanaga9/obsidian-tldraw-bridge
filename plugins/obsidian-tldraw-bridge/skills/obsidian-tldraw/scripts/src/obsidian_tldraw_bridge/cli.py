"""JSON CLI for structured operations and trusted SDK scripts."""
import argparse
import json
import sys
from pathlib import Path
from .obsidian import BridgeError, Client


def parser():
    p = argparse.ArgumentParser(description="Operate local Obsidian tldraw Markdown diagrams.")
    p.add_argument("--vault", required=True, help="Obsidian vault name or id")
    p.add_argument("--obsidian", help="Obsidian CLI executable")
    p.add_argument("--timeout", type=float, default=30)
    p.add_argument("--request-id", help="Idempotent request id; reuse only with identical arguments")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("doctor")
    sub.add_parser("forget", help="Release a completed receipt; its id must not be retried afterwards").add_argument("id")
    sub.add_parser("create", help="Create a new tldraw Markdown note and open its editor session").add_argument("path", help="New vault-relative .md path")
    for command in ("open", "state", "saved", "close"):
        sub.add_parser(command).add_argument("path", help="Vault-relative .md path")
    batch = sub.add_parser("batch")
    batch.add_argument("path")
    batch.add_argument("--revision", required=True)
    batch.add_argument("--input", required=True, help="Operations JSON file, or - for stdin")
    script = sub.add_parser("script", help="Run trusted synchronous JS with editor/app/plugin/require")
    script.add_argument("path")
    script.add_argument("--revision", required=True)
    script.add_argument("--input", required=True, help="Trusted JavaScript file, or - for stdin")
    for edit_parser in (batch, script):
        edit_parser.add_argument("--full", action="store_true", help="Include full document records and editor diagnostics in the result")
    preview = sub.add_parser("preview")
    preview.add_argument("path")
    preview.add_argument("--output", required=True)
    preview.add_argument("--revision")
    return p


def main(argv=None):
    options = parser().parse_args(argv)
    try:
        if options.timeout <= 0:
            raise BridgeError("Timeout must be positive")
        args = {}
        if hasattr(options, "path"):
            # Obsidian vault paths use forward slashes and never traverse outside the vault.
            path = options.path
            if not path or path.startswith("/") or ".." in path.split("/") or "\\" in path or not path.endswith(".md"):
                raise BridgeError("Use a vault-relative Markdown path without traversal")
            args["path"] = path
        if getattr(options, "revision", None):
            args["revision"] = options.revision
        if options.command in ("batch", "script"):
            if options.full:
                args["full"] = True
            source = sys.stdin.read() if options.input == "-" else Path(options.input).read_text()
            if options.command == "batch":
                data = json.loads(source)
                args["operations"] = data["operations"] if isinstance(data, dict) else data
            else:
                args["code"] = source
        if options.command == "preview":
            output = Path(options.output).expanduser().resolve()
            if not output.parent.is_dir():
                raise BridgeError("Preview output directory does not exist")
            args["output"] = str(output)
        client = Client(options.vault, options.obsidian, options.timeout)
        result = client.forget(options.id) if options.command == "forget" else client.call(options.command, args, options.request_id)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (BridgeError, OSError, ValueError, KeyError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1
