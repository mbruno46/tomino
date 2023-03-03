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

## [v0.3.2] - 2023-03-03

- First stable release of tomino

### Added

- Menus with basic functionalities (File, Edit, Window, Help)
- Left side bar, with buttons to fold the browser, recompile and open Settings panel
- Settings panel
- Browser module to browse files of a project. Features add file and folders, automatic file system watcher.
- Main editor to edit .tex and .bib files. Features syntax highlighting, find/replace, autocomplete, undo/redo history
- PDF Viewer to display compiled pdf. Features zoom functionalities, scroll. The page view is preserved after recompilation.