# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for doctomood-gui
# This file should be run from the packaging directory
# It references the DocToMoodle project without modifying its layout

import os
from pathlib import Path

# Get absolute paths
SPEC_DIR = Path(__file__).parent.absolute()
PACKAGING_DIR = SPEC_DIR.parent
PROJECT_ROOT = PACKAGING_DIR.parent

block_cipher = None

a = Analysis(
    [str(PROJECT_ROOT / 'doctomood' / 'gui.py')],
    pathex=[str(PROJECT_ROOT)],
    binaries=[],
    datas=[],
    hiddenimports=[
        'doctomood',
        'doctomood.main',
        'doctomood.process',
        'doctomood.ioutils',
        'doctomood.parser',
        'pandas',
        'numpy',  # Required by pandas
        'docx',
        'docx.oxml',
        'docx.oxml.ns',
        'docx.enum.text',
        'yaml',
        'odfpy',
        'lxml',
        'lxml.etree',
        'openpyxl',  # pandas dependency
        'pytz',  # pandas dependency
        'dateutil',  # pandas dependency
        'dateutil.parser',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'jupyter',
        'jupyterlab',
        'ipython',
        'notebook',
        'matplotlib',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='doctomood-gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window for GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one: 'icon.ico' for Windows, 'icon.icns' for macOS
)
