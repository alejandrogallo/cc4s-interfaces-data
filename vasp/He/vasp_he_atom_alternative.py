import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import lib

hfo = pd.read_csv("vasp_HFO.csv")
hfo_color = "b"
no = pd.read_csv("vasp_NO_alternative.csv")
no_color = "r"

plt.clf()

fig, ax1 = plt.subplots()

ax1.plot(hfo["inv n"], hfo["correlation energy"], "+", color=hfo_color, label="Hartree–Fock orbitals")
ax1.set_xlabel(r"$1/N_{\mathrm{HFO}}$")
ax1.set_ylabel(r"$E^{\mathrm{MP2}}_{\mathrm{corr.}}$ [mHa]")
ax1.tick_params(axis='x', colors=hfo_color)
#ax1.spines['bottom'].set_color(hfo_color)

# --- Secondary axis (top) for NO ---
ax2 = ax1.twiny()
ax2.plot(no["inv n"], no["correlation energy"], ".", color=no_color, label="Natural orbitals")
ax2.set_xlabel(r"$1/N_{\mathrm{NO}}$")
ax2.tick_params(axis='x', colors=no_color)
#ax2.spines['top'].set_color(no_color)

# --- Combine legends from both axes ---
lines_1, labels_1 = ax1.get_legend_handles_labels()
lines_2, labels_2 = ax2.get_legend_handles_labels()
ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc="best")


#plt.legend()

lib.maybe_plot(locals().get("__file__"))
