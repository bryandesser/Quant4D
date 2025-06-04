import pathlib
import sys
import os
import sphinx_rtd_theme
import sphinxcontrib.matlab
from datetime import datetime

sys.path.insert(0, "../src")

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Quant4D'
copyright = f"{datetime.today().year}, Bryan D Esser"
author = 'Bryan D Esser'
release = '2025.03.17'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx_rtd_theme",
    "sphinx.ext.intersphinx",
    'sphinxcontrib.matlab',
    'sphinx.ext.duration',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.imgmath',
    'sphinx.ext.githubpages',
]

# Configure the matlab extension
primary_domain = "mat"
this_dir = os.path.dirname(__file__)
matlab_src_dir = os.path.abspath(os.path.join(this_dir, "..", "..", "src"))
matlab_short_links = True
matlab_auto_link = "all"
matlab_show_property_default_value = True
matlab_show_property_specs = True
matlab_class_signature = True


user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54"

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
}

# Include todo items/lists
todo_include_todos = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
html_theme_path = ["_themes", ]