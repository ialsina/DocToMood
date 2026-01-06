# Building Standalone Executables

This guide explains how to build standalone executables for the doctomood GUI application on Linux and Windows.

**Note:** The build process is located in the `packaging/` directory to keep the application source layout clean. The final executable is created in `packaging/build/`.

## Prerequisites

- Python 3.10 or higher
- All application dependencies installed
- PyInstaller (will be installed automatically by build scripts)

## Directory Structure

The packaging directory is organized as follows:

```
packaging/
├─ pyinstaller/
│  └─ doctomood_gui.spec
├─ linux/
│  └─ build.sh
└─ windows/
   └─ build.ps1
```

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

## Manual Build

If you prefer to build manually:

### Linux/Windows

```bash
# Navigate to the packaging directory
cd packaging

# Install PyInstaller
pip install pyinstaller

# Build using the spec file, output to build directory
pyinstaller --distpath build --workpath build_pyinstaller pyinstaller/doctomood_gui.spec
```

The executable will be created in `packaging/build/` directory.

## Customization

### Adding an Icon

To add a custom icon to your executable:

1. **Windows**: Create or obtain an `.ico` file
2. **Linux**: Create or obtain a `.png` file (PyInstaller will convert it)

Then edit `packaging/pyinstaller/doctomood_gui.spec` and update the `icon` parameter in the `EXE` section:

```python
icon='path/to/your/icon.ico',  # Windows
# or
icon='path/to/your/icon.png',  # Linux
```

### Modifying Hidden Imports

If you encounter import errors at runtime, you may need to add missing modules to the `hiddenimports` list in `packaging/pyinstaller/doctomood_gui.spec`.

### One-file vs One-folder

The current configuration creates a one-file executable. If you prefer a one-folder distribution (which starts faster but includes multiple files), modify `packaging/pyinstaller/doctomood_gui.spec`:

Change the `EXE` section to:
```python
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='doctomood-gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
)
```

And add a `COLLECT` section:
```python
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='doctomood-gui',
)
```

## Troubleshooting

### Import Errors

If you get import errors when running the executable, check:
1. All required modules are in `hiddenimports` in `packaging/pyinstaller/doctomood_gui.spec`
2. The module is actually installed in your Python environment

### Large Executable Size

The executable may be large (50-100MB) because it bundles Python and all dependencies. This is normal for PyInstaller builds.

### Antivirus False Positives

Some antivirus software may flag PyInstaller executables as suspicious. This is a known false positive. You can:
- Submit the executable to your antivirus vendor for analysis
- Use code signing (Windows) to reduce false positives
- Distribute as a one-folder build instead

## Distribution

After building, you can distribute:
- **Linux**: The `packaging/build/doctomood-gui` file
- **Windows**: The `packaging\build\doctomood-gui.exe` file

The executable is standalone and doesn't require Python or any dependencies to be installed on the target machine.

## Build Location

All build artifacts are created in the `packaging/` directory:
- PyInstaller's temporary files: `packaging/build_pyinstaller/`
- Final executable: `packaging/build/doctomood-gui` (or `doctomood-gui.exe` on Windows)

This keeps the main project source directory clean and unmodified.
