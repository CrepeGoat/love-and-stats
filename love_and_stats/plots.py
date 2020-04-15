from love_and_stats.optimal import max_allowable_ranks

import numpy as np
import matplotlib.pyplot as plt


def basic_plot():
    for N in (5, 50, 500, 5000):#range(2, 50, 2):
        plt.plot(
            np.linspace(0, 1, N),
            np.array(max_allowable_ranks(N))/N,
            label=f"N={N}"
        )

    plt.legend()
    plt.xlabel("round fraction")
    plt.ylabel("place fraction")
    plt.show()


if __name__ == '__main__':
    basic_plot()
