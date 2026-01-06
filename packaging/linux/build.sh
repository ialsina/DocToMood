#!/bin/bash
# Build script for Linux standalone executable
# Run this script from the packaging directory
# This script builds the DocToMoodle application without modifying its source layout

set -e

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGING_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PROJECT_ROOT="$(cd "$PACKAGING_DIR/.." && pwd)"

cd "$PACKAGING_DIR"

echo "Building doctomood-gui for Linux..."
echo "Source project: $PROJECT_ROOT"
echo "Packaging directory: $PACKAGING_DIR"

# Ensure PyInstaller is installed and up-to-date
echo "Upgrading PyInstaller to latest version..."
pip install --upgrade "pyinstaller>=6.0.0"

# Install build dependencies
if [ -f "requirements-build.txt" ]; then
    echo "Installing build dependencies..."
    pip install -r requirements-build.txt
else
    # Fallback: install individual packages
    if ! python -c "import docx" 2>/dev/null; then
        echo "python-docx not found. Installing..."
        pip install python-docx
    fi
    pip install platformdirs
fi

# Clean previous builds (PyInstaller's temporary build directory and our output)
echo "Cleaning previous builds..."
rm -rf build_pyinstaller build/doctomood-gui build/*.exe

# Build using the spec file, output to build directory
echo "Building executable..."
pyinstaller --distpath build --workpath build_pyinstaller pyinstaller/doctomood_gui.spec

# Check if build was successful (onedir mode creates a directory)
if [ -f "build/doctomood-gui/doctomood-gui" ]; then
    echo ""
    echo "✓ Build successful!"
    echo "  Executable location: $PACKAGING_DIR/build/doctomood-gui/doctomood-gui"

    # Get build name using the utility script
    echo ""
    echo "Creating distribution archive..."
    BUILD_NAME=$(python get_build_info.py buildname)

    # Create tar.gz archive in the build directory
    cd build
    tar -czf "$BUILD_NAME" doctomood-gui/
    cd ..

    if [ -f "build/$BUILD_NAME" ]; then
        echo "Distribution archive created!"
        echo "  Archive: $PACKAGING_DIR/build/$BUILD_NAME"
        echo ""
        echo "To test the executable, run:"
        echo "  $PACKAGING_DIR/build/doctomood-gui/doctomood-gui"
        echo ""
        echo "To distribute, share the archive:"
        echo "  $PACKAGING_DIR/build/$BUILD_NAME"
    else
        echo "Warning: Archive creation failed, but executable is available"
        echo "To distribute, package the entire 'build/doctomood-gui/' directory"
    fi
else
    echo "Build failed!"
    exit 1
fi
