import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 1, 20)

w = 2*3.1415

x = np.sin(w*t)
y = np.sin(w*t + 3.1415/2)


for i,t_0 in enumerate(t):
    fig, ax = plt.subplots(figsize=(6,6))

    ax.set_aspect('equal')

    plt.xlabel('x')
    plt.ylabel('y')
    plt.plot(x, y)

    x_0 = np.sin(w*t_0)
    y_0 = np.sin(w*t_0 + 3.1415/2)

    puck = plt.Circle((x_0, y_0), 0.05, color='tomato')
    ax.add_artist(puck)

    plt.savefig(f'pics/{i}.png')














#
