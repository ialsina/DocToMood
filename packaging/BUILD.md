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
│  ├─ doctomood_gui.spec      # PyInstaller configuration
│  └─ hooks/
│     └─ hook-docx.py          # Custom hook for python-docx package
├─ linux/
│  └─ build.sh                 # Linux build script
├─ macos/
│  └─ build.sh                 # macOS build script
├─ windows/
│  └─ build.ps1                # Windows build script
├─ get_build_info.py           # Utility to extract version and build metadata
├─ requirements-build.txt      # Build dependencies
└─ BUILD.md                    # This file
```

And in the project root:

```
assets/
└─ icon.ico                    # Application icon (embedded in executable)
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

# The executable will be in packaging/build/doctomood-gui/
# Distribution archive will be at packaging/build/doctomood-gui-{version}-linux-{arch}.tar.gz
```

### macOS

```bash
# Navigate to the packaging directory
cd packaging

# Install build dependencies (if requirements-build.txt exists)
# pip install -r requirements-build.txt

# Build the executable
./macos/build.sh

# The application will be in packaging/build/doctomood-gui/
# Distribution archive will be at packaging/build/doctomood-gui-{version}-macos-{arch}.tar.gz
```

### Windows

```powershell
# Navigate to the packaging directory
cd packaging

# Install build dependencies (if requirements-build.txt exists)
# pip install -r requirements-build.txt

# Build the executable
.\windows\build.ps1

# The executable will be in packaging\build\doctomood-gui\doctomood-gui.exe
# Distribution archive will be at packaging\build\doctomood-gui-{version}-windows-{arch}.zip
```

## Manual Build

If you prefer to build manually on any platform:

```bash
# Navigate to the packaging directory
cd packaging

# Install PyInstaller
pip install pyinstaller

# Build using the spec file, output to build directory
pyinstaller --distpath build --workpath build_pyinstaller pyinstaller/doctomood_gui.spec

# Create distribution archive
python get_build_info.py buildname  # Get the build name
# Then create archive manually based on your platform
```

The executable will be created in `packaging/build/` directory.

## Distribution Archives

The build scripts automatically create distribution-ready archives with the following naming convention:

```
{appname}-{version}-{os}-{arch}.{ext}
```

Examples:
- Linux: `doctomood-gui-0.0.1-linux-x86_64.tar.gz`
- macOS: `doctomood-gui-0.0.1-macos-arm64.tar.gz`
- Windows: `doctomood-gui-0.0.1-windows-x86_64.zip`

The version is automatically extracted from `pyproject.toml`, and OS/architecture are detected at build time.

### macOS DMG Creation (Optional)

For macOS, you can optionally create a DMG file for easier distribution:

```bash
cd packaging
hdiutil create -volname doctomood-gui \
  -srcfolder build/doctomood-gui \
  -ov -format UDZO \
  build/doctomood-gui.dmg
```

## Icon

The application icon is automatically included from `assets/icon.ico` during the build process. To customize:

1. Create or replace the icon file in the `assets/` directory:
   - **Windows**: `assets/icon.ico` (recommended: 256x256 or multiple sizes in one .ico file)
   - **macOS**: `assets/icon.icns` (use `iconutil` to create from .iconset)
   - **Linux**: `assets/icon.ico` or `assets/icon.png` works

2. Update the icon path in `packaging/pyinstaller/doctomood_gui.spec` if using a different file:
   ```python
   icon=str(PROJECT_ROOT / 'assets' / 'icon.ico'),  # or 'icon.icns' for macOS
   ```

3. The icon will be automatically embedded in the executable during the next build

**Note**: Currently, the spec file uses `icon.ico` which works for Windows and Linux. For macOS app bundles, create an `icon.icns` file and update the spec accordingly.

## Customization

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

After building, distribute the generated archive file:
- **Linux**: `packaging/build/doctomood-gui-{version}-linux-{arch}.tar.gz`
- **macOS**: `packaging/build/doctomood-gui-{version}-macos-{arch}.tar.gz`
- **Windows**: `packaging\build\doctomood-gui-{version}-windows-{arch}.zip`

Users can extract the archive and run the executable directly. No Python or dependencies are required on the target machine.

**macOS Note**: If you created a DMG file, distribute that instead for a more native macOS experience.

### Build Information Utility

The `packaging/get_build_info.py` script provides build metadata:

```bash
# Get version
python get_build_info.py version

# Get OS name
python get_build_info.py os

# Get architecture
python get_build_info.py arch

# Get full build name
python get_build_info.py buildname
```

## Build Location

All build artifacts are created in the `packaging/` directory:
- PyInstaller's temporary files: `packaging/build_pyinstaller/`
- Final executable: `packaging/build/doctomood-gui` (or `doctomood-gui.exe` on Windows)

This keeps the main project source directory clean and unmodified.
