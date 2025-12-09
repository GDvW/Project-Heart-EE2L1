from pathlib import Path

def overlize(s, is_path=False):
    if is_path:
        return str(s).replace("\\", "/")
    else:
        return str(s).replace("\\", "/").replace("_", "\\_")

include_paths = ["./src", "./lib"]
include_extensions = ["*.py", "*.ini"]
exclude = ["NoCommit_", "\\old\\"]

files = [
    file
    for base in include_paths
    for pattern in include_extensions
    for file in Path(base).rglob(pattern)
    if not any(ex in str(file) for ex in exclude)
]

root = Path(".")
previous_parent_path = None
with open("NoCommit_Latex_include_code.tex", "w") as fp:
    for file in files:
        path = file.relative_to(root)
        parent_path = path.parent
        if parent_path != previous_parent_path:
            fp.write(f"""\\section{{{overlize(parent_path)}}}\n""")
            previous_parent_path = parent_path
        fp.write(f"""\\subsection{{{overlize(path)}}}\n\\lstinputlisting{{../../../{overlize(path, is_path=True)}}}\n""")