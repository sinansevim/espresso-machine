from src import esma
#Step 1 - Initialize model
model = esma.project(project_id="NbSe2_d3") #Define project
model.set_cores(128) #Define number of prcessing cores
model.get_structure(format="poscar",path="/work/bansil/s.sevim/Test/espresso-machine/Structures/NbSe2.poscar")
model.set_pseudo(path="/work/bansil/s.sevim/Test/espresso-machine/Pseudopotentials/PBE/PAW")
model.ecutwfc(100) #Set wavefunction cutoff
model.ecutrho(600) #Set wavefunction cutoff
model.k_points([36,36,1]) #Set number of k points
model.degauss(0.02) #Set degauss value
model.conv_thr(1e-12) #Set convergence threshold
model.ph_thr(1e-16) #Set convergence threshold
model.smearing('fd')
model.etot_conv_thr(10**-6)
model.forc_conv_thr(10**-5)
# model.hubbard(atom='Nb',orbital='4d',value=3)
model.config['ph']['inputph']['dftd3_hess']='automatic.hess'

model.make_layer()

model.cell_dof('2Dxy') #Fix cell relaxation to 2D
model.optimize(calculation='relax',max_iter=1)
model.optimize(calculation='vc-relax',max_iter=1)
model.optimize(calculation='relax',max_iter=1)

model.calculate('scf')
model.set_q(nq1=12,nq2=12,nq3=1) #Set parameters
model.calculate('ph')

model.calculate('q2r') #Run calculation
path = ['GAMMA','M',"K","GAMMA"] #define corners
model.band_points(path,number=50) #define path
model.calculate('bands')
model.plot('electron',ylim=[-3,3],save=True) #plot electron bands

num_points = 200 # Number of q points
model.calculate("matdyn") #Run calculation
model.plot('phonon',save=True) # Plot phonon band

