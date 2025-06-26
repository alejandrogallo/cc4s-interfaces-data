import sys
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pandas as pd




def ec(x, A0, A1, A2):
     return A0 + A1 / ( x + A2 )

def read_values(filename):
    data = np.genfromtxt(filename,missing_values='X', filling_values=np.nan)
    mp2 = data[~np.isnan(data)[:,1]][:, [0, 1]]
    ccsd = data[~np.isnan(data)[:,2]][:, [0, 2]]
    return mp2, ccsd

def fit(values):
    try:
        popt, _ = curve_fit(ec, values[:,0], values[:,1], p0= [-0.036, 1200., 310])
        print(popt[:])
    except:
        print("fit failred")
        pass
    return popt
    




exciting = np.genfromtxt("exciting_mp2_He_rmt15.dat")
ccECP0   = np.genfromtxt("abinit_mp2_ccECP_icutcoul0.dat")
pseudodojo   = np.genfromtxt("abinit_mp2_pseudodojo_icutcoul0.dat")

# Convert Ha -> mHa
exciting[:, 1] = exciting[:, 1] * 1000.
ccECP0[:, 1] = ccECP0[:, 1] * 1000.
pseudodojo[:, 1] = pseudodojo[:, 1] * 1000.

mp2_ccECP0_popt = fit(ccECP0[:, :])
mp2_pseudodojo_popt = fit(pseudodojo[:, :])
#print(mp2_ccECP0_popt)

xxx = np.arange(10, 1600, 5)
ax = plt.gca()
plt.plot(exciting[:, 0], exciting[:, 1], '-', color='green', label='Exciting')
plt.plot(pseudodojo[:, 0], pseudodojo[:, 1], '-', color='blue',label='Abinit pseudodojo')
plt.plot(ccECP0[:, 0], ccECP0[:, 1], '-', color='red', label='Abinit ccECP')
plt.plot(xxx, ec(xxx, *mp2_ccECP0_popt), '--', color='grey', label='fit: $E_{CBS} + \\alpha / (N_v + N_0)$')
plt.xlabel("Number of virtual orbitals $N_v$")
plt.ylabel("MP2 correlation energy (mHa)")
ax.axhline(y=mp2_ccECP0_popt[0], color='black', dashes=[4, 4])
plt.text(50, mp2_ccECP0_popt[0] + 0.5, 'Abinit ccECP extrapolation')
plt.xlim(xmin=0.)
plt.legend()
plt.tight_layout()
plt.savefig("abinit_he_atom.pdf")
plt.savefig("abinit_he_atom.png")
plt.show()

N0 = mp2_ccECP0_popt[2]
xxx = 1.0 / ( exciting[:, 0] + mp2_ccECP0_popt[2] )
plt.plot(xxx, exciting[:, 1], '-', label='Exciting')
xxx = 1.0 / ( ccECP0[:, 0] + mp2_ccECP0_popt[2] )
plt.plot(xxx, ccECP0[:, 1], '-', label='Abinit ccECP (spherical cutoff)')
xxx = 1.0 / ( pseudodojo[:, 0] + mp2_ccECP0_popt[2] )
plt.plot(xxx, pseudodojo[:, 1], '-', label='Abinit pseudodojo (spherical cutoff)')
xxx = np.arange(10, 50000, 100)
xxx = 1.0 / ( xxx + mp2_ccECP0_popt[2] )
plt.plot(xxx, mp2_ccECP0_popt[0] + mp2_ccECP0_popt[1] * xxx, color='grey', label='fit $E_{CBS} + x * \\alpha / (N_v + N_0)$')

ax.axhline(y=mp2_ccECP0_popt[0], color='black', dashes=[2, 2])
plt.xlabel("Number of virtual orbitals 1 / ($N_v$ + $N_0$) with $N_0=$" + f"{N0:.1f}")
plt.ylabel("MP2 correlation energy (mHa)")
plt.xlim(xmin=0.)
plt.legend()
plt.tight_layout()
plt.savefig("abinit_he_atom_inv.pdf")
plt.savefig("abinit_he_atom_inv.png")
plt.show()




sys.exit()

mp2_ccECP0, ccsd_ccECP0 = read_values("he_ccECP_icutcoul0.dat")
mp2_ccECP6, ccsd_ccECP6 = read_values("he_ccECP_icutcoul6.dat")
mp2_pseudodojo6, ccsd_pseudodojo6 = read_values("he_pseudodojo_icutcoul6.dat")


print("MP2")
mp2_ccECP0_popt = fit(mp2_ccECP0)
mp2_ccECP6_popt = fit(mp2_ccECP6)
mp2_pseudodojo6_popt = fit(mp2_pseudodojo6)

print(f"{mp2_ccECP0_popt[0]*1000=:.3f}")
print(f"{mp2_ccECP6_popt[0]*1000=:.3f}")
print(f"{mp2_pseudodojo6_popt[0]*1000=:.3f}")
#
print("CCSD")
ccsd_ccECP0_popt = fit(ccsd_ccECP0)
ccsd_ccECP6_popt = fit(ccsd_ccECP6)
ccsd_pseudodojo6_popt = fit(ccsd_pseudodojo6)

print(f"{ccsd_ccECP0_popt[0]*1000=:.3f}")
print(f"{ccsd_ccECP6_popt[0]*1000=:.3f}")
print(f"{ccsd_pseudodojo6_popt[0]*1000=:.3f}")





xxx=np.linspace(100,1400)

#popt = [-0.036 , 10, 10 ]
plt.title("He atom Ec MP2")
plt.plot(exciting[:,0], exciting[:,1], '-', label='Exciting MP2')
plt.plot(mp2_ccECP0[:,0]-1, mp2_ccECP0[:,1], 's', label='ABINIT MP2 ccECP spherical cutoff')
plt.plot(mp2_ccECP6[:,0]-1, mp2_ccECP6[:,1], 's', label='ABINIT MP2 ccECP Baldereschi-like')
plt.plot(mp2_pseudodojo6[:,0]-1, mp2_pseudodojo6[:,1], 's', label='ABINIT MP2 pseudodojo Baldereschi-like')
plt.plot(xxx,ec(xxx,*mp2_ccECP0_popt),'--',color='grey',label='Fit A + B/(Nv+C)')

#plt.plot(xxx,ec(xxx,*ccsd_popt),'--',label='Fit A + B/(Nv+C)')
ax = plt.gca()
ax.axhline(y=mp2_ccECP0_popt[0],ls='--',color='black',label=f'ABINIT extrapolation: {mp2_ccECP0_popt[0]*1000:.3f} mHa')
#ax.axhline(y=ccsd_popt[0],ls='--',color='black',label=f'ABINIT extrapolation: {ccsd_popt[0]*1000:.3f} mHa')
plt.xlabel("number of virtuals")
plt.ylabel("Ec (Ha)")
plt.legend()
plt.tight_layout()
plt.savefig("abinit_he_atom.pdf")
plt.show()

