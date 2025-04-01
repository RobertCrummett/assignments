import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl

data = np.loadtxt("profile.txt")
x = data[:,0]
z = data[:,1]

# Vertical gravity field due to a prism of infinite 
# extent in one horizontal direction
def gz(x, a, b, h2, h1):
    k = 6.67e-11 # SI units
    s = 1000 * 0.17 # kg / m^3
    g2 = h2 * (np.arctan2((x - a), h2) + np.arctan2((b - x), h2)) + \
         (x - a) / 2 * np.log(np.abs((x - a)**2 + h2**2)) + \
         (b - x) / 2 * np.log(np.abs((b - x)**2 + h2**2))
    g1 = h1 * (np.arctan2((x - a), h1) + np.arctan2((b - x), h1)) + \
         (x - a) / 2 * np.log(np.abs((x - a)**2 + h1**2)) + \
         (b - x) / 2 * np.log(np.abs((b - x)**2 + h1**2))
    return 2 * k * s * (g2 - g1)

a = 150 * 1000
b = 350 * 1000
h1 = 23 * 1000
h2 = 34 * 1000

mx = np.linspace(0, 462.5, 100) * 1000

mz = gz(mx, a, b, h2, h1) * 100 * 1000

fig, ax = plt.subplots()
ax.plot(x * 1000, z / 100 / 1000, label = "Complete Bouguer Anomaly")
plt.title("Vertical gravity anomaly over the West Africa Rift Zone")
plt.xlabel("Distance along profile [meters]")
plt.ylabel("Vertica gravity anomaly [meters / second^2]")
ax.get_xaxis().set_major_formatter(
    mpl.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
plt.savefig("profile.png", dpi=600)
