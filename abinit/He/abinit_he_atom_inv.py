from lib import *


N0 = mp2_ccECP0_popt[2]
xxx = 1.0 / (exciting[:, 0] + mp2_ccECP0_popt[2])
plt.plot(xxx, exciting[:, 1], '-', label='Exciting')
xxx = 1.0 / (ccECP0[:, 0] + mp2_ccECP0_popt[2])
plt.plot(xxx, ccECP0[:, 1], '-', label='Abinit ccECP (spherical cutoff)')
xxx = 1.0 / (pseudodojo[:, 0] + mp2_ccECP0_popt[2])
plt.plot(xxx,
         pseudodojo[:, 1],
         '-',
         label='Abinit pseudodojo (spherical cutoff)')
xxx = np.arange(10, 50000, 100)
xxx = 1.0 / (xxx + mp2_ccECP0_popt[2])
plt.plot(xxx,
         mp2_ccECP0_popt[0] + mp2_ccECP0_popt[1] * xxx,
         color='grey',
         label=r'fit $E_{\rm CBS} + x * \alpha / (N_{\rm v} + N_0)$')

ax.axhline(y=mp2_ccECP0_popt[0], color='black', dashes=[2, 2])
plt.xlabel("Number of virtual orbitals 1 / ($N_v$ + $N_0$) with $N_0=$" +
           f"{N0:.1f}")
plt.ylabel("MP2 correlation energy (mHa)")
plt.xlim(xmin=0.)
plt.legend()
plt.tight_layout()
plt.savefig("abinit_he_atom_inv.pdf")
plt.savefig("abinit_he_atom_inv.png")
if not "__file__" in locals():
    plt.show()
