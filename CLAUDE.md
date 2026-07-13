# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

**tomino** is a lightweight, desktop TeX/LaTeX editor for physicists, built with Python and PyQt6. The UI is a single `QMainWindow` split into three vertical panels:

- **Left** — `Browser` (`src/browser.py`): a toggleable side panel with a vertical toolbar switching between a file-system tree (`FileBrowserTree`) and a table of contents (`TOC`) generated from the parsed LaTeX document.
- **Center** — `FileEditor` (`src/editor.py`): a tabbed `QPlainTextEdit`-based editor with line numbers, syntax highlighting, and autocomplete, plus a `Finder` (`src/finder.py`) find/replace bar docked below it.
- **Right** — `Viewer` (`src/viewer.py`): a `QPdfView`-based PDF viewer with zoom/fit controls and a log/error panel that is shown when LaTeX compilation fails.

Only versions v1+ use this Python/PyQt6 stack. Older versions (pre-v1) were a Vue3/Vite/Tauri app (see `.github/workflows/publish.yml`, now dead/superseded by `release.yml`); do not reuse Tauri-era assumptions.

## Commands

There is no test suite, linter, or formatter configured in this repo — don't invent one.

```bash
# one-time environment setup (creates ./pyenv venv and installs requirements.txt)
sh bootstrap.sh python3

# run the app
./pyenv/bin/python src/main.py

# run the app in debug mode (auto-opens the folder hardcoded in main.py: MainWindow.__init__)
./pyenv/bin/python src/main.py -d

# build a standalone app bundle (uses tomino.spec, outputs to dist/ and build/)
./pyenv/bin/pyinstaller -y tomino.spec
```

`latexmk` must be installed on the system for LaTeX compilation to work (invoked as a subprocess, see `latex.py`).

### latexdb helper script

`./latexdb` (repo root, standalone script — not part of `src/`) inspects/edits the LaTeX keyword JSON databases in `src/` (`-t {math,cmds}` to view, `-a <word>` to add a new keyword). Note it currently only knows about `files = ['math','cmds']`, not `envs`.

## Architecture

### LaTeX document model (`src/latex.py`)

- `TexFile` parses a `.tex` file line-by-line with regex to find LaTeX commands (`\tag[square]{curly}`), builds a tree of `TexNode`s, and recursively follows `\input{...}` to build a tree of child `TexFile`s (and `BibFile`s for `\bibliography{...}`). Each `TexFile`/`BibFile` watches its own file via `QFileSystemWatcher` and re-parses itself on change, incrementally updating global autocomplete registries (`ref`, `cite` from `autocompleter.py`) and the TOC.
- `TexModel` (a `QAbstractItemModel`) is a **module-level singleton** (`latex.model`) that backs the `TOC` tree view in the browser panel. It's populated by section-like commands (`chapter`/`section`/`subsection`, see `latex_sections`) as files are parsed.
- `latex.init(filename)` is the entry point called when the user double-clicks a `.tex` file in the browser to set it as the "main" document; it resets `latex.model` and builds the `TexFile` tree from that file.
- `Compiler` is a `QThread` that shells out to `latexmk` (weak = normal recompile, hard = force + clean recompile), emitting a `success` signal consumed by `MainWindow.recompile` in `main.py` to load the resulting PDF or show the `.log` file as an error.

### Autocomplete (`src/autocompleter.py`)

- Keyword lists for math symbols/commands/environments are static JSON files at `src/latex.{math,cmds,envs}.json`, loaded once at import time.
- `AutoCompleter` (constructed once as `editor.completer`, shared across all open tabs) dispatches to per-command-type `QCompleter` subclasses (`AutoCompleterBasic` for generic `\cmd`, `AutoCompleterEnvironments` for `\begin{...}` snippets, `AutoCompleterGeneric` for `\input`/`\bibliography`/`\includegraphics`, `AutoCompleterRef`/`AutoCompleterCite` for cross-references) based on regex-matching the command name before the cursor.
- `ref` and `cite` are dynamic `AutoCompleterMultiple` registries keyed by source filename, kept in sync by `TexFile`/`BibFile` as documents are parsed/edited so that label/citation suggestions update live as files change elsewhere in the project.
- Autocomplete keyword updates for files (input/bibliography/includegraphics completions) are driven by `FileBrowserTree`'s `QFileSystemModel` row insert/remove signals in `browser.py`, not by the editor itself.

### Editor (`src/editor.py`)

- `Editor` is a `QPlainTextEdit` subclass with a custom `NumberBar` gutter widget (paints line numbers, redraws on `updateRequest`) and a `Highlighter` (`src/highligher.py`, regex-based `QSyntaxHighlighter` for commands/brackets/comments).
- `FileEditor` is the `QTabWidget` holding all open `Editor` tabs; it dynamically installs undo/redo/cut/copy/paste/comment wrapper methods that forward to `self.currentWidget()`, and tracks modified/unmodified state in tab labels (prefixing `* ` when dirty).
- Indentation, commenting (`Ctrl+/`), and completer key handling (arrow keys/tab/enter get forwarded to the completer popup instead of the text edit when it's visible) all live in `Editor.keyPressEvent`.

### Settings & theming (`src/settings.py`, `src/style.py`)

- `settings.init()` builds `QPalette`/`QFont` dicts (`settings.app`, `settings.editor`, `settings.browser`, `settings.viewer`) from a single hardcoded `themes["dark"]` dict — there is currently only one theme, and no persisted user config despite `SettingsWindow` existing as a stub (only font-size spinbox, not yet wired up).
- `style.py` builds Qt stylesheet strings from the same theme dict for tab bars, browser toolbar, PDF viewer toolbar, finder bar, and splitter handles.
- SVG toolbar icons are recolored at runtime per-theme via `src/svg.py` (`create_icon`), which parses the SVG string with `QDomDocument` and rewrites `stroke`/`fill` attributes rather than shipping separate icon assets per color.

### Menu wiring (`src/main.py`)

- Menus are declared as data (`menus` dict: label → list of `(text, shortcut, action_path)`), and `get_nested_attr` resolves dotted action paths (e.g. `'file_editor.save_file'`) against `self` at menu-build time — when adding a menu action, prefer extending this dict over writing bespoke `QAction` wiring.

## Known gaps (see `src/todo` and `CHANGELOG.md` `[Unreleased]`)

- No settings persistence (per-project `.tomino` config file, font/theme customization) yet — `SettingsWindow` is a placeholder.
- No SyncTeX support (jumping between PDF and source) yet.
- Find/replace (`Finder`) currently only supports "find", not "replace".
- Right-click context menu (Set Main / Preview / Delete / Rename) not implemented; "Set Main" is currently only reachable via double-click in the file browser.

## Packaging notes

- `tomino.spec` is the PyInstaller spec (bundles `icons/`, `src/latex.*.json`, `src/assets`); it builds a macOS `.app` bundle or Linux bundle depending on `os.uname().sysname`.
- Releases are built by `.github/workflows/release.yml` on push to the `release` branch (drafts a GitHub release, builds on `macos-latest` and `macos-13` runners only — no Linux CI build currently, despite Linux being a supported install target per README).
- `VERSION` (plain text, e.g. `v1.0.0-alpha`) is the single source of truth for the version used in both the PyInstaller bundle metadata and the release tag.
