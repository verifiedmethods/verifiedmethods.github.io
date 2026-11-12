"""Acceptance-check regression tests using deliberate faults in a built site.

Build the site first. Set VM_SITE_BUILD_DIR to test a nondefault build folder.
No downloads, private implementations or additional test packages are needed.
"""

import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from check_site import Result, check_links, validate_site

BUILD = Path(os.environ.get("VM_SITE_BUILD_DIR", ROOT / "docs/_build/html"))


class LinkChecks(unittest.TestCase):
    def test_encoded_anchor_query_and_directory_index_work_offline(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder).resolve()
            (root / "chapter").mkdir()
            (root / "chapter/index.html").write_text('<h1 id="a b">Chapter</h1>')
            (root / "index.html").write_text(
                '<a href="chapter/?from=home#a%20b">Chapter</a>'
                '<a href="https://verifiedmethods.github.io/chapter/#a%20b">Same site</a>'
                '<a href="https://example.invalid/not-requested">External</a>'
                '<img src="data:image/png;base64,ignored">')
            result = Result()
            check_links(root, result)
            self.assertEqual(result.errors, [])
            self.assertEqual(result.references, 2)

    def test_empty_build_is_not_a_pass(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertTrue(validate_site(folder).errors)


class BuiltSiteChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (BUILD / "a1-report-walkthrough.html").is_file():
            raise RuntimeError("Build the current website before running acceptance-check tests")

    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.root = Path(self.folder.name) / "site"
        shutil.copytree(BUILD, self.root)

    def assert_problem(self, phrase):
        errors = validate_site(self.root).errors
        self.assertTrue(any(phrase in error for error in errors), errors)

    def append_html(self, html):
        with (self.root / "index.html").open("a") as output:
            output.write(html)

    def change_report(self, edit):
        path = self.root / "examples/a1-example-report.html"
        path.write_text(edit(path.read_text()))

    def a1_manifest(self):
        page = (self.root / "units/ode-ivp/index.html").read_text()
        path = next(path for path in (self.root / "downloads").glob("verifiedmethods-ode-ivp-*-manifest.json")
                    if path.name in page)
        return path, json.loads(path.read_text())

    def test_current_build_passes(self):
        self.assertEqual(validate_site(self.root).errors, [])

    def test_missing_page_is_rejected(self):
        self.append_html('<a href="missing.html">Missing</a>')
        self.assert_problem("Missing local target")

    def test_missing_anchor_is_rejected(self):
        self.append_html('<a href="index.html#missing-anchor">Missing</a>')
        self.assert_problem("Missing anchor")

    def test_missing_asset_is_rejected(self):
        self.append_html('<img src="_static/missing.png">')
        self.assert_problem("Missing local target")

    def test_link_outside_public_build_is_rejected(self):
        self.append_html('<a href="../outside.txt">Outside</a>')
        self.assert_problem("Link leaves built site")

    def test_changed_download_is_rejected(self):
        _, manifest = self.a1_manifest()
        archive = self.root / "downloads" / next(name for name in manifest["files"] if name.startswith("verifiedmethods-"))
        with archive.open("ab") as output:
            output.write(b"accidental modification")
        self.assert_problem("download checksum differs")

    def test_changed_report_fingerprint_is_rejected(self):
        _, manifest = self.a1_manifest()
        self.change_report(lambda text: text.replace(manifest["check_suite_fingerprint"], "0" * 64))
        self.assert_problem("example report checker fingerprint differs")

    def test_changed_report_version_is_rejected(self):
        _, manifest = self.a1_manifest()
        self.change_report(lambda text: text.replace(manifest["version"], "999.0.0"))
        self.assert_problem("example report unit/version differs")

    def test_incomplete_example_is_rejected(self):
        self.change_report(lambda text: text.replace(">PASS</span>", ">FAIL</span>", 1))
        self.assert_problem("three complete passing methods")

    def test_missing_report_plot_is_rejected(self):
        self.change_report(lambda text: re.sub(r"<img\b[^>]*data:image/png;base64,[^>]*>", "", text, count=1))
        self.assert_problem("must contain two embedded plots")

    def test_stale_walkthrough_plot_is_rejected(self):
        (self.root / "_static/a1-example-cost.png").write_bytes(b"old plot")
        self.assert_problem("stale plot")

    def test_stale_rendered_plot_is_rejected_even_when_full_size_copy_matches(self):
        (self.root / "_images/a1-example-cost.png").write_bytes(b"stale rendered plot")
        self.assert_problem("stale displayed plot")

    def test_stale_walkthrough_numbers_are_rejected(self):
        path = self.root / "a1-report-walkthrough.html"
        path.write_text(path.read_text().replace("0.977", "0.123"))
        self.assert_problem("summary numbers differ")

    def test_stale_walkthrough_version_is_rejected(self):
        path = self.root / "a1-report-walkthrough.html"
        text = path.read_text()
        text = re.sub(r'(id="a1-example-version">)[^<]+', r'\g<1>999.0.0', text)
        path.write_text(text)
        self.assert_problem("walkthrough: example version is stale")

    def test_changed_checker_is_rejected_after_outer_checksum_is_updated(self):
        path, manifest = self.a1_manifest()
        name = next(name for name in manifest["files"] if name.startswith("verifiedmethods-"))
        archive = self.root / "downloads" / name
        with zipfile.ZipFile(archive) as original:
            contents = {name: original.read(name) for name in original.namelist()}
        runner = next(name for name in contents if name.endswith("/vm/runner.py"))
        contents[runner] += b"\n# changed checker\n"
        with zipfile.ZipFile(archive, "w") as output:
            for member, data in contents.items():
                output.writestr(member, data)
        old = manifest["files"][name]["sha256"]
        new = hashlib.sha256(archive.read_bytes()).hexdigest()
        manifest["files"][name]["sha256"] = new
        path.write_text(json.dumps(manifest))
        unit_page = self.root / "units/ode-ivp/index.html"
        unit_page.write_text(unit_page.read_text().replace(old, new))
        self.assert_problem("archive checker fingerprint differs")

    def test_missing_manifest_is_rejected(self):
        path, _ = self.a1_manifest()
        path.unlink()
        self.assert_problem("must link exactly one current manifest")

    def test_private_file_is_rejected_even_with_updated_download_checksum(self):
        path, manifest = self.a1_manifest()
        name = next(name for name in manifest["files"] if name.startswith("verifiedmethods-"))
        archive = self.root / "downloads" / name
        with zipfile.ZipFile(archive, "a") as output:
            output.writestr(name.removesuffix(".zip") + "/reference.py", "# must not ship\n")
        manifest["files"][name]["sha256"] = hashlib.sha256(archive.read_bytes()).hexdigest()
        path.write_text(json.dumps(manifest))
        self.assert_problem("private or maintainer file")


if __name__ == "__main__":
    unittest.main()
