from scipy.optimize import curve_fit
import matplotlib as mp
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

mp.rc_file("../../matplotlib.yaml")


def ec(x, A0, A1, A2):
    return A0 + A1 / (x + A2)


def read_values(filename):
    data = np.genfromtxt(filename, missing_values='X', filling_values=np.nan)
    mp2 = data[~np.isnan(data)[:, 1]][:, [0, 1]]
    ccsd = data[~np.isnan(data)[:, 2]][:, [0, 2]]
    return mp2, ccsd


def fit(values):
    popt, _ = curve_fit(ec,
                        values[:, 0],
                        values[:, 1],
                        p0=[-0.036, 1200., 310])
    print(popt[:])
    return popt


exciting = np.genfromtxt("exciting_mp2_He_rmt15.dat")
ccECP0 = np.genfromtxt("abinit_mp2_ccECP_icutcoul0.dat")
pseudodojo = np.genfromtxt("abinit_mp2_pseudodojo_icutcoul0.dat")

# Convert Ha -> mHa
exciting[:, 1] = exciting[:, 1] * 1000.
ccECP0[:, 1] = ccECP0[:, 1] * 1000.
pseudodojo[:, 1] = pseudodojo[:, 1] * 1000.

mp2_ccECP0_popt = fit(ccECP0[:, :])
mp2_pseudodojo_popt = fit(pseudodojo[:, :])
print("mp2_ccECP0_popt ⇒ ", mp2_ccECP0_popt)

ax = plt.gca()
