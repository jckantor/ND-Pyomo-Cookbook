import os
import re
import nbformat
from nbformat.v4.nbbase import new_markdown_cell
import itertools
import copy

from nbconvert import HTMLExporter
import shutil
from PyPDF2 import PdfFileMerger, PdfFileReader, PdfFileWriter

# import directory specfic stings
from configure import *


# Header on TOC page pointing back to github.io
TOC_HEADER = f"# [{PAGE_TITLE}]({PAGE_URL})"

# location of remote notebook directory
NBVIEWER_BASE_URL = f"http://nbviewer.jupyter.org/github/{GITHUB_USER}/{GITHUB_REPO}/blob/master/notebooks/"

# Header point to Table of Contents page viewed on nbviewer
README_TOC = f"### [Table of Contents]({NBVIEWER_BASE_URL}toc.ipynb?flush=true)"

# template for link to open notebooks in Google colaboratory
COLAB_LINK = f'<p><a href="https://colab.research.google.com/github/{GITHUB_USER}/{GITHUB_REPO}' \
             '/blob/master/notebooks/{notebook_filename}">' + \
             '<img align="left" src="https://colab.research.google.com/assets/colab-badge.svg"' + \
             ' alt="Open in Colab" title="Open in Google Colaboratory"></a>'

# location of the README.md file in the local repository
README_FILE = os.path.join(os.path.dirname(__file__), '..', 'README.md')

# location of notebook directory in the local repository
NOTEBOOK_DIR = os.path.join(os.path.dirname(__file__), '..', 'notebooks')
HTML_DIR = os.path.join(os.path.dirname(__file__), '..', 'html')
PDF_DIR = os.path.join(os.path.dirname(__file__), '..', 'pdf')
CUSTOM_CSS = os.path.join(os.path.dirname(__file__), 'custom.css')
if not os.path.exists(HTML_DIR):
    os.mkdir(HTML_DIR)
if not os.path.exists(PDF_DIR):
    os.mkdir(PDF_DIR)
shutil.copy(CUSTOM_CSS, os.path.join(HTML_DIR, 'custom.css'))

# location of the table of contents files in the local respository
TOC_FILE = os.path.join(NOTEBOOK_DIR, 'toc.md')
TOC_NB = os.path.join(NOTEBOOK_DIR, 'toc.ipynb')

# tag the location of the course information in each notebook
#NOTEBOOK_HEADER_TAG = "<!--NOTEBOOK_HEADER-->"
NOTEBOOK_HEADER_TAG = "<!--NOTEBOOK_HEADER-->"
NOTEBOOK_HEADER = "<!--NOTEBOOK_HEADER-->" + NOTEBOOK_HEADER_CONTENT

# regular expression that matches notebook filenames to be included in the TOC
REG = re.compile(r'(\d\d|[A-Z])\.(\d\d)-(.*)\.ipynb')

# nav bar templates
PREV_TEMPLATE = "< [{title}]({url}) "
CONTENTS = "| [Contents](toc.ipynb) |"
NEXT_TEMPLATE = " [{title}]({url}) >"
NAVBAR_TAG = "<!--NAVIGATION-->\n"


