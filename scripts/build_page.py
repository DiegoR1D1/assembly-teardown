"""Build the Outlier Check page: embed Reel covers as data URIs and fill the template.

Usage: python build_page.py data.json [out.html]
"""

from __future__ import annotations

import base64
import io
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

TEMPLATE = Path(__file__).resolve().parent.parent / "assets" / "template.html"
PLACEHOLDER = "/*__DATA__*/null"
THUMB_WIDTH = 240
TIMEOUT_S = 15


def fetch(url: str) -> bytes | None:
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT_S) as resp:
            return resp.read()
    except (urllib.error.URLError, TimeoutError, ValueError) as err:
        print(f"thumb failed: {url} ({err})", file=sys.stderr)
        return None


def shrink(raw: bytes) -> bytes:
    try:
        from PIL import Image
    except ImportError:
        return raw
    try:
        img = Image.open(io.BytesIO(raw)).convert("RGB")
    except OSError as err:
        print(f"thumb unreadable ({err}); embedding as is", file=sys.stderr)
        return raw
    if img.width > THUMB_WIDTH:
        img = img.resize((THUMB_WIDTH, round(img.height * THUMB_WIDTH / img.width)))
    out = io.BytesIO()
    img.save(out, "JPEG", quality=72, optimize=True)
    return out.getvalue()


def embed(node: object, cache: dict[str, str | None], stats: dict[str, int]) -> object:
    if isinstance(node, dict):
        for key, value in node.items():
            if key in ("thumb", "avatar") and isinstance(value, str) and value.startswith("http"):
                if value not in cache:
                    raw = fetch(value)
                    cache[value] = None if raw is None else "data:image/jpeg;base64," + base64.b64encode(shrink(raw)).decode()
                    stats["ok" if raw else "failed"] += 1
                node[key] = cache[value]
            else:
                embed(value, cache, stats)
    elif isinstance(node, list):
        for item in node:
            embed(item, cache, stats)
    return node


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("usage: build_page.py data.json [out.html]")
    data_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else data_path.with_name("outlier-check.html")
    data = json.loads(data_path.read_text())
    stats = {"ok": 0, "failed": 0}
    embed(data, {}, stats)
    template = TEMPLATE.read_text()
    if PLACEHOLDER not in template:
        sys.exit(f"template is missing {PLACEHOLDER}")
    payload = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    tmp = out_path.with_suffix(".tmp")
    tmp.write_text(template.replace(PLACEHOLDER, payload))
    tmp.replace(out_path)
    size_kb = out_path.stat().st_size // 1024
    print(f"wrote {out_path} ({size_kb} KB); covers embedded {stats['ok']}, failed {stats['failed']}")


if __name__ == "__main__":
    main()
