"""Shared operation boundary for CLI and other adapters; no shell or CLI parsing."""
import math
from pathlib import Path
from .obsidian import BridgeError, Client, validate_connection
from .freehand import compile_script
from .images import load_image


class Bridge:
    """Validate requests before connecting, then use the existing live runtime."""
    def __init__(self, vault, executable=None, timeout=30, client_factory=Client):
        validate_connection(vault, timeout)
        self.config = (vault, executable, timeout)
        self.client_factory = client_factory

    def call(self, action, args=None, request_id=None):
        if request_id is not None and (not isinstance(request_id, str) or not request_id.strip()):
            raise BridgeError("Request ID must be nonempty", code="INVALID_INPUT", outcome="not_applied")
        args = self.prepare(action, {} if args is None else args)
        client = self.client_factory(*self.config)
        return client.call("script" if action == "freehand" else action, args, request_id)

    def status(self, request_id):
        if not isinstance(request_id, str) or not request_id.strip():
            raise BridgeError("Specify a request ID", code="INVALID_INPUT", outcome="not_applied")
        return self.client_factory(*self.config).status(request_id)

    def forget(self, request_id):
        if not isinstance(request_id, str) or not request_id.strip():
            raise BridgeError("Specify a request ID", code="INVALID_INPUT", outcome="not_applied")
        return self.client_factory(*self.config).forget(request_id)

    @staticmethod
    def prepare(action, arguments):
        def invalid(message):
            raise BridgeError(message, code="INVALID_INPUT", outcome="not_applied")
        fields = {
            "doctor": set(), "capabilities": set(), "create": {"path"},
            "style-spec": {"path", "shapeType"},
            "open": {"path", "currentPageId"}, "state": {"path"}, "saved": {"path"}, "close": {"path"},
            "observe": {"path", "revision", "pageId", "limit", "offset", "ids", "bounds"},
            "apply": {"path", "revision", "pageId", "operations", "full"}, "batch": {"path", "revision", "operations", "full"},
            "script": {"path", "revision", "code", "full"}, "freehand": {"path", "revision", "drawing", "full"},
            "image-info": {"file", "maxDimension", "format", "quality", "maxBytes"},
            "insert-image": {"path", "revision", "file", "x", "y", "width", "height", "parentId", "pageId", "shapeId", "full",
                             "maxDimension", "format", "quality", "maxBytes"},
            "preview": {"path", "revision", "output", "ids", "bounds", "part", "scale", "format", "quality"},
        }
        if not isinstance(action, str) or action not in fields:
            invalid("Unknown action")
        if not isinstance(arguments, dict) or set(arguments) - fields[action]:
            invalid("Arguments must be an object with known fields")
        args = dict(arguments)
        if action == "style-spec":
            if not isinstance(args.get("shapeType"), str) or not args["shapeType"].strip():
                invalid("Specify a nonempty shapeType")
        if action not in {"doctor", "capabilities", "image-info"}:
            path = args.get("path")
            if (not isinstance(path, str) or not path or path.startswith("/") or
                    ".." in path.split("/") or "\\" in path or not path.endswith(".md")):
                invalid("Use a vault-relative Markdown path without traversal")
        if action in {"apply", "batch", "script", "freehand", "insert-image"}:
            if not isinstance(args.get("revision"), str) or not args["revision"]:
                invalid("A revision is required for edits")
        if action in {"insert-image", "image-info"}:
            for key in ('maxDimension', 'maxBytes'):
                if key in args and (type(args[key]) is not int or args[key] <= 0):
                    invalid(key + ' must be a positive integer')
            if args.get('format', 'original') not in ('original', 'webp'):
                invalid('format must be original or webp')
            if 'quality' in args and (isinstance(args['quality'], bool) or not isinstance(args['quality'], (int, float))
                                     or not 0 <= args['quality'] <= 1 or args.get('format') != 'webp'):
                invalid('quality must be between 0 and 1 and requires format=webp')
            for key in ('x', 'y', 'width', 'height'):
                if key in args and (isinstance(args[key], bool) or not isinstance(args[key], (int, float))
                                    or not math.isfinite(args[key]) or (key in ('width', 'height') and args[key] <= 0)):
                    invalid(key + ' must be finite' + (' and positive' if key in ('width', 'height') else ''))
            for key, prefix in (('parentId', 'shape:'), ('shapeId', 'shape:'), ('pageId', 'page:')):
                if key in args and (not isinstance(args[key], str) or not args[key].startswith(prefix)):
                    invalid(key + ' must be a ' + prefix + ' ID')
            if not isinstance(args.get('file'), str) or not args['file']:
                invalid('Specify an image file')
            try:
                args.update(load_image(args.pop('file')))
            except (OSError, ValueError) as exc:
                invalid(str(exc))
            # The retained request compares serialized arguments. Keep CLI and
            # Python image calls identical even when callers order keys differently.
            args = dict(sorted(args.items()))
        if action == "freehand":
            try:
                args["code"] = compile_script(args.pop("drawing"))
            except (ValueError, KeyError, TypeError) as exc:
                invalid(str(exc))
            # All adapters send the same compiled script to the runtime.
        if action in {"observe", "preview"}:
            selectors = [key for key in ("ids", "bounds", "part") if key in args]
            if len(selectors) > 1:
                invalid("Choose ids, part, or bounds, not more than one")
            if "ids" in args and (not isinstance(args["ids"], list) or not args["ids"] or
                                  any(not isinstance(i, str) for i in args["ids"])):
                invalid("ids must be a nonempty list of shape IDs")
            if "bounds" in args:
                b = args["bounds"]
                if (not isinstance(b, dict) or any(isinstance(b.get(k), bool) or
                    not isinstance(b.get(k), (int, float)) or not math.isfinite(b[k]) for k in ("x", "y", "w", "h"))
                    or b["w"] <= 0 or b["h"] <= 0):
                    invalid("Bounds must be finite with positive width and height")
        if action == "observe":
            limit = args.get("limit", 100)
            offset = args.get("offset", 0)
            if type(limit) is not int or not 1 <= limit <= 500 or type(offset) is not int or offset < 0:
                invalid("Observe requires limit 1-500 and offset >= 0")
            if offset and (not args.get("revision") or not args.get("pageId")):
                invalid("Observe pagination requires revision and pageId")
        if action == "preview":
            if args.get('format', 'webp') not in ('png', 'webp'):
                invalid("Preview format must be png or webp")
            if 'quality' in args and (isinstance(args['quality'], bool) or not isinstance(args['quality'], (int, float))
                                     or not 0 <= args['quality'] <= 1 or not math.isfinite(args['quality'])
                                     or args.get('format', 'webp') != 'webp'):
                invalid("Preview quality must be between 0 and 1 and is only supported for WebP")
            scale = args.get("scale", 1)
            if isinstance(scale, bool) or not isinstance(scale, (int, float)) or not 0 < scale <= 4:
                invalid("Preview scale must be greater than 0 and at most 4")
            output = Path(args.get("output", "")).expanduser().resolve()
            if not args.get("output") or not output.parent.is_dir():
                invalid("Preview output directory does not exist")
            args["output"] = str(output)
        return args
