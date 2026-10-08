# Intellij Islands Dark Theme

Port of the JetBrains **Islands Dark** color scheme (IntelliJ IDEA, PyCharm, WebStorm) to Antigravity & VS Code, with one consistent color language across Java / Spring Boot, Python / FastAPI, TypeScript / React / Next.js, JSON, YAML and properties files.

## Installation

### From VSIX
1. Build it: `python3 build_vsix.py` (writes `intellij-islands-dark-theme-<version>.vsix`).
2. Open the Extensions view (`Cmd+Shift+X`).
3. Click `...` in the top right → **Install from VSIX...** and pick the `.vsix`.
4. Command Palette → **Preferences: Color Theme** → **Intellij Islands Dark Theme**.

Or from a terminal: `antigravity-ide --install-extension intellij-islands-dark-theme-<version>.vsix` (`code` for VS Code).

### Antigravity — one command

```bash
python3 setup_antigravity.py
```

Then run **Developer: Reload Window**. The script reads `editor/antigravity-setup.json` and:

- installs the theme `.vsix` matching `package.json`'s version;
- **uninstalls Pylance** — it cannot run outside Microsoft's VS Code, and its bundled `PylancePython.tmLanguage` replaces the Python grammar, labelling every annotation class (`ApplyStatus`, `list[AppliedRecord]`) as a built-in;
- **uninstalls Python Environments** (`ms-python.vscode-python-envs`) — it depends on the native `pet` binary, which the Open VSX ("universal") build of the Python extension does not ship, so it cannot resolve any interpreter and keeps raising "Default interpreter path … could not be resolved". The Python extension itself does not need it (`python.useEnvironmentsExtension` is off by default) and finds interpreters with its JavaScript locator;
- installs **BasedPyright** for go-to-definition, hovers and type checking;
- drops stale `editor.tokenColorCustomizations` / `editor.semanticTokenColorCustomizations` (they override any theme) and orphaned `python-envs.*` settings, then sets the theme, `python.languageServer: "None"`, Python semantic highlighting off, and BasedPyright's `standard` checking mode. A backup of `settings.json` goes to the temp folder first.

Override the editor paths with `ANTIGRAVITY_CLI` and `ANTIGRAVITY_SETTINGS` (e.g. for VS Code or another fork). For interpreters outside the project (such as uv environments in `~/.uv/envs`), set `python.venvPath` to that folder and `python.defaultInterpreterPath` to the one to use.

## Color mapping

Values come from IntelliJ's bundled `themes/islands/IslandSchemeDark.xml` and PyCharm's `colorSchemes/PythonDarcula.xml`.

| Element | Color | Examples |
|---|---|---|
| Default text, operators, punctuation, calls, locals, parameters, type names | `#BCBEC4` | `=`, `&&`, `=>`, `findAll()`, `String`, `Props` |
| Keywords, modifiers, primitives, `true`/`false`/`None`, `this` | `#CF8E6D` | `public`, `def`, `const`, `int`, `string` (TS) |
| Function / method / constructor declarations | `#56A8F5` | `def list_users`, `function UserCard` |
| Fields, properties, Java record components, JSON keys | `#C77DBB` | `this.userName`, `record Point(int x)`, `obj.env`, `"name":` |
| Static fields, constants, enum members, JS globals | `#C77DBB` italic | `MAX_USERS`, `Color.RED`, `window` |
| Annotations and decorators | `#B3AE60` | `@RestController`, `@app.get` |
| Strings | `#6AAB73` | `"bob"` |
| Escapes, format placeholders | `#CF8E6D` | `\n`, `{0}` |
| Numbers | `#2AACB8` | `42` |
| Comments | `#7A7E85` | `// note`, `/* note */`, `# note` |
| Doc comments, Python docstrings | `#5F826B` italic | `/** ... */`, `"""..."""` |
| Type parameters | `#16BAAC` | `<T>` |
| HTML / JSX tags · components · attributes | `#D5B778` · `#2FBAA3` · `#BABABA` | `<div>` · `<Button>` · `className` |
| YAML and `.properties` keys | `#CF8E6D` | `spring:` |
| Python `self` / `cls` | `#94558D` | `self.items` |
| Python keyword arguments | `#AA4926` | `sep=", "` |
| Python built-ins | `#8888C6` | `print`, `len`, `str`, `ValueError` |
| Python dunder names | `#B200B2` | `__init__`, `__name__` |

Function and method **calls** are default text in every language (only declarations are blue), so Java, Python and TypeScript read the same way.

## Notes

- Semantic highlighting (Java language server, TypeScript) is enabled by the theme; it is what colors `console`/`window` as globals and type parameters at their use sites.
- **Python semantic highlighting is off** (set by `setup_antigravity.py`): BasedPyright's semantic tokens leave called and dotted decorators (`@app.get(...)`) uncolored, while this theme's TextMate rules match PyCharm.
- The bundled `syntaxes/python-builtins.injection.json` makes subscripted built-ins (`dict[str, Any]`, `frozenset[str]`) read as built-ins and keeps fields named like built-ins (`id: str`) plain, as PyCharm does.
