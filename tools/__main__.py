import os
import re
import nbformat
from nbformat.v4.nbbase import new_markdown_cell
import itertools

from configure import *

# Header on index page pointing back to github.io
INDEX_HEADER = "# [{0}]({1})".format(DESC, PAGE)

# location of remote notebook directory
NBVIEWER_BASE_URL = "http://nbviewer.jupyter.org/github/{0}/{1}/blob/master/notebooks/".format(USER, REPO)

# Header point to Table of Contents page viewed on nbviewer
README_TOC = "### [Table of Contents]({0}index.ipynb?flush=true)".format(NBVIEWER_BASE_URL)

# template for link to open notebooks in Google colaboratory
COLAB_TEMPLATE = """
<p><a href="https://colab.research.google.com/github/{0}/{1}/blob/master/notebooks/{2}"><img align="left" src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open in Colab" title="Open in Google Colaboratory"></a>
"""
COLAB_LINK = COLAB_TEMPLATE.format(USER, REPO, "{notebook_filename}")

# location of the README.md file in the local repository
README_FILE = os.path.join(os.path.dirname(__file__), '..', 'README.md')

# location of notebook directory in the local repository
NOTEBOOK_DIR = os.path.join(os.path.dirname(__file__), '..', 'notebooks')

# location of the index files in the local respository
INDEX_FILE = os.path.join(NOTEBOOK_DIR, 'index.md')
INDEX_NB = os.path.join(NOTEBOOK_DIR, 'index.ipynb')

# html comment used to tag the location of the course information in each notebook
COURSE_COMMENT = "<!--COURSE_INFORMATION-->"
COURSE_INFO = COURSE_COMMENT + COURSE_INFO_HEADER

# regular expression that matches notebook filenames to be included in the TOC
REG = re.compile(r'(\d\d|[A-Z])\.(\d\d)-(.*)\.ipynb')

# regular expression to match markdown figures
FIG = re.compile(r'(?:!\[(.*?)\]\((.*?)\))')

# functions to create Nav bar
PREV_TEMPLATE = "< [{title}]({url}) "
CONTENTS = "| [Contents](index.ipynb) |"
NEXT_TEMPLATE = " [{title}]({url}) >"
NAV_COMMENT = "<!--NAVIGATION-->\n"

FMT = {'##':   '- [{0}]({1})',
       '###':  '    - [{0}]({1})',
       '####': '        - [{0}]({1})',
       '#####':'            - [{0}]({1})'}


class notebook():
    def __init__(self, filename):
        self.filename = filename
        self.path = os.path.join(NOTEBOOK_DIR, filename)
        self.chapter, self.section, _ = REG.match(filename).groups()
        self.url = os.path.join(NBVIEWER_BASE_URL, filename)
        self.colab_link = COLAB_LINK.format(notebook_filename=os.path.basename(self.filename))
        self.nb = nbformat.read(self.path, as_version=4)
        self.title = self.read_title()
        self.navbar = None
        self.readme = self.get_readme()
        self.index = self.get_index()
        self.figs = self.get_figs()

    def read_title(self):
        title = None
        for cell in self.nb.cells:
            if cell.cell_type == "markdown":
                if cell.source.startswith('#'):
                    title = cell.source[1:].splitlines()[0].strip()
                    break
        return title

    def write_course_info(self):
        if self.nb.cells[0].source.startswith(COURSE_COMMENT):
            print('- amending comment for: {0}'.format(self.filename))
            self.nb.cells[0].source = COURSE_INFO
        else:
            print('- inserting comment for {0}'.format(self.filename))
            self.nb.cells.insert(0, new_markdown_cell(COURSE_INFO))
        nbformat.write(self.nb, self.path)

    def write_navbar(self):
        if self.nb.cells[1].source.startswith(NAV_COMMENT):
            print("- amending navbar for {0}".format(self.filename))
            self.nb.cells[1].source = self.navbar
        else:
            print("- inserting navbar for {0}".format(self.filename))
            self.nb.cells.insert(1, new_markdown_cell(source=self.navbar))
        if self.nb.cells[-1].source.startswith(NAV_COMMENT):
            self.nb.cells[-1].source = self.navbar
        else:
            self.nb.cells.append(new_markdown_cell(source=self.navbar))
        nbformat.write(self.nb, self.path)

    def get_readme(self):
        if self.chapter.isdigit():
            self.chapter = int(self.chapter)
            if self.chapter == 0:
                fmt = "\n### [{2}]({3})" if self.section in '00' else "- [{2}]({3})"
            else:
                fmt = "\n### [Chapter {0}. {2}]({3})" if self.section in '00' else "- [{0}.{1} {2}]({3})"
        else:
            fmt = "\n### [Appendix {0}. {2}]({3})" if self.section in '00' else "- [{0}.{1} {2}]({3})"
        return fmt.format(self.chapter, int(self.section), self.title, self.url)

    def get_index(self):
        if isinstance(self.chapter, int):
            self.chapter = int(self.chapter)
            fmt = "\n## [Chapter {0}. {2}]({3})" if self.section in '00' else "\n### [{0}.{1} {2}]({3})"
        else:
            fmt = "\n## [Appendix {0}. {2}]({3})" if self.section in '00' else "\n### [{0}.{1} {2}]({3})"
        toc = [fmt.format(self.chapter, int(self.section), self.title, self.url)]
        for cell in self.nb.cells:
            if cell.cell_type == "markdown":
                if cell.source.startswith('##'):
                    header = cell.source.splitlines()[0].strip().split()
                    txt = ' '.join(header[1:])
                    url = '#'.join([self.url, '-'.join(header[1:])])
                    toc.append(FMT[header[0]].format(txt, url))
        return toc

    def get_figs(self):
        figs = []
        for cell in self.nb.cells:
            if cell.cell_type == "markdown":
                figs.extend(FIG.findall(cell.source))
        return figs

    def __gt__(self, nb):
        return self.filename > nb.filename

    def __str__(self):
        return self.filename


def set_navbars(notebooks):
    a, b, c = itertools.tee(notebooks, 3)
    next (c)
    for prev_nb, this_nb, next_nb in zip(itertools.chain([None], a), b, itertools.chain(c, [None])):
        this_nb.navbar = NAV_COMMENT
        this_nb.navbar += PREV_TEMPLATE.format(title=prev_nb.title, url=prev_nb.url) if prev_nb else ''
        this_nb.navbar += CONTENTS
        this_nb.navbar += NEXT_TEMPLATE.format(title=next_nb.title, url=next_nb.url) if next_nb else ''
        this_nb.navbar += this_nb.colab_link

notebooks = sorted([notebook(filename) for filename in os.listdir(NOTEBOOK_DIR) if REG.match(filename)])

set_navbars(notebooks)

for n in notebooks:
    n.write_course_info()
    n.write_navbar()

with open(README_FILE, 'w') as f:
    f.write(README_HEADER)
    f.write(README_TOC)
    f.write('\n'.join([n.readme for n in notebooks]))
    f.write('\n' + README_FOOTER)

with open(INDEX_FILE, 'w') as f:
    f.write(INDEX_HEADER)
    #f.write('\n'.join(['\n'.join(n.index) for n in notebooks]))
    for n in notebooks:
        f.write('\n' + '\n'.join(n.index))
        f.write('\n' + '\n'.join(["* Figure: [{0}]({1})".format(fig[0] if fig[0] else fig[1], fig[1]) for fig in n.figs]))

os.system(' '.join(['notedown', INDEX_FILE, '>', INDEX_NB]))
