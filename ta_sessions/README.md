# Numerical Methods in Macroeconomics

## Setting up Python for Data Science (and Macro)

These are instructions you might want to follow if you want to set up your local machine (e.g., your laptop) to run Python.
I will also include details about the main packages we need.

The following instructions hold for Windows, Mac OS and Linux.


### Installing Python through Anaconda

Python alone cannot do much.
It's a bit like installing a new OS on a computer: can you do stuff with it?
Yes, but not much: you'll need additional applications.
With Python, we need [modules](https://docs.python.org/3/tutorial/modules.html).

As [it is not easy to manage modules](https://en.wikipedia.org/wiki/Dependency_hell) manually, we're going to need a [package manager](https://en.wikipedia.org/wiki/Package_manager).
The one we choose for this setup is [Anaconda](https://www.anaconda.com/), which is popular among people who need to do numerical and stastical work (some prefer calling it data science).

Go to https://www.anaconda.com/download/ and download the file that is relevant for your OS.
You should choose the Python 3.x version, as the 2.x is [legacy (read: old) software](https://en.wikipedia.org/wiki/Legacy_system) that is there for compatibility (i.e., targeting audiences different from us).
You can find instructions on how to install Anaconda for [Windows](https://docs.anaconda.com/anaconda/install/windows/), [macOS](https://docs.anaconda.com/anaconda/install/mac-os/) and [Linux](https://docs.anaconda.com/anaconda/install/linux/).

As the typical Anaconda installation includes all the packages we'll need (including the Python interpreter), **we're done**.
To confirm this is the case, search for [Spyder](https://www.spyder-ide.org/) among your applications and launch it: this will be our [IDE](https://en.wikipedia.org/wiki/Integrated_development_environment) for the rest of the course.

If one day you want to get rid of Anaconda, you can just follow the [instructions to uninstall](https://docs.anaconda.com/anaconda/install/uninstall/) it.

Anaconda by default installs the most common packages typical "data scientists" use.
We are not going to use all of them in this course.
If you're very mindful about your computer and you're interested in having a leaner installation, read the [README for pros](./README_pro.md).
You're also going to find extra software you might want to check out.


## Structure of TA sessions

This is a tentative schedule: even though most of the material is ready and present in this folder, unexpected things might come up.
However, this is what I will try to cover in each of the 6 meetings:

1. Introduction to Numerical Methods in Macroeconomics and introduction to Python
	- Perturbation methods
	- Projection methods
	- Numpy
	- Scipy
	- Matplotlib
2. Global solution methods under no uncertainty (example: household's problem in the neoclassical growth model)
	- Value Function iteration (VFI)
	- Policy Function iteration (PFI)
	- Time iteration (TI)
3. Global solution methods under uncertainty (example: household's problem in the stochastic neoclassical growth model)
	- Markov chains as discretized AR(1) processes
	- VFI, PFI and TI under stochastic environments
	- Simulation
	- Endogenous grid methods (if time allows)
4. Bewley-like models: idiosyncratic shocks to endowments in a simple exchange economy
	- Reading [Huggett (1993)](https://doi.org/10.1016/0165-1889(93)90024-M)
	- Replicating it
5. Bewley-like models: idiosyncratic shocks to labor income in a RBC model
	- Reading [Aiyagari (1994)](https://doi.org/10.2307/2118417)
	- Replicating it
6. Advanced tools
	- Binning (theory in class, here only code)
	- Transition dynamics (MIT shocks; theory in class, here only code)
	- [Krusell and Smith (1998)](https://doi.org/10.1086/250034): overview of code and highlight of main steps (if time allows)
	- [Reiter's (2009)](https://doi.org/10.1016/j.jedc.2008.08.010) method: solving models with idiosyncratic _and_ aggregate shocks (if time allows)

For each session, there ~~is~~ will be a [Jupyter notebook](https://jupyter.org/).
I might use extra material in class (e.g., slides) but they will have no additional content relative to the notebooks, so I will not post them here.


### Extra topics: web scraping, machine learning and natural language processing

Economists are learning their way through programming, and some used Python to [scrape the web](https://en.wikipedia.org/wiki/Web_scraping), run [machine learning](https://en.wikipedia.org/wiki/Machine_learning) algorithms or [parse natural language](https://en.wikipedia.org/wiki/Natural_language_processing).
These practices are becoming popular, so they deserve a bit of our attention.

While I will not have time to cover them, I want to showcase how those tools can be useful to us.
I will post some code I used in the past and, if I have time, I will accompany it with notebooks explaining the main steps and decisions.
