"""
Code for installing, making, and calling GOBNILP solver for 
Bayesian Network Structure learning from Python. 

The advantage of using this file is that the source 
code will be automatically compiled, error handling can be 
done automatically at all steps of the process, and most importantly,
GOBNILP functionality can now be included in any Python library.


Please note that this re-distribution of GOBNILP is
done under the GNU Public License - ALL credit for that
solver goes to its creators Dr. James Cussens and 
Dr. Mark Bartlett.

SCIP may be retrieved for ACADEMIC purposes only, and
therefore this code may only be retrieved as such.

References
----------
[1] Tobias Achterberg, SCIP: solving constraint integer programs,
Mathematical Programming Computation, v1, n1, pgs 1-41, 2009.


"""
__author__ = """Nicholas Cullen <ncullen.th@dartmouth.edu>"""

import os
import subprocess



class GOBN(object):
	"""
	This class is a wrapper for almost anything you would want to
	do in order to install, make, and run GOBNILP - except that
	you can do it unified Python commands instead of from the tedious
	and confusing command line.

	Command-Line GOBNILP Overview
	-----------------------------

	Command Line Arugments:

		GOBNILP current recognizes five command line arguments:
			
			1. "-g = filename"

				Sets the file from which the settings are read. For example,
				if a settings file is created, you would enter the following:
					bin/globnilp -g=mysettings.txt data/asia_100.data

			2. "-f = format"

				Sets the input file format - note that you must use "-f=dat" flag
				if data file ends in something other than .dat, otherwise it will
				think its a local scores file. Any common delimiter can be used by
				simply specifying as such in the settings file.

			3. "-x"

				Create the model and exit before solving it.

			4. "-q = filename"

				Sets the frequency file for pedigree learning.

			5. "-v = level"

				The verbosity level of the output.
				Verbosity can be set to any value between 0 and 5, where
				levels 0 and 1 just display error and warning messages. Level 2
				gives additional info about system run and output. Level 3 is the
				default and gives information about the progress of the search.
				Level 4 gives a more detailed progress of the search, and Level 5
				displays statistics about the search once the BN has been found.

	Global Behavior Settings:

		A 'settings' file is used to change the global behavior of GOBNILP. Lines
		beginning with a # are treated as comments and blank lines are permitted. 

		The settings take the form of paramter = value, e.g:
			gobnilp.outputfile/solution = "output.txt"




	Python GOBNILP Overview
	-----------------------
	This codebase includes (or plans to include) the following main functionality:

		- Downloading and Extracting the GOBNILP and SCIP source code tar files.
		- Making the GOBNILP and SCIP source code and linking them.
		- Altering and Setting global parameter settings for GOBNILP.
		- Calling GOBNILP to learn BN structure from discrete data.
		- Printing/returning/writing various output formats.

	Additionally, this code includes the following utility functionality:

		- converting various file formats to GOBNILP's '.dat' format.
		- linking GOBNILP/SCIP to existing source code or directories.


	"""


	def __init__(self, GOBN_DIR=None, SCIP_DIR=None, SET_DIR=None):
		
		if GOBN_DIR is None:
			self.GOBN_DIR = 'gobnilp1.6.1'
			self.GOBN_TARRED = False
		else:
			self.GOBN_DIR = GOBN_DIR
			self.GOBN_TARRED = True

		if SCIP_DIR is None:
			self.SCIP_DIR = 'scipoptsuite-3.1.1/scip-3.1.1'
			self.SCIP_TARRED = False
		else:
			self.SCIP_DIR = SCIP_DIR
			self.SCIP_TARRED = True

		if SET_DIR is None:
			self.SET_DIR = 'mysettings.txt'
		else:
			self.SET_DIR = SET_DIR

	### EXTRACT & MAKE METHODS ###
	
	def extract_gobn_tar(self):
		proc = subprocess.call(['tar', '-xzvf', 'gobnilp1.6.1.tar.gz', '-C', GOBN_DIR])
		return proc.returncode

	def extract_scip_tar(self):
		proc = subprocess.call(['tar', '-xzvf', 'scipoptsuite-3.1.1.tar.gz', '-C', SCIP_DIR])

	def make(self):
		subprocess.call()

	def make_GOBNILP(self, CPLEX=False):
		"""
		Make the GOBNILP source code.

		IMPORTANT: You must make SCIP before GOBNILP.
		Steps:
			1. Untar GOBN if necessary
			2. ./configure.sh SCIP_DIR
			3. make (LPS=cpx)
		"""
		if not self.GOBN_TARRED:
			print 'GOBN must be untarred.. Trying now'
			tar_code = self.extract_gobn_tar()
			if tar_code == 0:
				print 'Un-Tar successful'
				self.GOBN_TARRED = True
			else:
				print 'Un-Tar unsuccessful'
				return None

		config_proc = subprocess.call(['./configure.sh', SCIP_DIR])
		if CPLEX:
			make_proc = subprocess.call(['make', 'LPS=cpx', '-C', GOBN_DIR])
		else:
			make_proc = subprocess.call(['make', '-C', GOBN_DIR])

	def make_SCIP(self):
		"""
		Steps:
			1. Untar SCIP if necessary
			2. make
		"""
		if not self.SCIP_TARRED:
			print 'SCIP must be untarred.. Trying now'
			tar_code = self.extract_scip_tar()
			if tar_code == 0:
				print 'Un-Tar successful'
				self.SCIP_TARRED = True
			else:
				print 'Un-Tar unsuccessful'
				return None		

		make_proc = subprocess.call(['make', '-C', SKIP_DIR])

	### GOBNILP SETTINGS ###

	def set_settings(self, settings_dict):
		"""
		Create the "gobnilp.set" file that will be passed in
		as an argument on the command-line run of GOBNILP using
		the "-g=mysettings.txt" flag.

		For now, I think it's best to allow the user to just pass
		in the normal paramter name, and add on the GOBNILP
		settings preceeding path - i.e. the user can pass in
		'delimeter = "whitespace"' instead of 
		'gobnilp/delimeter = "whitespace"'.

		Arguments
		---------
		*settings_dict* : a dictionary, where
			key = setting and value = setting value.

		SETTINGS 
		OPTIONS
		--------
		(gobnilp/) 
			*dagconstraintsfile* : a string - file name
				the file where any dag constraints on edges/independencies
				are stored.
			*delimiter* : delimiter for passed-in data file
			*mergedelimiters* : whether to merge delimiters
			*minfounders* : min number of prior variables
			*edge_penality* : positive value will bias the solver
				toward sparser graphs.
			*nbns* : an integer,
				how many BNs to learn - e.g. if nbns = 10, the solver
				will return the 10 unqiue BNs with the highest score.


		(gobnilp/outputfile/) 
			*solution* : a string - file name
				the file to which stdout will be written
			*adjacencymatrix* : a string (ending in '.mat') - file name
				the file to which the adjacency matrix result will
				be written.
			*dot* : a string (ending in '.dot') - file name
				whether/where the result will be output as a dot file
				to be used with graphviz.
			*scoreandtime* : a string - file name
				whether to only output the score and the time it took
				to get that score - useful when comparing GOBNILP to
				other structure learning methods.
			*mec* : a string - file name
				whether to print out the markov equivalence class of the
				learned BN.
			*pedigree* : a string - file name
				whether to output the learned BN as a pedigree - only useful
				when using GOBNILP for finding perdigrees.

		(gobnilp/scoring/) 
			*alpha* : equivalent sample size
			*arities* : boolean, variable cardinalities
			*names* : boolean, whether variable names are given
			*palim* : max number of parents for each node
			*prune* : whether to prune during scoring
			*fast* : whether to use fast gamma function,
				which may be numerically instable for high equivalent samples

		(heuristics/sinks/) 
			*probing* : set to True if solver is failing to
					find any solution at all.
			*maxdivedepth* : increase this value if solver
					is failing to find any solution at all.

		(limits/) 
			*time* : max time limit for search
			*gap* : min optimality gap until termination


		"""
		with open('mysettings.txt', 'w') as f:
			pass

	def set_constraints(self, cons_dict):
		"""
		Set constraints/requirements on certain edges,
		parent-child relationships, or conditional independencies
		in the learned network.
		"""
		pass

	### RUN METHODS ###

	def run(self, data_path):
		"""
		Main function to run GOBNILP.

		Score Metric
		------------
		By default, GOBNILP searches for the BN with the highest
		BDeu score (log marginal likelihood) subject to no node
		having more than 3 parents. The default effective sample
		size is equal to 1.

		Settings
		--------
		GOBNILP has the ability to set and alter many global settings,
		along with constraints on the structure search - i.e. stipulating
		that a given variable MUST be the parent of another variable, etc.
		This is done by changing the settings file, which we store in the
		"mysettings.txt" file. This settings file is then included in
		the command line run by passing it in with "-g=gobnilp.set". See
		the "set_settings" function for more information.

		Output
		------
		By default, GOBNILP prints out the learned BN structure
		with one line for each node specifying its parents and
		the local score for that choice of parents.
		"""

		gob_exec_path = os.path.join(self.GOBN_DIR,'bin/gobnilp')
		try:
			proc = subprocess.call([gob_exec_path, data_path])
		except OSError:
			print 'Path to Data is not correct.'
		
		if proc.returncode == 0:
			print 'Successful Run'
		else:
			print 'Unsuccessful Run'






































