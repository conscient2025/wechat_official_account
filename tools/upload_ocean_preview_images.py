from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ARTICLE_DIR = ROOT / "the-truman-show"
DEFAULT_INPUT_HTML = DEFAULT_ARTICLE_DIR / "preview-ocean-calm-safe.html"
DEFAULT_OUTPUT_HTML = DEFAULT_ARTICLE_DIR / "preview-ocean-calm-safe.wechat.html"
DEFAULT_MAP_FILE = DEFAULT_ARTICLE_DIR / "preview-ocean-calm-safe.image-map.json"
CLI = Path(r"C:\Users\33941\AppData\Roaming\npm\md2wechat.cmd")


def upload_image(path: Path) -> dict[str, str]:
    result = subprocess.run(
        [str(CLI), "upload_image", str(path), "--json"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stdout or result.stderr)
    payload = json.loads(result.stdout)
    if not payload.get("success"):
        raise RuntimeError(json.dumps(payload, ensure_ascii=False, indent=2))
    data = payload["data"]
    return {
        "media_id": data.get("media_id", ""),
        "wechat_url": data.get("wechat_url", ""),
    }


def local_image_sources(html: str) -> list[str]:
    srcs = re.findall(r'<img\s+[^>]*src="([^"]+)"', html)
    local_srcs: list[str] = []
    for src in srcs:
        if src.startswith(("http://", "https://", "data:")):
            continue
        if src not in local_srcs:
            local_srcs.append(src)
    return local_srcs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--article-dir", type=Path, default=DEFAULT_ARTICLE_DIR)
    parser.add_argument("--input-html", type=Path, default=DEFAULT_INPUT_HTML)
    parser.add_argument("--output-html", type=Path, default=DEFAULT_OUTPUT_HTML)
    parser.add_argument("--map-file", type=Path, default=DEFAULT_MAP_FILE)
    parser.add_argument(
        "--replace-local",
        action="append",
        default=[],
        help="Local source replacement before upload, formatted old=new.",
    )
    args = parser.parse_args()

    article_dir = args.article_dir.resolve()
    html = args.input_html.read_text(encoding="utf-8")

    source_aliases: dict[str, str] = {}
    for item in args.replace_local:
        if "=" not in item:
            raise ValueError(f"Invalid --replace-local value: {item}")
        old, new = item.split("=", 1)
        source_aliases[old] = new
        html = html.replace(f'src="{old}"', f'src="{new}"')

    existing: dict[str, dict[str, str]] = {}
    existing_aliases: dict[str, str] = {}
    if args.map_file.exists():
        raw_existing = json.loads(args.map_file.read_text(encoding="utf-8"))
        if "images" in raw_existing:
            existing = raw_existing.get("images", {})
            existing_aliases = raw_existing.get("source_aliases", {})
        else:
            existing = raw_existing

    image_map = dict(existing)
    for src in local_image_sources(html):
        if src in image_map and image_map[src].get("wechat_url"):
            continue
        image_path = (article_dir / src).resolve()
        if not str(image_path).startswith(str(article_dir)):
            raise ValueError(f"Image path escapes article directory: {src}")
        image_map[src] = upload_image(image_path)
        args.map_file.write_text(
            json.dumps(image_map, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"uploaded {src}")

    rewritten = html
    for src, data in image_map.items():
        wechat_url = data.get("wechat_url", "")
        if wechat_url:
            rewritten = rewritten.replace(f'src="{src}"', f'src="{wechat_url}"')

    args.output_html.write_text(rewritten, encoding="utf-8")
    args.map_file.write_text(
        json.dumps(
            {"source_aliases": {**existing_aliases, **source_aliases}, "images": image_map},
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    print(args.output_html)


if __name__ == "__main__":
    main()
