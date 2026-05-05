from __future__ import annotations

import argparse
import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "the-truman-show" / "article.md"
DEFAULT_OUTPUT = ROOT / "the-truman-show" / "preview-ocean-calm-safe.html"


P_STYLE = (
    "font-size:16px;line-height:1.88;color:#263241;margin:0 0 18px;"
    "text-align:justify;word-break:break-word;"
)
CAPTION_STYLE = (
    "font-size:14px;line-height:1.72;color:#5e7185;margin:4px 0 18px;"
    "text-align:center;word-break:break-word;"
)
STRONG_STYLE = "color:#2f6585;font-weight:700;"
CODE_STYLE = (
    "background-color:#eef5fa;color:#2f6585;padding:2px 5px;"
    "border-radius:4px;font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;"
)


def parse_frontmatter(markdown: str) -> tuple[dict[str, str], str]:
    if not markdown.startswith("---\n"):
        return {}, markdown
    end = markdown.find("\n---", 4)
    if end == -1:
        return {}, markdown

    raw_meta = markdown[4:end].strip()
    body = markdown[end + 4 :].lstrip()
    metadata: dict[str, str] = {}
    for line in raw_meta.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"')
    return metadata, body


def inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(
        r"`(.+?)`",
        rf'<code style="{CODE_STYLE}">\1</code>',
        escaped,
    )
    escaped = re.sub(
        r"\*\*(.+?)\*\*",
        rf'<strong style="{STRONG_STYLE}">\1</strong>',
        escaped,
    )
    return escaped


def render_image(alt: str, src: str) -> str:
    caption = html.escape(alt)
    return (
        '<section style="margin:24px 0 20px;padding:0;">'
        f'<img src="{html.escape(src, quote=True)}" '
        f'alt="{caption}" '
        'style="display:block;width:100%;max-width:100%;height:auto;'
        'border-radius:6px;border:1px solid rgba(79,131,166,0.18);'
        'box-shadow:none;box-sizing:border-box;" />'
        f'<p style="{CAPTION_STYLE}"><span style="color:#5e7185;">{caption}</span></p>'
        "</section>"
    )


def render_markdown(markdown: str) -> str:
    blocks: list[str] = []
    for raw_line in markdown.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        image = re.fullmatch(r"!\[(.*?)\]\((.*?)\)", line)
        if image:
            blocks.append(render_image(*image.groups()))
            continue

        if line.startswith("## "):
            title = html.escape(line[3:].strip())
            blocks.append(
                '<h2 style="font-size:20px;line-height:1.45;color:#2f6585;'
                'margin:34px 0 16px;padding-bottom:0;">'
                '<span style="color:#4f83a6;">◆</span>'
                f'<span style="color:#2f6585;margin-left:8px;">{title}</span>'
                "</h2>"
            )
            continue

        if line.startswith("### "):
            title = html.escape(line[4:].strip())
            blocks.append(
                '<h3 style="font-size:17px;line-height:1.5;color:#2f6585;'
                'margin:26px 0 12px;border-left:3px solid #4f83a6;'
                f'padding-left:10px;">{title}</h3>'
            )
            continue

        strong_only = re.fullmatch(r"\*\*(.+?)\*\*", line)
        if strong_only:
            blocks.append(
                '<p style="font-size:14px;line-height:1.72;color:#5e7185;'
                'margin:10px 0 14px;text-align:center;word-break:break-word;">'
                f'<strong style="{STRONG_STYLE}">{html.escape(strong_only.group(1))}</strong>'
                "</p>"
            )
            continue

        italic = re.fullmatch(r"\*(.+?)\*", line)
        if italic:
            blocks.append(
                f'<p style="{CAPTION_STYLE}">'
                f'<span style="color:#5e7185;">{html.escape(italic.group(1))}</span>'
                "</p>"
            )
            continue

        blocks.append(f'<p style="{P_STYLE}">{inline_markdown(line)}</p>')

    return "\n".join(blocks)


def render_title(title: str) -> str:
    return (
        '<section style="margin:0 0 28px;padding:0;">'
        '<h1 style="font-size:24px;line-height:1.36;color:#2f6585;'
        'margin:0;font-weight:700;">'
        f'<span style="color:#2f6585;">{html.escape(title)}</span>'
        "</h1>"
        "</section>"
    )


def build_document(markdown: str, title_override: str | None = None) -> str:
    metadata, body_markdown = parse_frontmatter(markdown)
    title = title_override or metadata.get("title", "Ocean Calm Safe Preview")
    body = render_title(title) + "\n" + render_markdown(body_markdown)

    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{html.escape(title)}</title>
</head>
<body style="margin:0;">
  <div style="background-color:#f7fafc;padding:28px 10px;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,'PingFang SC','Hiragino Sans GB','Microsoft YaHei',sans-serif;letter-spacing:0;box-sizing:border-box;min-height:100vh;">
    <section style="max-width:760px;width:100%;box-sizing:border-box;margin:0 auto;padding:22px 20px 24px;background-color:#ffffff;border:1px solid rgba(79,131,166,0.14);border-radius:8px;">
{body}
    </section>
  </div>
</body>
</html>
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", nargs="?", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--title")
    args = parser.parse_args()

    markdown = args.source.read_text(encoding="utf-8")
    document = build_document(markdown, args.title)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(document, encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
