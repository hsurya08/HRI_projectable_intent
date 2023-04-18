import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import ListedColormap
import numpy as np

x = np.linspace(-1, 1, 20)
y = -np.exp(x)

colors = cm.rainbow(np.linspace(1, 0.5, len(y)))

# add text outside the figure
message = 'Goal: ROOM 030'
obstacle = False
goal_reached = False
border_color = np.array([1,1,1])
border_width = 30
fontsz = 40

if obstacle:
    message = 'OBSTACLE DETECTED'
    border_color = np.array([228, 235,75])/255
    colors = cm.rainbow(np.linspace(1, 0.8, len(y)))
    fontsz = 60

elif goal_reached:
    message = 'Goal: REACHED'
    border_color = np.array([58, 199, 105])/255
    
fig, ax = plt.subplots()
# ax.scatter(x, y, c=colors, linewidths=10)
for i in range(len(x)-1):
    ax.plot(x[i:i+2], y[i:i+2], color=colors[i], linewidth=20)

fig.text(0.05, 0.5, f"{message}", va='center', rotation=90, fontsize=fontsz)
fig.text(0.9, 0.5, f"{message}", va='center', rotation=-90, fontsize=fontsz)

# add a color border to the figure
fig.patch.set_edgecolor(border_color)
fig.patch.set_linewidth(border_width)

# show the plot
ax.axis("off")
plt.show()


