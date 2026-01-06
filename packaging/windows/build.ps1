# Build script for Windows standalone executable
# Run this script from the packaging directory
# This script builds the DocToMoodle application without modifying its source layout

$ErrorActionPreference = "Stop"

# Get the directory where this script is located
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PackagingDir = Split-Path -Parent $ScriptDir
$ProjectRoot = Split-Path -Parent $PackagingDir

Set-Location $PackagingDir

Write-Host "Building doctomood-gui for Windows..."
Write-Host "Source project: $ProjectRoot"
Write-Host "Packaging directory: $PackagingDir"

# Check if PyInstaller is installed
try {
    $null = python -m pip show pyinstaller 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "PyInstaller not found"
    }
} catch {
    Write-Host "PyInstaller not found. Installing..."
    python -m pip install pyinstaller
}

# Check if python-docx is installed
try {
    python -c "import docx" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "python-docx not found"
    }
} catch {
    Write-Host "python-docx not found. Installing..."
    python -m pip install python-docx
}

# Clean previous builds (PyInstaller's temporary build directory and our output)
Write-Host "Cleaning previous builds..."
if (Test-Path "build_pyinstaller") {
    Remove-Item -Recurse -Force "build_pyinstaller"
}
if (Test-Path "build\doctomood-gui") {
    Remove-Item -Recurse -Force "build\doctomood-gui"
}

# Build using the spec file, output to build directory
Write-Host "Building executable..."
pyinstaller --distpath build --workpath build_pyinstaller pyinstaller\doctomood_gui.spec

# Check if build was successful (onedir mode creates a directory)
if (Test-Path "build\doctomood-gui\doctomood-gui.exe") {
    Write-Host ""
    Write-Host "✓ Build successful!" -ForegroundColor Green
    Write-Host "  Executable location: $PackagingDir\build\doctomood-gui\doctomood-gui.exe"
    Write-Host ""
    Write-Host "To test the executable, run:"
    Write-Host "  $PackagingDir\build\doctomood-gui\doctomood-gui.exe"
    Write-Host ""
    Write-Host "To distribute, package the entire 'build\doctomood-gui\' directory"
} else {
    Write-Host "✗ Build failed!" -ForegroundColor Red
    exit 1
}

Read-Host "Press Enter to continue"
