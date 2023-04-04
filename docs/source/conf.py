# -- Project information

project = 'ASSIST-IoT'

release = '0.1'
version = '0.1.0'

# -- General configuration

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx', 
    'sphinx.ext.todo', 
    'sphinx.ext.viewcode', 
    'sphinx.ext.intersphinx',  
    'sphinx.ext.coverage', 
    'sphinx.ext.mathjax', 
    'sphinx.ext.ifconfig', 
    'sphinx.ext.githubpages', 
    'sphinx.ext.imgmath', 
    'sphinx.ext.graphviz', 
    'sphinx.ext.inheritance_diagram', 
    'sphinx.ext.napoleon', 
    'sphinx.ext.autosectionlabel', 
    'sphinx.ext.extlinks']

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output

html_theme = 'sphinx_rtd_theme'