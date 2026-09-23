from pathlib import Path
from datetime import datetime

VAULT = Path("/home/user/Downloads/The Forest Project/The Forest Project")

def has_frontmatter(text):
    return text.startswith("---\n")

def infer_tree(path):
    parts = [part.lower() for part in path.parts]

    tree_folders = {
        "bristlecone pine": "Bristlecone Pine",
        "cherry": "Cherry",
        "maple": "Maple",
        "cedar": "Cedar",
        "sycamore": "Sycamore",
    }

    for folder_name, tree_name in tree_folders.items():
        if folder_name in parts:
            return tree_name

    return None

today = datetime.now().strftime("%Y-%m-%d")

for path in VAULT.rglob("*.md"):
    text = path.read_text(encoding="utf-8", errors="ignore")

    if has_frontmatter(text):
        print(f"[KEEP] {path.relative_to(VAULT)}")
        continue

    tree = infer_tree(path)

    frontmatter = [
        "---",
        "project: The Forest",
        "status: active",
        f"created: {today}",
        f"updated: {today}",
    ]

    if tree:
        frontmatter.append(f"tree: {tree}")

    frontmatter.extend([
        "tags:",
        "  - the-forest",
        "---",
        "",
    ])

    new_text = "\n".join(frontmatter) + text

    path.write_text(new_text, encoding="utf-8")

    print(f"[ADDED] {path.relative_to(VAULT)}")
    if tree:
        print(f"  tree: {tree}")
