# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for doctomood-gui
# This file should be run from the packaging directory
# It references the DocToMoodle project without modifying its layout

import os
from pathlib import Path
from PyInstaller.utils.hooks import collect_submodules, collect_data_files, collect_all

# Get absolute paths
# PyInstaller runs from the directory where pyinstaller is invoked
# Our build scripts ensure we're in the packaging directory before running pyinstaller
# So os.getcwd() will be the packaging directory
PACKAGING_DIR = Path(os.getcwd()).resolve()
PROJECT_ROOT = PACKAGING_DIR.parent

# Collect all submodules for each major dependency
print("Collecting submodules for dependencies...")

# Collect pandas and its submodules
pandas_imports = collect_submodules('pandas')
print(f"  - pandas: {len(pandas_imports)} submodules")

# Collect numpy and its submodules
numpy_imports = collect_submodules('numpy')
print(f"  - numpy: {len(numpy_imports)} submodules")

# Collect docx and its submodules
docx_imports = collect_submodules('docx')
print(f"  - docx: {len(docx_imports)} submodules")

# Collect yaml and its submodules
yaml_imports = collect_submodules('yaml')
print(f"  - yaml: {len(yaml_imports)} submodules")

# Collect lxml and its submodules
lxml_imports = collect_submodules('lxml')
print(f"  - lxml: {len(lxml_imports)} submodules")

# Collect odfpy/odf and its submodules
try:
    odf_imports = collect_submodules('odf')
    print(f"  - odf: {len(odf_imports)} submodules")
except Exception:
    odf_imports = ['odf', 'odf.opendocument', 'odf.table', 'odf.text']
    print(f"  - odf: using fallback imports")

# Collect openpyxl (pandas dependency)
try:
    openpyxl_imports = collect_submodules('openpyxl')
    print(f"  - openpyxl: {len(openpyxl_imports)} submodules")
except Exception:
    openpyxl_imports = ['openpyxl']

# Collect pytz (pandas dependency)
try:
    pytz_imports = collect_submodules('pytz')
    print(f"  - pytz: {len(pytz_imports)} submodules")
except Exception:
    pytz_imports = ['pytz']

# Collect dateutil (pandas dependency)
try:
    dateutil_imports = collect_submodules('dateutil')
    print(f"  - dateutil: {len(dateutil_imports)} submodules")
except Exception:
    dateutil_imports = ['dateutil', 'dateutil.parser']

# Collect tqdm
try:
    tqdm_imports = collect_submodules('tqdm')
    print(f"  - tqdm: {len(tqdm_imports)} submodules")
except Exception:
    tqdm_imports = ['tqdm']

# Collect platformdirs (PyInstaller runtime dependency) - use collect_all for completeness
try:
    platformdirs_datas, platformdirs_binaries, platformdirs_imports = collect_all('platformdirs')
    print(f"  - platformdirs: {len(platformdirs_imports)} submodules, {len(platformdirs_datas)} data files")
except Exception as e:
    print(f"  - platformdirs: failed to collect with collect_all ({e}), using fallback")
    platformdirs_imports = ['platformdirs']
    platformdirs_datas = []
    platformdirs_binaries = []

# Collect setuptools and pkg_resources (required by PyInstaller runtime)
try:
    setuptools_imports = collect_submodules('setuptools')
    pkg_resources_imports = collect_submodules('pkg_resources')
    print(f"  - setuptools: {len(setuptools_imports)} submodules")
    print(f"  - pkg_resources: {len(pkg_resources_imports)} submodules")
except Exception:
    setuptools_imports = ['setuptools']
    pkg_resources_imports = ['pkg_resources']

# Collect data files for packages that need them
pandas_datas = collect_data_files('pandas', include_py_files=False)
numpy_datas = collect_data_files('numpy', include_py_files=False)

# Combine all data files
all_datas = pandas_datas + numpy_datas
if 'platformdirs_datas' in locals():
    all_datas += platformdirs_datas

block_cipher = None

a = Analysis(
    [str(PROJECT_ROOT / 'src' / 'doctomood' / 'gui.py')],
    pathex=[str(PROJECT_ROOT / 'src')],
    binaries=platformdirs_binaries if 'platformdirs_binaries' in locals() else [],
    datas=all_datas,
    hiddenimports=[
        # Doctomood modules
        'doctomood',
        'doctomood.main',
        'doctomood.process',
        'doctomood.ioutils',
        'doctomood.parser',
    ] + pandas_imports + numpy_imports + docx_imports + yaml_imports + lxml_imports + odf_imports + openpyxl_imports + pytz_imports + dateutil_imports + tqdm_imports + platformdirs_imports + setuptools_imports + pkg_resources_imports + [
        # Additional explicit imports that might be missed
        'tkinter',
        'tkinter.filedialog',
        'tkinter.messagebox',
        'tkinter.ttk',
        'pkg_resources.py2_warn',
    ],
    hookspath=[str(PACKAGING_DIR / 'pyinstaller' / 'hooks')],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'jupyter',
        'jupyterlab',
        'ipython',
        'notebook',
        'matplotlib',
        'IPython',
        'scipy',
        'pytest',
        'sphinx',
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
    [],
    exclude_binaries=True,
    name='doctomood-gui',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # No console window for GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=str(PROJECT_ROOT / 'assets' / 'icon.ico'),
)

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
