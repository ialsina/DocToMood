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

# Check if PyInstaller is installed
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller not found. Installing..."
    pip install pyinstaller
fi

# Clean previous builds (PyInstaller's temporary build directory and our output)
echo "Cleaning previous builds..."
rm -rf build_pyinstaller build/doctomood-gui

# Build using the spec file, output to build directory
echo "Building executable..."
pyinstaller --distpath build --workpath build_pyinstaller pyinstaller/doctomood_gui.spec

# Check if build was successful
if [ -f "build/doctomood-gui" ]; then
    echo ""
    echo "✓ Build successful!"
    echo "  Executable location: $PACKAGING_DIR/build/doctomood-gui"
    echo ""
    echo "To test the executable, run:"
    echo "  $PACKAGING_DIR/build/doctomood-gui"
else
    echo "✗ Build failed!"
    exit 1
fi
