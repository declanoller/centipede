import numpy as np
import matplotlib.pyplot as plt

t = np.linspace(0, 1, 100)

w = 2*3.1415

x = np.sin(w*t)
y = np.sin(w*t)

fig, ax = plt.subplots(figsize=(6,6))

ax.set_aspect('equal')

plt.xlabel('x')
plt.ylabel('y')
plt.plot(x, y)

t_0 = 0.3
x_0 = np.sin(w*t_0)
y_0 = np.sin(w*t_0)

puck = plt.Circle((x_0, y_0), 0.05, color='tomato')
ax.add_artist(puck)

plt.show()














#
