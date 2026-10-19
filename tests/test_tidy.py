from pathlib import Path

from tidyfiles import apply, category_for, plan
from tidyfiles.cli import main


def make(tmp_path: Path, *names: str):
    for n in names:
        (tmp_path / n).write_text("x")


def test_category():
    assert category_for(Path("a.JPG")) == "Images"
    assert category_for(Path("a.unknown")) == "Other"


def test_plan_and_apply(tmp_path):
    make(tmp_path, "a.pdf", "b.png", "c.zip", "d.weird", ".hidden", "e.crdownload", "desktop.ini")
    (tmp_path / "Documents").mkdir()
    (tmp_path / "Documents" / "a.pdf").write_text("old")
    moves = plan(tmp_path)
    names = {m.src.name: f"{m.dst.parent.name}/{m.dst.name}" for m in moves}
    assert names == {"a.pdf": "Documents/a (1).pdf", "b.png": "Images/b.png", "c.zip": "Archives/c.zip", "d.weird": "Other/d.weird"}
    assert apply(moves) == 4
    assert (tmp_path / "Images" / "b.png").exists()
    assert (tmp_path / ".hidden").exists() and (tmp_path / "e.crdownload").exists()


def test_by_ext_and_cli(tmp_path, capsys):
    make(tmp_path, "x.pdf", "y.PDF", "z")
    assert {m.dst.parent.name for m in plan(tmp_path, by="ext")} == {"PDF", "NO_EXTENSION"}
    assert main([str(tmp_path), "--dry-run"]) == 0
    assert "3 file(s) to move" in capsys.readouterr().out
    assert main([str(tmp_path), "-y"]) == 0
    assert (tmp_path / "Documents" / "x.pdf").exists()
    assert main([str(tmp_path), "-y"]) == 0  # already tidy
