from scipy.optimize import curve_fit
import matplotlib as mp
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys


mp.rc_file("../../matplotlib.yaml")

def maybe_plot(filename):
    output = "test.pdf" if not filename else filename.replace("py", "pdf")
    print(f"Saving in {output}")
    plt.savefig(output)
    if not filename:
        plt.show()
