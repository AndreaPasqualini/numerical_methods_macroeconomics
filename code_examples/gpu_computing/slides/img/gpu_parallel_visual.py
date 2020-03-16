import numpy as np
import matplotlib.pyplot as plt

n_frames = 10
n_blocks = 15
n_tbp = 15
x = np.zeros((n_tbp, 1), dtype=int)

fig_size = np.array((16, 8)) / 2.54

fig, ax = plt.subplots(ncols=n_blocks, figsize=fig_size)
for i in range(n_frames):
    x[n_tbp-(i+1), 0] = 1
    for j in range(n_blocks):
        ax[j].imshow(x, cmap='Oranges')
        ax[j].get_xaxis().set_visible(False)
        ax[j].get_yaxis().set_visible(False)
    fig.savefig('./img/gpu_parallel_visual_{}.pdf'.format(i+1))
