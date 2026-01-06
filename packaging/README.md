# DocToMoodle Packaging

This directory contains build scripts and configuration for creating standalone executables of the DocToMoodle application.

## Directory Structure

```
packaging/
├─ pyinstaller/
│  └─ doctomood_gui.spec
├─ linux/
│  └─ build.sh
└─ windows/
   └─ build.ps1
```

## Overview

The build process is located in the `packaging/` directory to keep the source directory clean. The final executable is created in `packaging/build/doctomood-gui` (or `packaging/build/doctomood-gui.exe` on Windows).

## Prerequisites

- Python 3.10 or higher
- All application dependencies installed

## Quick Start

### Linux

```bash
# Navigate to the packaging directory
cd packaging

# Install build dependencies (if requirements-build.txt exists)
# pip install -r requirements-build.txt

# Build the executable
./linux/build.sh

# The executable will be in packaging/build/doctomood-gui
```

### Windows

```powershell
# Navigate to the packaging directory
cd packaging

# Install build dependencies (if requirements-build.txt exists)
# pip install -r requirements-build.txt

# Build the executable
.\windows\build.ps1

# The executable will be in packaging\build\doctomood-gui.exe
```

## Files

- `pyinstaller/doctomood_gui.spec` - PyInstaller specification file
- `linux/build.sh` - Linux build script
- `windows/build.ps1` - Windows build script (PowerShell)

## Manual Build

If you prefer to build manually:

```bash
# Navigate to the packaging directory
cd packaging

# Install PyInstaller
pip install pyinstaller

# Build using the spec file, output to build directory
pyinstaller --distpath build --workpath build_pyinstaller pyinstaller/doctomood_gui.spec
```

The executable will be created in the `packaging/build/` directory.

## Customization

To customize the build (e.g., add an icon, modify hidden imports), edit `pyinstaller/doctomood_gui.spec`. See the DocToMoodle project's BUILD.md for detailed customization instructions.
