"""Offline acceptance checks for the built website, downloads and examples.

    python tools/check_site.py --build-dir docs/_build/html

Checks consistency of the supplied evidence; it does not authenticate a release
or establish numerical correctness. Run after unit synchronisation and Sphinx.
"""

from __future__ import annotations

import argparse
import ast
import base64
from dataclasses import dataclass, field
import hashlib
from html.parser import HTMLParser
import json
from pathlib import Path, PurePosixPath
import re
from urllib.parse import unquote, urlsplit
import zipfile

from sync_units import UNITS

ROOT = Path(__file__).resolve().parents[1]


def normalise(text):
    return " ".join(text.split())


class Page(HTMLParser):
    """Read links and the report's visible metadata/tables without executing JS."""

    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids, self.references, self.images = set(), [], []
        self.metadata, self.tables, self.marked_text = {}, [], {}
        self.subtitle = ""
        self._capture, self._data, self._key = None, [], None
        self._table = self._row = self._cell = None
        self._mark = None
        self._mark_data = []
        self.feed(text)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.ids.add(attrs["name"])
        self.references.extend(attrs[key] for key in ("href", "src") if attrs.get(key))
        if tag == "img":
            self.images.append(attrs)
        if tag in ("dt", "dd") or (tag == "p" and "sub" in attrs.get("class", "").split()):
            self._capture, self._data = tag, []
        if tag == "span" and attrs.get("id") == "a1-example-version":
            self._mark, self._mark_data = tag, []
        if tag == "table":
            self._table = []
        elif tag == "tr" and self._table is not None:
            self._row = []
        elif tag in ("th", "td") and self._row is not None:
            self._cell = []

    def handle_data(self, data):
        if self._capture:
            self._data.append(data)
        if self._cell is not None:
            self._cell.append(data)
        if self._mark:
            self._mark_data.append(data)

    def handle_endtag(self, tag):
        if tag == self._capture:
            text = normalise(" ".join(self._data))
            if tag == "dt":
                self._key = text
            elif tag == "dd" and self._key:
                self.metadata[self._key] = text
            elif tag == "p":
                self.subtitle = text
            self._capture = None
        if tag == self._mark:
            self.marked_text["a1-example-version"] = normalise(" ".join(self._mark_data))
            self._mark = None
        if tag in ("th", "td") and self._cell is not None:
            self._row.append(normalise(" ".join(self._cell)))
            self._cell = None
        elif tag == "tr" and self._row is not None:
            self._table.append(self._row)
            self._row = None
        elif tag == "table" and self._table is not None:
            self.tables.append(self._table)
            self._table = None


@dataclass
class Result:
    pages: int = 0
    references: int = 0
    units: int = 0
    errors: list[str] = field(default_factory=list)


def check_links(root: Path, result: Result):
    pages = {p.resolve(): Page(p.read_text(encoding="utf-8")) for p in root.rglob("*.html")}
    result.pages = len(pages)
    if not pages:
        result.errors.append("No HTML pages found; build the website first.")
    for path, page in pages.items():
        for reference in page.references:
            url = urlsplit(reference)
            same_site = url.netloc.lower() == "verifiedmethods.github.io" and url.scheme in ("", "http", "https")
            if (url.scheme or url.netloc) and not same_site:
                continue
            result.references += 1
            url_path = (url.path or "/") if same_site else url.path
            target = (root / unquote(url_path.lstrip("/")) if url_path.startswith("/")
                      else path.parent / unquote(url_path) if url_path else path).resolve()
            label = f"{path.relative_to(root)}: {reference}"
            if not target.is_relative_to(root):
                result.errors.append(f"Link leaves built site: {label}")
                continue
            if target.is_dir():
                target /= "index.html"
            if not target.exists():
                result.errors.append(f"Missing local target: {label}")
            elif url.fragment and target in pages and unquote(url.fragment) not in pages[target].ids:
                result.errors.append(f"Missing anchor: {label}")
    return pages


def suite_fingerprint(archive, prefix):
    """Recompute the documented checker identifier directly from ZIP bytes."""
    files = sorted(name for name in archive.namelist()
                   if name.startswith(prefix + "/vm/") and name.endswith(".py")
                   and "/" not in name[len(prefix + "/vm/"):])
    if not files:
        raise ValueError("archive has no checker Python files")
    files += [prefix + "/vm/expected.json", prefix + "/verify.py"]
    digest = hashlib.sha256()
    for name in files:
        checksum = hashlib.sha256(archive.read(name).replace(b"\r\n", b"\n")).hexdigest()
        digest.update(PurePosixPath(name).name.encode() + b"\0" + checksum.encode() + b"\n")
    return digest.hexdigest()


def version_in_source(source):
    for node in ast.parse(source).body:
        if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "__version__"
                                                for target in node.targets):
            return ast.literal_eval(node.value)
    raise ValueError("archive has no __version__")


def report_images(page):
    images = []
    for image in page.images:
        source = image.get("src", "")
        if source.startswith("data:image/png;base64,"):
            data = base64.b64decode(source.partition(",")[2], validate=True)
            if not data.startswith(b"\x89PNG\r\n\x1a\n"):
                raise ValueError("report plot is not a PNG")
            images.append(data)
    return images


