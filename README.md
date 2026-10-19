# tidyfiles

A command-line tool that sorts a messy folder (looking at you, Downloads) into tidy subfolders. Safe by default: it shows the plan and asks before moving, never overwrites (it renames duplicates to `file (1).pdf`), and skips half-finished downloads.

```bash
pip install git+https://github.com/xacking/tidyfiles
```

```
$ tidyfiles ~/Downloads
  Archives        12 file(s)
  Documents       48 file(s)
  Images          131 file(s)
  Installers      9 file(s)
  Other           4 file(s)
  Videos          7 file(s)

211 file(s) to move.
Proceed? [y/N] y
Done.
```

## Usage

```bash
tidyfiles                     # current folder, grouped by type
tidyfiles ~/Downloads -n      # dry run: list every move
tidyfiles ~/Desktop --by date # 2026-09/, 2026-10/ ...
tidyfiles . --by ext -y       # PDF/, PNG/, ZIP/ ..., no prompt
```

Categories: Images, Videos, Audio, Documents, Spreadsheets, Presentations, Archives, Installers, Code, Fonts, Other.

Skipped automatically: subfolders, dotfiles (unless `--hidden`), `desktop.ini`, `Thumbs.db`, `.DS_Store`, and in-progress downloads (`.crdownload`, `.part`, `.tmp`).

## Use it from Python

```python
from tidyfiles import plan, apply

moves = plan("~/Downloads", by="type")
for m in moves:
    print(m.src.name, "->", m.dst)
apply(moves)
```

## License

MIT
