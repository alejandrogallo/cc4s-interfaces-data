import sys
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import pandas as pd

def linear(x, A0, A1):
    return A0 * x + A1

def ec2(x, A0, A1):
    return A0 + A1 / x


def ec(x, A0, A1, A2):
    return A0 + A1 / ( x + A2 )

def read_values(filename):
    data = np.genfromtxt(filename,missing_values='?', filling_values=np.nan)
    mp2 = data[~np.isnan(data)[:,1]][:, [0, 1]]
    ccsd = data[~np.isnan(data)[:,2]][:, [0, 2]]
    return mp2, ccsd

def fit(values):
    try:
        popt, _ = curve_fit(ec, values[:,0], values[:,1], p0= [values[-1,1]-1.0e-3, 500., -310.])
        print(popt[:])
    except:
        popt = np.array([values[-1,1], 0., 0.])
        print("fit failed")
        pass
    return popt

def fit2(values):
    try:
        popt, _ = curve_fit(ec2, values[:,0], values[:,1], p0= [values[-1,1], 5.])
        print(popt[:])
    except:
        popt = np.array([values[-1,1], 0., 0.])
        print("fit failed")
        pass
    return popt
    


mp2_box10, ccsd_box10 = read_values("abinit_lih_molecule_box10.dat")
mp2_box12, ccsd_box12 = read_values("abinit_lih_molecule_box12.dat")
mp2_box14, ccsd_box14 = read_values("abinit_lih_molecule_box14.dat")

# Conversion: Ha -> mHa
mp2_box10[:,1]  = mp2_box10[:,1] * 1000
mp2_box12[:,1]  = mp2_box12[:,1] * 1000
mp2_box14[:,1]  = mp2_box14[:,1] * 1000
ccsd_box10[:,1]  = ccsd_box10[:,1] * 1000
ccsd_box12[:,1]  = ccsd_box12[:,1] * 1000
ccsd_box14[:,1]  = ccsd_box14[:,1] * 1000


print("MP2")
mp2_box10_popt = fit(mp2_box10)
mp2_box12_popt = fit(mp2_box12)
mp2_box14_popt = fit(mp2_box14)
print(f"{mp2_box10_popt[0]=:.3f} mHa")
print(f"{mp2_box12_popt[0]=:.3f} mHa")
print(f"{mp2_box14_popt[0]=:.3f} mHa")
print(f"{mp2_box10_popt[-1]=:.3f}")
print(f"{mp2_box12_popt[-1]=:.3f}")
print(f"{mp2_box14_popt[-1]=:.3f}")

inv_vol    = [1.0/10**3, 1.0/12**3, 1.0/14**3]
mp2_extrap = [mp2_box10_popt[0], mp2_box12_popt[0], mp2_box14_popt[0] ]

print("CCSD")
ccsd_box10_popt = fit(ccsd_box10)
ccsd_box12_popt = fit(ccsd_box12)
ccsd_box14_popt = fit(ccsd_box14)
print(f"{ccsd_box10_popt[0]=:.3f} mHa")
print(f"{ccsd_box12_popt[0]=:.3f} mHa")
print(f"{ccsd_box14_popt[0]=:.3f} mHa")
print(f"{ccsd_box10_popt[-1]=:.3f}")
print(f"{ccsd_box12_popt[-1]=:.3f}")
print(f"{ccsd_box14_popt[-1]=:.3f}")

ccsd_extrap = [ccsd_box10_popt[0], ccsd_box12_popt[0], ccsd_box14_popt[0] ]



xxx=np.linspace(400,1600,1000)