def check_unit(root, slug, code, pages, result):
    manifests = sorted((root / "downloads").glob(f"verifiedmethods-{slug}-*-manifest.json"))
    unit_path = (root / "units" / slug / "index.html").resolve()
    unit_text = unit_path.read_text()
    # Select the manifest actually linked from this unit page, not an old mirror.
    linked = [path for path in manifests if path.name in unit_text]
    if len(linked) != 1:
        raise ValueError("unit page must link exactly one current manifest")
    manifest = json.loads(linked[0].read_text())
    version, fingerprint = manifest["version"], manifest["check_suite_fingerprint"]
    if manifest["schema"] != 1 or manifest["slug"] != slug or manifest["unit"] != code:
        raise ValueError("manifest unit/schema mismatch")
    name = f"verifiedmethods-{slug}-{version}.zip"
    download = root / "downloads" / name
    checksum = hashlib.sha256(download.read_bytes()).hexdigest()
    if checksum != manifest["files"][name]["sha256"]:
        result.errors.append(f"{code}: download checksum differs from manifest")
    for value, label in ((checksum, "download checksum"), (fingerprint, "checker fingerprint"), (version, "version")):
        if value not in unit_text:
            result.errors.append(f"{code}: unit page is missing the current {label}")
    prefix = f"verifiedmethods-{slug}-{version}"
    with zipfile.ZipFile(download) as archive:
        for path in archive.namelist():
            parts = PurePosixPath(path).parts
            if not parts or parts[0] != prefix or ".." in parts:
                result.errors.append(f"{code}: unexpected archive path: {path}")
            if any(part.lower() in {"solutions", "tests", ".git", ".venv", "__pycache__", "reference.py"}
                   for part in parts):
                result.errors.append(f"{code}: private or maintainer file in student archive: {path}")
        if suite_fingerprint(archive, prefix) != fingerprint:
            result.errors.append(f"{code}: archive checker fingerprint differs from manifest")
        if version_in_source(archive.read(prefix + "/vm/__init__.py")) != version:
            result.errors.append(f"{code}: archive version differs from manifest")
        citation = archive.read(prefix + "/CITATION.cff").decode()
        match = re.search(r'^version:\s*[\"\']?([^\s\"\']+)', citation, re.MULTILINE)
        if not match or match[1] != version:
            result.errors.append(f"{code}: citation version differs from manifest")
    report = pages[(root / "examples" / f"{code.lower()}-example-report.html").resolve()]
    reported = re.findall(r"\b[0-9a-f]{64}\b", report.metadata.get("Check-suite fingerprint", ""))
    if reported != [fingerprint]:
        result.errors.append(f"{code}: example report checker fingerprint differs from manifest")
    if f"Unit {code}:" not in report.subtitle or not re.search(r"\bversion\s+" + re.escape(version) + r"(?:\s|$)", report.subtitle):
        result.errors.append(f"{code}: example report unit/version differs from manifest")
    summary = report.tables[0]
    if len(summary) != 4 or any(row[1] != "PASS" or row[2].replace(" ", "") != "4/4" for row in summary[1:]):
        result.errors.append(f"{code}: example must show three complete passing methods")
    if len(report_images(report)) != 2:
        result.errors.append(f"{code}: example report must contain two embedded plots")
    result.units += 1
    return version, report


def check_walkthrough(root, version, report, pages, result):
    guide = pages[(root / "a1-report-walkthrough.html").resolve()]
    if guide.marked_text.get("a1-example-version") != version:
        result.errors.append("A1 walkthrough: example version is stale")
    expected = [[row[0].rsplit(" ", 1)[0], row[2], row[3], row[4]] for row in report.tables[0][1:]]
    actual = guide.tables[0][1:]
    compact = lambda rows: [[value.replace(" ", "") for value in row] for row in rows]
    if compact(actual) != compact(expected):
        result.errors.append("A1 walkthrough: summary numbers differ from example report")
    errors = next(table for table in report.tables if "P2 error" in table[0])
    source = {row[0]: row[errors[0].index("P2 error")] for row in errors[1:]}
    for row in guide.tables[1][1:]:
        if row[0] not in source or float(row[2]) != float(source[row[0]]):
            result.errors.append("A1 walkthrough: Euler error-table numbers differ from example report")
    images = report_images(report)
    displayed = {PurePosixPath(urlsplit(image.get("src", "")).path).name: image.get("src", "")
                 for image in guide.images}
    for filename, image in zip(("a1-example-convergence.png", "a1-example-cost.png"), images):
        if (root / "_static" / filename).read_bytes() != image:
            result.errors.append(f"A1 walkthrough: stale plot {filename}")
        if filename not in displayed:
            result.errors.append(f"A1 walkthrough: missing displayed plot {filename}")
            continue
        target = (root / unquote(urlsplit(displayed[filename]).path).lstrip("/")).resolve()
        if not target.is_relative_to(root) or target.read_bytes() != image:
            result.errors.append(f"A1 walkthrough: stale displayed plot {filename}")


def validate_site(root):
    root = Path(root).resolve()
    result = Result()
    pages = check_links(root, result)
    if not pages:
        return result
    for slug, unit in UNITS.items():
        try:
            version, report = check_unit(root, slug, unit["code"], pages, result)
            if unit["code"] == "A1":
                check_walkthrough(root, version, report, pages, result)
        except (OSError, ValueError, KeyError, TypeError, IndexError, StopIteration,
                SyntaxError, zipfile.BadZipFile) as error:
            result.errors.append(f"{unit['code']}: invalid or missing release/example data: {error}")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build-dir", type=Path, default=ROOT / "docs/_build/html")
    args = parser.parse_args()
    result = validate_site(args.build_dir)
    if result.errors:
        for error in result.errors:
            print("FAIL:", error)
        return 1
    print(f"PASS: {result.pages} HTML pages, {result.references} local links/resources/anchors, "
          f"{result.units} unit downloads/examples and the A1 walkthrough")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
