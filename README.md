# pyGOBN

<h2>Overview</h2>
This is a project to create Python bindings for the GOBNILP solver
for Global Optimization of Bayesian Network structure learning. The purpose
of this repository is to encourage and allow easy integration of GOBNILP into
existing Python libraries focused on Bayesian networks. The first
example of such integration is found in "neuroBN" -- github.com/ncullen93/neuroBN.

This work is not affiliated with GOBNILP or SCIP. Still, all credit for the real
code behind all of this goes to Dr. James Cussens and Dr. Mark Bartlett 
for the creation of GOBNILP, and to the creators of SCIP. Please contact me - Nick Cullen - at
ncullen.th@dartmouth.edu with any comments or concerns.

Here are the links to GOBNILP and SCIP:

	- https://www.cs.york.ac.uk/aig/sw/gobnilp/

	- http://scip.zib.de/#scipoptsuite

<h2>Usage</h2>
To unpack/link/make GOBNILP & SCIP for the first time, run the following commands:

	>>> from pyGOBN import *
	>>> gobn = GOBN()
	>>> gobn.make()

To set or alter global parameter settings for the GOBNILP solver, use the following function:

	>>> gobn = GOBN()
	>>> settings = {'delimiter':'whitespace', 'time':120, alpha:1000}
	>>> gobn.set_settings(settings)

To set or alter the learned network constraints for the GOBNILP solver, use the following function:

	>>> gobn = GOBN()
	>>> edge_reqs = {'A':['B','C'],'B':['D']} # require that A->B, A->C, and B->D
	>>> ind_reqs = [('A','D'),(('A','B'),'D','C')] # require that A _|_ D and A,B _|_ D | C
	>>> nonedge_reqs = {'B':['C']} # disallow that B->C
	>>> gobn.set_constraints(edge_reqs, ind_reqs, nonedge_reqs)

Additionally, the global parameter settings and constraints can be passed in to the main 'learn' function,
along with a numpy ndarray or a pandas dataframe:

	>>> gobn = GOBN()
	>>> settings = {'delimiter':'whitespace', 'time':120, 'alpha':1000}
	>>> edge_reqs = {'A':['B','C'],'B':['D']} # require that A->B, A->C, and B->D
	>>> ind_reqs = [('A','D'),(('A','B'),'D','C')] # require that A _|_ D and A,B _|_ D | C
	>>> nonedge_reqs = {'B':['C']} # disallow that B->C
	>>> data = np.loadtxt('testfile.txt')
	>>> gobn.learn(data, settings, edge_reqs, ind_reqs, nonedge_reqs)

<h2>Pre-Reqs</h2>
From my understanding, the only necessary requirement for setting up GOBNILP
is access to the 'make' command (i.e. a compiler). This code was written for a Mac, 
which already has the 'make' command built-in. Since the code calls the 'tar' 
command to unpack the source code files, i'm assuming it's necessary to have 
that command as well. It's quite likely that this code will only work on Mac OS 
and probably Linux at the moment. If any Windows users come across any issues, please
let me know at ncullen.th@dartmouth.edu and i'll fix it!






