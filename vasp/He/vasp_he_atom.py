import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import lib

hfo = pd.read_csv("vasp_HFO.csv")
hfo_color = "b"
no = pd.read_csv("vasp_NO.csv")
no_color = "r"

plt.clf()
plt.plot(hfo["inv n"],
         hfo["correlation energy"],
         "+",
         color=hfo_color,
         label=r"Hartree-Fock orbitals")
plt.plot(no["inv n"],
         no["correlation energy"],
         ".",
         color=no_color,
         label=r"Natural orbitals")

plt.ylabel(r"$E^{\mathrm{MP2}}_{\mathrm{corr.}}$ [mHa]")
plt.xlabel(r"$1/N_{orbitals}$")
#plt.xticks([rmt30_cbs, rmt20_cbs, rmt15_cbs])
plt.legend()

lib.maybe_plot(locals().get("__file__"))
