"""  ==========================================================================
PhD Eco-Fin, Bocconi University, Milan
Macroeconomics 3
Prof.: Marco Maffezzoli
TA: Andrea Pasqualini

TA session 1 - Exercise 0
Proposed solution
==========================================================================  """


this_year = 2018
studs = {'Jack': 1992,
         'Rick': 1990,
         'Andrew': 1990,
         'Crash': 1996,
         'Penta': 1997}
ages = [this_year - studs[name] for name in studs.keys()]