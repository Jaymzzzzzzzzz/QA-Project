from fastmcp import FastMCP
import os
import re
import math
import json

treasury_app = FastMCP("treasury")
CORPUS_DIR = "/app/corpus"

@treasury_app.tool()
def list_corpus_files() -> str:
    """List all Treasury Bulletin files in the corpus."""
    index_path = os.path.join(CORPUS_DIR, "index.txt")
    if os.path.exists(index_path):
        with open(index_path, "r") as f:
            return f.read()
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

@treasury_app.tool()
def compute_stats(values: list, operation: str) -> str:
    """Perform statistical calculations on a list of numbers.
    Args:
        values: List of numbers e.g. [100.5, 200.3, 150.0]
        operation: One of: sum, mean, geometric_mean, percent_change, linear_regression, boxcox
    """
    try:
        nums = [float(str(v).replace(",","")) for v in values]
        
        if operation == "sum":
            return str(round(sum(nums), 6))
        
        elif operation == "mean":
            return str(round(sum(nums)/len(nums), 6))
        
        elif operation == "geometric_mean":
            product = 1.0
            for n in nums:
                product *= n
            gm = product ** (1.0/len(nums))
            return str(round(gm, 6))
        
        elif operation == "percent_change":
            if len(nums) != 2:
                return "Error: percent_change needs exactly 2 values [old, new]"
            old, new = nums[0], nums[1]
            pct = abs((new - old) / old) * 100
            return str(round(pct, 6))
        
        elif operation == "linear_regression":
            # OLS linear regression: values are Y, X is 0,1,2,...
            # But caller should pass [x1,y1,x2,y2,...] pairs
            # We treat as Y values with X = index
            n = len(nums)
            x = list(range(n))
            x_mean = sum(x)/n
            y_mean = sum(nums)/n
            num = sum((x[i]-x_mean)*(nums[i]-y_mean) for i in range(n))
            den = sum((x[i]-x_mean)**2 for i in range(n))
            slope = num/den
            intercept = y_mean - slope*x_mean
            return f"slope={round(slope,6)}, intercept={round(intercept,6)}"
        
        elif operation == "boxcox":
            # Box-Cox with lambda=0.75 (default for treasury questions)
            lam = 0.75
            transformed = [(v**lam - 1)/lam for v in nums]
            return str([round(t,6) for t in transformed])
        
        else:
            return f"Unknown operation: {operation}. Use: sum, mean, geometric_mean, percent_change, linear_regression, boxcox"
    
    except Exception as e:
        return f"Error: {e}"

@treasury_app.tool()
def linear_regression_years(years: list, values: list) -> str:
    """Fit OLS linear regression with actual year numbers as X.
    Args:
        years: List of year numbers e.g. [1929, 1930, 1931]
        values: Corresponding Y values e.g. [2.3, 1.1, 0.8]
    Returns slope and intercept rounded to 3 decimal places.
    """
    try:
        x = [float(y) for y in years]
        y = [float(str(v).replace(",","")) for v in values]
        n = len(x)
        x_mean = sum(x)/n
        y_mean = sum(y)/n
        num = sum((x[i]-x_mean)*(y[i]-y_mean) for i in range(n))
        den = sum((x[i]-x_mean)**2 for i in range(n))
        slope = num/den
        intercept = y_mean - slope*x_mean
        return f"[{round(slope,3)}, {round(intercept,3)}]"
    except Exception as e:
        return f"Error: {e}"

@treasury_app.tool()
def boxcox_transform(value: float, lam: float) -> str:
    """Apply Box-Cox transformation to a single value.
    Args:
        value: The number to transform
        lam: Lambda parameter (e.g. 0.75)
    """
    try:
        result = (value**lam - 1) / lam
        return str(round(result, 6))
    except Exception as e:
        return f"Error: {e}"
