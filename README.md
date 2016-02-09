# pyGOBN

<h2>Overview</h2>
This is a project to create Python bindings for the GOBNILP solver
for Global Optimization of Bayesian Network structure learning. The purpose
of this repository is to encourage and allow easy integration of GOBNILP into
existing Python libraries focused on Bayesian networks. The first
example of such integration is found in "neuroBN" -- github.com/ncullen93/neuroBN.

This work is not affiliated with GOBNILP or SCIP. Still, all credit for the real
code behind this project goes to Dr. James Cussens and Dr. Mark Bartlett 
for the creation of GOBNILP, and to the creators of SCIP. Please contact me - Nick Cullen - at
ncullen.th@dartmouth.edu with any comments or concerns.

Here are the links to GOBNILP and SCIP:

	- https://www.cs.york.ac.uk/aig/sw/gobnilp/

	- http://scip.zib.de/#scipoptsuite

<h2>Usage</h2>
The pyGOBN project comes pre-packed with the tar files for both the GOBNILP and SCIP projects. Therefore, there
is absolutely no need to download anything except this package. You do, however, have to actually 
unpack, link, and make GOBNILP & SCIP when using pyGOBN for the first time. Note that you only have to call
the 'make()' function ONE TIME in the entire lifetime of using pyGOBN. Here is the command:

	>>> from pyGOBN import *
	>>> gobn = GOBN()
	>>> gobn.make()

If you already have GOBNILP set up on your local machine, but in a different directory than the pre-packaged
version, pass in the path to that directory and you're good to go! The path should be of the form
'.../gobnilp-1.6.1' - or whichever version you're using. Here is an example:

	>>> from pyGOBN import *
	>>> gobn = GOBN(GOBN_DIR='/users/nick/desktop/gobnilp1.6.1')

Setting and altering global parameter settings for the GOBNILP solver is made simple in pyGOBN - 
create a settings dictionary and call the 'set_settings()' function on your GOBN object. Here's an example:

	>>> gobn = GOBN()
	>>> settings = {'delimiter':'whitespace', 'time':120, alpha:1000}
	>>> gobn.set_settings(settings)

For more refined structure learning, you may want to add network constraints for the GOBNILP solver. Through the
'set_constraints()' method, pyGOBN supports constraints for required edges, disallowed edges, and (conditional) independencies 
between random variables that will be satisfied in the learned network. The following examples highlights this functionality:

	>>> gobn = GOBN()
	>>> edge_reqs = {'A':['B','C'],'B':['D']} # require that A->B, A->C, and B->D
	>>> ind_reqs = [('A','D'),(('A','B'),'D','C')] # require that A _|_ D and A,B _|_ D | C
	>>> nonedge_reqs = {'B':['C']} # disallow that B->C
	>>> gobn.set_constraints(edge_reqs, ind_reqs, nonedge_reqs)

Finally, the purpose of GOBNILP is of course to actually learn Bayesian network structures from data. For that,
pyGOBN implements the 'learn()' method, which supports learning from 1) a file path to the data, 2) a numpy array, and
3) a pandas dataframe. Here is what a short-but-complete pyGOBN session might look like:
	
	>>> from pyGOBN import *
	>>> gobn = GOBN() # Create a GOBN object
	>>> settings = {'delimiter':'whitespace', 'time':120, alpha:1000}
	>>> gobn.set_settings(settings) # Parameter Settings
	>>> edge_reqs = {'A':['B','C'],'B':['D']} # require that A->B, A->C, and B->D
	>>> gobn.set_constraints(edge_reqs=edge_reqs) # Constraints
	>>> data = np.loadtxt('testdata.txt')
	>>> gobn.learn(data) # Call the GOBNILP solver

<h2>Example</h2>
Here is a real example of running pyGOBN from the IPython shell. Here, the 'gobnilp' and 'scip' projects are
already installed on my local machine, so I can simply set the parameter settings - walltime equal to 10 seconds - and
then learn the Bayesian network from the data file.

![alt tag](https://cloud.githubusercontent.com/assets/13004360/12934044/b6246e24-cf59-11e5-8e3f-73f467f18469.png)

<h2>Pre-Reqs</h2>
From my understanding, the only necessary requirement for setting up GOBNILP
is access to the 'make' command (i.e. a compiler). This code was written for a Mac, 
which already has the 'make' command built-in. Since the code calls the 'tar' 
command to unpack the source code files, i'm assuming it's necessary to have 
that command as well. It's quite likely that this code will only work on Mac OS 
and probably Linux at the moment. If any Windows users come across any issues, please
let me know at ncullen.th@dartmouth.edu and i'll fix it!

<h2>References</h2>
[1] Tobias Achterberg, SCIP: solving constraint integer programs,
Mathematical Programming Computation, v1, n1, pgs 1-41, 2009.

[2] Mark Bartlett and James Cussens. Advances in Bayesian network learning
using integer programming. In Proceedings of the 29th Conference on
Uncertainty in Artificial Intelligence (UAI 2013). AUAI Press, 2013. To
appear.

[3] James Cussens. Bayesian network learning with cutting planes. In Fabio G.
Cozman and Avi Pfeffer, editors, Proceedings of the 27th Conference on
Uncertainty in Artificial Intelligence (UAI 2011), pages 153-160. 
AUAI Press, 2011.

[4] James Cussens, Mark Bartlett, Elinor M. Jones, and Nuala A. Sheehan.
Maximum likelihood pedigree reconstruction using

[5] Milan Studeny. How matroids occur in the context of learning Bayesian 
network structure. Proceedings of the 31st Conference on Uncertainty 
in Artificial Intelligence (UAI-15) July 2015.

[6] James Cussens, David Haws and Milan Studeny. Polyhedral aspects of score 
equivalence in Bayesian network structure learning. Arkiv 1503.00829, March 2015.

[7] Tommi Jaakkola, David Sontag, Amir Globerson, and Marina Meila. Learning
Bayesian network structure using LP relaxations. In Proceedings of the
13th International Conference on Artificial Intelligence and Statistics (AISTATS
2010), volume 9 of Journal of Machine Learning Research: Workshop
and Conference Proceedings, pages 358-365. Society for Artificial Intelligence
and Statistics, 2010.