ax = plt.gca()
plt.title("MP2")
plt.plot(mp2_box10[:,0]-1, mp2_box10[:,1], 's', label='MP2 box 10')
plt.plot(mp2_box12[:,0]-1, mp2_box12[:,1], 's', label='MP2 box 12')
plt.plot(mp2_box14[:,0]-1, mp2_box14[:,1], 's', label='MP2 box 14')
plt.plot(xxx-1,ec(xxx,*mp2_box10_popt),'--', color='black', label='Fit to MP2 A + B/(Nv+C)')
plt.plot(xxx-1,ec(xxx,*mp2_box12_popt),'--', color='black', label='Fit to MP2 A + B/(Nv+C)')
plt.plot(xxx-1,ec(xxx,*mp2_box14_popt),'--', color='black', label='Fit to MP2 A + B/(Nv+C)')
ax.axhline(y=mp2_box10_popt[0],ls=':',color='black',label=f'Extrapolation: {mp2_box10_popt[0]:.3f} mHa')
ax.axhline(y=mp2_box12_popt[0],ls=':',color='black',label=f'Extrapolation: {mp2_box12_popt[0]:.3f} mHa')
ax.axhline(y=mp2_box14_popt[0],ls=':',color='black',label=f'Extrapolation: {mp2_box14_popt[0]:.3f} mHa')
plt.xlabel("number of virtuals")
plt.ylabel("Ec (mHa per LiH)")
plt.legend()
plt.tight_layout()
plt.savefig("lih_molecule_mp2.pdf")
plt.savefig("lih_molecule_mp2.png")
plt.show()

ax = plt.gca()
plt.title("CCSD")
plt.plot(ccsd_box10[:,0]-1, ccsd_box10[:,1], 's', label='CCSD box 10')
plt.plot(ccsd_box12[:,0]-1, ccsd_box12[:,1], 's', label='CCSD box 12')
plt.plot(ccsd_box14[:,0]-1, ccsd_box14[:,1], 's', label='CCSD box 14')
plt.plot(xxx-1,ec(xxx,*ccsd_box10_popt),'--', color='black', label='Fit to CCSD A + B/(Nv+C)')
plt.plot(xxx-1,ec(xxx,*ccsd_box12_popt),'--', color='black', label='Fit to CCSD A + B/(Nv+C)')
plt.plot(xxx-1,ec(xxx,*ccsd_box14_popt),'--', color='black', label='Fit to CCSD A + B/(Nv+C)')
ax.axhline(y=ccsd_box10_popt[0],ls=':',color='black',label=f'Extrapolation: {ccsd_box10_popt[0]:.3f} mHa')
ax.axhline(y=ccsd_box12_popt[0],ls=':',color='black',label=f'Extrapolation: {ccsd_box12_popt[0]:.3f} mHa')
ax.axhline(y=ccsd_box14_popt[0],ls=':',color='black',label=f'Extrapolation: {ccsd_box14_popt[0]:.3f} mHa')
plt.xlabel("number of virtuals")
plt.ylabel("Ec (mHa per LiH)")
plt.legend()
plt.tight_layout()
plt.savefig("lih_molecule_ccsd.pdf")
plt.savefig("lih_molecule_ccsd.png")
plt.show()


mp2_popt, _  = curve_fit(linear, inv_vol, mp2_extrap)
ccsd_popt, _ = curve_fit(linear, inv_vol, ccsd_extrap)

xxx = np.linspace(0, 2e-3,1600,1000)
plt.title("LiH molecule: Volume extrap")
plt.plot(inv_vol, mp2_extrap,'o-', label='MP2')
plt.plot(inv_vol, ccsd_extrap,'o-', label='CCSD')
plt.plot(xxx,linear(xxx,*mp2_popt),':', label='A0 / V + A1 fit')
plt.plot(xxx,linear(xxx,*ccsd_popt),':', label='A0 / V + A1 fit')
plt.text(0,mp2_popt[1],f"{mp2_popt[1]:.3f} mHa")
plt.text(0,ccsd_popt[1],f"{ccsd_popt[1]:.3f} mHa")
plt.xlim(xmin=0, xmax=0.002)
#plt.ylim(ymin=-42, ymax=-22)
plt.xlabel("1 / V (bohr^-3)")
plt.ylabel("Ec (mHa)")
plt.legend()
plt.tight_layout()
plt.savefig("lih_molecule_vol_extrap.png")
plt.savefig("lih_molecule_vol_extrap.pdf")
plt.show()



