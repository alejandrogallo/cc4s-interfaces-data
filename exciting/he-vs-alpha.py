import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import lib


def linear(x, a, b):  # Replace with your function
    return a * x + b


filename = "he_ccsd.csv"
df = pd.read_csv(filename)

x, y = 1 / (df["nv"] + 310), df["correlation energy"]
popt, pcov = curve_fit(linear, x, y)

newx = np.array([0] + list(x))

plt.plot(newx, linear(newx, *popt), "--", label="CBS")
plt.plot(1 / (df["nv"] + 310),
         df["correlation energy"],
         "o",
         label=r"$\alpha = 310$")
plt.plot(1 / (df["nv"] + 0),
         df["correlation energy"],
         "+",
         label=r"$\alpha = 0$")
plt.xlabel(r"$1/(N_\mathrm{virtuals} + \alpha)$")
plt.ylabel(r"$E^{\mathrm{MP2}}_{\mathrm{corr.}}$ [mHa]")
plt.xlim(0, 7e-3)
plt.legend()

lib.maybe_plot(locals().get("__file__"))
