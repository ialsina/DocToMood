#!/bin/bash
# Build script for macOS standalone executable
# Run this script from the packaging directory
# This script builds the DocToMoodle application without modifying its source layout

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGING_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PROJECT_ROOT="$(cd "$PACKAGING_DIR/.." && pwd)"

cd "$PACKAGING_DIR"

echo "Building doctomood-gui for macOS..."
echo "Source project: $PROJECT_ROOT"
echo "Packaging directory: $PACKAGING_DIR"

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller not found. Installing..."
    pip install pyinstaller
fi

# Check if python-docx is installed
if ! python -c "import docx" 2>/dev/null; then
    echo "python-docx not found. Installing..."
    pip install python-docx
fi

# Clean previous builds (PyInstaller's temporary build directory and our output)
echo "Cleaning previous builds..."
rm -rf build_pyinstaller build/doctomood-gui.app build/*.dmg build/*.tar.gz

# Build using the spec file, output to build directory
echo "Building executable..."
pyinstaller --distpath build --workpath build_pyinstaller pyinstaller/doctomood_gui.spec

# Check if build was successful (onedir mode creates a directory)
# On macOS, PyInstaller creates a .app bundle
if [ -d "build/doctomood-gui/doctomood-gui.app" ] || [ -f "build/doctomood-gui/doctomood-gui" ]; then
    echo ""
    echo "✓ Build successful!"

    # Determine what was created
    if [ -d "build/doctomood-gui/doctomood-gui.app" ]; then
        echo "  Application bundle: $PACKAGING_DIR/build/doctomood-gui/doctomood-gui.app"
        APP_EXISTS=true
    else
        echo "  Executable location: $PACKAGING_DIR/build/doctomood-gui/doctomood-gui"
        APP_EXISTS=false
    fi

    # Get build name using the utility script
    echo ""
    echo "Creating distribution archive..."
    BUILD_NAME=$(python get_build_info.py buildname)

    # Create tar.gz archive in the build directory
    cd build
    tar -czf "$BUILD_NAME" doctomood-gui/
    cd ..

    if [ -f "build/$BUILD_NAME" ]; then
        echo "✓ Distribution archive created!"
        echo "  Archive: $PACKAGING_DIR/build/$BUILD_NAME"
        echo ""
        echo "To test the application:"
        if [ "$APP_EXISTS" = true ]; then
            echo "  open $PACKAGING_DIR/build/doctomood-gui/doctomood-gui.app"
        else
            echo "  $PACKAGING_DIR/build/doctomood-gui/doctomood-gui"
        fi
        echo ""
        echo "To distribute, share the archive:"
        echo "  $PACKAGING_DIR/build/$BUILD_NAME"
        echo ""
        echo "Optional: Create a DMG for easier distribution"
        echo "  hdiutil create -volname doctomood-gui -srcfolder build/doctomood-gui -ov -format UDZO build/doctomood-gui.dmg"
    else
        echo "⚠ Warning: Archive creation failed, but executable is available"
        echo "To distribute, package the entire 'build/doctomood-gui/' directory"
    fi
else
    echo "✗ Build failed!"
    exit 1
fi
