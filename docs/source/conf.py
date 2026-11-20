# Configuration file for the Sphinx documentation builder.
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import re
import sys
from datetime import datetime
import sphinx_rtd_theme

# Make the package importable from the repo root (for autodoc).
# conf.py lives in docs/source/, so go up two levels.
sys.path.insert(0, os.path.abspath("../.."))

# -- Project information -----------------------------------------------------
project = "pyQuant4D"
copyright = f"{datetime.today().year}, Bryan D Esser"
author = "Bryan D Esser"


def _version() -> str:
    """The version in pyproject.toml (the checkout being documented), else the installed package's."""
    try:
        with open(os.path.join(os.path.dirname(__file__), "..", "..", "pyproject.toml"), encoding="utf-8") as f:
            match = re.search(r'^version\s*=\s*"([^"]+)"', f.read(), re.MULTILINE)
        if match:
            return match.group(1)
    except OSError:
        pass
    try:
        from importlib.metadata import version
        return version("pyquant4d")
    except Exception:
        return "unknown"


release = _version()                  # e.g. 0.3.0 (never edited here: pyproject.toml is the one place)
version = ".".join(release.split(".")[:2])

# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx_rtd_theme",
    "sphinx.ext.intersphinx",
    "sphinx.ext.duration",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.imgmath",
    "sphinx.ext.githubpages",
    "sphinx_autodoc_typehints",
    "myst_parser",
]

napoleon_numpy_docstring = True
napoleon_google_docstring = True
napoleon_use_param = True
napoleon_preprocess_types = True

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
}
autodoc_typehints = "description"

todo_include_todos = True

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Allow both .rst and .md source files
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}

# -- Options for HTML output -------------------------------------------------
html_theme = "sphinx_rtd_theme"

this_dir = os.path.dirname(__file__)
html_static_path = [os.path.abspath(os.path.join(this_dir, "..", "_static"))]

html_baseurl = "https://pyquant4d.readthedocs.io/en/latest"

html_context = {
    "display_github": True,
    "github_user": "bryandesser",
    "github_repo": "pyQuant4D",
    "github_version": "main",
    "conf_py_path": "/docs/source/",
    "edit_on_github_text": "View on GitHub",
}

# -- Intersphinx mapping -----------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://numpy.org/doc/stable", None),
    "matplotlib": ("https://matplotlib.org/stable", None),
    "scipy": ("https://docs.scipy.org/doc/scipy", None),
}
