# CLI reference

Direct CLI use is intended for development and debugging. It is not part of the plugin user's setup.

## Command examples

Run these commands from the repository root; package installation is not required.

```sh
python3 bridge.py --vault Documents doctor
python3 bridge.py --vault Documents open 'Drawings/example.md'
python3 bridge.py --vault Documents state 'Drawings/example.md'
```

Use the `revision` returned by `state` when submitting edits:

```sh
python3 bridge.py --vault Documents batch 'Drawings/example.md' \
  --revision '<revision-from-state>' --input examples/create.json
python3 bridge.py --vault Documents preview 'Drawings/example.md' --output /tmp/example.png
python3 bridge.py --vault Documents close 'Drawings/example.md'
```

Use `--obsidian /path/to/executable` or the `OBSIDIAN_CLI` environment variable to override the Obsidian CLI location. Always specify the vault. Diagram paths are vault-relative `.md` paths. For `batch` and `script`, `--input -` reads from standard input. Results are JSON; handled errors are written as JSON to standard error with exit code 1.

Optional Python package installation with `python3 -m pip install .` exposes the `obsidian-tldraw` command. Normal plugin use does not require this installation.

## Release retained results

A request with an explicit `--request-id` can retrieve its result using the same ID and arguments. Release a completed result when it is no longer needed:

```sh
python3 bridge.py --vault Documents forget '<request-id>'
```

Forgetting an ID also removes its deduplication protection. Ordinary results are released automatically after retrieval; timed-out requests are retained. At the 128-receipt limit, new requests are rejected without executing them.
