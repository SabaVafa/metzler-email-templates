"""
Audit each template's hero td to find the visual bottom padding asymmetry.

For each template:
1. Find the <td class="hero" ...> opening
2. Find the closing </td> of the hero
3. Inside, find the LAST <td style="padding:..."> before the closing
4. Extract the bottom padding of that last inner row
5. Compute correct hero pad-bottom = 36 - bottom_inner_padding for visual symmetry

Outputs a table of: template, last-inner-bottom, current-hero-pad-bottom, target-hero-pad-bottom, delta.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "templates"

HERO_OPEN_RE = re.compile(r'<td class="hero"[^>]*?>')
PADDING_RE = re.compile(r'padding:\s*(\d+)px(?:\s+(\d+)px)?(?:\s+(\d+)px)?(?:\s+(\d+)px)?')
INLINE_PAD_BOTTOM_RE = re.compile(r'padding-bottom:\s*(\d+)px')


def parse_padding(style_value: str):
    """Extract (top, right, bottom, left) from a padding shorthand."""
    m = PADDING_RE.search(style_value)
    if not m:
        return None
    t = int(m.group(1))
    r = int(m.group(2)) if m.group(2) else t
    b = int(m.group(3)) if m.group(3) else t
    l = int(m.group(4)) if m.group(4) else r
    return (t, r, b, l)


def find_hero_block(html: str):
    """Return (hero_open_match, hero_close_offset) or None."""
    m = HERO_OPEN_RE.search(html)
    if not m:
        return None
    # Find matching </td> by counting nested <td>...</td>
    start = m.end()
    depth = 1
    i = start
    while i < len(html):
        next_open = html.find('<td', i)
        next_close = html.find('</td>', i)
        if next_close == -1:
            return None
        if next_open != -1 and next_open < next_close:
            depth += 1
            i = next_open + 3
        else:
            depth -= 1
            if depth == 0:
                return (m, next_close)
            i = next_close + 5
    return None


def find_last_inner_row(hero_inner: str):
    """Find the last <td style="padding:..."> inside the hero block, return its bottom-padding."""
    # Find all <td style="..."> occurrences with padding
    matches = list(re.finditer(r'<td[^>]*style="([^"]*padding[^"]*)"', hero_inner))
    if not matches:
        return None, None
    last = matches[-1]
    pad = parse_padding(last.group(1))
    if pad:
        return pad[2], last.group(0)[:80]
    return None, None


def get_hero_pad_bottom(hero_open_tag: str):
    """Returns the current hero pad-bottom: inline override if any, else default 36."""
    inline = INLINE_PAD_BOTTOM_RE.search(hero_open_tag)
    if inline:
        return int(inline.group(1))
    return 36  # default from .hero class


def main():
    files = sorted(p for p in TEMPLATES_DIR.glob("*.html") if p.name != "theme-preview.html")
    print(f"{'Template':<42} {'inner-pb':>9} {'hero-pb':>9} {'target':>7} {'delta':>6}")
    print("-" * 80)
    for path in files:
        html = path.read_text(encoding="utf-8")
        block = find_hero_block(html)
        if not block:
            print(f"{path.name:<42} (no hero td)")
            continue
        hero_open_match, hero_close = block
        hero_open_tag = hero_open_match.group(0)
        hero_inner = html[hero_open_match.end():hero_close]
        inner_pb, _sample = find_last_inner_row(hero_inner)
        current_pb = get_hero_pad_bottom(hero_open_tag)
        if inner_pb is None:
            print(f"{path.name:<42} (no inner padding td)")
            continue
        target = max(0, 36 - inner_pb)
        delta = current_pb - target
        mark = "  OK" if delta == 0 else f" {'+' if delta > 0 else ''}{delta}px"
        print(f"{path.name:<42} {inner_pb:>7}px  {current_pb:>7}px  {target:>5}px  {mark:>6}")


if __name__ == "__main__":
    main()
