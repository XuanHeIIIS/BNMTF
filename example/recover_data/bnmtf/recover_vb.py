"""
Recover the toy dataset generated by example/generate_toy/bnmtf/generate_bnmtf.py
We use the parameters for the true priors.
"""

project_location = "/home/tab43/Documents/Projects/libraries/"
import sys
sys.path.append(project_location)

from BNMTF.code.bnmtf_vb import bnmtf_vb
from ml_helpers.code.mask import calc_inverse_M

import numpy, matplotlib.pyplot as plt

##########

input_folder = project_location+"BNMTF/example/generate_toy/bnmtf/"

iterations = 100
init_FG = 'kmeans'
init_S = 'random'
I, J, K, L = 50,40,10,5 #50, 40, 10, 5

alpha, beta = 1., 1.
lambdaF = numpy.ones((I,K))
lambdaS = numpy.ones((K,L))
lambdaG = numpy.ones((J,L))
priors = { 'alpha':alpha, 'beta':beta, 'lambdaF':lambdaF, 'lambdaS':lambdaS, 'lambdaG':lambdaG }

# Load in data
R = numpy.loadtxt(input_folder+"R.txt")
M = numpy.loadtxt(input_folder+"M.txt")
M_test = calc_inverse_M(M)

# Run the Gibbs sampler
BNMTF = bnmtf_vb(R,M,K,L,priors)
BNMTF.initialise(init_S=init_S,init_FG=init_FG)

expF = BNMTF.expF
expS = BNMTF.expS
expG = BNMTF.expG

BNMTF.run(iterations)

# Also measure the performances
performances = BNMTF.predict(M_test)
print performances

# Plot the tau expectation values to check convergence
plt.plot(BNMTF.all_exp_tau)