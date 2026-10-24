"""JSON CLI for structured operations and trusted SDK scripts."""
import argparse
import json
import sys
from pathlib import Path
from .obsidian import BridgeError, Client
from .api import Bridge, list_vaults


def parser():
    p = argparse.ArgumentParser(description="Operate local Obsidian tldraw Markdown diagrams.")
    p.add_argument("--vault", help="Obsidian vault name or id (required except for vaults)")
    p.add_argument("--obsidian", help="Obsidian CLI executable")
    p.add_argument("--timeout", type=float, default=30, help="Total dispatch/poll timeout in seconds (default: 30)")
    p.add_argument("--request-id", help="Idempotent request id; reuse only with identical arguments")
    sub = p.add_subparsers(dest="command", required=True)
    vaults = sub.add_parser("vaults", help="List registered vaults and on-disk tldraw installation status")
    vaults.add_argument("--config-dir", default=".obsidian", help="Configuration folder name to inspect in each vault (default: .obsidian)")
    sub.add_parser("doctor")
    sub.add_parser("capabilities", help="Discover runtime operations and limits")
    style_spec = sub.add_parser("style-spec", help="Read installed style values and defaults from an open document")
    style_spec.add_argument("path", help="Open vault-relative .md path")
    style_spec.add_argument("--shape-type", required=True, help="Registered shape type, e.g. geo")
    languages = sub.add_parser('language-status', help='Inspect language freshness without translating or changing pages')
    languages.add_argument('path')
    languages.add_argument('--diagram-id', help='Inspect one logical diagram in this note')
    checkpoint = sub.add_parser('language-checkpoint', help='Record a reviewed translation/layout checkpoint; never translates')
    checkpoint.add_argument('path')
    checkpoint.add_argument('--revision', required=True)
    checkpoint.add_argument('--input', required=True, help='Reviewed checkpoint JSON file, or - for stdin')
    sub.add_parser("status", help="Inspect a retained request without re-executing it").add_argument("id")
    observe = sub.add_parser("observe", help="Read compact current-page shapes, text, bounds, and connections")
    observe.add_argument("path")
    observe.add_argument("--revision", help="Required when continuing an observation at an offset")
    observe.add_argument("--page-id", help="Pin currentPageId when continuing observation")
    observe.add_argument("--limit", type=int, default=100)
    observe.add_argument("--offset", type=int, default=0)
    selection = observe.add_mutually_exclusive_group()
    selection.add_argument("--ids", nargs="+")
    selection.add_argument("--bounds", nargs=4, type=float, metavar=("X", "Y", "W", "H"))
    apply = sub.add_parser("apply", help="Apply named, validated operations")
    apply.add_argument("path")
    apply.add_argument("--revision", required=True)
    apply.add_argument("--page-id", help="Reject if the dedicated Editor changed pages")
    apply.add_argument("--input", required=True, help="Operations JSON file, or - for stdin")
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
    freehand = sub.add_parser("freehand", help="Create or redraw named strokes from authored curves")
    freehand.add_argument("path")
    freehand.add_argument("--revision", required=True)
    freehand.add_argument("--input", required=True, help="Stroke definitions JSON file, or - for stdin")
    image = sub.add_parser("insert-image", help="Embed a local PNG, WebP or JPEG image")
    image.add_argument("path", help="Open vault-relative .md path")
    image.add_argument("--revision", required=True)
    info = sub.add_parser('image-info', help='Inspect image dimensions and embedded size without editing a diagram')
    for image_parser in (image, info):
        image_parser.add_argument('--file', required=True, help='Local PNG, WebP or JPEG file')
        image_parser.add_argument('--max-dimension', type=int, help='Resize pixels to fit this longest edge; never upscale')
        image_parser.add_argument('--format', choices=('original', 'webp'), help='Default: original; WebP conversion is opt-in')
        image_parser.add_argument('--quality', type=float, help='WebP encoding quality 0–1 (default 0.85 when encoding)')
        image_parser.add_argument('--max-bytes', type=int, help='Optional limit on processed image bytes, before base64 encoding')
    for dimension in ('x', 'y', 'width', 'height'):
        image.add_argument('--' + dimension, type=float)
    image.add_argument('--parent-id', help="Parent shape on the current page; coordinates are parent-local")
    image.add_argument('--page-id', help="Pin the current page")
    image.add_argument('--shape-id', help="Optional new shape: ID (existing shapes are never replaced)")
    for edit_parser in (apply, batch, script, freehand, image, checkpoint):
        edit_parser.add_argument("--full", action="store_true", help="Include full document records and editor diagnostics in the result")
    preview = sub.add_parser("preview")
    preview.add_argument("path")
    preview.add_argument("--output", required=True)
    preview.add_argument("--revision")
    region = preview.add_mutually_exclusive_group()
    region.add_argument("--ids", nargs="+", help="Preview only these current-page shape IDs")
    region.add_argument("--part", help="Preview only freehand strokes tagged with this part")
    region.add_argument("--bounds", nargs=4, type=float, metavar=("X", "Y", "W", "H"),
                        help="Crop the full current page to this page-coordinate rectangle, including surrounding shapes")
    preview.add_argument("--scale", type=float, default=1, help="Export scale, greater than 0 and at most 4")
    preview.add_argument("--format", choices=('png', 'webp'), help="Output format (default: webp; not inferred from the filename)")
    preview.add_argument("--quality", type=float, help="WebP encoding quality 0–1 (default 0.9); not supported with --format png")
    return p


