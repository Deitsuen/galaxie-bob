#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from mock import MagicMock
import re

sys.path.insert(0, os.path.abspath('../..'))

#
# Galaxie BoB documentation build configuration file, created by
# sphinx-quickstart on Fri Jan 27 13:25:39 2017.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'guzzle_sphinx_theme',
    'sphinx.ext.githubpages'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'Galaxie BoB'
copyright = u'2017, Jérôme Ornech alias Tuux <tuux at rtnp dot org>'
author = u'Jérôme Ornech alias Tuux <tuux at rtnp dot org>'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = u'0.1'
# The full version, including alpha/beta/rc tags.
release = u'0.1'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
#html_theme = 'alabaster'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
#html_static_path = ['_static']


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
#htmlhelp_basename = 'GalaxieBoBdoc'

# Guzzle theme
# -- HTML theme settings ------------------------------------------------
html_show_sourcelink = False
html_sidebars = {
    '**': ['logo-text.html',
           'globaltoc.html',
           'localtoc.html',
           'searchbox.html']
}
# -- End HTML theme settings --------------------------------------------

import guzzle_sphinx_theme

extensions.append("guzzle_sphinx_theme")
html_translator_class = 'guzzle_sphinx_theme.HTMLTranslator'
html_theme_path = guzzle_sphinx_theme.html_theme_path()
html_theme = 'guzzle_sphinx_theme'

# Guzzle theme options (see theme.conf for more information)
html_theme_options = {
    # Set the name of the project to appear in the sidebar
    "project_nav_name": "Galaxie BoB",
}

html_static_path = ['_static']
htmlhelp_basename = 'GalaxieBoBdoc'
# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'GalaxieBoB.tex', 'Galaxie BoB Documentation',
     'Jerome Ornech', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, u'galaxiebob', u'Galaxie BoB Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, u'GalaxieBoB', u'Galaxie BoB Documentation',
     author, u'GalaxieBoB', u'One line description of project.',
     u'Miscellaneous'),
]

event_sig_re = re.compile(r'([a-zA-Z-]+)\s*\((.*)\)')
os.environ['TERM'] = "linux"


def run_apidoc(_):
    cur_dir = os.path.abspath(os.path.dirname(__file__))
    print(cur_dir)
    module = os.path.abspath(os.path.join(cur_dir, "..", "..", "GLXBob"))
    print(module)

    from sphinx.apidoc import main
    main(['-e', '-o', cur_dir, module, '--force'])


def setup(app):
    app.connect('builder-inited', run_apidoc)


# Python Curses is a C application bind
class Mock(MagicMock):
    @classmethod
    def __getattr__(cls, name):
            return MagicMock()

MOCK_MODULES = ['curses', 'argparse', 'numpy']
sys.modules.update((mod_name, Mock()) for mod_name in MOCK_MODULES)

autoclass_content = 'both'
autodoc_member_order = 'bysource'