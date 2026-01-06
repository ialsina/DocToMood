from argparse import ArgumentParser
from datetime import datetime
from glob import glob
from pathlib import Path

import yaml

from doctomood.ioutils import df_to_docx, df_to_xml
from doctomood.process import process_multiple


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
    defaults = parse_config()
    parser.set_defaults(**defaults)
    return parser


def process_glob(glob_patterns):
    paths = []
    for glob_pattern in glob_patterns:
        paths.extend(glob(glob_pattern))
    return process_multiple(paths)


def main():
    args = get_parser().parse_args()
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = args.output_dir

    docs_output = output_dir / f"questions_{now}.docx"
    xml_output = output_dir / f"moodle_questions_{now}.xml"

    df = process_glob(args.input)

    if args.write:
        df_to_docx(df, docs_output)
        print(f"Saved DOCX file to {docs_output}")

        df_to_xml(df, xml_output)
        print(f"Saved Moodle XML file to {xml_output}")


if __name__ == "__main__":
    main()
