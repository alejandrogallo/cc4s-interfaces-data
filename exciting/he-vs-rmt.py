import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import lib

rmt15 = pd.read_csv("he_rmt_15.csv")
rmt15_cbs = 1044
rmt15_color = "k"
rmt20 = pd.read_csv("he_rmt_20.csv")
rmt20_cbs = 460
rmt20_color = "r"
rmt30 = pd.read_csv("he_rmt_30.csv")
rmt30_cbs = 146
rmt30_color = "g"

plt.clf()
plt.axvline(rmt30_cbs, color=rmt30_color)
plt.axvline(rmt20_cbs, color=rmt20_color)
plt.axvline(rmt15_cbs, color=rmt15_color)
plt.plot(rmt15["nv"],
         rmt15["correlation energy"],
         "+",
         color=rmt15_color,
         label=r"$R_\mathrm{MT} = 1.5 a_0$")
plt.plot(rmt20["nv"],
         rmt20["correlation energy"],
         ".",
         color=rmt20_color,
         label=r"$R_\mathrm{MT} = 2.0 a_0$")
plt.plot(rmt30["nv"],
         rmt30["correlation energy"],
         "p",
         color=rmt30_color,
         label=r"$R_\mathrm{MT} = 3.0 a_0$")
plt.ylabel(r"$E^{\mathrm{MP2}}_{\mathrm{corr.}}$ [mHa]")
plt.xlabel(r"$N_{\mathrm{virtual}}$")
plt.xticks([rmt30_cbs, rmt20_cbs, rmt15_cbs])
plt.legend()

lib.maybe_plot(locals().get("__file__"))
