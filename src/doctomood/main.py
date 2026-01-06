from datetime import datetime
from glob import glob
from pathlib import Path

from doctomood.ioutils import df_to_docx, df_to_xml
from doctomood.parser import get_parser
from doctomood.process import process_multiple


def process_glob(glob_patterns):
    paths = []
    for glob_pattern in glob_patterns:
        paths.extend(glob(glob_pattern))
    return process_multiple(paths)


def process_single_file(input_file, output_dir, respect_name=True, write=True):
    """
    Process a single input file and generate output files.

    Args:
        input_file: Path to input file (str or Path)
        output_dir: Output directory (Path)
        respect_name: If True, use input file stem for output names
        write: If True, write output files

    Returns:
        tuple: (docs_output_path, xml_output_path, dataframe)
    """
    input_path = Path(input_file)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if respect_name:
        name_stem = input_path.stem
    else:
        name_stem = datetime.now().strftime("%Y%m%d_%H%M%S")

    docs_output = output_dir / f"questions_{name_stem}.docx"
    xml_output = output_dir / f"questions_{name_stem}.xml"

    df = process_multiple([input_path])

    if write:
        df_to_docx(df, docs_output)
        print(f"Saved DOCX file to {docs_output}")

        df_to_xml(df, xml_output)
        print(f"Saved Moodle XML file to {xml_output}")

    return docs_output, xml_output, df


def main():
    args = get_parser().parse_args()
    output_dir = args.output_dir

    if args.respect_name:
        if len(args.input) > 1:
            raise ValueError(
                "--respect-name can only be used with a single input file. "
                f"Got {len(args.input)} input(s): {args.input}"
            )
        # Get the first (and only) input pattern, expand glob, and get the stem
        input_paths = glob(args.input[0])
        if not input_paths:
            raise ValueError(f"No files found matching pattern: {args.input[0]}")
        if len(input_paths) > 1:
            raise ValueError(
                "--respect-name can only be used with a single input file. "
                f"Pattern '{args.input[0]}' matched {len(input_paths)} file(s): {input_paths}"
            )
        name_stem = Path(input_paths[0]).stem
    else:
        name_stem = datetime.now().strftime("%Y%m%d_%H%M%S")

    docs_output = output_dir / f"questions_{name_stem}.docx"
    xml_output = output_dir / f"questions_{name_stem}.xml"

    df = process_glob(args.input)

    if args.write:
        df_to_docx(df, docs_output)
        print(f"Saved DOCX file to {docs_output}")

        df_to_xml(df, xml_output)
        print(f"Saved Moodle XML file to {xml_output}")


if __name__ == "__main__":
    main()
