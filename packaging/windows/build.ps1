# Build script for Windows standalone executable
$ErrorActionPreference = "Stop"

# Directories
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$PackagingDir = Split-Path -Parent $ScriptDir
$ProjectRoot = Split-Path -Parent $PackagingDir

Set-Location $PackagingDir

Write-Host "Building doctomood-gui for Windows..."
Write-Host "Source project: $ProjectRoot"
Write-Host "Packaging directory: $PackagingDir"

# Ensure PyInstaller is installed and up-to-date
Write-Host "Upgrading PyInstaller to latest version..."
python -m pip install --upgrade "pyinstaller>=6.0.0"

# Ensure build dependencies are installed
Write-Host "Checking build dependencies..."
if (Test-Path "requirements-build.txt") {
    python -m pip install -r requirements-build.txt
} else {
    # Fallback: install individual packages
    try {
        python -c "import docx" > $null 2>&1
        if ($LASTEXITCODE -ne 0) { throw "python-docx not found" }
    } catch {
        Write-Host "python-docx not found. Installing..."
        python -m pip install python-docx
    }
    python -m pip install platformdirs
}

# Clean previous builds
Write-Host "Cleaning previous builds..."
if (Test-Path "build_pyinstaller") { Remove-Item -Recurse -Force "build_pyinstaller" }
if (Test-Path "build/doctomood-gui") { Remove-Item -Recurse -Force "build/doctomood-gui" }

# Build executable
Write-Host "Building executable..."
pyinstaller --distpath build --workpath build_pyinstaller pyinstaller/doctomood_gui.spec

# Check build success
$ExePath = Join-Path -Path "build/doctomood-gui" -ChildPath "doctomood-gui.exe"

if (Test-Path $ExePath) {

    Write-Host ""
    Write-Host "Build successful!" -ForegroundColor Green
    Write-Host "  Executable location: $ExePath"

    # Create distribution archive
    Write-Host ""
    Write-Host "Creating distribution archive..."
    $BuildName = -join ($(python get_build_info.py buildname).Trim())

    $ZipPath = Join-Path -Path "build" -ChildPath $BuildName

    if (Test-Path $ZipPath) {
        Remove-Item -Recurse -Force $ZipPath
    }

    # Wrap Compress-Archive in parentheses to avoid parser confusion
    Compress-Archive `
        -Path "build/doctomood-gui" `
        -DestinationPath $ZipPath `
        -CompressionLevel Optimal

    if (Test-Path $ZipPath) {
        Write-Host "Distribution archive created!" -ForegroundColor Green
        Write-Host "  Archive: $ZipPath"
        Write-Host ""
        Write-Host "To test the executable, run:"
        Write-Host "  $ExePath"
        Write-Host ""
        Write-Host "To distribute, share the archive:"
        Write-Host "  $ZipPath"
    } else {
        Write-Host "Warning: Archive creation failed, but executable is available" -ForegroundColor Yellow
        Write-Host "To distribute, package the entire 'build/doctomood-gui' directory"
    }

} else {

    Write-Host "Build failed!" -ForegroundColor Red
    exit 1

}

Read-Host "Press Enter to continue"
