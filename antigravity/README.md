# Antigravity editor setup

Editor configuration that makes Python work in Antigravity (a VS Code fork) and lets the
[Islands Dark theme](../README.md) render as it does in PyCharm. Separate from the theme
plugin: it has no version of its own and is never packaged into the `.vsix`.

## Run

```bash
python3 antigravity/setup_antigravity.py
```

Then **Developer: Reload Window**. Install the theme first (see the [repository README](../README.md)).

It is idempotent — rerun it after upgrading Antigravity or the Python extension. Settings and
extensions live outside the app (`~/Library/Application Support/Antigravity IDE/User/settings.json`,
`~/.antigravity-ide/extensions`), so an app upgrade keeps them; a Python-extension update can
pull its pack members (Pylance, Python Environments) back in, and a rerun removes them again.

Everything it applies is in [`setup.json`](setup.json). Override the paths with
`ANTIGRAVITY_CLI` and `ANTIGRAVITY_SETTINGS` (e.g. for VS Code or another fork). A backup of
`settings.json` goes to the temp folder before it is rewritten.

## What it changes, and why

| Change | Why |
|---|---|
| Uninstall **Pylance** (`ms-python.vscode-pylance`) | Its server only runs in Microsoft's VS Code, and its bundled `PylancePython.tmLanguage` replaces the Python grammar, labelling every annotation class (`ApplyStatus`, `list[AppliedRecord]`) as a built-in. |
| Uninstall **Python Environments** (`ms-python.vscode-python-envs`) | It needs the native `pet` binary, which the Open VSX ("universal") build of the Python extension does not ship (`spawn …/python-env-tools/bin/pet ENOENT`), so it can never resolve an interpreter and keeps raising "Default interpreter path … could not be resolved". The Python extension does not need it. |
| Install **BasedPyright** (`detachhead.basedpyright`) | Open-source Pyright build: go-to-definition, hovers, type checking. |
| `python.languageServer: "None"` | Stops the Python extension from trying to start Pylance. |
| `basedpyright.analysis.typeCheckingMode: "standard"` | BasedPyright's default mode flags every `Any`, implicit string concatenation, unannotated class attributes, … |
| `[python]` → `editor.semanticHighlighting.enabled: false` | BasedPyright's semantic tokens leave called and dotted decorators (`@app.get(...)`) uncolored; the theme's TextMate rules match PyCharm. |
| `workbench.colorTheme: "Intellij Islands Dark Theme"` | Selects the theme. |
| Drop `editor.tokenColorCustomizations`, `editor.semanticTokenColorCustomizations`, `python-envs.*` | Color customizations override any theme; `python-envs.*` is orphaned once Python Environments is gone. |

Interpreters outside the project (such as uv environments in `~/.uv/envs`) are found by the
Python extension through `python.venvPath` (the folder) and `python.defaultInterpreterPath`
(the one to use); set those per machine.
