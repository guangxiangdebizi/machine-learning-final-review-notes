from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHAPTER_DIR = ROOT / "review_notes" / "chapters"
OUTPUT_FILE = ROOT / "review_notes" / "机器学习期末总复习.md"
SECTION_SEPARATOR = "\n***\n"
CHAPTER_SEPARATOR = "\n\n***\n\n"


def chapter_sort_key(path: Path) -> tuple[int, str]:
    prefix = path.stem.split("_", 1)[0]
    try:
        return int(prefix), path.name
    except ValueError:
        return 999, path.name


def main() -> None:
    chapter_files = sorted(CHAPTER_DIR.glob("*.md"), key=chapter_sort_key)
    if not chapter_files:
        raise SystemExit(f"No chapter markdown files found under: {CHAPTER_DIR}")

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    parts = [
        "# 机器学习期末总复习\n",
        "> 本文由章节复习笔记自动合并生成。若需更新，请先修改 `review_notes/chapters/` 下的对应章节，再运行 `python scripts/merge_review_notes.py`。\n",
        "\n",
        "## 使用建议\n",
        "- 先看 `00 机器学习期末考试总览`，明确老师强调的高频点。\n",
        "- 再按 `03 / 05 / 06 / 07 / 14 / 15 / 16 / 19` 的顺序抓重点章。\n",
        "- 对计算题，优先复习：梯度下降、前向传播、反向传播、FGSM、PCA 基本步骤。\n",
        "- 对概念题，优先复习：监督 / 半监督 / 无监督、最大似然、正则化、bias / variance。\n",
        "\n",
        "## 目录\n",
    ]

    for chapter in chapter_files:
        title = chapter.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
        parts.append(f"- {title}\n")

    parts.append(SECTION_SEPARATOR)

    for index, chapter in enumerate(chapter_files):
        text = chapter.read_text(encoding="utf-8").rstrip()
        parts.append(text)
        parts.append(CHAPTER_SEPARATOR if index != len(chapter_files) - 1 else "\n")

    OUTPUT_FILE.write_text("".join(parts), encoding="utf-8")
    print(f"wrote {OUTPUT_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
