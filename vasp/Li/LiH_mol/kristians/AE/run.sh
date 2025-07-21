VASPBIN="vasp_gam"
CC4SBIN="/home/grueneis/Projects/src_local/cc4s_version100/cc4s/build/gcc-oblas-ompi/bin/Cc4s"

VASP="mpirun -np 4 $VASPBIN"
CC4S="mpirun -np 1 $CC4SBIN"

#cc4s.in, POSCAR, POTCAR and KPOINTS need to be present

enc=500
egw=300

cat POSCAR
rm WAVECAR

cat >KPOINTS<<!
Automatically generated mesh
       0
gamma
 1 1 1
!



echo "++++++++++++++++++++++++++++++"
echo "RUN DFT to get a converged guess for HF"
echo "++++++++++++++++++++++++++++++"

cat >INCAR <<!
ENCUT = $enc
#SIGMA=0.0001
EDIFF = 1E-6
ISYM=-1
PREC=Accurate
LREAL=.TRUE.
!
cat INCAR
$VASP
cp OUTCAR OUTCAR.DFT


echo "++++++++++++++++++++++++++++++"
echo "RUN HF"
echo "++++++++++++++++++++++++++++++"

cat >INCAR <<!
ENCUT = $enc
SIGMA=0.001
EDIFF = 1E-6
LHFCALC=.TRUE.
AEXX=1.0
ALGO=C
NELM=10000
#LHFMEANPOT = T
#LHFMEANPOT_PROBECHARGE = T
ISYM=-1
PREC=Accurate
LREAL=.TRUE.
!
cat INCAR
$VASP
cp OUTCAR OUTCAR.HF


nb=`awk <OUTCAR.HF "/maximum number of plane-waves:/ { print \\$5*2-1 }"`


echo "++++++++++++++++++++++++++++++"
echo "RUN HF diag"
echo "++++++++++++++++++++++++++++++"


cat >INCAR <<!
ENCUT = $enc
SIGMA=0.001
EDIFF = 1E-6
#LHFCALC=.TRUE.
#AEXX=1.0
ISYM=-1
ALGO = sub ; NELM = 1
NBANDS = $nb
#LHFMEANPOT = T
#LHFMEANPOT_PROBECHARGE = T
ISYM=-1
PREC=Accurate
LREAL=.TRUE.
!
cat INCAR
$VASP
cp OUTCAR OUTCAR.HFdiag
cp WAVECAR WAVECAR.diag

cp WAVECAR.diag WAVECAR

echo "++++++++++++++++++++++++++++++"
echo "RUN MP2 NOs"
echo "++++++++++++++++++++++++++++++"


cat >INCAR <<!
ENCUT = $enc
SIGMA=0.0001
LHFCALC=.TRUE.
AEXX=1.0
ISYM=-1
ALGO = MP2NO ;
NBANDS = $nb
LAPPROX=.TRUE.
#LHFMEANPOT = T
#LHFMEANPOT_PROBECHARGE = T
ISYM=-1
PREC=Accurate
LREAL=.TRUE.
!
rm WAVEDER
cat INCAR
$VASP
cp OUTCAR OUTCAR.MP2-NOs


nocc=`awk <OUTCAR.HF "/NELEC/ { print \\$3/2 }"`

echo "going to use $nb bands"
echo "there are $nocc occupied bands"


#for nbfp in 21 41 61 81 101 121 131
for nbfp in 21 51 101 151
do


echo "for fpX we need " $nbfp
nbno=`awk <OUTCAR.HF "/NELEC/ { print (\\$3/2)*$nbfp }"`
echo "for fpX we need $nbno  bands"

cp WAVECAR.FNO WAVECAR

echo "++++++++++++++++++++++++++++++"
echo "RUN HF diag of NOs using " $nbno " bands."
echo "++++++++++++++++++++++++++++++"


