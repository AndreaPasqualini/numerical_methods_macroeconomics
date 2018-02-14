"""  ==========================================================================
PhD Eco-Fin, Bocconi University, Milan
Macroeconomics 3
Prof.: Marco Maffezzoli
TA: Andrea Pasqualini

TA session 1 - Code seen in class
==========================================================================  """


import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt


#  =========================================================================  #

print('Hello world!')


#  =========================================================================  #

greeting = "Hello world!"
print(greeting)


#  =========================================================================  #

[print(i) for i in range(3, 11)]  # this is called 'list comprehension'

for i in range(3, 11):
    print(i)


#  =========================================================================  #

n = [1, 2, 3, 4, 5, 6, 7]  # this is a list
m = (1, 2, 3, 4, 5, 6, 7)  # this is a tuple
o = {'name': 'Andrea', 'surname': 'Pasqualini', 'age': 27}  # this is a dict
n[0] = -1    #   mutable data type
m[0] = -1    # immutable data type
n.append(8)  # a method of a list
o[0]         # cannot access a dictionary entry by numerical indexing
o['name']    # can index with 'keys'
o.keys()     # a method of a dict


#  =========================================================================  #

smth = ['el1', 'el2', 'el3']
def passByReference(l):
    return l.pop(0)
passByReference(smth)


#  =========================================================================  #

3 + 2      # addition
3 * 2      # multiplication
3 ** 2     # exponentiation
50 / 22    # division (result is a float regardless of inputs)
50. // 22  # floor division (result is same type as dividend)
50 % 22    # remainder of floor division


#  =========================================================================  #

this = False
if this is not True:
    print("Hey, that's true!")
else:
    print("Bummer, that's false...")


n = 0
while True:  # do this ONLY IF you know what you are doing!
    n += 1
    if n >= 100:
        print("Hey, you forgot to stop me!")
        break

m = 0
for i in range (10):
#    print('The result is: ' + m + i)
    print('The result is', m + i, sep=': ')


raise TypeError('The type of the input must have been wrong...')
raise ValueError('The type was good, but its value...')


class MyError(Exception):
    pass


raise MyError('Feels good to throw my own exceptions!')


#  =========================================================================  #

def f(x):
    return np.sqrt(x)

x = np.linspace(0, 2, num=100)
fig, ax = plt.subplots(figsize=(5,4))
ax.plot((0, 2), (0, 2), linewidth=1, linestyle='dashed', alpha=0.3,
        color='black', label=r'45-degree line')
ax.plot(x, f(x), linewidth=2, color='black', label=r'$y=f(x)$')
ax.grid(alpha=0.25)
ax.legend()
ax.set_xlabel(r'$x$')
ax.set_ylabel(r'$y$')
ax.set_title(r'$f(x) = \sqrt{x}$')


#  =========================================================================  #

def ols(y, x, const=True):
    n = y.shape[0]

    if const:  # if we want to add a constant to the regression
        X = np.concatenate((np.ones((n, 1)), x), axis=1)
    else:
        X = x

    k = X.shape[1]

    if n < 10000:  # if the no. of obs. is small enough
        Q, R = la.qr(X, mode='economic')
        xxi = la.solve(R.T @ R, np.eye(k))  # this is (X'X)^(-1)
    else:
        xxi = la.solve(X.T @ X, np.eye(k))  # this is (X'X)^(-1)

    beta = xxi @ (X.T @ y)
    u = y - X @ beta
    sigma2 = (u.T @ u) / (n-k)
    se_beta = np.sqrt(sigma2 * np.diag(xxi))

    return beta, se_beta


#  =========================================================================  #

class OLS(object):

    def __init__(self, y, x, const=True):

        self.y = y
        self.n = y.shape[0]

        if const:
            self.X = np.concatenate((np.ones((self.n, 1)), x), axis=1)
        else:
            self.X = x

        self.k = self.X.shape[1]

        if self.n < 10000:
            Q, R = la.qr(self.X, mode='economic')
            self.xxi = la.solve(R.T @ R, np.eye(self.k))
        else:
            self.xxi = la.solve(self.X.T @ self.X, np.eye(self.k))

        self.beta = self.xxi @ (self.X.T @ self.y)
        self.u = self.y - self.X @ self.beta
        self.sigma2 = (self.u.T @ self.u) / (self.n - self.k)
        self.se_beta = np.sqrt(self.sigma2 * np.diag(self.xxi).reshape((-1,1)))

    def r2(self, adj=False):
        rss = (self.u.T @ self.u)[0, 0]
        tss = (self.y.T @ self.y)[0, 0]
        r2 = 1 - rss/tss

        if not adj:
            return r2
        else:
            return 1 - (1-r2) * ((self.n - 1) / (self.n - self.k))


a = np.array([[0],
              [1],
              [0]], dtype=float)
b = np.array([[-2],
              [ 4],
              [ 1]], dtype=float)

mdl = OLS(a, b, const=True)
mdl.beta
mdl.se_beta
mdl.r2()

fig, ax = plt.subplots()
ax.scatter(b, a, color='black')
ax.plot(b, np.polyval(mdl.beta, b), color='blue')


#  =========================================================================  #

