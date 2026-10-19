"""Organize a messy folder (hello, Downloads) into tidy subfolders by file type or date."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

__all__ = ["CATEGORIES", "Move", "category_for", "plan", "apply"]
__version__ = "0.1.0"

CATEGORIES: dict[str, set[str]] = {
    "Images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".heic", ".bmp", ".tiff", ".ico"},
    "Videos": {".mp4", ".mov", ".mkv", ".avi", ".webm", ".flv", ".wmv", ".m4v"},
    "Audio": {".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a", ".wma"},
    "Documents": {".pdf", ".doc", ".docx", ".odt", ".rtf", ".txt", ".md", ".epub"},
    "Spreadsheets": {".xls", ".xlsx", ".csv", ".ods", ".tsv"},
    "Presentations": {".ppt", ".pptx", ".odp", ".key"},
    "Archives": {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".tgz"},
    "Installers": {".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm", ".apk", ".appimage"},
    "Code": {".py", ".js", ".ts", ".tsx", ".jsx", ".html", ".css", ".json", ".yaml", ".yml", ".java", ".c", ".cpp", ".go", ".rs", ".php", ".sh", ".ipynb", ".sql"},
    "Fonts": {".ttf", ".otf", ".woff", ".woff2"},
}

_SKIP = {"desktop.ini", "thumbs.db", ".ds_store"}
_PARTIAL = {".crdownload", ".part", ".tmp", ".download"}


@dataclass(frozen=True)
class Move:
    src: Path
    dst: Path


def category_for(path: Path) -> str:
    ext = path.suffix.lower()
    for name, exts in CATEGORIES.items():
        if ext in exts:
            return name
    return "Other"


def _unique(dst: Path, taken: set[Path]) -> Path:
    if not dst.exists() and dst not in taken:
        return dst
    stem, suffix, i = dst.stem, dst.suffix, 1
    while True:
        candidate = dst.with_name(f"{stem} ({i}){suffix}")
        if not candidate.exists() and candidate not in taken:
            return candidate
        i += 1


def plan(folder: str | Path, by: str = "type", include_hidden: bool = False) -> list[Move]:
    """Work out what would move where, without touching anything.

    by: "type" (Images/, Documents/...), "date" (2026-10/), or "ext" (PDF/, PNG/).
    """
    root = Path(folder).expanduser().resolve()
    if not root.is_dir():
        raise NotADirectoryError(root)
    moves: list[Move] = []
    taken: set[Path] = set()
    for f in sorted(root.iterdir()):
        if not f.is_file() or f.name.lower() in _SKIP or f.suffix.lower() in _PARTIAL:
            continue
        if f.name.startswith(".") and not include_hidden:
            continue
        if by == "type":
            sub = category_for(f)
        elif by == "date":
            sub = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m")
        elif by == "ext":
            sub = f.suffix.lstrip(".").upper() or "NO_EXTENSION"
        else:
            raise ValueError("by must be 'type', 'date' or 'ext'")
        dst = _unique(root / sub / f.name, taken)
        taken.add(dst)
        moves.append(Move(f, dst))
    return moves


def apply(moves: list[Move]) -> int:
    for m in moves:
        m.dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(m.src), str(m.dst))
    return len(moves)
