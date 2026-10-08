# Intellij Islands Dark Theme

Port of the JetBrains **Islands Dark** color scheme (IntelliJ IDEA, PyCharm, WebStorm) to Antigravity & VS Code, with one consistent color language across Java / Spring Boot, Python / FastAPI, TypeScript / React / Next.js, JSON, YAML and properties files.

## Installation

### From VSIX
1. Build it: `python3 build_vsix.py` (writes `intellij-islands-dark-theme-<version>.vsix`).
2. Open the Extensions view (`Cmd+Shift+X`).
3. Click `...` in the top right → **Install from VSIX...** and pick the `.vsix`.
4. Command Palette → **Preferences: Color Theme** → **Intellij Islands Dark Theme**.

Or from a terminal: `antigravity-ide --install-extension intellij-islands-dark-theme-<version>.vsix` (`code` for VS Code).

## Color mapping

Values come from IntelliJ's bundled `themes/islands/IslandSchemeDark.xml` and PyCharm's `colorSchemes/PythonDarcula.xml`.

| Element | Color | Examples |
|---|---|---|
| Default text, operators, punctuation, calls, locals, parameters, type names | `#BCBEC4` | `=`, `&&`, `=>`, `findAll()`, `String`, `Props` |
| Keywords, modifiers, primitives, `true`/`false`/`None`, `this` | `#CF8E6D` | `public`, `def`, `const`, `int`, `string` (TS) |
| Function / method / constructor declarations | `#56A8F5` | `def list_users`, `function UserCard` |
| Fields, properties, JSON keys | `#C77DBB` | `this.userName`, `obj.env`, `"name":` |
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
- **Python in Antigravity / other VS Code forks:** Pylance only runs in Microsoft's VS Code, so use the open-source **BasedPyright** extension (`detachhead.basedpyright`) for go-to-definition, set `"python.languageServer": "None"`, and turn semantic highlighting off for Python. BasedPyright's semantic tokens leave called and dotted decorators (`@app.get(...)`) uncolored, while this theme's TextMate rules match PyCharm:

  ```json
  "[python]": { "editor.semanticHighlighting.enabled": false }
  ```
- The bundled `syntaxes/python-builtins.injection.json` makes subscripted built-ins (`dict[str, Any]`, `frozenset[str]`) read as built-ins and keeps fields named like built-ins (`id: str`) plain, as PyCharm does.
