"""Copy each unit's tutorial, briefs and supervisor material into the site, and
its offline bundle into extra/downloads/.

    uv run python tools/sync_units.py

Unit sources are sibling folders by default (../ode-ivp). In CI, set
VM_UNIT_SRC_ODE_IVP to the checkout path.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOWNLOADS = ROOT / "extra" / "downloads"

UNITS = {
    "ode-ivp": {"code": "A1", "title": "ODE initial value problems"},
    "linear-systems": {"code": "A2", "title": "Iterative methods for linear systems"},
}
SECTIONS = {"tutorial": "Tutorial", "briefs": "Project briefs", "supervisors": "For supervisors"}


def unit_source(slug: str) -> Path:
    env = os.environ.get("VM_UNIT_SRC_" + slug.upper().replace("-", "_"))
    return Path(env).resolve() if env else (ROOT.parent / slug).resolve()


def unit_version(src: Path) -> str:
    text = (src / "vm" / "__init__.py").read_text(encoding="utf-8")
    return re.search(r'__version__\s*=\s*"([^"]+)"', text).group(1)


def copy_section(src: Path, dst: Path, title: str):
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)
    readme = (src / "README.md").read_text(encoding="utf-8") if (src / "README.md").exists() else f"# {title}\n"
    files = sorted(p for p in src.glob("*.md") if p.name != "README.md")
    listed = [n for n in dict.fromkeys(re.findall(r"\]\(([^)/]+\.md)\)", readme)) if (src / n).exists()]
    pages = [src / n for n in listed] + [p for p in files if p.name not in listed]  # README order first
    for p in pages:
        shutil.copy2(p, dst / p.name)
    index = readme
    index = re.sub(r"\A# .*", f"# {title}", index, count=1)  # short title: the page sits under its unit in the menu
    toc = "\n".join(p.stem for p in pages)
    index += f"\n```{{toctree}}\n:hidden:\n\n{toc}\n```\n"
    (dst / "index.md").write_text(index, encoding="utf-8")


def human_size(n: int) -> str:
    return f"{n / 1024:.0f} KB"


def main() -> int:
    DOWNLOADS.mkdir(parents=True, exist_ok=True)
    for slug, meta in UNITS.items():
        src = unit_source(slug)
        version = unit_version(src)
        subprocess.run([sys.executable, str(src / "tools" / "build_bundle.py")], cwd=src, check=True,
                       stdout=subprocess.DEVNULL)
        dist = src / "dist"
        zip_name = f"verifiedmethods-{slug}-{version}.zip"
        shutil.copy2(dist / zip_name, DOWNLOADS / zip_name)
        sums = dict(line.split()[::-1] for line in (dist / "SHA256SUMS").read_text().splitlines() if line.strip())
        fingerprint = (dist / "check-suite-fingerprint.txt").read_text().split()[1]

        unit_dir = DOCS / "units" / slug
        for section, title in SECTIONS.items():
            copy_section(src / section, unit_dir / section, title)

        size = human_size((DOWNLOADS / zip_name).stat().st_size)
        (unit_dir / "_download.md").write_text(
            f'<a class="vm-button" href="../../downloads/{zip_name}">Download unit {meta["code"]} '
            f"(version {version}, {size})</a>\n\n"
            f"| | |\n|---|---|\n"
            f"| Version | {version} |\n"
            f"| File | `{zip_name}` |\n"
            f"| SHA-256 of the zip | <span class=\"vm-fingerprint\">{sums[zip_name]}</span> |\n"
            f"| Check-suite fingerprint | <span class=\"vm-fingerprint\">{fingerprint}</span> |\n",
            encoding="utf-8",
        )
        print(f"{slug}: version {version}, {zip_name} ({size}), fingerprint {fingerprint[:16]}...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
