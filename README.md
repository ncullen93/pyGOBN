# pyGOBN

<h2>Overview</h2>
This is a project to create Python bindings for the amazing GOBNILP solver
for Global Optimization of Bayesian Network structure learning. The purpose
and advantage of this repository is to allow easy integration of GOBNILP into
existing Python libraries focused on Bayesian networks or otherwise. The first
example of such integration is found in "neuroBN" -- github.com/ncullen93/neuroBN.

This work is not affiliated with GOBNILP or SCIP creators. Still, all credit for the real
code behind all of this goes to Dr. James Cussens and Dr. Mark Bartlett 
for the creation of GOBNILP, and to the creators of SCIP.

<h2>Quick Usage</h2>
To unpack/link/make the GOBNILP solver, simply run the following commands:

	- change directories to be in 'pyGOBN-master' folder.

	- 'from pyGOBN import *'

	- 'g = GOBN()'

	- 'g.make()'

Any errors will be reported to you, but it has been extensively tested.

<h2>Extended Usage</h2>

To get up-and-running with pyGOBN, start by downloading a copy of the code
by clicking "Download ZIP" towards the upper right corner of this page. Unzip
the file wherever you want - this new directory called 'pyGOBN-master' will be
henceforth referred to as $(MASTER_DIR).

Now, GOBNILP relies on its own source code, along with the source code of SCIP (a
high-quality optimization solver). Assuming you have never used GOBNILP or SCIP before, 
pyGOBN makes it incredibly easy to install GOBNILP and SCIP, because it includes the
zipped source code directory of both.

You should see the following in $(MASTER_DIR):

	- pyGOBN.py file : the main driver behind pyGOBN.

	- /gobnilp/ folder : the folder currently containing 'gobnilp1.6.1.tar.gz' (the
		zipped source code of GOBNILP).

	- /scip/ folder : the folder currently containing 'scipoptsuite-3.1.1.tgz' (the
		ziped source code of SCIP).

	- __init__.py : not important here.

	- README.md : not important here.

We will refer to the '/gobnilp/' folder as $(GOBN_DIR) and '/scip/' as $(SCIP_DIR).

In order to get running with GOBNILP, the following must happen:

	- gobnilp and scipoptsuite tar files must be unpacked (unzipped).

	- we must call 'make' on SCIP.

	- we must call 'make' on gobnilp.

Thankfully, pyGOBN does ALL of this for you.

There are two main commands regarding the installing/making of GOBNILP, all wrapped
in an object called 'GOBN()' - unpack() and make(). Those two main commands both
call the SCIP and GOBN versions - i.e. unpack() calls unpack_SCIP() and unpack_GOBN(),
and make() calls make_SCIP() and make_GOBN(). There is certainly a necessary order
in which those commands must be called, by pyGOBN resolves an issues by simply calling
the necessary commands to run any command the user inputs. As described earlier, calling
make() will do everything for you.

<h2>Pre-Requirements</h2>
From my understanding, the only necessary requirement for setting up GOBNILP
is a C++ compiler. This code was written for a Mac computer, which already has
the 'make' command built-in. Since the code calls the 'tar' command to unpack
the source code files, i'm assuming it's necessary to have the command as well. For
that reason, it's quite likely that this code will only work on Mac OS and probably
Linux at the moment. I welcome any feedback from Windows users who want this to
work on their machines.






