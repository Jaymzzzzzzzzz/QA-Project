from fastmcp import FastMCP
import os
import re

treasury_app = FastMCP("treasury")
CORPUS_DIR = "/app/corpus"

@treasury_app.tool()
def list_corpus_files() -> str:
    """List all Treasury Bulletin files in the corpus."""
    index_path = os.path.join(CORPUS_DIR, "index.txt")
    if os.path.exists(index_path):
        with open(index_path, "r") as f:
            return f.read()
    if not os.path.exists(CORPUS_DIR):
        return f"Corpus not found at {CORPUS_DIR}"
    files = sorted(os.listdir(CORPUS_DIR))
    return f"Total files: {len(files)}\n" + "\n".join(files)

@treasury_app.tool()
def search_corpus(keyword: str) -> str:
    """Search all Treasury Bulletin documents for a keyword.
    Args:
        keyword: Word or phrase to search for e.g. national defense
    """
    if not os.path.exists(CORPUS_DIR):
        return f"Corpus not found at {CORPUS_DIR}"
    matches = []
    for fname in sorted(os.listdir(CORPUS_DIR)):
        if not fname.endswith(".txt"):
            continue
        fpath = os.path.join(CORPUS_DIR, fname)
        try:
            with open(fpath, "r", errors="ignore") as f:
                if keyword.lower() in f.read().lower():
                    matches.append(fname)
        except:
            pass
    if not matches:
        return f"No files found containing: {keyword}"
    return f"Found {len(matches)} files:\n" + "\n".join(matches)

@treasury_app.tool()
def search_corpus_multi(keywords: list) -> str:
    """Search corpus for files containing ALL given keywords.
    Args:
        keywords: List of keywords that must ALL appear in the file
    """
    if not os.path.exists(CORPUS_DIR):
        return f"Corpus not found at {CORPUS_DIR}"
    matches = []
    for fname in sorted(os.listdir(CORPUS_DIR)):
        if not fname.endswith(".txt"):
            continue
        fpath = os.path.join(CORPUS_DIR, fname)
        try:
            with open(fpath, "r", errors="ignore") as f:
                content = f.read().lower()
                if all(kw.lower() in content for kw in keywords):
                    matches.append(fname)
        except:
            pass
    if not matches:
        return f"No files found containing all of: {keywords}"
    return f"Found {len(matches)} files:\n" + "\n".join(matches)

@treasury_app.tool()
def read_document(filename: str) -> str:
    """Read a Treasury Bulletin document.
    Args:
        filename: e.g. treasury_bulletin_1941_01.txt
    """
    fpath = os.path.join(CORPUS_DIR, filename)
    if not os.path.exists(fpath):
        return f"File not found: {filename}"
    try:
        with open(fpath, "r", errors="ignore") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {e}"

@treasury_app.tool()
def search_in_file(filename: str, keyword: str) -> str:
    """Search for a keyword in a specific file and return surrounding lines.
    Args:
        filename: e.g. treasury_bulletin_1941_01.txt
        keyword: word or phrase to find
    """
    fpath = os.path.join(CORPUS_DIR, filename)
    if not os.path.exists(fpath):
        return f"File not found: {filename}"
    try:
        with open(fpath, "r", errors="ignore") as f:
            lines = f.readlines()
        results = []
        for i, line in enumerate(lines):
            if keyword.lower() in line.lower():
                start = max(0, i - 3)
                end = min(len(lines), i + 10)
                context = "".join(lines[start:end])
                results.append(f"--- Match at line {i+1} ---\n{context}")
        if not results:
            return f"Keyword not found in {filename}"
        return "\n".join(results[:5])
    except Exception as e:
        return f"Error: {e}"

@treasury_app.tool()
def calculate(expression: str) -> str:
    """Safely evaluate a math expression.
    Args:
        expression: e.g. (2602 - 1500) / 1500 * 100
    """
    try:
        cleaned = expression.replace(",", "")
        if re.match(r"^[\d\s\+\-\*\/\(\)\.\%]+$", cleaned):
            result = eval(cleaned)
            return str(round(result, 6))
        return "Error: unsafe characters in expression"
    except Exception as e:
        return f"Calculation error: {e}"
