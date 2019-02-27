# Examples

## Uses of `NMmacro`

Here there are some scripts that use methods from the [`NMmacro`](../NMmacro/) package.


## Other notebooks

The notebook [`discretizing_ar1_processes.ipynb`](./discretizing_ar1_processes.ipynb) shows the use of the [Tauchen (1986)](https://www.sciencedirect.com/science/article/pii/0165176586901680) and [Tauchen and Hussey (1991)](https://doi.org/10.2307/2938261) methods to discretize AR(1) processes.
It compares simulations of two different AR(1) models to simulations of the corresponding discrete Markov Chains to show how the "fit" changes after changes in the structural parameters.

The notebook [`hermgauss_vs_linspace.ipynb`](./hermgauss_vs_linspace.ipynb) compares a linearly spaced grid (obtained with `numpy.linspace`) to the Gauss-Hermite nodes (obtained with `numpy.polynomial.hermite.hermgauss`).
It provides an intuition on why the [Tauchen and Hussey (1991)](https://doi.org/10.2307/2938261) method is an improvement relative to [Tauchen (1986)](https://www.sciencedirect.com/science/article/pii/0165176586901680).


## Miscellanea

The file [`vfi_convergence.m`](./vfi_convergence.m) is a Matlab script that shows how VFI happens in the deterministic case of the Neoclassical Growth Model.
It creates a figure that is updated at every click (or button) press.
Every update corresponds to a new proposal for the value function.
It finally shows the approximate solution of the problem.