def _read_input(path):
    if path != "-":
        return Path(path).read_text(encoding="utf-8-sig")
    # Decode redirected input independently of Python's locale or stdio settings.
    buffer = getattr(sys.stdin, "buffer", None)
    if buffer is not None:
        return buffer.read().decode("utf-8-sig")
    source = sys.stdin.read()
    return source[1:] if source.startswith("\ufeff") else source


def _print_json(value, stream, *, ensure_ascii=False):
    text = json.dumps(value, ensure_ascii=ensure_ascii, indent=2) + "\n"
    buffer = getattr(stream, "buffer", None)
    if buffer is not None:
        stream.flush()
        buffer.write(text.encode("utf-8"))
        buffer.flush()
    else:
        # In-process callers may supply text-only streams such as StringIO.
        stream.write(text)
        stream.flush()


def main(argv=None):
    options = parser().parse_args(argv)
    try:
        if options.command == 'vaults':
            if options.vault is not None or options.request_id is not None:
                raise BridgeError('vaults does not accept --vault or --request-id', code='INVALID_INPUT', outcome='not_applied')
            result = list_vaults(options.obsidian, options.timeout, options.config_dir)
        else:
            result = _execute(options)
    except (BridgeError, OSError, ValueError, KeyError) as exc:
        error = exc if isinstance(exc, BridgeError) else BridgeError(str(exc), code="INVALID_INPUT", outcome="not_applied")
        _print_json({"error": error.as_dict()}, sys.stderr)
        return 1
    return _output(options, result)


def _execute(options):
    bridge = Bridge(options.vault, options.obsidian, options.timeout, client_factory=Client)
    args = {}
    if hasattr(options, "path"):
        args["path"] = options.path
    if getattr(options, "revision", None):
        args["revision"] = options.revision
    if options.command == "style-spec":
        args["shapeType"] = options.shape_type
    if options.command == 'language-status' and options.diagram_id is not None:
        args['diagramId'] = options.diagram_id
    if options.command in ('insert-image', 'image-info'):
        args['file'] = options.file
        for option, key in (('max_dimension', 'maxDimension'), ('format', 'format'), ('quality', 'quality'), ('max_bytes', 'maxBytes')):
            value = getattr(options, option)
            if value is not None:
                args[key] = value
    if options.command == 'insert-image':
        for key in ('x', 'y', 'width', 'height', 'parent_id', 'page_id', 'shape_id'):
            value = getattr(options, key)
            if value is not None:
                args[{'parent_id': 'parentId', 'page_id': 'pageId', 'shape_id': 'shapeId'}.get(key, key)] = value
        if options.full:
            args['full'] = True
    if options.command in ("apply", "batch", "script", "freehand", "language-checkpoint"):
        if options.full:
            args["full"] = True
        source = _read_input(options.input)
        if options.command in ("apply", "batch"):
            data = json.loads(source)
            args["operations"] = data["operations"] if isinstance(data, dict) else data
        elif options.command == 'language-checkpoint':
            args['checkpoint'] = json.loads(source)
        elif options.command == "freehand":
            args["drawing"] = json.loads(source)
        else:
            args["code"] = source
    if options.command in ("observe", "preview"):
        if options.ids is not None:
            args["ids"] = options.ids
        if options.bounds is not None:
            args["bounds"] = dict(zip(("x", "y", "w", "h"), options.bounds))
    if options.command == "apply" and options.page_id is not None:
        args["pageId"] = options.page_id
    if options.command == "observe":
        args.update(limit=options.limit, offset=options.offset)
        if options.page_id is not None:
            args["pageId"] = options.page_id
    if options.command == "preview":
        args["output"] = options.output
        if options.format is not None:
            args['format'] = options.format
        if options.quality is not None:
            args['quality'] = options.quality
        if options.scale != 1:
            args["scale"] = options.scale
        if options.part is not None:
            args["part"] = options.part
    if options.command == "forget":
        result = bridge.forget(options.id)
    elif options.command == "status":
        result = bridge.status(options.id)
    else:
        result = bridge.call(options.command, args, options.request_id)
    return result


def _output(options, result):
    # Output errors happen after execution and cannot make a completed edit
    # unapplied. Keep the successful result, including when no receipt was retained.
    try:
        _print_json(result, sys.stdout)
    except (OSError, ValueError) as exc:
        if isinstance(exc, OSError):
            # Discard pending output so shutdown does not retry a failed flush
            # and append a traceback to the structured stderr diagnostic.
            try:
                close = getattr(sys.stdout, 'close', None)
                if close is not None:
                    close()
            except (OSError, ValueError):
                pass
        mutating = options.command in {'create', 'open', 'close', 'apply', 'batch', 'script',
                                       'freehand', 'insert-image', 'preview', 'forget', 'language-checkpoint'}
        outcome = 'applied' if mutating else 'unknown' if options.command == 'status' else 'not_applied'
        request_id = options.id if options.command in {'status', 'forget'} else options.request_id
        error = BridgeError('Could not output completed command result: ' + str(exc),
                            code='OUTPUT_FAILED', outcome=outcome, request_id=request_id,
                            details={'command': options.command, 'result': result,
                                     'recovery': 'The command completed. Inspect this result; do not repeat mutations.'})
        # Escaping also preserves results that could not be encoded as UTF-8.
        _print_json({'error': error.as_dict()}, sys.stderr, ensure_ascii=True)
        return 1
    return 0
