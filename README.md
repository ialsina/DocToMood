# DocToMoodle

CLI and GUI tool to parse DOCX multiple-choice questions into Moodle XML and DOCX.

## Installation

### Prerequisites

- Python 3.10 or higher
- pip

### Install from Source

```bash
# Clone the repository
git clone <repository-url>
cd DocToMoodle

# Install dependencies
pip install -e .
```

Or install dependencies directly:

```bash
pip install python-docx odfpy pandas pyyaml tqdm
```

## Usage

### Input Format

DocToMoodle expects DOCX files containing multiple-choice questions with the following format:

1. **Question Format**: Questions must start with a number followed by optional punctuation:
   - `1. What is...`
   - `2) Which of...`
   - `3- How many...`

2. **Answer Format**: Answers are labeled with letters (a, b, c, d) with optional punctuation:
   - `a) First option`
   - `b. Second option`
   - `c- Third option`
   - `d Fourth option` (space-only format also supported)

3. **Correct Answer Marking**: Mark the correct answer using one of these methods:
   - **Highlighting**: Highlight the correct answer text in the DOCX file
   - **Checkmark**: Prefix the correct answer with `✔` (checkmark character)

4. **Question Separation**: Questions must be separated by at least one blank line (double newline).

5. **Extra Content**: Additional content (explanations, notes) can be included:
   - Lines starting with "explicacion" or "nota" (case-insensitive) will be merged with the previous question
   - Any content after the answers will be included in the "extra" field

**Example Input:**
```
1. What is the capital of France?
a) London
b) Berlin
c) Paris
d) Madrid

2. Which planet is closest to the Sun?
a) Venus
b) Mercury
c) Earth
d) Mars

Explicacion: Mercury is the closest planet to the Sun.
```

### Command Line Interface

#### Basic Usage

Process a single file:

```bash
doctomood input.docx -o output_dir/
```

This generates two files in `output_dir/`:
- `questions_YYYYMMDD_HHMMSS.docx` - Formatted DOCX with questions in a table
- `questions_YYYYMMDD_HHMMSS.xml` - Moodle XML import file

#### Use Input Filename for Output

To use the input filename stem for output files (only works with single file):

```bash
doctomood input.docx -o output_dir/ --respect-name
```

This generates:
- `questions_input.docx`
- `questions_input.xml`

#### Process Multiple Files

Process multiple files at once:

```bash
doctomood file1.docx file2.docx file3.docx -o output_dir/
```

All questions from all files will be combined into a single output.

#### Use Glob Patterns

Process files matching a pattern:

```bash
doctomood "*.docx" -o output_dir/
doctomood "questions/*.docx" -o output_dir/
```

#### Process Without Writing Files

Process files and see results without writing output:

```bash
doctomood input.docx -o output_dir/ --no-write
```

#### Command-Line Options

- `input`: One or more input files or glob patterns (required)
- `-o, --output-dir`: Output directory for generated files (required unless using config)
- `--respect-name`: Use input filename stem for output names (only for single file)
- `--no-write`: Process files without writing output files

### GUI Application

Launch the graphical interface:

```bash
doctomood-gui
```

The GUI provides:
- **File Browser**: Select input DOCX or ODT files
- **Output Directory**: Choose where to save generated files
- **Process Button**: Convert questions with a single click
- **Status Feedback**: See processing status and results

**GUI Workflow:**
1. Click "📁 Browse" to select your input file
2. Click "📂 Browse" to select the output directory
3. Click "▶ Process Questions" to convert
4. View success message with file paths and question count

### Configuration File

Create a `config.yml` file in your working directory or project root to set default options:

```yaml
output_dir: "./output"
```

The configuration file is optional. Command-line arguments override config values.

## Output Formats

### DOCX Output

The generated DOCX file contains a table with the following columns:
- **question**: The question text (number prefix removed)
- **A, B, C, D**: The four answer options
- **extra**: Additional content (explanations, notes)

The correct answer is highlighted in yellow in the corresponding answer column.

### Moodle XML Output

The XML file is formatted for direct import into Moodle:
- Each question is a multichoice question type
- Answers are shuffled by default
- Correct answer is marked with 100% fraction
- Includes Spanish feedback messages (customizable in code)
- Question numbering uses the "extra" field if available, otherwise `q_1`, `q_2`, etc.

**Import to Moodle:**
1. Log into your Moodle course
2. Go to Question Bank → Import
3. Select "Moodle XML format"
4. Upload the generated XML file
5. Click "Import"

## Examples

### Example 1: Single File Processing

```bash
doctomood quiz.docx -o ./moodle_questions/ --respect-name
```

Output:
- `./moodle_questions/questions_quiz.docx`
- `./moodle_questions/questions_quiz.xml`

### Example 2: Batch Processing

```bash
doctomood chapter1.docx chapter2.docx chapter3.docx -o ./output/
```

All questions from all chapters are combined into a single output.

### Example 3: Pattern Matching

```bash
doctomood "exams/*.docx" -o ./moodle_output/
```

Processes all DOCX files in the `exams/` directory.

## Building Standalone Executables

To build standalone executables for Linux and Windows, see [BUILD.md](packaging/BUILD.md) for detailed instructions.

**Note:** Build scripts are located in the `packaging/` directory to keep the source directory clean.

Quick start:
- **Linux**: `cd packaging && ./linux/build.sh`
- **Windows**: `cd packaging && .\windows\build.ps1`

The executable will be created in `packaging/build/`.

## Tips

- **Question Formatting**: Ensure questions are clearly separated by blank lines
- **Answer Labels**: Use consistent formatting (a, b, c, d) for all answers
- **Correct Answers**: Highlighting is the most reliable method for marking correct answers
- **File Organization**: Use `--respect-name` when processing individual files to maintain clear naming
- **Batch Processing**: Combine multiple question files into a single Moodle import for efficiency
