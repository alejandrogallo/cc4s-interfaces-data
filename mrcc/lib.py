from scipy.optimize import curve_fit
import matplotlib as mp
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys


mp.rc_file("../matplotlib.yaml")

def maybe_plot(filename):
    output = "test.pdf" if not filename else filename.replace("py", "pdf")
    print(f"Saving in {output}")
    plt.savefig(output)
    if not filename:
        plt.show()

def linear(x, a, b):
    return a * x + b

molgw = pd.read_csv("molgw.csv")
molgw_color = "b"

popt, pcov = curve_fit(linear, molgw["inv x3"], molgw["correlation energy"]*1000)
a, b = popt

x_fit = np.linspace(min(molgw["inv x3"]), max(molgw["inv x3"]), 10)
y_fit = linear(x_fit, a, b)
