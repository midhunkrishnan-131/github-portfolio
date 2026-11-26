"""Copy the portfolio into a GitHub Pages folder and prefix root paths.

Local preview stays at http://localhost:8767/. The live site is served from
https://midhunkrishnan-131.github.io/github-portfolio/, so absolute URLs need
that prefix only in the published copy.
"""
import re
import shutil
import sys
from pathlib import Path

BASE = "/github-portfolio"
ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "dev-portfolio-template-main"
SKIP_NAMES = {"wall.json", "wall.txt"}
SUFFIXES = {".html", ".css", ".js", ".json"}
PATH = re.compile(
    r"""(?P<prefix>["'(])/(?P<path>favicon\.svg|intros/|assets/|site/|themes\.json|github-snapshot\.json)"""
)


def rewrite(text):
    text = text.replace('href="/"', f'href="{BASE}/"')
    text = text.replace('location.href = "/"', f'location.href = "{BASE}/"')
    return PATH.sub(lambda match: f"{match.group('prefix')}{BASE}/{match.group('path')}", text)


def main():
    out = Path(sys.argv[1] if len(sys.argv) > 1 else ROOT / "_site")
    if out.exists():
        shutil.rmtree(out)
    shutil.copytree(
        SRC,
        out,
        ignore=shutil.ignore_patterns(".git", "__pycache__", ".venv", "node_modules", ".DS_Store"),
    )
    changed = []
    for path in out.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in SUFFIXES or path.name in SKIP_NAMES:
            continue
        original = path.read_text(encoding="utf-8")
        updated = rewrite(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8", newline="\n")
            changed.append(path.relative_to(out).as_posix())
    (out / ".nojekyll").write_text("", encoding="utf-8")
    print(f"prepared {out} ({len(changed)} files rewritten)")
    for name in changed:
        print(name)


if __name__ == "__main__":
    main()
