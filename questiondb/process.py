import docx
import re
import pandas as pd
from itertools import zip_longest

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

def find_block_questions(paragraphs):
    """
    Detect block-based questions.
    Returns:
        question_starts: list[int]
        claimed_indices: set[int]  # ALL lines in qualifying blocks
    """
    question_starts = []
    claimed_indices = set()

    i = 0
    n = len(paragraphs)

    while i < n:
        if not paragraphs[i].strip():
            i += 1
            continue

        block_start = i
        block_indices = []

        while i < n and paragraphs[i].strip():
            block_indices.append(i)
            i += 1

        # Require question + ≥ 2 answers
        if len(block_indices) == 5:
            q_idx = block_indices[0]
            if _matches_question_criteria(paragraphs[q_idx]):
                question_starts.append(q_idx)
                claimed_indices.update(block_indices)

    return question_starts, claimed_indices


def find_inline_questions(paragraphs, exclude=None):
    """
    Identify question candidates using the original logic,
    excluding already-consumed indices.
    """
    if exclude is None:
        exclude = []
    return [
        i
        for i, p in enumerate(paragraphs)
        if i not in exclude and _matches_question_criteria(p)
    ]

def process(paragraphs, as_dataframe=True):
    paragraphs = [p.strip() for p in paragraphs]

    # 🔹 Phase 1: block-based detection
    block_questions, consumed = find_block_questions(paragraphs)

    # 🔹 Phase 2: fallback inline detection
    inline_questions = find_inline_questions(paragraphs, consumed)

    # 🔹 Combine & sort
    start_with_number = sorted(block_questions + inline_questions)

    parts = []
    for cur, nxt in zip_longest(
        start_with_number,
        start_with_number[1:],
        fillvalue=len(paragraphs)
    ):
        block = [line.strip() for line in paragraphs[cur:nxt] if line.strip()]
        n_lines = len(block)
        question = block[0]
        answers = _right_pad(block[1:min(5, n_lines)])
        answers, correct = _get_correct_answers(answers)

        question = re.sub(RE_REPL_QUESTION, "", question).strip()
        answers = [re.sub(RE_REPL_ANSWER[0], "", a).strip() for a in answers]
        answers = [re.sub(RE_REPL_ANSWER[1], "", a).strip() for a in answers]

        extra = block[5:n_lines] if n_lines > 5 else []
        parts.append((question, *answers, correct, "\n".join(extra)))

    if as_dataframe:
        df = pd.DataFrame(
            parts,
            columns=["question", "ans0", "ans1", "ans2", "ans3", "correct", "extra"],
        )
        return df, start_with_number

    return parts, start_with_number

def process_multiple(paths):
    dfs = []
    for path in paths:
        pars = get_docx_with_highlight_mark(path)
        df, _ = process(pars)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)
