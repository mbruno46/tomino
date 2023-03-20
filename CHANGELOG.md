# Changelog

All notable changes to this project will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

### Added 

- Documentation
- Context menu (right-click) currently not supported in tauri. When available the following features will be implemented: Set Main, Preview, Delete File, Rename. Temporary solution for `Set Main` under `File` menu.
- Settings panel. Add support to customize font size in editor, global theme
- Editor. Add syntax helpers for unclosed parethensis {}
- Footer. Add git support to detect unstaged changes
- File menu. Add support for `Save as..`

### Fixed

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