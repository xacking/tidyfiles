from __future__ import annotations

import argparse
from collections import Counter

from . import __version__, apply, plan


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="tidyfiles", description="Sort a messy folder into subfolders.")
    p.add_argument("folder", nargs="?", default=".", help="folder to organize (default: current)")
    p.add_argument("--by", choices=["type", "date", "ext"], default="type", help="how to group files (default: type)")
    p.add_argument("-n", "--dry-run", action="store_true", help="show the plan without moving anything")
    p.add_argument("-y", "--yes", action="store_true", help="don't ask for confirmation")
    p.add_argument("--hidden", action="store_true", help="include dotfiles")
    p.add_argument("-V", "--version", action="version", version=f"%(prog)s {__version__}")
    args = p.parse_args(argv)

    moves = plan(args.folder, by=args.by, include_hidden=args.hidden)
    if not moves:
        print("Already tidy. Nothing to move.")
        return 0

    counts = Counter(m.dst.parent.name for m in moves)
    for name, n in sorted(counts.items()):
        print(f"  {name:<15} {n} file(s)")
    print(f"\n{len(moves)} file(s) to move.")

    if args.dry_run:
        for m in moves:
            print(f"  {m.src.name}  ->  {m.dst.parent.name}/{m.dst.name}")
        return 0

    if not args.yes and input("Proceed? [y/N] ").strip().lower() not in ("y", "yes"):
        print("Aborted.")
        return 1

    apply(moves)
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
