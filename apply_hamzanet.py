from __future__ import annotations

import re
import sys
from pathlib import Path

CLIENT_NAME = "HamzaNet Client"
WATERMARK = "HamzaNet v0.1"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="")


def patch_version(repo: Path) -> bool:
    path = repo / "src/game/version.h"
    if not path.exists():
        print(f"[skip] version.h not found: {path}")
        return False

    text = read_text(path)
    old = text
    text = re.sub(r'#define\s+GAME_NAME\s+"[^"]+"', f'#define GAME_NAME "{CLIENT_NAME}"', text)

    if text != old:
        write_text(path, text)
        print("[ok] Patched GAME_NAME in src/game/version.h")
        return True
    print("[skip] GAME_NAME pattern not found or already patched")
    return False


def patch_timer(repo: Path) -> bool:
    path = repo / "src/game/client/components/hud.cpp"
    if not path.exists():
        print(f"[skip] hud.cpp not found: {path}")
        return False

    text = read_text(path)
    old = text

    # Only patch the first timer font occurrence inside RenderGameTimer area.
    text = text.replace("\tfloat FontSize = 10.0f;", "\tfloat FontSize = 14.0f;", 1)
    text = text.replace("TextRender()->Text(Half - w / 2, 2, FontSize, aBuf, -1.0f);", "TextRender()->Text(Half - w / 2, 4.0f, FontSize, aBuf, -1.0f);", 1)

    if text != old:
        write_text(path, text)
        print("[ok] Patched bigger center timer in hud.cpp")
        return True
    print("[skip] Timer pattern not found or already patched")
    return False


def patch_watermark(repo: Path) -> bool:
    path = repo / "src/game/client/components/hud.cpp"
    if not path.exists():
        print(f"[skip] hud.cpp not found: {path}")
        return False

    text = read_text(path)
    if WATERMARK in text:
        print("[skip] Watermark already present")
        return False

    overlay = f'''
\n\t// HamzaNet custom clean HUD overlay - visual only, no gameplay changes.
\tTextRender()->TextColor(0.45f, 0.85f, 1.0f, 1.0f);
\tTextRender()->Text(5.0f, 18.0f, 10.0f, "{WATERMARK}", -1.0f);
\tTextRender()->TextColor(TextRender()->DefaultTextColor());
'''

    pattern = r"(void\s+CHud::RenderTextInfo\s*\(\s*\)\s*\{)(.*?)(\n\}\s*\n\s*void\s+CHud::RenderConnectionWarning)"
    match = re.search(pattern, text, flags=re.DOTALL)
    if not match:
        print("[skip] RenderTextInfo pattern not found; watermark not injected")
        return False

    new_text = text[: match.start()] + match.group(1) + match.group(2) + overlay + match.group(3) + text[match.end() :]
    write_text(path, new_text)
    print("[ok] Added HamzaNet HUD watermark to RenderTextInfo")
    return True


def write_build_marker(repo: Path) -> None:
    marker = repo / "HAMZANET_CHANGES.txt"
    marker.write_text(
        "HamzaNet DDNet Custom Client v0.1\n"
        "Changes: GAME_NAME branding, bigger HUD timer, top-left HUD watermark.\n"
        "No cheat / no movement / no protocol / no bypass changes.\n",
        encoding="utf-8",
    )
    print("[ok] Wrote HAMZANET_CHANGES.txt")


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python apply_hamzanet.py <path-to-ddnet-repo>")
        return 2

    repo = Path(sys.argv[1]).resolve()
    if not repo.exists():
        print(f"DDNet repo path does not exist: {repo}")
        return 2

    print(f"Applying HamzaNet patch to: {repo}")
    patched = [patch_version(repo), patch_timer(repo), patch_watermark(repo)]
    write_build_marker(repo)

    print("Patch summary:", sum(1 for item in patched if item), "main changes applied")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
