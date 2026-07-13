# <img src="icons/icon.png" height='48px' style='vertical-align: bottom'> tomino

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Publish](https://github.com/mbruno46/tomino/actions/workflows/release.yml/badge.svg)](https://github.com/mbruno46/tomino/actions/workflows/release.yml)
[![Latest Release](https://img.shields.io/github/v/release/mbruno46/tomino)](https://github.com/mbruno46/tomino/releases/latest)

A lightweight and intuitive TeX editor for the everyday physicist. **tomino** is built using Python and the PyQt library.

Versions older than v1 were built using [Vue3](https://vuejs.org), [Vite](https://vitejs.dev) and [Tauri](https://tauri.app), and supersededed the older predecessor [ToM](https://github.com/mbruno46/ToM).

- **Website:** https://mbruno46.github.io/tomino/
- **Source code:** https://github.com/mbruno46/tomino/
- **Bug reports:** https://github.com/mbruno46/tomino/issues

### Authors

Copyright (C) 2023-2025, Mattia Bruno

## Requirements

 - `latexmk` for the compilation of LaTeX files. Instructions to install it on your system can be found [here](https://mg.readthedocs.io/latexmk.html)

## Installation (macOS, Linux)

### macOS

*Note: the app is free software and not signed for macOS. As a consequence, 
macOS prevents its installation and execution.
To use tomino on macOS users should follow the instructions below.*

  * Download the lastest `.tar.gz` release from [here](https://github.com/mbruno46/tomino/releases/), unpack it and run the following command
```bash
xattr -dr com.apple.quarantine /path/to/tomino.app
```

### Linux

Download the lastest release from [here](https://github.com/mbruno46/tomino/releases/)

