from argparse import ArgumentParser
from pathlib import Path

import yaml


def find_config_file():
    """Find config.yml file, checking current directory first, then project root."""
    # Check current working directory first (most common use case)
    cwd_config = Path.cwd() / "config.yml"
    if cwd_config.exists():
        return cwd_config

    # Check project root (for development)
    project_root = Path(__file__).parent.parent
    project_config = project_root / "config.yml"
    if project_config.exists():
        return project_config

    # Return None if not found (will use defaults)
    return None


def parse_config():
    config_file = find_config_file()
    if config_file is None:
        return {}
    try:
        with open(config_file, "r") as f:
            config = yaml.safe_load(f)
        return config if config else {}
    except Exception:
        return {}


def get_parser():
    parser = ArgumentParser()
    parser.add_argument(
        "input",
        type=str,
        nargs="+",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        required=False,
    )
    parser.add_argument(
        "--no-write",
        action="store_false",
        dest="write",
    )
    parser.add_argument(
        "--respect-name",
        action="store_true",
    )
    defaults = parse_config()
    parser.set_defaults(**defaults)
    return parser
