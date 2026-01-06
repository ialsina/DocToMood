# DocToMoodle Packaging

This directory contains build scripts and configuration for creating standalone executables of the DocToMoodle application.

## Directory Structure

```
packaging/
├─ pyinstaller/
│  ├─ doctomood_gui.spec      # PyInstaller configuration
│  └─ hooks/
│     └─ hook-docx.py          # Custom hook for python-docx
├─ linux/
│  └─ build.sh                 # Linux build script
├─ macos/
│  └─ build.sh                 # macOS build script
├─ windows/
│  └─ build.ps1                # Windows build script
├─ get_build_info.py           # Build metadata utility
└─ requirements-build.txt      # Build dependencies
```

## Overview

The build process is located in the `packaging/` directory to keep the source directory clean. Build scripts automatically:

- Create standalone executables for Linux, macOS, or Windows
- Embed the application icon from `assets/icon.ico`
- Package the output as distribution archives with standardized naming: `{appname}-{version}-{os}-{arch}.{ext}`
- Extract version information from `pyproject.toml`

The final executable is created in `packaging/build/doctomood-gui/` along with a distribution archive.

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

# Output: packaging/build/doctomood-gui-{version}-linux-{arch}.tar.gz
```

### macOS

```bash
# Navigate to the packaging directory
cd packaging

# Install build dependencies (if requirements-build.txt exists)
# pip install -r requirements-build.txt

# Build the executable
./macos/build.sh

# Output: packaging/build/doctomood-gui-{version}-macos-{arch}.tar.gz
```

### Windows

```powershell
# Navigate to the packaging directory
cd packaging

# Install build dependencies (if requirements-build.txt exists)
# pip install -r requirements-build.txt

# Build the executable
.\windows\build.ps1

# Output: packaging\build\doctomood-gui-{version}-windows-{arch}.zip
```

## Files

- `pyinstaller/doctomood_gui.spec` - PyInstaller specification file
- `pyinstaller/hooks/hook-docx.py` - Custom PyInstaller hook for python-docx
- `linux/build.sh` - Linux build script
- `macos/build.sh` - macOS build script
- `windows/build.ps1` - Windows build script (PowerShell)
- `get_build_info.py` - Utility to extract version and build metadata
- `requirements-build.txt` - Build-time dependencies

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
