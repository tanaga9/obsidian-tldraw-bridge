# Known limitations

The following implementation boundaries apply to the current bridge.

Python 3.9.6+ is an environment prerequisite. The bridge does not bundle or install Python. Codex notifies the user if it is missing or too old. Providing a Python runtime is not outstanding work. User setup consists only of installing the Codex plugin.

| Item | Status | Current approach |
| --- | --- | --- |
| Public plugin directory publication | Not published | A local marketplace package is provided. |
| Automatic session recovery or forced disposal after file rename/deletion or disabling the existing plugin | Not implemented | If normal session closure cannot recover, restart Obsidian and reopen an existing document using its current path. This does not restore a deleted document. |
| Updating the runtime loader itself | Requires restart | Drawing runtime source changes at the same installed path reload automatically after persistence checks. Changes to `loader.cjs` itself require restarting Obsidian. |
| Cancelling or restoring arbitrary asynchronous scripts | Unsupported | Use synchronous scripts only. Detecting a Promise does not cancel already scheduled work. |
| Automatically supporting SDK updates | Not implemented | Accept only the currently supported plugin versions; reject others. |

Restoring Store records after a synchronous script failure is implemented and tested. Side effects outside the Store and full mutual exclusion with human GUI edits are outside the guarantee.
