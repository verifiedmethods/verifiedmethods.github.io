# verifiedmethods.github.io

Source of the verifiedmethods website, https://verifiedmethods.github.io.

## Build locally

The unit repositories must be sibling folders (for example `../ode-ivp`).

    uv run python tools/sync_units.py                       # copy unit material and the offline bundles
    uv run sphinx-build -W -b html docs docs/_build/html    # build
    open docs/_build/html/index.html

`tools/sync_units.py` copies each unit's `tutorial/`, `briefs/` and
`supervisors/` into `docs/units/<unit>/`, builds the unit's offline bundle into
`extra/downloads/`, and writes the download box with the published check-suite
fingerprint. These generated files are not committed.

`extra/examples/a1-example-report.html` is an example verification report,
produced from the maintainers' private reference code with example details.
Regenerate it when the check suite changes.

## Publishing

`.github/workflows/pages.yml` builds the site on every push to `main` (it
checks out `verifiedmethods/ode-ivp` alongside) and deploys it to GitHub Pages.
In the repository settings, Pages must use "GitHub Actions" as its source.

Pages are written in MyST Markdown, with Furo as the theme (chosen for small
pages on slow connections).
