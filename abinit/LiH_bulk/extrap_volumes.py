import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


import re
import os
outpdf = re.sub("py", "pdf", os.path.basename(__file__))

def linear(x, A, B):
    return A + B * x

filename = "abinit_lih_bulk_volume.dat"

df = pd.read_csv(filename)

# Conversion Ha -> mHa
df["MP2"] = df["MP2"] * 1000
df["CCSD"] = df["CCSD"] * 1000

print(df.columns)

x = 1.0 / df["volume"]

y = df["MP2"]
popt_mp2, pcov = curve_fit(linear, x, y)
print(popt_mp2)
y = df["CCSD"]
popt_ccsd, pcov = curve_fit(linear, x, y)
print(popt_ccsd)

xxx = np.linspace(0, max(x))

plt.plot(xxx, linear(xxx, *popt_mp2), '--', color='blue', label='MP2')
plt.plot(x, df["MP2"], 'o-', color='blue', label='MP2')
plt.plot(xxx, linear(xxx, *popt_ccsd), '--', color='red', label='CCSD')
plt.plot(x, df["CCSD"], 'o-', color='red', label='CCSD')
plt.text(0, popt_mp2[0], f'{popt_mp2[0]:.3f} mHa')
plt.text(0, popt_ccsd[0], f'{popt_ccsd[0]:.3f} mHa')
plt.xlabel("1/V in unitcell")
plt.ylabel("Ec (mHa)")
plt.title("ABINIT LiH solid")
plt.legend()
plt.tight_layout()
plt.savefig("abinit_lih_volume.pdf")
plt.savefig("abinit_lih_volume.png")
plt.show()
