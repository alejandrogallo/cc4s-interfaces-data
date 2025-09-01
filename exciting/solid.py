import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import lib


def linear(x, a, b):  # Replace with your function
    return a * x + b


filename = "solid.csv"
df = pd.read_csv(filename)

df.to_latex(filename.replace("csv", "tex"), index=False)

plt.plot(df["supercell"], df["ccsd"], "o--", label="CCSD")
plt.plot(df["supercell"], df["mp2"], "+--", label="MP2")
plt.xlabel(r"Supercell")
plt.ylabel(r"$E^{}_{\mathrm{corr.}}$ [mHa]")
plt.legend()
plt.xticks(df["supercell"])
lib.maybe_plot(locals().get("__file__"))
