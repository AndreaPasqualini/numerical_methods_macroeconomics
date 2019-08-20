# Material for TA sessions at Bocconi University

## Structure of TA sessions

**This is a tentative schedule**: even though most of the material is ready and present in this folder, unexpected things might come up.
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
	- Transition dynamics (aka, MIT shocks; theory in class, here only code)
	- [Krusell and Smith (1998)](https://doi.org/10.1086/250034): overview of code and highlight of main steps (if time allows)
	- [Reiter's (2009)](https://doi.org/10.1016/j.jedc.2008.08.010) method: solving models with idiosyncratic _and_ aggregate shocks (if time allows)

For each session, there is a [Jupyter notebook](https://jupyter.org/).
I might use extra material in class (e.g., slides) but they will have no additional content relative to the notebooks, so I will not post them here.


### Extra topics: web scraping, machine learning and natural language processing

Economists are learning their way through programming, and some used Python to [scrape the web](https://en.wikipedia.org/wiki/Web_scraping), run [machine learning](https://en.wikipedia.org/wiki/Machine_learning) algorithms or [parse natural language](https://en.wikipedia.org/wiki/Natural_language_processing).
These practices are becoming popular, so they deserve a bit of our attention.

While I will not have time to cover them, I want to showcase how those tools can be useful to us.
I will post some code I used in the past and, if I have time, I will accompany it with notebooks explaining the main steps and decisions.
