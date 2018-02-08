"""  ==========================================================================
PhD Eco-Fin, Bocconi University, Milan
Macroeconomics 3
Prof.: Marco Maffezzoli
TA: Andrea Pasqualini

TA session 1 - Exercise 2
Proposed solution
==========================================================================  """


def isVowel(a):

    if not isinstance(a, str):
        raise TypeError('String expected as input.')

    if len(a) > 1:
        raise ValueError('String of one character expected as input')

    return a in ['a', 'e', 'i', 'o', 'u']
