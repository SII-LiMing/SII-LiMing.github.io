#!/usr/bin/env python3
"""
Convert a Typora markdown note into a Jekyll blog post.

This script handles the common differences between Typora/GitHub-flavored
notes and this Academic Pages/Jekyll site:

1. Read the first H1 as the post title, then comment it out to avoid rendering
   a duplicate title below the Jekyll page title.
2. Normalize display math blocks and wrap top-level ``\\`` rows in
   ``gathered`` so MathJax renders them on separate lines.
3. Convert Typora ``==highlight==`` and ``^superscript^`` syntax into
   semantic HTML ``<mark>`` and ``<sup>`` elements.
4. Copy local markdown/html image assets into the public images directory.
5. Convert GitHub/Obsidian callouts such as > [!NOTE] into notice blocks.
6. Add Jekyll front matter when the source note does not already have it.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from datetime import date
from pathlib import Path
from urllib.parse import unquote, urlparse


CALLOUT_CLASSES = {
    "NOTE": "notice--info",
    "TIP": "notice--success",
    "IMPORTANT": "notice--primary",
    "WARNING": "notice--warning",
    "CAUTION": "notice--danger",
}

H1_PATTERN = re.compile(r"^ {0,3}#(?!#)[ \t]+(.+?)(?:[ \t]+#+)?[ \t]*$")
COMMENTED_H1_PATTERN = re.compile(
    r"^\s*<!--\s*#(?!#)[ \t]+(.+?)(?:[ \t]+#+)?[ \t]*-->\s*$"
)


def split_front_matter(text: str) -> tuple[str | None, str]:
    """Return existing YAML front matter and body."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None, text

    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            front_matter = "\n".join(lines[: index + 1])
            body = "\n".join(lines[index + 1 :])
            return front_matter, body

    return None, text


