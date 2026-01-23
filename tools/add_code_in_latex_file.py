from pathlib import Path
import re

def overlize(s: Path, is_path=False):
    if str(s) == ".":
        return "Project Root"
    if is_path:
        return str(s).replace("\\", "/")
    else:
        return str(s).replace("\\", "/").replace("_", "\\_")
    
def get_command(path: Path):
    match path.suffix:
        case ".py":
            return "pythonfile"
        case ".ini":
            return "inifile"
        case ".csv":
            return "csvfile"
        case ".txt":
            return "txtfile"
        case _:
            return "undefined"
def safe_label(s: str) -> str:
    return re.sub(r'[^a-zA-Z0-9:_-]', '_', s)
def get_unique_label(path: Path, labels: list[str]) -> str:
    name = safe_label(path.stem)
    test = name
    i = 0
    while test in labels:
        test = f"{safe_label(path.parent.stem)}-{name}" + (f"-{i}" if i > 0 else "")
        i += 1
    labels.append(test)
    return test

def sort_key(p: Path):
    parts = p.parts

    return (
        not(p.is_file() and p.parent.resolve() == Path.cwd().resolve()),
        parts[0].lower(),                      # 2. group by top-level folder
        len(parts),                            # 3. shorter depth first
        str(p).lower()                         # 4. alphabetical
    )

include_paths = ["./src", "./lib", "./Calibration", "./tools"]
include_extensions = ["*.py", "*.ini", "*.csv", "*.txt"]
exclude = ["NoCommit_", "\\old\\", "__init__", "config new.ini"]

files = [
    file
    for base in include_paths
    for pattern in include_extensions
    for file in Path(base).rglob(pattern)
    if not any(ex in str(file) for ex in exclude)
]
# Also add files in root directory
files.extend([
    file
    for pattern in include_extensions
    for file in Path(".").glob(pattern)
    if not any(ex in str(file) for ex in exclude)
])

files = sorted(files, key=sort_key)
with open("NoCommit_files.txt", "w") as fp:
    fp.write("\n".join(map(str, files)))
# files.insert(0, Path("config.ini"))

root = Path(".")
previous_parent_path = None
labels = []
with open("NoCommit_Latex_include_code.tex", "w") as fp:
    fp.write("\\chapter{Code}\n\n")

    for file in files:
        path = file.relative_to(root)
        parent_path = path.parent
        
        if parent_path != previous_parent_path:
            fp.write(f"""\\section{{{overlize(parent_path)}}}\n""")
            previous_parent_path = parent_path
        fp.write(f"""
\\phantomsection
\\subsection*{{{overlize(path)}}}
\\label{{ap:{get_unique_label(path, labels)}}}
\\{get_command(path)}{{../../../{overlize(path, is_path=True)}}}\n""")