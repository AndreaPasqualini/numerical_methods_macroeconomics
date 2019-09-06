# Numerical Methods for Macroeconomics

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/apsql/numerical_methods_macroeconomics/master)

This repository contains material for the PhD course in [Macroeconomics 3](https://www.unibocconi.eu/wps/wcm/connect/Bocconi/SitoPubblico_EN/Navigation+Tree/Home/Programs/PhD/PhD+in+Economics+and+Finance/Courses+and+Requirements/), taught by [Marco Maffezzoli](http://faculty.unibocconi.eu/marcomaffezzoli/) at [Bocconi University](https://www.unibocconi.eu/).
I'm the TA for the Spring 2018 and Spring 2019 iterations.

However, this repo will not be limited in scope to the course.
Given enough time, this should be a full-fledged library (with examples) especially aimed at learning Python for (Macro)Economic applications.
I'll update this repo with teaching (or self-learning) material as I progress in life.


## Overview of material in this repo

The folder [`ta_sessions`](./ta_sessions) contains Jupyter notebooks covering material for (surprise surprise) the TA sessions of the course mentioned above.

The package [`NMmacro`](./NMmacro) contains code developed around the topics of the course.
The code that can be re-used for various appllications.
However, it has not been developed with generality in mind: code in the package is tailored for the sake of teaching how to deal with classical examples in Economics.

The folder [`code_examples`](./code_examples) includes scripts that use the functions and classes written in [`NMmacro`](./NMmacro).
It's more of a showcase than anything else.

Inside [`other_applications`](./other_applications) there is some code that showcases the use of Python in applications other than numerical computation.
At the moment, it contains an application of _Beautiful Soup_ to scrape HTML code found online.
I'd like to code examples for some general data cleaning with _Pandas_, _Selenium_ and _NLTK_.


## Other references

Here is a list of references and related material you might want to check out.
There is no specific reason these are here for, except for my own gut-feeling that suggested me to put them here.

- [This overwhelming bunch of stuff](http://www.wouterdenhaan.com/notes.htm) from Wouter Den Haan
- [The QuantEcon (Py)Lectures](https://lectures.quantecon.org/py/) website
- [This GitHub repository](https://github.com/zhouweimin233/QuantMacro) of somebody at The University of Alabama at Birmingham with a PhD course similar to this one, with code and notebooks
- [Gianluca Violante's course in Quantitative Macro](https://sites.google.com/a/nyu.edu/glviolante/teaching/quantmacro) at NYU, referenced by the previous source
- [This GitHub repo](https://github.com/jstac/nyu_macro_fall_2018) of John Stachurski for a course at NYU, with (a lot more) math-y material
- [This GitHub repo](https://github.com/OpenSourceMacro/BootCamp2018) of OSM Boot Camp 2018, a [summer school](https://bfi.uchicago.edu/osm18) offered by uChicago
- Aruoba, S.B. and Fernández-Villaverde, J., 2015. "A Comparison of Programming Languages in Macroeconomics." _Journal of Economic Dynamics and Control, 58_, pp.265-273 ([Published version](https://doi.org/10.1016/j.jedc.2015.05.009)) ([Working-paper version](https://www.sas.upenn.edu/~jesusfv/comparison_languages.pdf)) ([Code](https://github.com/jesusfv/Comparison-Programming-Languages-Economics)) ([Update](https://www.sas.upenn.edu/~jesusfv/Update_March_23_2018.pdf))
