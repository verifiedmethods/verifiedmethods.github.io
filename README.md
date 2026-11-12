# verifiedmethods.github.io

Source of the verifiedmethods website, https://verifiedmethods.github.io.

## Build locally

The unit repositories must be sibling folders (for example `../ode-ivp`).

    uv run python tools/sync_units.py                       # copy unit material and the offline bundles
    uv run sphinx-build -W -b html docs docs/_build/html    # build
    uv run python tools/check_site.py                     # offline acceptance checks
    uv run python -m unittest discover -s tests -v          # deliberate-fault checks
    open docs/_build/html/index.html

`tools/sync_units.py` copies each unit's `tutorial/`, `briefs/` and
`supervisors/` into `docs/units/<unit>/`, builds the unit's offline bundle into
`extra/downloads/`, and writes the download box with the published check-suite
fingerprint. These generated files are not committed.

`extra/examples/a1-example-report.html` and `a2-example-report.html` are
verification reports produced from the maintainers' private reference code
with example details. Regenerate both when the check suite changes, using
`build_example_reports.py` in the private solutions repository. Only the
generated HTML belongs in this repository.

## Publishing

`.github/workflows/pages.yml` builds the site on every push to `main` (it
checks out pinned revisions of `verifiedmethods/ode-ivp` and
`verifiedmethods/linear-systems` alongside) and deploys it to GitHub Pages.
When publishing unit changes, update both `ref` values in that workflow to the
reviewed unit commits so the downloads, documentation, and example reports
describe the same check suites. Local builds use the sibling working trees.
In the repository settings, Pages must use "GitHub Actions" as its source.

Deployment stops if the acceptance checks or their regression tests fail. The
checker follows local links and anchors, checks referenced assets, verifies
student ZIP checksums and recomputes checker fingerprints from ZIP contents.
It also checks citation/report versions, complete reference summaries, embedded
plots, and the A1 walkthrough's version, tables and plot copies. These checks
detect inconsistent published material; they do not authenticate a release or
replace the units' numerical tests. External links are not fetched by this check.

For a build elsewhere, use `tools/check_site.py --build-dir PATH` and set
`VM_SITE_BUILD_DIR=PATH` when running the regression tests. If an example report
changes, review its walkthrough text and tables, and replace the two PNGs in
`docs/_static/` with the corresponding decoded plots from that report. The
acceptance check will reject stale copies. Keep the tagged pilot ZIPs unchanged.

Pages are written in MyST Markdown, with Furo as the theme (chosen for small
pages on slow connections).

## Pilot checklist

`tools/pilot_checklist.json` is the shared source for the web checklist and
its printable PDF. After editing it, regenerate and inspect both outputs:

    uv run --with reportlab python tools/build_pilot_checklist.py

Commit `docs/pilot-checklist.md` and `extra/handouts/lecturer-pilot-checklist.pdf`
alongside the source and generator. The PDF is a static printable checklist,
not an upload form. Completed feedback is returned by email.