def is_fence_line(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("```") or stripped.startswith("~~~")


def find_title_heading(lines: list[str]) -> tuple[int, str, bool] | None:
    """Find the first unfenced H1, including one already commented out."""
    in_fence = False

    for index, line in enumerate(lines):
        if is_fence_line(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        match = H1_PATTERN.match(line)
        if match:
            return index, match.group(1).strip(), False

        match = COMMENTED_H1_PATTERN.match(line)
        if match:
            return index, match.group(1).strip(), True

    return None


def extract_title(body: str, source: Path) -> str:
    """Use the first visible or commented H1, otherwise use the filename."""
    heading = find_title_heading(body.splitlines())
    if heading:
        return heading[1]

    stem = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", source.stem)
    return stem.replace("-", " ").replace("_", " ").strip() or "Untitled Post"


def comment_out_title_heading(body: str) -> str:
    """Comment out the first H1 so the Jekyll layout is the only title layer."""
    lines = body.splitlines()
    heading = find_title_heading(lines)
    if heading is None or heading[2]:
        return body

    index = heading[0]
    lines[index] = f"<!-- {lines[index].strip()} -->"
    trailing_newline = "\n" if body.endswith("\n") else ""
    return "\n".join(lines) + trailing_newline


def slugify(value: str, fallback: str = "post") -> str:
    """Create a conservative URL slug."""
    value = value.lower().strip()
    value = re.sub(r"[\s_]+", "-", value)
    value = re.sub(r"[^a-z0-9-]+", "", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or fallback


def make_front_matter(title: str, post_date: str, slug: str, tags: list[str]) -> str:
    year, month, _ = post_date.split("-")
    permalink = f"/posts/{year}/{month}/{slug}/"
    lines = [
        "---",
        f'title: "{title}"',
        f"date: {post_date}",
        f"permalink: {permalink}",
    ]

    if tags:
        lines.append("tags:")
        lines.extend(f"  - {tag}" for tag in tags)

    lines.append("---")
    return "\n".join(lines)


def convert_callouts(text: str) -> str:
    """Convert > [!NOTE] style callouts into Academic Pages notice blocks."""
    lines = text.splitlines()
    output: list[str] = []
    index = 0
    in_fence = False

    callout_pattern = re.compile(
        r"^>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\][+-]?\s*(.*?)\s*$",
        re.IGNORECASE,
    )

    while index < len(lines):
        line = lines[index]

        if is_fence_line(line):
            in_fence = not in_fence
            output.append(line)
            index += 1
            continue

        match = None if in_fence else callout_pattern.match(line)
        if not match:
            output.append(line)
            index += 1
            continue

        kind = match.group(1).upper()
        title = match.group(2).strip()
        notice_class = CALLOUT_CLASSES[kind]
        label = kind.title()
        body: list[str] = []
        index += 1

        while index < len(lines):
            current = lines[index]
            if current.startswith(">"):
                body.append(re.sub(r"^>\s?", "", current))
                index += 1
                continue
            break

        while body and not body[0].strip():
            body.pop(0)
        while body and not body[-1].strip():
            body.pop()

        output.append(f'<div class="{notice_class}" markdown="1">')
        heading = f"**{label}:**"
        if title:
            heading += f" {title}"
        output.append(heading)
        if body:
            output.append("")
            output.extend(body)
        output.append("</div>")

    return "\n".join(output) + ("\n" if text.endswith("\n") else "")


def is_escaped(text: str, index: int) -> bool:
    """Return whether the character at ``index`` is backslash-escaped."""
    backslashes = 0
    index -= 1
    while index >= 0 and text[index] == "\\":
        backslashes += 1
        index -= 1
    return backslashes % 2 == 1


def find_unescaped(text: str, delimiter: str, start: int) -> int:
    """Find the next unescaped delimiter, or return ``-1``."""
    index = text.find(delimiter, start)
    while index != -1:
        if not is_escaped(text, index):
            return index
        index = text.find(delimiter, index + len(delimiter))
    return -1


def is_typora_opening_delimiter(line: str, index: int, delimiter: str) -> bool:
    """Return whether ``delimiter`` starts exact Typora inline markup."""
    delimiter_character = delimiter[0]
    content_start = index + len(delimiter)
    return (
        line.startswith(delimiter, index)
        and not is_escaped(line, index)
        and (index == 0 or line[index - 1] != delimiter_character)
        and not (delimiter == "^" and index > 0 and line[index - 1] == "[")
        and content_start < len(line)
        and line[content_start] != delimiter_character
        and not line[content_start].isspace()
    )


def find_typora_closing_delimiter(
    line: str, delimiter: str, content_start: int
) -> int:
    """Find an exact Typora closing delimiter with nonblank content."""
    delimiter_character = delimiter[0]
    closing_index = line.find(delimiter, content_start)

    while closing_index != -1:
        delimiter_end = closing_index + len(delimiter)
        content = line[content_start:closing_index]
        if (
            closing_index > content_start
            and not is_escaped(line, closing_index)
            and line[closing_index - 1] != delimiter_character
            and not line[closing_index - 1].isspace()
            and (delimiter != "^" or not any(char.isspace() for char in content))
            and (
                delimiter_end == len(line)
                or line[delimiter_end] != delimiter_character
            )
        ):
            return closing_index
        closing_index = line.find(delimiter, closing_index + len(delimiter))

    return -1


def convert_typora_inline_markup_in_line(line: str) -> str:
    """Convert Typora highlight/superscript outside code, math, and HTML."""
    output: list[str] = []
    index = 0

    while index < len(line):
        character = line[index]

        if character == "<":
            tag_end = line.find(">", index + 1)
            if tag_end != -1:
                output.append(line[index : tag_end + 1])
                index = tag_end + 1
                continue

        if character == "`" and not is_escaped(line, index):
            delimiter_end = index + 1
            while delimiter_end < len(line) and line[delimiter_end] == "`":
                delimiter_end += 1
            delimiter = line[index:delimiter_end]
            code_end = line.find(delimiter, delimiter_end)
            if code_end != -1:
                code_end += len(delimiter)
                output.append(line[index:code_end])
                index = code_end
                continue

        if character == "$" and not is_escaped(line, index):
            delimiter = "$$" if line.startswith("$$", index) else "$"
            math_end = find_unescaped(line, delimiter, index + len(delimiter))
            if math_end != -1:
                math_end += len(delimiter)
                output.append(line[index:math_end])
                index = math_end
                continue

        converted = False
        for delimiter, tag in (("==", "mark"), ("^", "sup")):
            if not is_typora_opening_delimiter(line, index, delimiter):
                continue
            content_start = index + len(delimiter)
            closing_index = find_typora_closing_delimiter(
                line, delimiter, content_start
            )
            if closing_index == -1:
                continue
            content = line[content_start:closing_index]
            output.append(f"<{tag}>{content}</{tag}>")
            index = closing_index + len(delimiter)
            converted = True
            break

        if converted:
            continue

        output.append(character)
        index += 1

    return "".join(output)


def convert_typora_inline_markup(text: str) -> str:
    """Convert Typora inline markup outside fenced and display math blocks."""
    lines = text.splitlines()
    output: list[str] = []
    in_fence = False
    in_display_math = False

    for line in lines:
        if is_fence_line(line) and not in_display_math:
            in_fence = not in_fence
            output.append(line)
            continue

        if not in_fence and line.strip() == "$$":
            in_display_math = not in_display_math
            output.append(line)
            continue

        if in_fence or in_display_math:
            output.append(line)
        else:
            output.append(convert_typora_inline_markup_in_line(line))

    return "\n".join(output) + ("\n" if text.endswith("\n") else "")


def has_top_level_row_break(lines: list[str]) -> bool:
    """Return whether a math block contains ``\\`` outside nested structures."""
    environment_depth = 0
    brace_depth = 0
    begin_pattern = re.compile(r"\\begin\s*\{[^{}]+\}")
    end_pattern = re.compile(r"\\end\s*\{[^{}]+\}")

    for line in lines:
        index = 0
        while index < len(line):
            character = line[index]

            # An unescaped percent sign starts a TeX comment. Escaped percent
            # signs are consumed by the backslash branch below.
            if character == "%":
                break

            if character != "\\":
                if character == "{":
                    brace_depth += 1
                elif character == "}" and brace_depth:
                    brace_depth -= 1
                index += 1
                continue

            begin_match = begin_pattern.match(line, index)
            if begin_match:
                environment_depth += 1
                index = begin_match.end()
                continue

            end_match = end_pattern.match(line, index)
            if end_match:
                environment_depth = max(0, environment_depth - 1)
                index = end_match.end()
                continue

            if line.startswith("\\\\", index):
                if environment_depth == 0 and brace_depth == 0:
                    return True
                index += 2
                continue

            # Skip a TeX control word or escaped symbol so constructs such as
            # \% and \{ do not affect comment or brace tracking.
            index += 1
            if index < len(line) and line[index].isalpha():
                while index < len(line) and line[index].isalpha():
                    index += 1
            elif index < len(line):
                index += 1

    return False


def normalize_display_math(text: str) -> str:
    """Normalize standalone ``$$`` blocks for Jekyll and MathJax."""
    lines = text.splitlines()
    output: list[str] = []
    in_fence = False
    in_math = False
    math_content_start: int | None = None
    just_closed_math = False

    for line in lines:
        if just_closed_math:
            if not line.strip():
                continue
            just_closed_math = False

        if is_fence_line(line) and not in_math:
            in_fence = not in_fence
            output.append(line)
            continue

        if in_fence:
            output.append(line)
            continue

        if line.strip() == "$$":
            if not in_math:
                if output and output[-1].strip():
                    output.append("")
                output.append("$$")
                in_math = True
                math_content_start = len(output)
            else:
                if math_content_start is not None:
                    math_lines = output[math_content_start:]
                    if has_top_level_row_break(math_lines):
                        output[math_content_start:] = [
                            r"\begin{gathered}",
                            *math_lines,
                            r"\end{gathered}",
                        ]
                output.append("$$")
                output.append("")
                in_math = False
                math_content_start = None
                just_closed_math = True
            continue

        if in_math and not line.strip():
            continue

        output.append(line)

    while output and not output[-1].strip():
        output.pop()

    return "\n".join(output) + "\n"


def split_markdown_link_target(raw: str) -> tuple[str, str]:
    """Split a markdown link target into destination and optional title."""
    target = raw.strip()
    if target.startswith("<"):
        end = target.find(">")
        if end != -1:
            return target[1:end], target[end + 1 :].strip()

    quote_match = re.match(r"^(\S+)(\s+['\"].*['\"])\s*$", target)
    if quote_match:
        return quote_match.group(1), quote_match.group(2).strip()

    return target, ""


def should_skip_asset(path_text: str) -> bool:
    parsed = urlparse(path_text)
    if parsed.scheme and parsed.scheme not in {"file"}:
        return True
    if path_text.startswith("#"):
        return True
    if path_text.startswith("/") and not Path(path_text).exists():
        return True
    return False


def resolve_asset_path(path_text: str, source_md: Path, repo_root: Path) -> Path | None:
    parsed = urlparse(path_text)
    if parsed.scheme == "file":
        candidate = Path(unquote(parsed.path)).expanduser()
        return candidate if candidate.exists() else None

    decoded = unquote(path_text)
    candidate = Path(decoded).expanduser()
    if candidate.is_absolute():
        return candidate if candidate.exists() else None

    candidates = [
        source_md.parent / candidate,
        repo_root / candidate,
    ]
    for item in candidates:
        if item.exists():
            return item.resolve()
    return None


def unique_destination(asset_dir: Path, filename: str, source: Path) -> Path:
    """Return a non-conflicting destination for an asset."""
    destination = asset_dir / filename
    if not destination.exists() or destination.resolve() == source.resolve():
        return destination

    stem = destination.stem
    suffix = destination.suffix
    counter = 2
    while True:
        candidate = asset_dir / f"{stem}-{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def copy_asset(
    path_text: str,
    source_md: Path,
    repo_root: Path,
    asset_dir: Path,
    copied: dict[Path, str],
) -> str | None:
    """Copy a local asset and return its site-root URL path."""
    if should_skip_asset(path_text):
        return None

    source = resolve_asset_path(path_text, source_md, repo_root)
    if source is None or not source.is_file():
        return None

    source = source.resolve()
    if source not in copied:
        destination = unique_destination(asset_dir, source.name, source)
        asset_dir.mkdir(parents=True, exist_ok=True)
        if destination.resolve() != source:
            shutil.copy2(source, destination)
        copied[source] = "/" + destination.relative_to(repo_root).as_posix()

    return copied[source]


def rewrite_markdown_images(
    text: str,
    source_md: Path,
    repo_root: Path,
    asset_dir: Path,
    copied: dict[Path, str],
) -> str:
    pattern = re.compile(r"!\[([^\]]*)\]\(([^)\n]+)\)")

    def replace(match: re.Match[str]) -> str:
        alt = match.group(1)
        raw_target = match.group(2)
        destination, title = split_markdown_link_target(raw_target)
        new_url = copy_asset(destination, source_md, repo_root, asset_dir, copied)
        if new_url is None:
            return match.group(0)
        title_part = f" {title}" if title else ""
        return f"![{alt}]({new_url}{title_part})"

    return pattern.sub(replace, text)


def rewrite_html_images(
    text: str,
    source_md: Path,
    repo_root: Path,
    asset_dir: Path,
    copied: dict[Path, str],
) -> str:
    pattern = re.compile(r'(<img\b[^>]*?\bsrc=["\'])([^"\']+)(["\'][^>]*>)', re.IGNORECASE)

    def replace(match: re.Match[str]) -> str:
        new_url = copy_asset(match.group(2), source_md, repo_root, asset_dir, copied)
        if new_url is None:
            return match.group(0)
        return f"{match.group(1)}{new_url}{match.group(3)}"

    return pattern.sub(replace, text)


def parse_tags(values: list[str]) -> list[str]:
    tags: list[str] = []
    for value in values:
        for item in value.split(","):
            tag = item.strip()
            if tag:
                tags.append(tag)
    return tags


def convert(args: argparse.Namespace) -> Path:
    repo_root = Path(args.repo_root).expanduser().resolve()
    source_md = Path(args.input).expanduser().resolve()
    if not source_md.exists():
        raise FileNotFoundError(f"Input file does not exist: {source_md}")

    raw_text = source_md.read_text(encoding="utf-8")
    existing_front_matter, body = split_front_matter(raw_text)
    title = args.title or extract_title(body, source_md)
    body = comment_out_title_heading(body)
    post_date = args.date
    slug = args.slug or slugify(source_md.stem)
    tags = parse_tags(args.tag)

    if args.output:
        output_path = Path(args.output).expanduser()
        if not output_path.is_absolute():
            output_path = repo_root / output_path
    else:
        output_path = repo_root / args.post_dir / f"{post_date}-{slug}.md"

    if args.asset_dir:
        asset_dir = Path(args.asset_dir).expanduser()
        if not asset_dir.is_absolute():
            asset_dir = repo_root / asset_dir
    else:
        asset_dir = repo_root / args.image_root / slug

    copied: dict[Path, str] = {}
    body = convert_callouts(body)
    body = convert_typora_inline_markup(body)
    body = normalize_display_math(body)
    body = rewrite_markdown_images(body, source_md, repo_root, asset_dir, copied)
    body = rewrite_html_images(body, source_md, repo_root, asset_dir, copied)

    front_matter = existing_front_matter
    if front_matter is None or args.replace_front_matter:
        front_matter = make_front_matter(title, post_date, slug, tags)

    final_text = f"{front_matter}\n\n{body.rstrip()}\n"

    if output_path.exists() and not args.overwrite:
        raise FileExistsError(
            f"Output already exists: {output_path}. Use --overwrite to replace it."
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(final_text, encoding="utf-8")

    print(f"Wrote post: {output_path.relative_to(repo_root)}")
    if copied:
        print(f"Copied images: {asset_dir.relative_to(repo_root)}")
    return output_path


def build_parser() -> argparse.ArgumentParser:
    repo_root = Path(__file__).resolve().parents[1]
    today = date.today().isoformat()
    parser = argparse.ArgumentParser(
        description="Convert a Typora markdown note into a Jekyll post.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python scripts/typora_to_jekyll_post.py notes/flow.md --title \"Flow Matching Lecture 1\" --slug flow-matching-lecture1 --tag \"flow matching\"\n"
            "  python scripts/typora_to_jekyll_post.py notes/flow.md --slug flow-matching-lecture1 --overwrite\n"
        ),
    )
    parser.add_argument("input", help="Source Typora markdown file.")
    parser.add_argument("--title", help="Post title. Defaults to first H1 or filename.")
    parser.add_argument("--date", default=today, help=f"Post date. Default: {today}.")
    parser.add_argument("--slug", help="URL/file slug. Defaults to slugified filename.")
    parser.add_argument(
        "--tag",
        action="append",
        default=[],
        help="Post tag. Can be repeated or comma-separated.",
    )
    parser.add_argument(
        "--output",
        help="Output markdown path. Default: _posts/YYYY-MM-DD-slug.md.",
    )
    parser.add_argument("--post-dir", default="_posts", help="Jekyll post directory.")
    parser.add_argument("--image-root", default="images", help="Public image root.")
    parser.add_argument(
        "--asset-dir",
        help="Directory for copied images. Default: images/slug.",
    )
    parser.add_argument(
        "--replace-front-matter",
        action="store_true",
        help="Replace existing front matter instead of preserving it.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite output file if it already exists.",
    )
    parser.add_argument(
        "--repo-root",
        default=str(repo_root),
        help="Repository root. Defaults to this script's parent repository.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    try:
        convert(args)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
