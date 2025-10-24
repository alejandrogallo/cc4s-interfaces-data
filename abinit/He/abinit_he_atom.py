from lib import *

xxx = np.arange(10, 1600, 5)
plt.plot(exciting[:, 0], exciting[:, 1], '-', color='green', label='Exciting')
plt.plot(pseudodojo[:, 0],
         pseudodojo[:, 1],
         '-',
         color='blue',
         label='Abinit pseudodojo')
plt.plot(ccECP0[:, 0], ccECP0[:, 1], '-', color='red', label='Abinit ccECP')
plt.plot(xxx,
         ec(xxx, *mp2_ccECP0_popt),
         '--',
         color='grey',
         label='fit: $E_{CBS} + \\alpha / (N_v + N_0)$')
plt.xlabel("Number of virtual orbitals $N_v$")
plt.ylabel("MP2 correlation energy (mHa)")
ax.axhline(y=mp2_ccECP0_popt[0], color='black', dashes=[4, 4])
plt.text(50, mp2_ccECP0_popt[0] + 0.5, 'Abinit ccECP extrapolation')
plt.xlim(xmin=0.)
plt.legend()
plt.tight_layout()
plt.savefig("abinit_he_atom.pdf")
plt.savefig("abinit_he_atom.png")
if not "__file__" in locals():
    plt.show()
