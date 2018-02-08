"""  ==========================================================================
PhD Eco-Fin, Bocconi University, Milan
Macroeconomics 3
Prof.: Marco Maffezzoli
TA: Andrea Pasqualini

TA session 1 - Exercise 5
Proposed solution
==========================================================================  """


def fibonacci(n):
    
    if n == 0:
        return None
    
    elif n == 1:
        return 0
    
    elif n == 2:
        return [0, 1]
    
    else:
        return fibonacci(n-1) + fibonacci(n-2)