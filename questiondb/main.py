from argparse import ArgumentParser
from glob import glob
import yaml
from datetime import datetime
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
CONFIG_FILE = ROOT_DIR / "config.yml"

from process import process_multiple
from ioutils import df_to_docx, df_to_xml

def parse_config():
    with open(CONFIG_FILE, "r") as f:
        config = yaml.safe_load(f)
    return config

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

    df_to_docx(df, docs_output)
    print(f"Saved DOCX file to {docs_output}")

    df_to_xml(df, xml_output)
    print(f"Saved Moodle XML file to {xml_output}")

if __name__ == "__main__":
    main()