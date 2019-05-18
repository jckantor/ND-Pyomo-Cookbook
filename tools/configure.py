
# Edit the following string variables to customize tools to a new notebook repository
GITHUB_USER = "jckantor"
GITHUB_REPO = "ND-Pyomo-Cookbook"
PAGE_TITLE = "ND Pyomo Cookbook"


PAGE_URL = f"http://{GITHUB_USER}.github.io/{GITHUB_REPO}/"

# header to be inserted at the top of each notebook
NOTEBOOK_HEADER_CONTENT = f"""
*This notebook contains material from the [{PAGE_TITLE}]({PAGE_URL}) by 
Jeffrey Kantor (jeff at nd.edu); the content is available [on GitHub](https://github.com/{GITHUB_USER}/{GITHUB_REPO}).
*The text is released under the [CC-BY-NC-ND-4.0 license](https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode),
and code is released under the [MIT license](https://opensource.org/licenses/MIT).*
"""

# header for README.md
README_HEADER = f"""
# {PAGE_TITLE}

**{PAGE_TITLE}** is a collection of notebooks showing how to use [Pyomo](http://www.pyomo.org/) to solve
modeling and optimization problems. With Pyomo, one can embed within Python an optimization model consisting of
**decision variables**, **constraints**, and an optimization **objective**. A rich set of features enables the modeling
and analysis of complex systems.

The notebooks in this collection were developed for instructional purposes at Notre Dame. Originally
developed using the [Anaconda distribution of Python](https://www.anaconda.com/download/), the notebooks have been
updated to open directly [Google Colaboratory](https://colab.research.google.com/) where they can be run using
only a browser window.

PyomoFest at Notre Dame was held June 5-7, 2018. This repository contains the 
[agenda](https://github.com/jckantor/ND-Pyomo-Cookbook/tree/master/PyomoFest/PyomoFest.md), 
[slides](https://github.com/jckantor/ND-Pyomo-Cookbook/tree/master/PyomoFest/slides) and
[exercises](https://github.com/jckantor/ND-Pyomo-Cookbook/tree/master/PyomoFest/exercises_wo_soln/exercises)
distributed during that event.

"""

README_FOOTER = """
"""
