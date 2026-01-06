"""
PyInstaller hook for python-docx package.
This hook ensures that the docx template files are included in the build.
"""

from PyInstaller.utils.hooks import collect_data_files

# Collect all data files from the docx package (including templates)
datas = collect_data_files("docx")

# Explicitly collect template files which are critical for python-docx
hiddenimports = [
    "docx",
    "docx.oxml",
    "docx.oxml.xmlchemy",
]
