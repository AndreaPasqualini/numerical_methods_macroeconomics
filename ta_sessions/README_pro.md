# Setting up Python like a Pro

## A leaner way: Miniconda

The magic behind Anaconda is called `conda`.
It is a small [CLI](https://en.wikipedia.org/wiki/Command-line_interface) program that manages all the modules and makes sure they work together (it also manages [virtual environments](https://docs.python.org/3/library/venv.html), but that's a feature we're not going to use).
If you care about your local machine being lean and avoiding unnecessary software, then you might want to check it out.

You can find the appropriate installer at https://conda.io/miniconda.html.
Again, you should choose Python 3.x instead of 2.x.

For instructions on how to install (as well as uninstall, if ever interested), refer to the official documentation for [Windows](https://conda.io/docs/user-guide/install/windows.html), [macOS](https://conda.io/docs/user-guide/install/macos.html) and [Linux](https://conda.io/docs/user-guide/install/linux.html).
Once you installed the conda system, you will access it through a terminal (aka, command prompt or PowerShell in Windows).

Using the syntax `conda install pkg1 pkg2 pkg3`, you can install what we need.
We are going to use the following packages for the course:

- `numpy` (N-dimensional numeric arrays);
- `scipy` (mathematical and statistical recipes);
- `matplotlib` (plotting); and
- `spyder` (IDE).

Additionally, you might be interested in the following packages

- `jupyter` (the web-based app to produce [notebooks](https://jupyter.org/) with Python code and [markdown](https://daringfireball.net/projects/markdown/) commentaries);
- `pandas` (Stata-like features to manage real-world data);
- `sympy` (symbolic mathematics);
- `numba` (LLVM interface and parallel computing); and
- `xlrd` (interface to Excel files).

As a function of your choice, `conda` will also pull in other necessary dependencies.

To understand the difference between Anaconda and Miniconda, you can look at the list of packages included in Anaconda (entirely omitted in Miniconda) for [Windows](https://docs.anaconda.com/anaconda/packages/py3.7_win-64/), [macOS](https://docs.anaconda.com/anaconda/packages/py3.7_osx-64/) and [Linux](https://docs.anaconda.com/anaconda/packages/py3.7_linux-64/).


## Other useful tools

If you think you'll often deal with programming, you might want to have a look at the following great software:

- [Sublime Text](https://www.sublimetext.com/) (an extensible, lean text editor for any programming language);
- [Visual Studio Code](https://code.visualstudio.com/) (an extensible text editor with IDE-like features for the more popular programming languages);
- [JetBrains PyCharm](https://www.jetbrains.com/pycharm/) (a full-fledged Python IDE, with all you need to develop _anything_ in Python);
- [Git](https://git-scm.com/) (a versioning system for source code management; free hosting at [GitHub](https://github.com/), [BitBucket](https://bitbucket.org/) or [GitLab](https://about.gitlab.com/));
- [SQLite Browser](https://sqlitebrowser.org/) (a [GUI](https://en.wikipedia.org/wiki/Graphical_user_interface) for exploring SQL databases).
