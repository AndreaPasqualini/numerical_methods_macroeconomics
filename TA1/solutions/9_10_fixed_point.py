"""  ==========================================================================
PhD Eco-Fin, Bocconi University, Milan
Macroeconomics 3
Prof.: Marco Maffezzoli
TA: Andrea Pasqualini

TA session 1 - Exercises 9 and 10
Proposed solution
==========================================================================  """


from numpy import sqrt, array, linspace, tile
from matplotlib.pyplot import subplots, tight_layout
from matplotlib import rc
rc('text', usetex=True)


def f(x):
    return sqrt(1 + x) - 2/3


def iter_fixed_point(fun, x0, tol=1e-5, max_iter=int(1e5)):
    crit = 1
    path = [x0]
    
    while crit > tol:
        x0 = path[-1]
        x1 = f(x0)
        crit = abs(x1 - x0)
        path.append(x1)
        if len(path) >= max_iter:
            raise ValueError("Algorithm did't produce a convergent sequence.")
    
    return array(path)


# Applying the iteration
path = iter_fixed_point(f, 0.01)
fp = path[-1]


# Inferring the number of necessary iterations
path = array(path).reshape((-1, 1))
n_iter = path.size


# Laying down the path to the fixed point for the plot
path0 = tile(path, (1, 2)).reshape((-1, 1))
path1 = path0[1:]
path0 = path0[:-1]


# Spawning a grid for the plot and computing the function in that grid
x = linspace(0, 1, num=100)
y = f(x)


# Drawing the plot
fig, ax = subplots(figsize=(5, 4))
ax.plot(path0, path1, color='blue', linewidth=0.5)
ax.plot((fp, fp, 0), (0, fp, fp), color='red', linewidth=1, linestyle='dotted')
ax.plot((0,1), (0,1), color='black', linewidth=1, linestyle='dashed')
ax.plot(x, y, color='black', linewidth=2, label='$y = f(x)$')
ax.legend()
ax.set_xlabel('$x$')
ax.set_ylabel('$y$')
ax.set_title(r'$f(x) = \sqrt{1+x} - \frac{2}{3}$')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
tight_layout()
fig.savefig('./fixed_point.pdf')
