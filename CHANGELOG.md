# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added

- Settings persistence (per-project `.tomino` config file, font/theme customization)
- Find/replace in the `Finder` bar (currently only "find" is supported)
- Right-click context menu in the file browser (Set Main / Preview / Delete / Rename)


## [1.0] - 2026-07-14

Complete rewrite: **tomino** is now a native desktop app built with Python and PyQt6,
replacing the previous Vue3/Vite/Tauri stack. This is a full break from the `0.x`
releases below — no migration path, own versioning going forward.

### Added

- Three-panel desktop UI: file browser + table of contents, tabbed editor, PDF viewer
- Autocomplete for LaTeX commands, math symbols, environments, cross-references,
  citations, and file paths (`\input`, `\bibliography`, `\includegraphics`)
- Syntax highlighting, line numbers, indentation-aware editing, line commenting
- Find bar
- LaTeX compilation via `latexmk`, run in the background so the UI never freezes,
  with inline log view on compile errors
- PDF viewer with zoom/fit controls, preserving scroll position across recompiles
- SyncTeX support: double-click in the editor jumps to the matching PDF location
  and vice versa
- macOS and Linux app bundles via PyInstaller


## [0.4.2] - 2023-05-01

### Added

- New file browser engine, with new internal file system responding to file deletion/creation/modification
- Addded suggestion for bib and tex files, alongside figures

### Fixed

- Fixed scrolling bug in suggestions/autocomplete
- Fixed bug rebuilding pdf viewer on latex error; now focus page preserved


## [0.4.0] - 2023-03-20

### Added

- New rendering engine with better memory efficiency (only pages in viewport are rendered) and better zoom handling and several bug fixes
- Extended latex support also for math commands

### Fixed

- Fixed bug Cmd/Ctrl+R not working from editor
- Fixed bug comment not updating selection/caret
- Fixed bug wrong repainting pdf pages (canvas) on zoom
- Fixed bug rendering last page of document on scroll
- Changed pdf.js version to 2.14.305 from 2.12.313; `core-js` required

## [0.3.3] - 2023-03-04

### Changed

- Fixed latex compilation bug: `$PATH` env variable is now properly set when tomino launches `latexmk`
- Fixed PDF viewer bug: `pdfjsLib.GlobalWorkerOptions` is now properly initialized with pdfjsWorker

## [0.3.2] - 2023-03-03

- First stable release of tomino

### Added

- Menus with basic functionalities (File, Edit, Window, Help)
- Left side bar, with buttons to fold the browser, recompile and open Settings panel
- Settings panel
- Browser module to browse files of a project. Features add file and folders, automatic file system watcher.
- Main editor to edit .tex and .bib files. Features syntax highlighting, find/replace, autocomplete, undo/redo history
- PDF Viewer to display compiled pdf. Features zoom functionalities, scroll. The page view is preserved after recompilation.
