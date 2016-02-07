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
Tobias Achterberg,
SCIP: solving constraint integer programs,
Mathematical Programming Computation, v1, n1, pgs 1-41, 2009.


"""
__author__ = """Nicholas Cullen <ncullen.th@dartmouth.edu>"""

import os
import subprocess



class GOBNILP(object):
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

				Sets the file from which the parameters are read. For example,
				if a settings file is created, you would enter the following:
					bin/globnilp -g=mysettings.txt data/asia_100.data

			2. "-f = format"

				Sets the input file format

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


	def __init__(self, GOB_DIR=None, SCIP_DIR=None):
		
		if GOB_DIR is None:
			self.GOB_DIR = 'gobnilp1.6.1'
		else:
			self.GOB_DIR = GOB_DIR

		if SCIP_DIR is None:
			self.SCIP_DIR = 'scipoptsuite-3.1.1/scip-3.1.1'
		else:
			self.SCIP_DIR = SCIP_DIR

	### EXTRACT & MAKE METHODS ###
	
	def extract_gob_tar(self):
		proc = subprocess.call(['tar', '-xzvf', 'gobnilp1.6.1.tar.gz', '-C', GOB_DIR])

	def extract_scip_tar(self):
		proc = subprocess.call(['tar', '-xzvf', 'scipoptsuite-3.1.1.tar.gz', '-C', SCIP_DIR])

	def make(self):
		subprocess.call()

	def make_GOBNILP(self, CPLEX=False):
		"""
		Make the GOBNILP source code.

		IMPORTANT: You must make SCIP before GOBNILP.
		Steps:
			1. ./configure.sh SCIP_DIR
			2. make (LPS=cpx)
		"""
		config_proc = subprocess.call(['./configure.sh', SCIP_DIR])
		if CPLEX:
			make_proc = subprocess.call(['make', 'LPS=cpx', '-C', GOB_DIR])
		else:
			make_proc = subprocess.call(['make', '-C', GOB_DIR])

	def make_SCIP(self):
		"""
		Steps:
			1. make
		"""
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
			*delimiter* : delimiter for passed-in data file
			*mergedelimiters* : whether to merge delimiters
			*minfounders* : min number of prior variables
			*edge_penality* : positive value will bias the solver
				toward sparser graphs.

		(gobnilp/outputfile/) 
			*solution* : a string,
				the file to which stdout will be written

		(gobnilp/scoring/) 
			*alpha* : equivalent sample size
			*arities* : boolean, variable cardinalities
			*names* : boolean, whether names are given
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

		gob_exec_path = os.path.join(self.GOB_DIR,'bin/gobnilp')
		try:
			proc = subprocess.call([gob_exec_path, data_path])
		except OSError:
			print 'Path to Data is not correct.'
		
		if proc.returncode == 0:
			print 'Successful Run'
		else:
			print 'Unsuccessful Run'






































