# GPU Computing for Economists

This folder contains resources I used to create a class on GPU computing.


## Replication instructions


### C vs Python loop speeds

The file [`loop.sh`](./loop.sh) executes [`loop.py`](./loop.py) and [`loop.c`](./loop.c).
You need to have both a shell-compatible interpreter (e.g., Bash, zsh) and a GCC-compatible compiler.
Linux and macOS have both out-of-the-box (Debian---and derivatives---users may need to `apt install build-essential`)
Windows has none by default, although you can easily obtain them through the [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/about) (WSL).

The `time` function in [`loop.sh`](./loop.sh) is intended as the [Bash/zsh keyword](https://en.wikipedia.org/wiki/Time_(Unix)#Bash) and not as the [standalone GNU program](https://en.wikipedia.org/wiki/Time_(Unix)), although both do the same thing, essentially.


### VFI benchmarks

The file [`run-benchmarks.sh`](./run-benchmarks.sh) is a shell script that executes [`bench_cpu.py`](./bench_cpu.py), [`bench_jit.py`](./bench_jit.py) and [`bench_gpu.py`](./bench_gpu.py).
They produce the files [`results_cpu.csv`](./results_cpu.csv), [`results_jit.csv`](./results_jit.csv) and [`results_gpu.csv`](./results_gpu.csv) respectively.

I ran the code on an [Asus N550JK "VivoBook Pro"](https://www.asus.com/Laptops/N550JK/specifications/), which has the following hardware and software.

- [Intel Core i7-4700HQ](https://ark.intel.com/content/www/us/en/ark/products/75116/intel-core-i7-4700hq-processor-6m-cache-up-to-3-40-ghz.html)
- [Nvidia GeForce GTX 850M](https://www.geforce.com/hardware/notebook-gpus/geforce-gtx-850m/specifications)
- 8 GB of RAM
- 256 GB SSD, SATA 3 (6 GB/s)
- [Ubuntu](https://ubuntu.com/desktop) 19.10 (Linux kernel 5.3.0)

I installed Miniconda and the following packages

```bash
$ conda install numpy numba pandas tqdm cudatoolkit=10.1.243
```

The package `tqdm` is used to draw fancy progress bars on the terminal.
The specific version of `cudatoolkit` is a specific hard-dependency of the GTX 850M.

After the `.csv` files have been generated, I used [`benchmarks_gpu.r`](./benchmarks_gpu.r) with [R](https://www.r-project.org/), together with the [tidyverse](https://www.tidyverse.org/) packages to produce the charts [`benchmarks.pdf`](./benchmarks.pdf) and [`benchmarks-logscale.pdf`](benchmarks-logscale.pdf).


## Slides

The file [`ta6_gpu_computing.tex`](./slides/ta6_gpu_computing.tex) use the [Metropolis theme](https://github.com/matze/mtheme) and require [xelatex](https://en.wikipedia.org/wiki/XeTeX) and the [Fira font family](http://mozilla.github.io/Fira/) to be compiled with the proper font.

The file [`gpu_parallel_visual.py`](./slides/img/gpu_parallel_visual.py) generates a bunch of images that illustrate why GPU computing times tend to grow "less exponentially" with the size of the problem than CPU's.


## Credits

> Render to Caesar the things that are Caesar's.

Huge shout out to [@giacomobattiston](https://github.com/giacomobattiston), for understanding GPUs together with me.

- I took the images [`hw-sw-thread_block.jpg`](./slides/img/hw-sw-thread_block.jpg) and [`block-thread.pdf`](./slides/img/block-thread.pdf) from the [Wikipedia page on thread blocks](https://en.wikipedia.org/wiki/Thread_block_(CUDA_programming)).
- I took the image [`stencil.pdf`](./slides/img/stencil.pdf) from the [Wikipedia page on stencil code](https://en.wikipedia.org/wiki/Stencil_code).
- I took the image [`nvidia-rtx-2080-ti.jpg`](./slides/img/nvidia-rtx-2080-ti.jpg) from this [TechSpot article](https://www.techspot.com/products/graphics-cards/nvidia-geforce-rtx-2080-ti-11gb-gddr6-pcie.187702/).
