import docx
import re
import pandas as pd
from itertools import zip_longest
import unicodedata

from ioutils import get_docx_with_highlight_mark

MIN_QUESTION_LENGTH = 12
MAX_QUESTION_DIGIT_FRACTION = 0.32
RE_QUESTION_MARK = re.compile(r"\d+\s*\b")
# RE_REPL_QUESTION = re.compile(r"^(\d+)(?:[.\)\-\s])*(?=\b)")
RE_REPL_QUESTION = re.compile(r"^(\d+)(?:[.\)\-\s])*(?=\b|¿)")
RE_REPL_ANSWER = [
    re.compile(r"^([a-d])(?:[.\)\-\s])*(?=\b)"),
    # re.compile(r"^-*\s*(?=\b)"),
    re.compile(r"^-*\s*"),
]
RE_ANSWER_MARK = re.compile(r"^([a-d])(?:[.\)\-\s])*(?=\b)")
EXTRA_CONTENT_WORDS = ["explicacion", "nota"]

def _right_pad(lst, length=4):
    return lst + [""] * (length - len(lst))

def _matches_question_criteria(p: str) -> bool:
    if len(p) == 0:
        return False
    digit_fraction = len(list(el for el in p if el.isdigit())) / len(p)
    return (
        RE_QUESTION_MARK.match(p.strip())
        and len(p) >= MIN_QUESTION_LENGTH
        and digit_fraction <= MAX_QUESTION_DIGIT_FRACTION
    )

def _get_correct_answers(answers):
    if any(el.endswith("[HIGHLIGHTED]") for el in answers):
        correct = list(map(lambda x: x.endswith("[HIGHLIGHTED]"), answers)).index(True)
        answers = [str.removesuffix(element, " [HIGHLIGHTED]") for element in answers]
    elif any(el.startswith("✔") for el in answers):
        correct = list(map(lambda x: x.startswith("✔"), answers)).index(True)
        answers = [str.removeprefix(element, "✔") for element in answers]
    else:
        correct = -1
    return answers, correct

def _is_answer_line(line: str) -> bool:
    """Check if a line starts with an answer marker (a, b, c, d)."""
    return RE_ANSWER_MARK.match(line.strip()) is not None

def find_blocks(paragraphs):
    """
    Find blocks separated by double (or more) newlines.
    This function ONLY detects where blocks are - it does NOT analyze content.
    
    Returns:
        blocks: list[list[str]]  # Each block is a list of paragraph text lines
    """
    blocks = []
    i = 0
    n = len(paragraphs)

    while i < n:
        # Count empty lines before potential block
        empty_before = 0
        while i < n and not paragraphs[i].strip():
            empty_before += 1
            i += 1
        
        # If we've reached the end, break
        if i >= n:
            break

        # Start of a potential block
        block_start = i
        block_lines = []

        # Collect consecutive non-empty lines (the block)
        while i < n and paragraphs[i].strip():
            block_lines.append(paragraphs[i])
            i += 1

        # Count empty lines after the block
        empty_after = 0
        j = i
        while j < n and not paragraphs[j].strip():
            empty_after += 1
            j += 1

        # Block is valid if separated by 2+ newlines (double newline)
        # Blocks at start/end are also valid
        is_at_start = block_start == 0
        is_at_end = i >= n
        has_double_newline_before = empty_before >= 1
        has_double_newline_after = empty_after >= 1
        
        if has_double_newline_before or has_double_newline_after or is_at_start or is_at_end:
            if block_lines:  # Only add non-empty blocks
                blocks.append(block_lines)

    return blocks

def _normalize_text(text: str) -> str:
    """Normalize text by removing accents and converting to lowercase."""
    # Remove accents and convert to lowercase
    nfd = unicodedata.normalize('NFD', text)
    return ''.join(c for c in nfd if unicodedata.category(c) != 'Mn').lower()

def _starts_with_extra_content_word(text: str) -> bool:
    """Check if text starts with any of the EXTRA_CONTENT_WORDS (case and accent insensitive)."""
    text_normalized = _normalize_text(text.strip())
    for word in EXTRA_CONTENT_WORDS:
        if text_normalized.startswith(_normalize_text(word)):
            return True
    return False

def post_process_blocks(blocks):
    """
    Merge blocks that start with EXTRA_CONTENT_WORDS into the previous block.
    Note: This function only works with block indices. Content checking is done
    in process() where paragraphs are available.
    
    Args:
        blocks: list[list[int]]  # List of blocks (each block is list of paragraph indices)
    
    Returns:
        list[list[int]]  # Processed blocks
    """
    # This function is called from process() after checking content
    # For now, just return blocks as-is - merging happens in process()
    return blocks

def process(paragraphs, as_dataframe=True):
    paragraphs = [p.strip() for p in paragraphs]

    # Find all blocks separated by double newlines
    blocks = find_blocks(paragraphs)

    # Merge blocks that start with EXTRA_CONTENT_WORDS into the previous block
    processed_blocks = []
    for i, block in enumerate(blocks):
        if i == 0:
            # First block always stays as is
            processed_blocks.append(block)
        else:
            # Check if current block starts with an extra content word
            if block and _starts_with_extra_content_word(block[0]):
                # Merge with previous block
                processed_blocks[-1] = processed_blocks[-1] + block
            else:
                # Keep as separate block
                processed_blocks.append(block)
    
    blocks = post_process_blocks(processed_blocks)

    parts = []
    for block in blocks:
        n_lines = len(block)
        
        if n_lines == 0:
            continue
            
        question = block[0]

        print(block)        
        # Extract answers: look for lines starting with answer markers
        answers = []
        answer_indices = []
        for i in range(1, n_lines):
            if _is_answer_line(block[i]):
                answers.append(block[i])
                answer_indices.append(i)
        
        # If no labeled answers found, fall back to assuming positions 1-4 are answers
        if not answers:
            answers = block[1:min(5, n_lines)]
        else:
            # Only take up to 4 answers, right-pad if needed
            answers = _right_pad(answers[:4], 4)
        
        answers, correct = _get_correct_answers(answers)

        # Clean up question and answer text
        question = re.sub(RE_REPL_QUESTION, "", question).strip()
        answers = [re.sub(RE_REPL_ANSWER[0], "", a).strip() for a in answers]
        answers = [re.sub(RE_REPL_ANSWER[1], "", a).strip() for a in answers]

        # Extra content: lines starting with EXTRA_CONTENT_WORDS or after answers
        extra_lines = []
        
        # Determine where answers end
        if answer_indices:
            # Answers end after the last labeled answer
            answer_end_idx = answer_indices[-1] + 1
        else:
            # If no labeled answers, assume answers are in positions 1-4
            answer_end_idx = min(5, n_lines)
        
        # Collect extra content:
        # 1. Any line that starts with EXTRA_CONTENT_WORDS (anywhere in block)
        # 2. Any line after the answers
        for i in range(1, n_lines):
            if _starts_with_extra_content_word(block[i]) or i >= answer_end_idx:
                extra_lines.append(block[i])
        
        extra = "\n".join(extra_lines)
        parts.append((question, *answers, correct, extra))

    if as_dataframe:
        df = pd.DataFrame(
            parts,
            columns=["question", "ans0", "ans1", "ans2", "ans3", "correct", "extra"],
        )
        return df, blocks

    return parts, blocks

def process_multiple(paths):
    dfs = []
    for path in paths:
        pars = get_docx_with_highlight_mark(path)
        df, _ = process(pars)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)
