# <img src="src-tauri/icons/512x512.png" height='48px'> tomino

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Publish](https://github.com/mbruno46/tomino/actions/workflows/publish.yml/badge.svg)](https://github.com/mbruno46/tomino/actions/workflows/publish.yml)
[![Latest Release](https://img.shields.io/github/v/release/mbruno46/tomino)](https://github.com/mbruno46/tomino/releases/latest)

A lightweight and intuitive TeX editor for the everyday physicist. **tomino** is built using [Vue3](https://vuejs.org), [Vite](https://vitejs.dev) and [Tauri](https://tauri.app), and supersedes its older predecessor [ToM](https://github.com/mbruno46/ToM).

- **Website:** https://mbruno46.github.io/tomino/
- **Source code:** https://github.com/mbruno46/tomino/
- **Bug reports:** https://github.com/mbruno46/tomino/issues


### Authors

Copyright (C) 2023, Mattia Bruno

## Installation (macOS, Linux)

### macOS

*Note: the app is free software and not signed for macOS. As a consequence, 
macOS prevents its installation and execution.
To use tomino on macOS users should follow the instructions below.*

  * To automatically download and install the latest version in `$HOME/Applications/` 
    open a terminal and type
```bash
# macOS
curl -Ls https://raw.githubusercontent.com/mbruno46/tomino/main/scripts/macos_installer.sh | bash -s
```
  * Alternatively, download the lastest `.tar.gz` release from [here](https://github.com/mbruno46/tomino/releases/), unpack it and run
```bash
xattr -dr com.apple.quarantine /path/to/tomino.app
```

### Linux

Download the lastest release from [here](https://github.com/mbruno46/tomino/releases/)

