"""Sphinx configuration for https://verifiedmethods.github.io."""

project = "verifiedmethods"
author = "Abd'gafar Tunde Tiamiyu and the verifiedmethods contributors"
copyright = "2026, Abd'gafar Tunde Tiamiyu and the verifiedmethods contributors"

extensions = ["myst_parser", "sphinx.ext.mathjax"]
myst_enable_extensions = ["dollarmath", "amsmath", "colon_fence", "deflist", "attrs_inline"]
myst_heading_anchors = 3
source_suffix = {".md": "markdown"}
exclude_patterns = ["_build", "**/_download.md"]
suppress_warnings = ["myst.header"]

html_theme = "furo"
html_title = "verifiedmethods"
html_baseurl = "https://verifiedmethods.github.io/"
html_static_path = ["_static"]
html_css_files = ["custom.css"]
html_extra_path = ["../extra"]  # downloads/ and examples/ at the site root
html_show_sourcelink = False
html_copy_source = False
html_last_updated_fmt = "%d %B %Y"
html_theme_options = {
    "announcement": "Prototype: units A1 and A2 are ready to try.",
    "light_css_variables": {"color-brand-primary": "#1d5c8f", "color-brand-content": "#1d5c8f"},
    "dark_css_variables": {"color-brand-primary": "#8bbbe6", "color-brand-content": "#8bbbe6"},
    "top_of_page_buttons": [],  # unit pages are copied in at build time, so edit links would break
}
