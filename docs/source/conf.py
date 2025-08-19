import pathlib
import sys
import os
import sphinx_rtd_theme
import sphinxcontrib.matlab
from datetime import datetime

sys.path.insert(0, "../src")

project = 'Quant4D'
copyright = f"{datetime.today().year}, Bryan D Esser"
author = 'Bryan D Esser'
release = '2025.03.17'

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
    'sphinx_autodoc_typehints',
    'sphinxcontrib.video',
]

napoleon_numpy_docstring = True
napoleon_custom_sections = [('Returns', 'params_style')]
napoleon_use_param = True
napoleon_preprocess_types = True

primary_domain = "mat"
this_dir = os.path.dirname(__file__)
matlab_src_dir = os.path.abspath(this_dir)
matlab_short_links = True
matlab_auto_link = "all"
matlab_show_property_default_value = False
matlab_show_property_specs = False
matlab_class_signature = False


user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54"

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
}

todo_include_todos = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
html_theme_path = ["_themes", ]
html_baseurl = "https://quant4d.readthedocs.io/en/latest"

#html_context = {
#   'display_github': True,
#   'github_user': 'bryandesser',
#   'github_repo': 'Quant4D',
#}