class nb():

    def __init__(self, filename):
        self.filename = filename
        self.path = os.path.join(NOTEBOOK_DIR, filename)
        self.html = os.path.join(HTML_DIR, filename.replace('.ipynb', '.html'))
        self.pdf = os.path.join(PDF_DIR, filename.replace('.ipynb', '.pdf'))
        self.chapter, self.section, _ = REG.match(filename).groups()
        self.isfrontmatter = self.chapter in "00"
        self.ischapter = self.chapter.isdigit() and (not self.chapter in "00")
        self.isappendix = not (self.ischapter or self.isfrontmatter)
        self.issection = not self.section in "00"
        self.url = os.path.join(NBVIEWER_BASE_URL, filename)
        self.colab_link = COLAB_LINK.format(notebook_filename=os.path.basename(self.filename))
        self.content = nbformat.read(self.path, as_version=4)
        self.navbar = None

    @property
    def title(self):
        for cell in self.content.cells:
            if cell.cell_type == "markdown":
                if cell.source.startswith('#'):
                    return cell.source[1:].splitlines()[0].strip()

    FIG = re.compile(r'(?:!\[(.*?)\]\((.*?)\))')
    @property
    def figs(self):
        figs = []
        for cell in self.content.cells:
            if cell.cell_type == "markdown":
                figs.extend(self.__class__.FIG.findall(cell.source))
        return figs

    LINK = re.compile(r'(?:[^!]\[(.*?)\]\((.*?)\))')
    @property
    def links(self):
        links = []
        for cell in self.content.cells[2:-1]:
            if cell.cell_type == "markdown":
                links.extend(self.__class__.LINK.findall(cell.source))
        return links

    IMG = re.compile(r'<img[^>]*>')
    @property
    def imgs(self):
        imgs = []
        for cell in self.content.cells[2:-1]:
            if cell.cell_type == "markdown":
                imgs.extend(self.__class__.IMG.findall(cell.source))
        return imgs

    @property
    def numbered_title(self):
        if self.isfrontmatter:
            return f"{self.title}"
        elif self.ischapter:
            if not self.issection:
                return f"Chapter {int(self.chapter)}. {self.title}"
            else:
                return f"{int(self.chapter)}.{int(self.section)} {self.title}"
        else:
            if not self.issection:
                return f"Appendix {self.chapter}. {self.title}"
            else:
                return f"{self.chapter}.{int(self.section)} {self.title}"

    @property
    def link(self):
        return f"[{self.numbered_title}]({self.url}]"

    @property
    def readme(self):
        return "- " + self.link if self.issection else "\n### " + self.link

    @property
    def toc(self):
        toc = ["### " + self.link if self.issection else "\n## " + self.link]
        hcells = (cell for cell in self.content.cells if cell.cell_type == "markdown" and cell.source.startswith("##"))
        for hcell in hcells:
            header = hcell.source.splitlines()[0].strip().split()
            txt = ' '.join(header[1:])
            url = '#'.join([self.url, '-'.join(header[1:])])
            toc.append("    "*(len(header[0])-2) + f"- [{txt}]({url})")
        return toc

    ORPHAN = re.compile(r"^#+")
    @property
    def orphan_headers(self):
        orphans = []
        for cell in self.content.cells:
            if cell.cell_type == "markdown":
                 for line in cell.source.splitlines()[1:]:
                     if self.__class__.ORPHAN.match(line):
                         orphans.append(line)
        return orphans

    def write_header(self):
        if self.content.cells[0].source.startswith(NOTEBOOK_HEADER_TAG):
            print('- amending header for {0}'.format(self.filename))
            self.content.cells[0].source = NOTEBOOK_HEADER
        else:
            print('- inserting header for {0}'.format(self.filename))
            self.content.cells.insert(0, new_markdown_cell(NOTEBOOK_HEADER))
        nbformat.write(self.content, self.path)

    def write_navbar(self):
        for cell in [self.content.cells[1], self.content.cells[-1]]:
            if cell.source.startswith(NAVBAR_TAG):
                print(f"- amending navbar for {self.filename}")
                cell.source = self.navbar
            else:
                print(f"- inserting navbar for {self.filename}")
                self.content.cells.insert(1, new_markdown_cell(source=self.navbar))
        nbformat.write(self.content, self.path)

    def write_html(self):
        print("writing", self.html)
        html_exporter = HTMLExporter()
        html_exporter.template_file = 'full'
        # do a deeo copy to any chance of overwriting the original notebooks
        content = copy.deepcopy(self.content)
        content.cells = content.cells[2:-1]
        content.cells[0].source = "# " + self.numbered_title
        (body, resources) = html_exporter.from_notebook_node(content)
        with open(self.html, 'w') as f:
            f.write(body)

    def write_pdf(self, page_offset=0):
        print("writing", self.pdf)
        os.system(' '.join(['wkhtmltopdf',
                            "--header-left", f"'{self.numbered_title}'",
                            "-L 1in -R 1in -T 1in -B 1in",
                            "--header-spacing 6",
                            "--header-line",
                            "--header-right '[page]'",
                            "--javascript-delay 5000",
                            "--page-offset " + str(page_offset),
                            self.html,
                            self.pdf]))

    def __gt__(self, nb):
        return self.filename > nb.filename

    def __str__(self):
        return self.filename


