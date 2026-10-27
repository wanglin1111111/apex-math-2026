"""Write SHA-256 for every delivered file (excluding the manifest itself)."""

from __future__ import annotations

import hashlib
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
TARGETS = [ROOT / "code", ROOT / "artifacts", ROOT / "report"]
EXTRA = [ROOT / "submission.md", ROOT / "submission-challenge.md", ROOT / "PROGRESS.md", ROOT / "BLOCKED.md"]


def sha256(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _publishable(path: pathlib.Path) -> bool:
    """Exclude interpreter caches: they are machine-specific and git-ignored,
    so listing them would make the manifest unverifiable after a clone."""
    if "__pycache__" in path.parts:
        return False
    if path.suffix in (".pyc", ".pyo"):
        return False
    return True


def main() -> None:
    paths = []
    for target in TARGETS:
        paths.extend(sorted(p for p in target.rglob("*") if p.is_file()))
    paths.extend(p for p in EXTRA if p.exists())
    paths = [p for p in paths if _publishable(p)]
    manifest = ROOT / "report" / "SHA256SUMS.txt"
    lines = []
    for path in sorted(set(paths)):
        if path == manifest:
            continue
        lines.append(f"{sha256(path)}  {path.relative_to(ROOT).as_posix()}")
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("wrote", manifest)
    print("entries", len(lines))


if __name__ == "__main__":
    main()
