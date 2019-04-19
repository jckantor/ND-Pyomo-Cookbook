import os
import re
import nbformat

# location of notebook directory in the local repository
NOTEBOOK_DIR = os.path.join(os.path.dirname(__file__), '..', 'notebooks')

# location of the index file in the local respository
INDEX_FILE = os.path.join(NOTEBOOK_DIR, 'index.md')

# location of the index notebook in the local repository
INDEX_NB = os.path.join(NOTEBOOK_DIR, 'index.ipynb')

# header for the index file and notebook
INDEX_HEADER = """
# [ND Pyomo Cookbook](http://jckantor.github.io/ND-Pyomo-Cookbook/)

## Table of Contents
"""

# location of the README.md file in the local repository
README_FILE = os.path.join(os.path.dirname(__file__), '..', 'README.md')

# header for README.md
README_HEADER = """
# ND Pyomo Cookbook

T[Pyomo](http://www.pyomo.org/) is a state-of-the-art Python package for 
modeling and solving optimization problems. Using Pyomo, a user can embed an 
optimization model consisting of **decision variables**, **constraints**, and 
an optimization **objective** within Python. Pyomo includes a rich set of 
features to enable modeling of complex systems, specifying a solver, and 
accessing the solution.

This repository provides instructions on getting started with Pyomo, and a 
collection of Pyomo modeling notebooks that have been developed for 
instructional purposes at Notre Dame. The notebooks were originally developed 
using the [Anaconda distribution of Python](https://www.anaconda.com/download/).
The notebooks have been recently updated to open directly on 
[Google Colaboratory](https://colab.research.google.com/) which enables their 
using only a browser window.

PyomoFest at Notre Dame was held June 5-7, 2018. This repository contains the 
[agenda](PyomoFest.md), [slides](PyomoFest/slides/) and 
[exercises](PyomoFest/exercises_wo_soln/exercises/) distributed during that 
event.

## Contents
---
"""

# regular expression that matches notebook filenames to be included in the TOC
REG = re.compile(r'(\d\d|[A-Z])\.(\d\d)-(.*)\.ipynb')

def iter_notebooks():
    """Return list of notebooks matched by regular expression"""
    return sorted(nb_file for nb_file in os.listdir(NOTEBOOK_DIR) if REG.match(nb_file))

def get_notebook_title(nb_file):
    """Returns notebook title header if it exists, else None"""
    nb = nbformat.read(os.path.join(NOTEBOOK_DIR, nb_file), as_version=4)
    for cell in nb.cells:
        if cell.cell_type == "markdown":
            if cell.source.startswith('#'):
                return cell.source[1:].splitlines()[0].strip()

def gen_contents(directory=None):
    for nb_file in iter_notebooks():
        nb_url = os.path.join(directory, nb_file) if directory else nb_file
        chapter, section, name = REG.match(nb_file).groups()
        if chapter.isdigit():
            chapter = int(chapter)
            if chapter == 0:
                fmt = "\n### [{2}]({3})" if section in '00' else "- [{2}]({3})"
            else:
                fmt = "\n### [Chapter {0}. {2}]({3})" if section in '00' else "- [{0}.{1} {2}]({3})"
        else:
            fmt = "\n### [Appendix {0}. {2}]({3})" if section in '00' else "- [{0}.{1} {2}]({3})"

        yield fmt.format(chapter, int(section), get_notebook_title(nb_file), nb_url)


def write_contents(FILE, HEADER, directory=None):
    with open(FILE, 'w') as f:
        f.write(HEADER)
        f.write('\n'.join(gen_contents(directory)))


if __name__ == '__main__':
    directory = 'http://nbviewer.jupyter.org/github/jckantor/ND-Pyomo-Cookbook/blob/master/notebooks/'
    write_contents(INDEX_FILE, INDEX_HEADER, directory)
    os.system(' '.join(['notedown', INDEX_FILE, '>', INDEX_NB]))
    write_contents(README_FILE, README_HEADER,  directory)