class nbcollection():

    def __init__(self, dir=NOTEBOOK_DIR):
        self.notebooks = sorted([nb(filename) for filename in os.listdir(dir) if REG.match(filename)])

    def write_headers(self):
        for nb in self.notebooks:
            nb.write_header()

    def write_navbars(self):
        a, b, c = itertools.tee(self.notebooks, 3)
        next (c)
        for prev_nb, nb, next_nb in zip(itertools.chain([None], a), b, itertools.chain(c, [None])):
            nb.navbar = NAVBAR_TAG
            nb.navbar += PREV_TEMPLATE.format(title=prev_nb.title, url=prev_nb.url) if prev_nb else ''
            nb.navbar += CONTENTS
            nb.navbar += NEXT_TEMPLATE.format(title=next_nb.title, url=next_nb.url) if next_nb else ''
            nb.navbar += nb.colab_link
            nb.write_navbar()

    def write_toc(self):
        with open(TOC_FILE, 'w') as f:
            print(TOC_HEADER, file=f)
            for nb in self.notebooks:
                f.write('\n')
                f.write('\n'.join(nb.toc) + '\n')
                if nb.figs:
                    print("* Figures", file=f)
                    for txt, url in nb.figs:
                        print("    - [{0}]({1})".format(txt if txt else url, url), file=f)
                if nb.links:
                    print("* Links", file=f)
                    for txt, url in nb.links:
                        print(f"    - [{txt}]({url})", file=f)
        os.system(' '.join(['notedown', TOC_FILE, '>', TOC_NB]))

    def write_readme(self):
        with open(README_FILE, 'w') as f:
            f.write(README_HEADER)
            f.write(README_TOC)
            f.write('\n'.join([nb.readme for nb in self.notebooks]))
            f.write('\n' + README_FOOTER)

    def write_html(self):
        for nb in self.notebooks:
            nb.write_html()

    def write_pdf(self):
        for nb in self.notebooks:
            nb.write_pdf()

    def merge_pdf(self):
        pdf_writer = PdfFileWriter()
        page = 0
        for nb in self.notebooks:
            pdf_reader = PdfFileReader(nb.pdf)
            for spage in range(pdf_reader.numPages):
                page += 1
                v = pdf_reader.getPage(spage)
                pdf_writer.addPage(v)
        f = open(f"{GITHUB_REPO}.pdf", 'wb')
        pdf_writer.write(f)
        f.close()

    def write_book(self):
        page_number = 0
        pdf_writer = PdfFileWriter()
        for nb in self.notebooks:
            nb.write_html()
            nb.write_pdf(page_number)
            pdf_reader = PdfFileReader(nb.pdf)
            for page in range(pdf_reader.numPages):
                page_number += 1
                pdf_writer.addPage(pdf_reader.getPage(page))
        f = open(f"{GITHUB_REPO}.pdf", 'wb')
        pdf_writer.write(f)
        f.close()


    def lint(self):
        for nb in self.notebooks:
            if nb.imgs:
                print("\n", nb.filename)
                for img in nb.imgs:
                    print(img)
            if nb.orphan_headers:
                print("\nOrphan headers in ", nb.filename)
                for orphan in nb.orphan_headers:
                    print(orphan)


notebooks = nbcollection()
#notebooks.write_headers()
#notebooks.write_navbars()
#notebooks.write_toc()
#notebooks.write_readme()
notebooks.write_book()
#notebooks.lint()

