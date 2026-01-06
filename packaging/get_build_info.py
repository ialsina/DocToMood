#!/usr/bin/env python3
"""
Utility script to extract build information for packaging.
Reads version from pyproject.toml and provides OS/arch information.
"""

import platform
import sys
from pathlib import Path

try:
    import tomllib
except ImportError:
    import tomli as tomllib


def get_version():
    """Extract version from pyproject.toml"""
    project_root = Path(__file__).parent.parent
    pyproject_path = project_root / "pyproject.toml"

    with open(pyproject_path, "rb") as f:
        data = tomllib.load(f)

    return data["project"]["version"]


def get_os_name():
    """Get standardized OS name"""
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    return system


def get_arch():
    """Get standardized architecture name"""
    machine = platform.machine().lower()
    # Normalize architecture names
    arch_map = {
        "x86_64": "x86_64",
        "amd64": "x86_64",
        "arm64": "arm64",
        "aarch64": "arm64",
        "i386": "x86",
        "i686": "x86",
    }
    return arch_map.get(machine, machine)


def get_extension():
    """Get appropriate archive extension for the OS"""
    system = platform.system().lower()
    if system == "windows":
        return "zip"
    else:
        return "tar.gz"


def get_build_name(appname="doctomood-gui"):
    """Generate full build name with convention: {appname}-{version}-{os}-{arch}.{ext}"""
    version = get_version()
    os_name = get_os_name()
    arch = get_arch()
    ext = get_extension()

    return f"{appname}-{version}-{os_name}-{arch}.{ext}"


def main():
    """Main entry point for CLI usage"""
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "version":
            print(get_version())
        elif command == "os":
            print(get_os_name())
        elif command == "arch":
            print(get_arch())
        elif command == "ext":
            print(get_extension())
        elif command == "buildname":
            appname = sys.argv[2] if len(sys.argv) > 2 else "doctomood-gui"
            print(get_build_name(appname))
        else:
            print(f"Unknown command: {command}", file=sys.stderr)
            sys.exit(1)
    else:
        # Print all info
        print(f"Version: {get_version()}")
        print(f"OS: {get_os_name()}")
        print(f"Arch: {get_arch()}")
        print(f"Extension: {get_extension()}")
        print(f"Build name: {get_build_name()}")


if __name__ == "__main__":
    main()
