import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pandas as pd




def ec(x,A0,A1,A2):
     return A0 + A1 / ( x + A2 )


filename = 'abinit_lih_bulk16.dat'
#filename = 'abinit_lih_bulk54.dat'

data = np.genfromtxt(filename, missing_values='X', filling_values=np.nan)

# Remove rows with any NaN values
mp2 = data[~np.isnan(data)[:,1]][:, [0, 1]]
ccsd = data[~np.isnan(data)[:,2]][:, [0, 2]]

print(mp2)
print(ccsd)



popt, _ = curve_fit(ec, mp2[:,0], mp2[:,1], p0= [-0.040, 5.,  10.])
print(popt)

ccsd_popt, _ = curve_fit(ec, ccsd[:,0], ccsd[:,1], p0=[-0.040, 5.,  10.])
print(ccsd_popt)


print(f"MP2  Nv-extrapolated: {popt[0]:.6f}")
print(f"CCSD Nv-extrapolated: {ccsd_popt[0]:.6f}")

xxx=np.linspace(30,1400)

#popt = [-0.036 , 10, 10 ]
plt.title("LiH bulk Ec")
#plt.plot(exciting[:,0], exciting[:,1], '-', label='Exciting MP2')
plt.plot(mp2[:,0]-1, mp2[:,1], 's', label='ABINIT MP2')
plt.plot(ccsd[:,0]-1, ccsd[:,1], 's', label='ABINIT CCSD')
plt.plot(xxx,ec(xxx,*popt),'--',label='Fit A + B/(Nv+C)')
plt.plot(xxx,ec(xxx,*ccsd_popt),'--',label='Fit A + B/(Nv+C)')
ax = plt.gca()
ax.axhline(y=popt[0],ls='--',color='black',label=f'ABINIT extrapolation: {popt[0]*1000:.3f} mHa')
ax.axhline(y=ccsd_popt[0],ls='--',color='black',label=f'ABINIT extrapolation: {ccsd_popt[0]*1000:.3f} mHa')
plt.xlabel("number of virtuals")
plt.ylabel("Ec (Ha)")
plt.legend()
plt.tight_layout()
plt.show()

