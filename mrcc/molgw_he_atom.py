import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from lib import *

plt.clf()

plt.plot(x_fit,
         y_fit,
         "--",
         color="grey",
         label="fit")

plt.plot(molgw["inv x3"],
         molgw["correlation energy"]*1000,
         "+",
         color=molgw_color,
         label="MOLGW")

plt.ylabel(r"$E^{\mathrm{MP2}}_{\mathrm{corr.}}$ [mHa]")
plt.xlabel(r"$1/x^{3}$")
plt.legend()

maybe_plot(locals().get("__file__"))