cat >INCAR <<!
ENCUT = $enc
SIGMA=0.0001
EDIFF = 1E-6
LHFCALC=.TRUE.
AEXX=1.0
ISYM=-1
ALGO = sub ; NELM = 1
NBANDS = $nbno
NBANDSHIGH = $nbno
#LHFMEANPOT = T
#LHFMEANPOT_PROBECHARGE = T
ISYM=-1
PREC=Accurate
LREAL=.TRUE.
!
rm WAVEDER
cat INCAR
$VASP
cp OUTCAR OUTCAR.HFdiag-NOs


echo "++++++++++++++++++++++++++++++"
echo "RUN MP2"
echo "++++++++++++++++++++++++++++++"


cat >INCAR <<!
ENCUT = $enc
SIGMA=0.0001
LHFCALC=.TRUE.
AEXX=1.0
ISYM=-1
ALGO = MP2
NBANDS = $nbno
NBANDSHIGH = $nbno
LSFACTOR=.TRUE.
#LHFMEANPOT = T
#LHFMEANPOT_PROBECHARGE = T
ISYM=-1
PREC=Accurate
LREAL=.TRUE.
!
rm WAVEDER
cat INCAR
$VASP
cp OUTCAR OUTCAR.MP2-CBS.$nbfp

done


for nbfp in 6 11 16 21
do


echo "for fpX we need " $nbfp
nbno=`awk <OUTCAR.HF "/NELEC/ { print (\\$3/2)*$nbfp }"`
echo "for fpX we need $nbno  bands"

cp WAVECAR.FNO WAVECAR

echo "++++++++++++++++++++++++++++++"
echo "RUN HF diag of NOs using " $nbno " bands."
echo "++++++++++++++++++++++++++++++"


cat >INCAR <<!
ENCUT = $enc
SIGMA=0.0001
EDIFF = 1E-6
LHFCALC=.TRUE.
AEXX=1.0
ISYM=-1
ALGO = sub ; NELM = 1
NBANDS = $nbno
NBANDSHIGH = $nbno
#LHFMEANPOT = T
#LHFMEANPOT_PROBECHARGE = T
PREC=Accurate
LREAL=.TRUE.
!
rm WAVEDER
cat INCAR
$VASP
cp OUTCAR OUTCAR.HFdiag-NOs


echo "++++++++++++++++++++++++++++++"
echo "Dump CC4S input using " $nbno " bands."
echo "++++++++++++++++++++++++++++++"


cat >INCAR <<!
ENCUT = $enc
SIGMA=0.0001
EDIFF = 1E-5
LHFCALC=.TRUE.
AEXX=1.0
ISYM=-1
ALGO=CC4S
NBANDS = $nbno
NBANDSHIGH = $nbno
ENCUTGW=$egw
ENCUTGWSOFT=$egw
#LHFMEANPOT = T
#LHFMEANPOT_PROBECHARGE = T
PREC=Accurate
LREAL=.TRUE.
!
cat INCAR
$VASP
cp OUTCAR OUTCAR.CC4S

#In this step the following files will be written that are needed for CC4S
#
#
#FockOperator.yaml, FockOperator.dat
#GridVectors.yaml, GridVectors.dat
#CoulombPotential.yaml, CoulombPotential.dat
#DeltaPPHH.yaml, DeltaPPHH.dat
#DeltaHH.yaml, DeltaHH.dat
#CoulombVertexSingularVectors.yaml, CoulombVertexSingularVectors.dat
#CoulombVertex.yaml, CoulombVertex.dat
#EigenEnergies.yaml, EigenEnergies.dat
#Spins.yaml, Spins.dat

echo "++++++++++++++++++++++++++++++"
echo "Run CC4S using " $nb " bands."
echo "++++++++++++++++++++++++++++++"

rm atrip-checkpoint.yaml
$CC4S -i ccsd.yaml | tee  cc4s.stdout.$nbno.bands


done
~
