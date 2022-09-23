#!/usr/bin/env python
# coding: utf-8

# # Notebook Style Guide
# 
# Keywords: style guide, notebook format

# Maintaining a collection of Jupyter notebooks requires attention several important details, among them are the structure and style of the individual notebooks. Maintaining a consistent notebook structure and style enables the use of tools to automate management of the overall collection. The purpose of this notebook is document the standards adopted for this particular collection.

# ## Notebook naming and ancillary/generated files
# 
# All notebooks in a repository should reside in a top-level directory named `notebooks`. The filenames begin with a prefix indicating their position in book-like organization. The first two digits indicate a chapter number with 00 reserved for front matter. Replacing the digits with a character indicates an appendix. Following a separating '.', a second pair of digits indicates a section with the front matter, chapter, or appendix. A hyphen separates the prefix from the rest of the filename. The standard `.ipynb` Jupyter notebook suffix is required.
# 
#     my-repository-title/
#     |-- notebooks/
#         |--data/
#         |--figures/
#         |--00.00-Front-Matter.ipynb
#         |--00.01-Preface.ipynb
#         |--00.02-Acknowledgments.ipynb
#         |--01.00-Getting-Started.ipynb
#         |--01.01-First-Section.ipynb
#         |--02.00-Second-Chapter.ipynb
#         |--A.00-Style-Guid
#         
# This style guide assumes the use of software tools to manage the collection of notebooks. The software tools will perform the following tasks:
# 
# * Generate a `Readme.md` file to be written to the top-level directory.
# * Generate a table of contents written to `toc.md` and `toc.ipynb` in the notebooks directory.
# * Insert and update a common header for all notebooks
# * Insert and update a navigation bar located in the second and terminal cell of each notebook.
# * A listing of all links and figures found in the notebooks.
# * A listing of stylistic `lint` encountered during the processing of the notebooks.

# ## Notebook title and headers

# ### Title
# Each notebook begins with a markdown level 1 header containing the title of the corresponding chapter or section. This should be capitalized following the Chicago Manual of Style. The hashtag `#` appears as the first line in the cell, and there is one and only one level 1 header per notebook. The title cell may include a brief summary of the notebook contents.

# ### Subheadings
# 
# A notebook will typically consist of multiple sections.  The sections are organized hierarchically as markdown headings. Following the document title, the highest level heading begins as markdown level 2 (i.e., `##`). The hierarchy is strict meaning that the next level in the hierarchy, `###`, and must appear before the first heading of the next higher level. This, for example, is an allowable hierarchy:
# 
#     # Notebook Title
#     ## First section
#     ### First subsection
#     #### First sub-subsection
#     #### Second sub-subsection
#     ### Second subsection
#     ## Second section
#     ### Another subsection
#     
# This is not allowable because it skips from `##` to `####` without an intervening `###`:
# 
#     # Notebook Title
#     ## First section
#     #### First sub-subsection
#     #### Second sub-subsection
#     ### Second subsection
#     ## Second section
#     ### Another subsection
#     
# The following guidelines apply to headings and subheadings:
#     
# * Following the Chicago Manual of Style, only the first word in headings and subheadings are capitalized.
# * Each heading or subheading appears as the first line in a markdown cell.
# * At this point in the development this style guide, titles, headings, and subheadings should remain unnumbered.

# ### Keywords
# 
# Keywords should be included in the level 1 headers designating a title. The keywords are specified in a new line beginning with `Keywords:` followed by a comma separated list of keyword phrases. Keywords are used to construct an index for the notebook collection.

# ## External Files
# 
# Notebooks will often incorporate figures, data, or video. Any external files must be appropriately licensed for reuse. If that isn't possible, then that information should be accessed by linking to a resource showing the user how to properly access that information.
# 
# In general, external resources should be referenced by an external link whenever possible. If the resource is in the same repository, the link should be the public repository. This practice enables cross-platform use of notebooks, and streamlines the import and use of notebooks by other users.

# ### Figures
# 
# Figures included within the repository should located within a common figures directory. This practice enables reuse of figures, and streamlines the editing and maintenance of figures. Figures should be `.png` or `.jpg` format as appropriate, and resized for use with the standard markdown `![]()` markup.

# ### Data
# 
# Data files distributed with the repository should be located within a common data directory. 

# ## Design for Portability
# 
# Notebooks are intended as durable and robust means of communicating with a diverse audience. To this end, special effort attention must be given to making it possible to run the notebooks on multiple platforms. 

# ### Installations and Imports
# 
# It is good practice to include all necessary installations and imports in first few executable cells of a notebook, and may be included in a special section entitled **Installations and imports**.
# 
# To the extent possible, the installation and import cells should be written to run cross-platform without raising exceptions. Code can written with the assumption that standard Python libraries, including Matplotlib, Numpy, Pandas, and Scipy, are present. Any needed installations should included in the first code cell of the notebook and written for cross-platform use. For example,
# 
#     import sys
#     if 'google.colab' in sys.modules:
#         !pip install pyomo
#         !pin install glpk
#         
# Conditional installs may have been previously installed on the user's computer.
# 
#     try:
#         import glpk
#     except
#         !pip install glpk
#         import glpk

# ### Markdown
# 
# Plain github-flavored markdown should be used wherever possible. Avoid use of non-markdown constructs, such as html tags.
# 
# * Any references should be collected under a separate heading entitled References, and formatted using the Chicago Manual of Style.
# * Additional sections entitled Exercises, Additional resources, Further reading may be included in the notebooks. Each exercise should be given a separate subsection to be included in the table of contents.

# ## Further reading

# * [Space Telescope Science Institute Style Guide](https://github.com/spacetelescope/style-guides/blob/master/guides/jupyter-notebooks.md)
# * [Jupyter notebook best practices and style guide](https://github.com/chrisvoncsefalvay/jupyter-best-practices)
# * [Dataquest: An In-Depth Style Guide for Data Science Projects](https://www.dataquest.io/blog/data-science-project-style-guide/)
# * [ESRI: Coding Standards for Jupyter Notebook](https://www.esri.com/about/newsroom/arcuser/coding-standards-for-jupyter-notebook/)

# In[ ]:




